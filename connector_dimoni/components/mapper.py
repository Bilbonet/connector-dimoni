# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.components.mapper import mapping


class DimoniImportMapper(AbstractComponent):
    _name = "dimoni.import.mapper"
    _inherit = ["base.dimoni.connector", "base.import.mapper"]
    _usage = "import.mapper"

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}


class DimoniExportMapper(AbstractComponent):
    _name = "dimoni.export.mapper"
    _inherit = ["base.dimoni.connector", "base.export.mapper"]
    _usage = "export.mapper"
