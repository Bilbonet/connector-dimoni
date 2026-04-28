# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DimoniBinding(models.AbstractModel):
    _name = "dimoni.binding"
    _inherit = "external.binding"
    _description = "Dimoni Binding (abstract)"
    _rec_name = "external_id"

    # Common fields for all Dimoni binding models
    # 'odoo_id': odoo-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name="dimoni.backend",
        string="Dimoni Backend",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    binding_active = fields.Boolean(
        default=True,
        help=(
            "Technical active state of the Dimoni binding. This field is not "
            "named active to avoid shadowing the delegated Odoo record active "
            "field in _inherits binding models."
        ),
    )
    external_id = fields.Integer(
        string="Dimoni ROW_ID",
        readonly=True,
        required=True,
        help="Primary key in database Dimoni",
    )
    sync_date = fields.Datetime(
        string="Last Synchronization",
        readonly=True,
        help="Date and time of the last synchronization with Dimoni.",
    )
    raw_payload = fields.Text(
        readonly=True,
        help="Raw Payload (JSON)",
    )

    _sql_constraints = [
        (
            "dimoni_uniq",
            "unique(backend_id, external_id)",
            "A record with same ID on Dimoni already exists.",
        ),
    ]
