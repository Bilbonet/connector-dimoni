# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from odoo.addons.component.core import AbstractComponent


class DimoniBackendAdapter(AbstractComponent):
    """Shared backend adapter for Dimoni database access."""

    _name = "dimoni.backend.adapter"
    _inherit = ["base.backend.adapter", "base.dimoni.connector"]
    _usage = "backend.adapter"

    def _backend_scope_params(self, **params):
        """Return query parameters scoped to the selected Dimoni company.

        Dimoni stores data for multiple companies in the same database, so
        every query must include the ``GRP_ID`` filter. This helper ensures the
        backend has a selected company and injects its identifier as
        ``GRP_ID`` before merging any extra parameters.
        """
        if not self.backend_record.grp_id:
            raise UserError(
                self.env._(
                    "Import the companies from Dimoni and select "
                    "one on the backend before importing records."
                )
            )
        scoped_params = {"grp_id": self.backend_record.grp_id}
        scoped_params.update(params)
        return scoped_params

    def _execute(self, query, params=None, metadata=False):
        """Execute a query on the datasource configured on the backend.

        query: SQL query to execute.
        params (dict | list | tuple | None): Optional query parameters.
        metadata (bool): Whether the datasource should also return column metadata
                         together with the fetched rows.

        Local variables:
            dbsource: Datasource record linked to the current backend.

        Returns:
            list: Query result rows when ``metadata`` is ``False``.
            dict: A dictionary with ``cols`` and ``rows`` keys when using the
                MSSQL connector and ``metadata`` is ``True``.
            Any: Whatever is returned by ``dbsource.execute(...)`` for
                non-MSSQL datasources.
        """
        dbsource = self.backend_record.dbsource_id
        if dbsource.connector == "mssql":
            rows, cols = dbsource.execute_mssql(query, params, metadata)
            if metadata:
                return {"cols": cols, "rows": rows}
            return rows
        return dbsource.execute(
            query=query,
            execute_params=params,
            metadata=metadata,
        )

    def _normalize_value(self, value):
        while True:
            mapping = getattr(value, "_mapping", None)
            if mapping is not None:
                if len(mapping) == 1:
                    value = next(iter(mapping.values()), False)
                    continue
                return {
                    key: self._normalize_value(item) for key, item in mapping.items()
                }
            if isinstance(value, dict):
                return {key: self._normalize_value(item) for key, item in value.items()}
            if isinstance(value, list | tuple):
                if len(value) == 1:
                    value = value[0]
                    continue
                return [self._normalize_value(item) for item in value]
            if isinstance(value, bytes):
                return value.decode(errors="ignore")
            return value

    def _row_to_dict(self, row, columns=None):
        mapping = getattr(row, "_mapping", None)
        if mapping:
            return {key: self._normalize_value(value) for key, value in mapping.items()}
        if isinstance(row, dict):
            return {key: self._normalize_value(value) for key, value in row.items()}
        if isinstance(row, list | tuple) and len(row) == 1:
            nested = row[0]
            nested_mapping = getattr(nested, "_mapping", None)
            if nested_mapping is not None or isinstance(nested, dict | list | tuple):
                return self._row_to_dict(nested, columns=columns)
        if columns is None:
            raise ValueError("columns are required to normalize sequence rows")
        return {
            key: self._normalize_value(value)
            for key, value in zip(columns, row, strict=False)
        }

    def _rows_to_dicts(self, rows, columns=None):
        return [self._row_to_dict(row, columns=columns) for row in rows]

    def _execute_rows(self, query, params=None):
        return self._execute(query=query, params=params)

    def _execute_dicts(self, query, params=None, columns=None):
        rows = self._execute_rows(query=query, params=params)
        return self._rows_to_dicts(rows, columns=columns)

    def _execute_one(self, query, params=None, columns=None):
        rows = self._execute_dicts(query=query, params=params, columns=columns)
        return rows[0] if rows else None
