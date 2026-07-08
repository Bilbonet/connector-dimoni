# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields

from odoo.addons.component.core import Component


class DimoniResPartnerBankImporter(Component):
    _name = "dimoni.res.partner.bank.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.res.partner.bank"

    def import_for_partner(
        self, *, partner_ref=None, id_fiscal=None, partner=None, force_update=False
    ):
        if not partner_ref or not id_fiscal or not partner:
            return self.env["res.partner.bank"].browse()

        rows = self.backend_adapter.search_for_partner(
            partner_ref=partner_ref,
            id_fiscal=id_fiscal,
        )
        bank_accounts = self.env["res.partner.bank"].browse()
        for row in rows:
            row_id = row.get("ROW_ID")
            if row_id is None:
                continue
            bank_account = self._ensure_res_partner_bank_record(
                row,
                partner=partner,
                force_update=force_update,
            )
            if bank_account:
                bank_accounts |= bank_account
        return bank_accounts

    def get_bank_account(self, *, row_id=None, partner=None, force_update=False):
        if row_id is None or not partner:
            return None
        if not isinstance(row_id, int):
            raise TypeError("row_id must be an int")

        bank_data = self.backend_adapter.get_by_row_id(row_id)
        if not bank_data:
            self._deactivate_missing_binding(row_id)
            return False

        return self._ensure_res_partner_bank_record(
            bank_data[0],
            partner=partner,
            force_update=force_update,
        )

    def _ensure_res_partner_bank_record(
        self, bank_data, *, partner, force_update=False
    ):
        external_id = bank_data.get("ROW_ID")
        if not external_id:
            return None

        mapper = self.component(usage="import.mapper")
        map_record = mapper.map_record(bank_data)
        vals = map_record.values()
        acc_number = vals.get("acc_number")
        if not acc_number or not self.env["res.partner.bank"].check_iban(acc_number):
            return None

        binder = self.binder_for()
        binding = binder.to_internal(external_id)
        if binding:
            if force_update:
                self._update_binding(binding, vals, partner=partner)
            self._ensure_mandate(binding.odoo_id, bank_data)
            return binding.odoo_id

        existing_bank = self._search_bank_account(
            partner=partner, acc_number=acc_number
        )
        if existing_bank:
            vals["odoo_id"] = existing_bank.id
        else:
            vals["partner_id"] = partner.id

        binding = self.env["dimoni.res.partner.bank"].sudo().create(vals)
        self._ensure_mandate(binding.odoo_id, bank_data)
        return binding.odoo_id

    def _update_binding(self, binding, vals, *, partner):
        acc_number = vals.get("acc_number")
        existing_bank = self._search_bank_account(
            partner=partner, acc_number=acc_number
        )
        if existing_bank and existing_bank != binding.odoo_id:
            vals["odoo_id"] = existing_bank.id
        else:
            vals["partner_id"] = partner.id
        binding.sudo().write(vals)
        return binding

    def _ensure_mandate(self, bank_account, bank_data):
        mandate_ref = str(bank_data.get("Referen") or "").strip()
        signature_date = fields.Date.to_date(bank_data.get("FecFirma"))
        if not bank_account or not mandate_ref or not signature_date:
            return self.env["account.banking.mandate"].browse()

        company = self.backend_record.company_id
        mandate_model = (
            self.env["account.banking.mandate"].sudo().with_company(company)
        )
        mandate = mandate_model.search(
            [
                ("unique_mandate_reference", "=", mandate_ref),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )
        vals = {
            "unique_mandate_reference": mandate_ref,
            "signature_date": signature_date,
            "partner_bank_id": bank_account.id,
            "company_id": company.id,
            "state": "valid",
        }
        self._add_optional_sepa_mandate_vals(vals, mandate_model, bank_data)
        if mandate:
            mandate.write(vals)
            return mandate
        return mandate_model.create(vals)

    def _add_optional_sepa_mandate_vals(self, vals, mandate_model, bank_data):
        if "format" in mandate_model._fields:
            format_values = self._get_selection_values(mandate_model, "format")
            vals["format"] = "sepa" if "sepa" in format_values else "basic"
        if "type" in mandate_model._fields:
            type_values = self._get_selection_values(mandate_model, "type")
            if "recurrent" in type_values:
                vals["type"] = "recurrent"
            elif "generic" in type_values:
                vals["type"] = "generic"
        if "recurrent_sequence_type" in mandate_model._fields:
            vals["recurrent_sequence_type"] = "first"
        if "scheme" in mandate_model._fields:
            vals["scheme"] = self._map_mandate_scheme(bank_data)

    @staticmethod
    def _map_mandate_scheme(bank_data):
        mandate_type = str(bank_data.get("TipoAdeu") or "").strip()
        return "B2B" if mandate_type == "1" else "CORE"

    @staticmethod
    def _get_selection_values(model, field_name):
        field_info = model.fields_get([field_name])[field_name]
        return {value for value, _label in field_info["selection"]}

    def _search_bank_account(self, *, partner, acc_number):
        return (
            self.env["res.partner.bank"]
            .sudo()
            .with_context(active_test=False)
            .search(
                [
                    ("partner_id", "=", partner.id),
                    ("acc_number", "=", acc_number),
                ],
                limit=1,
            )
        )

    def _deactivate_missing_binding(self, row_id):
        binding = (
            self.env["dimoni.res.partner.bank"]
            .with_context(active_test=False)
            .search(
                [
                    ("backend_id", "=", self.backend_record.id),
                    ("external_id", "=", row_id),
                ],
                limit=1,
            )
        )
        if not binding:
            return False

        vals = {"binding_active": False, "sync_date": fields.Datetime.now()}
        message = (
            "Partner bank account no longer exists in Dimoni "
            f"(ROW_ID: {row_id})."
        )
        vals["raw_payload"] = (
            f"{binding.raw_payload}\n\n{message}" if binding.raw_payload else message
        )
        binding.write(vals)
        return binding
