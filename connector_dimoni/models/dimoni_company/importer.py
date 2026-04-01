# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.component.core import Component


class DimoniCompanyImporter(Component):
    _name = "dimoni.company.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.company"

    def _clean_scalar(self, value):
        while True:
            mapping = getattr(value, "_mapping", None)
            if mapping is not None:
                value = next(iter(mapping.values()), False)
                continue
            if isinstance(value, (list, tuple)) and len(value) == 1:
                value = value[0]
                continue
            if isinstance(value, bytes):
                value = value.decode(errors="ignore")
            return value

    def _clean_char(self, value):
        value = self._clean_scalar(value)
        return (str(value) if value not in (False, None) else "").strip()

    def _clean_int(self, value):
        value = self._clean_scalar(value)
        if value in (False, None, ""):
            return 0
        return int(str(value).strip())

    def run(self):
        company_model = self.env["dimoni.company"]
        imported_companies = company_model.browse()

        for row in self.backend_adapter.search():
            external_id = str(self._clean_int(row.get("ROW_ID")))
            binding = self.binder.to_internal(external_id)
            map_record = self.mapper.map_record(row)
            vals = dict(map_record.values())
            vals["row_id"] = self._clean_int(row.get("ROW_ID"))
            vals["grp_id"] = self._clean_char(row.get("GRP_ID"))
            vals["code"] = self._clean_char(row.get("CodEmpre"))
            vals["name"] = self._clean_char(row.get("Nombre"))
            vals["sync_date"] = fields.Datetime.now()

            if binding:
                binding.write(vals)
                company = binding
            else:
                company = company_model.search(
                    [
                        ("backend_id", "=", self.backend_record.id),
                        ("grp_id", "=", vals["grp_id"]),
                    ],
                    limit=1,
                )
                if company:
                    company.write(dict(vals, external_id=external_id))
                else:
                    company = company_model.create(dict(vals, external_id=external_id))

            self.binder.bind(external_id, company)
            imported_companies |= company

        return imported_companies
