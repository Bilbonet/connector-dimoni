from odoo import fields
from odoo.exceptions import UserError

from odoo.addons.component.core import Component


class DimoniProductRecordImporter(Component):
    _name = "dimoni.product.record.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.product.template"

    def run(self, code):
        rows = self.backend_adapter.search_by_code(code)
        if not rows:
            raise UserError("No product found in Dimoni for the given code and backend.")
        row = rows[0]
        external_id = str(row["ROW_ID"])

        binding = self.binder.to_internal(external_id)
        map_record = self.mapper.map_record(row)
        vals = map_record.values()
        vals["default_code"] = (vals.get("default_code") or "").strip()
        vals["name"] = (vals.get("name") or "").strip()

        if binding:
            binding.odoo_id.write(vals)
            binding.write(
                {
                    "dimoni_grp_id": row["GRP_ID"],
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
                "dimoni_grp_id": row["GRP_ID"],
                "sync_date": fields.Datetime.now(),
            }
        )
        self.binder.bind(external_id, binding)
        return product
