from odoo import fields
from odoo.exceptions import UserError

from odoo.addons.component.core import Component


class DimoniProductTemplateImporter(Component):
    _name = "dimoni.product.template.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.product.template"

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

    def run(self, code):
        rows = self.backend_adapter.search_by_code(code)
        if not rows:
            raise UserError(
                self.env._("No product found in Dimoni for the given code and backend.")
            )
        row = rows[0]
        external_id = self._clean_char(row.get("ROW_ID"))

        binding = self.binder.to_internal(external_id)
        map_record = self.mapper.map_record(row)
        vals = dict(map_record.values())
        vals["default_code"] = self._clean_char(row.get("Codigo"))
        vals["name"] = self._clean_char(row.get("Descripc"))

        if binding:
            binding.odoo_id.write(vals)
            binding.write(
                {
                    "dimoni_grp_id": self._clean_char(row.get("GRP_ID")),
                    "sync_date": fields.Datetime.now(),
                }
            )
            return binding.odoo_id

        product = self.env["product.template"].search(
            [("default_code", "=", vals["default_code"])],
            limit=1,
        )
        if product:
            product.write(vals)
        else:
            product = self.env["product.template"].create(vals)

        binding = self.env["dimoni.product.template"].create(
            {
                "backend_id": self.backend_record.id,
                "odoo_id": product.id,
                "external_id": external_id,
                "dimoni_grp_id": self._clean_char(row.get("GRP_ID")),
                "sync_date": fields.Datetime.now(),
            }
        )
        self.binder.bind(external_id, binding)
        return product
