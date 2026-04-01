# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class DimoniBinder(Component):
    """Bind records and give Odoo/Dimoni ids correspondence."""

    _name = "dimoni.binder"
    _inherit = ["base.binder", "base.dimoni.connector"]
    _external_field = "external_id"
    _apply_on = [
        "dimoni.company",
        "dimoni.product.template",
    ]
