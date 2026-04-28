# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models

from odoo.addons.component.core import Component


class ResPartner(models.Model):
    _inherit = "res.partner"

    dimoni_binding_ids = fields.One2many(
        comodel_name="dimoni.res.partner",
        inverse_name="odoo_id",
        string="Dimoni Bindings",
    )

    def action_open_dimoni_partners(self):
        self.ensure_one()
        partners = self.dimoni_binding_ids
        if not partners:
            return {"type": "ir.actions.act_window_close"}
        action = {
            "type": "ir.actions.act_window",
            "name": self.env._("Dimoni Partners"),
            "res_model": "dimoni.res.partner",
            "target": "current",
        }
        if len(partners) == 1:
            action.update(
                {
                    "view_mode": "form",
                    "res_id": partners.id,
                }
            )
            return action
        action.update(
            {
                "view_mode": "list,form",
                "domain": [("odoo_id", "=", self.id)],
                "context": {"default_odoo_id": self.id},
            }
        )
        return action

    def action_refresh_dimoni_partner(self):
        self.ensure_one()
        binding = self.dimoni_binding_ids[:1]
        if not binding:
            return {"type": "ir.actions.act_window_close"}
        binding.action_refresh()
        return {"type": "ir.actions.client", "tag": "reload"}


class DimoniResPartner(models.Model):
    _name = "dimoni.res.partner"
    _inherit = "dimoni.binding"
    _inherits = {"res.partner": "odoo_id"}
    _description = "Dimoni Partner Binding"

    odoo_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        readonly=True,
        required=True,
        ondelete="cascade",
    )

    def action_refresh(self):
        self.ensure_one()
        with self.backend_id.work_on("dimoni.res.partner") as work:
            importer = work.component(usage="record.importer")
            importer.get_partner(row_id=self.external_id, force_update=True)


class DimoniResPartnerAdapter(Component):
    _name = "dimoni.res.partner.adapter"
    _inherit = "dimoni.backend.adapter"
    _apply_on = "dimoni.res.partner"
    _dimoni_src = "PCTAS"

    def search_by_code(self, code):
        """Search Dimoni partners by code."""
        query = f"""
            SELECT ROW_ID, GRP_ID, Codigo
            FROM {self._dimoni_src}
            WHERE GRP_ID = :grp_id
              AND LTRIM(RTRIM(Codigo)) = :code
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(code=code.strip()),
            columns=["ROW_ID", "GRP_ID", "Codigo"],
        )

    def get_by_row_id(self, row_id):
        query = f"""
            SELECT
                p.ROW_ID,
                p.GRP_ID,
                p.Codigo,
                p.Activo,
                p.Nombre,
                p.Razon,
                p.direccio,
                p.CPostal,
                p.Localida,
                p.Nif
            FROM {self._dimoni_src} p
            WHERE p.GRP_ID = :grp_id
              AND p.ROW_ID = :row_id
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(row_id=row_id),
            columns=[
                "ROW_ID",
                "GRP_ID",
                "Codigo",
                "Activo",  # 1:Activo / 2:Inactivo
                "Nombre",
                "Razon",
                "direccio",
                "CPostal",
                "Localida",
                "Nif",
            ],
        )
