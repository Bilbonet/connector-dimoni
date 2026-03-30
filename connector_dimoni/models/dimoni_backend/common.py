from odoo import fields, models


class DimoniBackend(models.Model):
    _name = "dimoni.backend"
    _inherit = "connector.backend"
    _description = "Dimoni Backend"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    dbsource_id = fields.Many2one(
        comodel_name="base.external.dbsource",
        string="External DB Source",
        required=True,
        ondelete="restrict",
        domain=[("connector", "=", "mssql")],
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    dimoni_grp_id = fields.Char(
        string="Dimoni GRP_ID",
        required=True,
        help="Company key in Dimoni PARTI table used to scope the import.",
    )

    _sql_constraints = [
        (
            "dimoni_backend_company_grp_uniq",
            "unique(company_id, dimoni_grp_id)",
            "A backend already exists for this company and GRP_ID.",
        )
    ]

    def action_open_product_import_wizard(self):
        self.ensure_one()
        return {
            "name": "Import product from Dimoni",
            "type": "ir.actions.act_window",
            "res_model": "dimoni.product.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_backend_id": self.id},
        }
