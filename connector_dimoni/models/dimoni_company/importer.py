# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tools import mute_logger

from odoo.addons.component.core import Component


class DimoniCompanyImporter(Component):
    _name = "dimoni.company.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.company"

    def _get_existing_company(self, external_id, vals):
        dimoni_company_model = self.env["dimoni.company"].with_context(active_test=False)
        return dimoni_company_model.search(
            [
                ("backend_id", "=", self.backend_record.id),
                "|",
                ("external_id", "=", external_id),
                ("grp_id", "=", vals["grp_id"]),
            ],
            limit=1,
        )

    def _deactivate_or_delete_missing_companies(self, imported_companies):
        dimoni_company_model = self.env["dimoni.company"].with_context(active_test=False)
        missing_companies = dimoni_company_model.search(
            [
                ("backend_id", "=", self.backend_record.id),
                ("id", "not in", imported_companies.ids),
            ]
        )
        for company in missing_companies:
            try:
                with self.env.cr.savepoint(), mute_logger("odoo.sql_db"):
                    company.unlink()
            except Exception:
                company.write({"active": False})

    def run(self):
        dimoni_company_model = self.env["dimoni.company"]
        dimoni_imported_companies = dimoni_company_model.browse()
        sync_date = fields.Datetime.now()
        rows = self.backend_adapter.search()

        if not rows:
            return dimoni_imported_companies

        for row in rows:
            external_id = row.get("ROW_ID")

            # Map the data
            mapper = self.component(usage="import.mapper")
            map_record = mapper.map_record(row)
            vals = dict(map_record.values(), sync_date=sync_date, active=True)

            dimoni_company = self._get_existing_company(external_id, vals)
            if dimoni_company:
                dimoni_company.write(dict(vals, external_id=external_id))
            else:
                dimoni_company = dimoni_company_model.create(
                    dict(vals, external_id=external_id)
                )

            self.binder.bind(external_id, dimoni_company)
            dimoni_imported_companies |= dimoni_company

        self._deactivate_or_delete_missing_companies(dimoni_imported_companies)
        return dimoni_imported_companies
