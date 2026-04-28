# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.exceptions import UserError
from odoo.osv.expression import AND

from odoo.addons.component.core import Component


class DimoniProductTemplateImporter(Component):
    _name = "dimoni.product.template.importer"
    _inherit = "base.importer"
    _usage = "record.importer"
    _apply_on = "dimoni.product.template"

    def search_product(self, *, search_ref=None, force_update=False):
        """
        Search and import Dimoni product by field (code).
        First search the Dimoni product with minimal fields to better performance.
        If any result is found, then retrieve the full record and create/update
        the local binding and linked Odoo prouct.
        """
        if search_ref is None:
            return None
        if isinstance(search_ref, int):
            search_ref = str(search_ref)
        elif not isinstance(search_ref, str):
            raise TypeError("search_ref must be str or int")

        search_ref = search_ref.strip()
        if not search_ref:
            return None

        rows = self.backend_adapter.search_by_code(search_ref)
        if not rows:
            raise UserError(
                self.env._(
                    "No product found in Dimoni for the given referenca and backend."
                )
            )

        products = self.env["dimoni.product.template"].browse()
        for row in rows:
            row_id = row.get("ROW_ID")
            if row_id is None:
                continue
            product = self.get_product(
                row_id=int(row_id),
                force_update=force_update,
            )
            if product:
                products |= product
        return products

    def get_product(self, *, row_id=None, force_update=False):
        """
        Get fields for a single Dimoni product by field (ROW_ID).
        """
        if row_id is None:
            return None
        if not isinstance(row_id, int):
            raise TypeError("row_id must be an int")

        product_data = self.backend_adapter.get_by_row_id(row_id)
        if not product_data:
            self._deactivate_missing_binding(row_id)
            return False

        product = self._ensure_product_template_record(
            product_data[0], force_update=force_update
        )

        return product

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _ensure_product_template_record(self, product_data, force_update=False):
        """
        Ensure that a product template record exists for the given Dimoni product data.
        1.) Search if product already exists.
        2.) If not found, search product.template by dimoni_code.
        :param item_data: dict with Dimoni item data
        :return: dimoni.product.template record
        """
        # 1.) Search Dimoni Product Template.
        external_id = product_data.get("ROW_ID")
        if not external_id:
            return None
        binder = self.binder_for()
        binding = binder.to_internal(external_id)
        if binding:
            if force_update:
                self._update_dimoni_product(product_data=product_data)
            return binding

        # 2.) Search product in product.template by Dimoni Code.
        product_template = self._search_product_by_code(product_data=product_data)
        product = self._create_dimoni_product(
            product_data=product_data, product_template=product_template
        )
        return product

    def _update_dimoni_product(self, *, product_data):
        """
        Update existing Dimoni product binding from item_data.

        :param item_data: dict with item data from Dimoni
        :return: updated dimoni product record or None
        """
        external_id = product_data.get("ROW_ID")
        binder = self.binder_for()
        binding = binder.to_internal(external_id)

        mapper = self.component(usage="import.mapper")
        map_record = mapper.map_record(product_data)
        product_vals = map_record.values()
        if not product_vals:
            return binding

        binding.write(product_vals)
        return binding

    def _search_product_by_code(self, *, product_data):
        """
        Search product template by Dimoni code.

        :item_data: dict with item data from Dimoni
        :return: product template record or None
        """
        dimoni_code = product_data.get("Codigo")
        company_id = self.backend_record.company_id.id
        company_domain = [
            ("company_id", "in", [False, company_id]),
        ]

        pt_obj = self.env["product.template"].sudo()
        product_template = pt_obj.browse()
        product_template_domain = [("default_code", "=", dimoni_code)]
        search_domain = AND([product_template_domain, company_domain])

        product_template = pt_obj.search(search_domain, limit=1)
        if product_template:
            return product_template

    def _create_dimoni_product(self, *, product_data, product_template=None):
        """
        Create Dimoni Product from item_data.

        :param:
        item_data: dict with item data from Dimoni
        product_template: Object product template or none

        :return: created Dimoni product record or None
        """
        mapper = self.component(usage="import.mapper")
        map_record = mapper.map_record(product_data)
        product_vals = map_record.values()
        if not product_vals:
            return False

        if product_template:
            product_vals.update(
                {
                    "odoo_id": product_template.id,
                }
            )

        product_model = self.env["dimoni.product.template"].sudo()
        product = product_model.create(product_vals)
        if product:
            return product

        return None

    def _deactivate_missing_binding(self, row_id):
        binding = (
            self.env["dimoni.product.template"]
            .with_context(active_test=False)
            .search(
                [
                    ("backend_id", "=", self.backend_record.id),
                    ("external_id", "=", row_id),
                ],
                limit=1,
            )
        )
        if not binding:
            return False

        vals = {"binding_active": False, "sync_date": fields.Datetime.now()}
        message = (
            "Product no longer exists in Dimoni for the current backend "
            f"(ROW_ID: {row_id})."
        )
        vals["raw_payload"] = (
            f"{binding.raw_payload}\n\n{message}" if binding.raw_payload else message
        )
        binding.write(vals)
        return binding
