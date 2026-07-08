# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.exceptions import UserError
from odoo.osv.expression import AND

from odoo.addons.component.core import Component


class DimoniResPartnerImporter(Component):
    _name = "dimoni.res.partner.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.res.partner"

    def search_partner(self, *, search_ref=None, force_update=False):
        """
        Search and import one Dimoni partner by code.
        """
        if search_ref is None:
            return None
        if isinstance(search_ref, int):
            search_ref = str(search_ref)
        elif not isinstance(search_ref, str):
            raise TypeError("search_ref must be str or int")

        search_ref = search_ref.strip()
        if not search_ref:
            return None

        rows = self.backend_adapter.search_by_code(search_ref)
        if not rows:
            raise UserError(
                self.env._(
                    "No partner found in Dimoni for the given reference and backend."
                )
            )

        partners = self.env["dimoni.res.partner"].browse()
        for row in rows:
            row_id = row.get("ROW_ID")
            if row_id is None:
                continue
            partner = self.get_partner(
                row_id=int(row_id),
                force_update=force_update,
            )
            if partner:
                partners |= partner
        return partners

    def get_partner(self, *, row_id=None, force_update=False):
        """
        Get fields for a single Dimoni partner by ROW_ID.
        """
        if row_id is None:
            return None
        if not isinstance(row_id, int):
            raise TypeError("row_id must be an int")

        partner_data = self.backend_adapter.get_by_row_id(row_id)
        if not partner_data:
            self._deactivate_missing_binding(row_id)
            return False

        return self._ensure_res_partner_record(
            partner_data[0], force_update=force_update
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _ensure_res_partner_record(self, partner_data, force_update=False):
        """
        Ensure that a partner record exists for the given Dimoni data.
        1.) Partner has already been imported
        2.) Not imported but exists a partner with the code in ref
        :param partner_data: dict with Dimoni partner data
        :return: dimoni.res.partner record
        """
        # 1.) Partner has already been imported
        external_id = partner_data.get("ROW_ID")
        if not external_id:
            return None
        binder = self.binder_for()
        binding = binder.to_internal(external_id)
        if binding:
            if force_update:
                binding = self._update_dimoni_partner(partner_data=partner_data)
            self._import_bank_accounts(binding, partner_data, force_update=force_update)
            return binding

        # 2.) Not imported but exists a partner with the code in ref
        partner = self._search_partner_by_ref(partner_data=partner_data)

        binding = self._create_dimoni_partner(
            partner_data=partner_data, partner=partner
        )
        self._import_bank_accounts(binding, partner_data, force_update=force_update)
        return binding

    def _update_dimoni_partner(self, *, partner_data):
        external_id = partner_data.get("ROW_ID")
        binder = self.binder_for()
        binding = binder.to_internal(external_id)

        mapper = self.component(usage="import.mapper")
        map_record = mapper.map_record(partner_data)
        partner_vals = map_record.values()
        if not partner_vals:
            return binding

        binding.write(partner_vals)
        return binding

    def _search_partner_by_ref(self, *, partner_data):
        dimoni_code = partner_data.get("Codigo")
        if not dimoni_code:
            return self.env["res.partner"].browse()

        company_id = self.backend_record.company_id.id
        company_domain = [
            ("company_id", "in", [False, company_id]),
        ]
        partner_domain = [("ref", "=", str(dimoni_code).strip())]
        search_domain = AND([partner_domain, company_domain])

        return self.env["res.partner"].sudo().search(search_domain, limit=1)

    def _create_dimoni_partner(self, *, partner_data, partner=None):
        mapper = self.component(usage="import.mapper")
        map_record = mapper.map_record(partner_data)
        partner_vals = map_record.values()
        if not partner_vals:
            return False

        if partner:
            partner_vals.update({"odoo_id": partner.id})

        return self.env["dimoni.res.partner"].sudo().create(partner_vals)

    def _import_bank_accounts(self, binding, partner_data, force_update=False):
        if not binding:
            return
        id_fiscal = (partner_data.get("Nif") or "").strip()
        partner_ref = (partner_data.get("Codigo") or "").strip()
        if not id_fiscal or not partner_ref:
            return
        importer = self.component(
            usage="record.importer", model_name="dimoni.res.partner.bank"
        )
        importer.import_for_partner(
            id_fiscal=id_fiscal,
            partner_ref=partner_ref,
            partner=binding.odoo_id,
            force_update=force_update,
        )

    def _deactivate_missing_binding(self, row_id):
        binding = (
            self.env["dimoni.res.partner"]
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
            "Partner no longer exists in Dimoni for the current backend "
            f"(ROW_ID: {row_id})."
        )
        vals["raw_payload"] = (
            f"{binding.raw_payload}\n\n{message}" if binding.raw_payload else message
        )
        binding.write(vals)
        return binding
