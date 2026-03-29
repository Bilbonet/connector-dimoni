from odoo.addons.component.core import Component


class DimoniProductAdapter(Component):
    _name = "dimoni.product.adapter"
    _inherit = "dimoni.base"
    _usage = "backend.adapter"
    _apply_on = "dimoni.product.template"

    def _dbsource(self):
        return self.backend_record.dbsource_id

    def _row_to_dict(self, row):
        mapping = getattr(row, "_mapping", None)
        if mapping:
            return dict(mapping)
        if isinstance(row, dict):
            return row
        return {
            "ROW_ID": row[0],
            "GRP_ID": row[1],
            "Codigo": row[2],
            "Descripc": row[3],
        }

    def search_by_code(self, code):
        query = """
            SELECT ROW_ID, GRP_ID, Codigo, Descripc
            FROM PARTI
            WHERE GRP_ID = :grp_id
              AND LTRIM(RTRIM(Codigo)) = :code
        """
        rows = self._dbsource().execute(
            query=query,
            execute_params={
                "grp_id": self.backend_record.dimoni_grp_id,
                "code": code.strip(),
            },
        )
        return [self._row_to_dict(row) for row in rows]
