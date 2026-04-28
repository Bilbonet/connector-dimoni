# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DimoniPartnerImportWizard(models.TransientModel):
    _name = "dimoni.partner.import.wizard"
    _description = "Wizard to import one partner from Dimoni"

    backend_id = fields.Many2one(
        comodel_name="dimoni.backend",
        required=True,
        string="Backend",
        default=lambda self: self.env["dimoni.backend"]._get_default_backend().id,
    )
    partner_code = fields.Char(required=True, string="Partner code")

    def action_import(self):
        self.ensure_one()
        with self.backend_id.work_on("dimoni.res.partner") as work:
            importer = work.component(usage="record.importer")
            binding = importer.search_partner(search_ref=self.partner_code.strip())
        if not binding:
            return {"type": "ir.actions.act_window_close"}

        binding = binding[:1]
        partner = binding.odoo_id

        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "res_id": partner.id,
            "view_mode": "form",
            "target": "current",
        }
