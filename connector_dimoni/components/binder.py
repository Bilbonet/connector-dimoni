from odoo.addons.component.core import Component


class DimoniModelBinder(Component):
    """Bind records and give Odoo/Dimoni ids correspondence."""

    _name = "dimoni.binder"
    _inherit = ["base.binder", "base.dimoni.connector"]
    _external_field = "external_id"
    _apply_on = [
        "dimoni.product.template",
    ]
