from odoo.addons.component.core import AbstractComponent


class DimoniImportMapper(AbstractComponent):
    _name = "dimoni.import.mapper"
    _inherit = ["base.dimoni.connector", "base.import.mapper"]
    _usage = "import.mapper"
