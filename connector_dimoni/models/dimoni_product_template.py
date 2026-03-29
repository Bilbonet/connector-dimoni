from odoo import fields, models


class DimoniProductTemplate(models.Model):
    _name = "dimoni.product.template"
    _inherit = "external.binding"
    _inherits = {"product.template": "odoo_id"}
    _description = "Dimoni Product Template Binding"

    odoo_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        required=True,
        ondelete="cascade",
    )
    backend_id = fields.Many2one(
        comodel_name="dimoni.backend",
        required=True,
        ondelete="restrict",
    )
    external_id = fields.Char(string="Dimoni ROW_ID", required=True)
    dimoni_grp_id = fields.Char(string="Dimoni GRP_ID", required=True)

    _sql_constraints = [
        (
            "dimoni_product_backend_external_uniq",
            "unique(backend_id, external_id)",
            "A product binding already exists for this backend and external ID.",
        )
    ]
