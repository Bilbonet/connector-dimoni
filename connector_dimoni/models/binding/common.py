from odoo import fields, models


class DimoniBinding(models.AbstractModel):
    _name = "dimoni.binding"
    _inherit = "external.binding"
    _description = "Dimoni Binding (abstract)"
    # _rec_name = "external_id"

    # 'odoo_id': odoo-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name="dimoni.backend",
        string="Dimoni Backend",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    active = fields.Boolean(default=True, readonly=True)
    external_id = fields.Char(
        string="Dimoni ROW_ID",
        readonly=True,
        required=True,
    )
    sync_date = fields.Datetime(
        string="Last Synchronization",
        readonly=True,
        help="Date and time of the last synchronization with Dimoni.",
    )

    _sql_constraints = [
        (
            "dimoni_uniq",
            "unique(backend_id, external_id)",
            "A record with same ID on Dimoni already exists.",
        ),
    ]
