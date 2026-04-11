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

    def _prepare_product_vals(self, row):
        return {
            "default_code": self._clean_char(row.get("Codigo")),
            "name": self._clean_char(row.get("Descripc")),
        }

    def run(self, code):
        rows = self.backend_adapter.search_by_code(code)
        if not rows:
            raise UserError(
                self.env._("No product found in Dimoni for the given code and backend.")
            )

        row = rows[0]
        external_id = self._clean_char(row.get("ROW_ID"))
        product_vals = self._prepare_product_vals(row)
        sync_date = fields.Datetime.now()

        binding = self.binder.to_internal(external_id)
        if binding:
            binding.odoo_id.write(product_vals)
            binding.write({"sync_date": sync_date, "active": True})
            return binding.odoo_id

        product = self.env["product.template"].search(
            [("default_code", "=", product_vals["default_code"])],
            limit=1,
        )
        if product:
            product.write(product_vals)
        else:
            product = self.env["product.template"].create(product_vals)

        binding = self.env["dimoni.product.template"].create(
            {
                "backend_id": self.backend_record.id,
                "odoo_id": product.id,
                "external_id": external_id,
                "sync_date": sync_date,
            }
        )
        self.binder.bind(external_id, binding)
        return product
