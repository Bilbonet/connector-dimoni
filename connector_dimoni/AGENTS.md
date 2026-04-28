# AGENTS.md

Module context for `connector_dimoni`.

Repository-level context stays in the parent `AGENTS.md`. Keep this file limited to
module-specific impact and risks.

## Functional Intent

Connect Odoo 18 with Exact Dimoni through the OCA Connector framework and an MSSQL
external datasource.

The implemented scope is manual import of Dimoni companies, products, and partners.
Imports preserve an Odoo <-> Dimoni binding using Dimoni `ROW_ID` and the selected
backend company scope `GRP_ID`.

## Current Scope

- Configure Dimoni backends with one `base.external.dbsource` MSSQL connection.
- Import Dimoni companies from `SEMPE`; the selected company provides backend `GRP_ID`.
- Import one product at a time by `Codigo` from `PARTI`, with extended description from
  `PARTT`.
- Import one partner at a time by `Codigo` from `PCTAS`.
- Refresh already bound products or partners from their binding/form buttons.
- Store raw payload JSON only when `dimoni.backend.store_raw_payload` is enabled.

Out of scope in the current code: scheduled sync, queue jobs, batch imports, exports,
variants, bank accounts, sales, stock, accounting, and child contact synchronization.

## Key Models

- `dimoni.backend`: connector backend, datasource, selected `dimoni.company`, active/default flags.
- `dimoni.binding`: shared binding base with `backend_id`, integer `external_id`, `binding_active`,
  `sync_date`, and optional `raw_payload`.
- `dimoni.company`: imported Dimoni company; unique by backend and `GRP_ID`.
- `dimoni.product.template`: `_inherits` binding for `product.template`.
- `dimoni.res.partner`: `_inherits` binding for `res.partner`.
- `dimoni.product.import.wizard` and `dimoni.partner.import.wizard`: manual single-record import
  entry points.

## Import Flows

- Companies: backend button reads all `SEMPE` rows, upserts by backend plus `ROW_ID` or `GRP_ID`,
  binds them, and deletes or deactivates missing companies.
- Products: wizard/backend/product UI searches `PARTI` by trimmed `Codigo`, fetches by `ROW_ID`,
  reuses an existing binding, otherwise matches `product.template.default_code` in the backend
  Odoo company or global records, then creates the binding.
- Partners: wizard/backend/partner UI searches `PCTAS` by trimmed `Codigo`, fetches by `ROW_ID`,
  reuses an existing binding, otherwise matches `res.partner.ref` in the backend Odoo company or
  global records, then creates the binding.

## Mapped Fields

- Company: `ROW_ID`, `GRP_ID`, `CodEmpre`, `Nombre`.
- Product: `ROW_ID`, `Codigo`, `Descripc`, `Ampliaci`, `Activo`, `Pvp_01`, `TipoArti`.
- Partner: `ROW_ID`, `Codigo`, `Razon`, `Nombre`, `direccio`, `CPostal`, `Localida`, `Nif`,
  `Activo`.

## Sensitive Areas

- Integration: every product and partner query must remain scoped by backend `GRP_ID`.
- Identity: `ROW_ID` is the external identifier; do not replace binder usage with ad hoc links.
- Deduplication: fallback matching by `default_code` and `ref` can bind Dimoni records to existing
  Odoo records; review company scope before changing it.
- Security: ACLs give connector managers write/create/unlink on bindings and backends; normal users
  have read-only binding/backend access but can open the import wizards.
- UI hooks: JS view registrations add Dimoni import buttons to product and partner list/kanban views.
- Migration: `18.0.1.0.1` renames old binding `active` columns to `binding_active`.

## Dependencies

- `connector`
- `base_external_dbsource_mssql`
- `product`

## Open Points

- No automated tests are present.
- No record rules are defined in this module.
- No server actions, crons, or queue jobs are defined.
