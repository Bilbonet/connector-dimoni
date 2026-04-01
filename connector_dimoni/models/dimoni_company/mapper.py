# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class DimoniCompanyImportMapper(Component):
    _name = "dimoni.company.import.mapper"
    _inherit = "dimoni.import.mapper"
    _apply_on = "dimoni.company"

    direct = [
        ("ROW_ID", "row_id"),
        ("GRP_ID", "grp_id"),
        ("CodEmpre", "code"),
        ("Nombre", "name"),
    ]
