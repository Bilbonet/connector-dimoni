from odoo.addons.component.core import AbstractComponent


class BaseDimoniConnectorComponent(AbstractComponent):
    _name = "base.dimoni.connector"
    _inherit = "base.connector"
    _collection = "dimoni.backend"
