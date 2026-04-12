from odoo import fields, models


class DimoniProductImportWizard(models.TransientModel):
    _name = "dimoni.product.import.wizard"
    _description = "Wizard to import one product from Dimoni"

    backend_id = fields.Many2one(
        comodel_name="dimoni.backend",
        required=True,
        string="Backend",
        default=lambda self: self.env["dimoni.backend"]._get_default_backend().id,
    )
    product_code = fields.Char(required=True, string="Product code")

    def action_import(self):
        self.ensure_one()
        with self.backend_id.work_on("dimoni.product.template") as work:
            importer = work.component(usage="record.importer")
            binding = importer.search_product(search_ref=self.product_code.strip())
        if not binding:
            return {"type": "ir.actions.act_window_close"}

        binding = binding[:1]
        product = binding.odoo_id

        return {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": product.id,
            "view_mode": "form",
            "target": "current",
        }
