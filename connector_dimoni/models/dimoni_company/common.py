# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.component.core import Component


class DimoniCompany(models.Model):
    _name = "dimoni.company"
    _inherit = "dimoni.binding"
    _description = "Dimoni Company"
    _rec_name = "name"
    _order = "code, name"

    row_id = fields.Integer(
        string="Dimoni ROW_ID",
        required=True,
        readonly=True,
        index=True,
        help="Primary key of the company in Dimoni.",
    )
    grp_id = fields.Char(
        string="Dimoni GRP_ID",
        required=True,
        readonly=True,
        index=True,
        help="Company key used by Dimoni to scope the rest of the data.",
    )
    code = fields.Char(
        string="Company Code",
        required=True,
        readonly=True,
        help="Short company code shown to the user in the interface.",
    )
    name = fields.Char(
        required=True,
        readonly=True,
    )

    _sql_constraints = [
        (
            "dimoni_company_backend_grp_uniq",
            "unique(backend_id, grp_id)",
            "A company with the same GRP_ID already exists on this backend.",
        ),
    ]

    def _compute_display_name(self):
        for record in self:
            label = record.name or record.external_id
            if record.code:
                label = f"[{record.code}] {label}"
            elif record.grp_id:
                label = f"[{record.grp_id}] {label}"
            record.display_name = label


class DimoniCompanyAdapter(Component):
    _name = "dimoni.company.adapter"
    _inherit = "dimoni.backend.adapter"
    _apply_on = "dimoni.company"

    def search(self):
        query = """
            SELECT ROW_ID, GRP_ID, CodEmpre, Nombre
            FROM SEMPE
            ORDER BY CodEmpre, Nombre
        """
        return self._execute_dicts(
            query=query,
            columns=["ROW_ID", "GRP_ID", "CodEmpre", "Nombre"],
        )
