# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import AbstractComponent


class BaseDimoniConnector(AbstractComponent):
    _name = "base.dimoni.connector"
    _inherit = "base.connector"
    _collection = "dimoni.backend"
