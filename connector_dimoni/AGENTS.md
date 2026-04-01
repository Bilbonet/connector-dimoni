# AGENTS.md

Context file for the `connector_dimoni` Odoo 18 module.

General Odoo/OCA rules and detailed OCA Connector architecture guidance come
from the active skills, especially `odoo-oca-connector`. This file keeps only
module-specific context that an agent needs before changing code.

## Module Identification

- Technical name: `connector_dimoni`
- Functional name: `Dimoni Connector`
- Status: `active - alpha`
- Odoo version: `18.0`
- Module version: `18.0.1.0.0`
- Target branch: `18.0`

## Module Purpose

This module connects Odoo 18 Community with Exact Dimoni through the OCA
Connector framework.

Current implemented goal:

- manually import one `product.template` at a time by product code
- avoid re-entering master data already maintained in Dimoni
- preserve a persistent Odoo <-> Dimoni identity link through connector
  bindings

## Current Functional Scope

Included:

- backend configuration model `dimoni.backend`
- product binding model `dimoni.product.template`
- manual wizard `dimoni.product.import.wizard`
- product import adapter, mapper, binder, and importer flow
- re-import of already linked products
- fallback matching by `default_code` when no binding exists yet

Not included by default:

- scheduled synchronization
- batch imports
- product export flows
- variant-level synchronization
- partner, bank account, sale, stock, or accounting synchronization

## Current Business Rules

- The authoritative external identity is `ROW_ID`.
- Dimoni searches are always scoped by backend `dimoni_grp_id`.
- Manual imports are performed one record at a time by external code.
- If a binding exists, the linked Odoo record is updated.
- If no binding exists, the importer may reuse an existing
  `product.template` by `default_code`.
- If no Odoo match exists, a new `product.template` is created.

## External Contract

- External system: `Exact Dimoni`
- Access mode: `MSSQL` via `base.external.dbsource`
- Current source table: `PARTI`
- Current scope key: `GRP_ID`
- Current external identifier: `ROW_ID`
- Current imported fields:
  - `ROW_ID`
  - `GRP_ID`
  - `Codigo`
  - `Descripc`

Do not assume other Dimoni tables, keys, or semantics without checking the real
external schema first.

## Important Module Areas

- `components/` contains shared connector abstractions reused by entities.
- `models/dimoni_backend/` contains backend configuration.
- `models/binding/` contains the shared binding base.
- `models/product_template/` contains the current entity-specific product
  integration.
- `wizard/` contains the thin manual trigger for product import.

## Data and Risk Constraints

- Preserve Odoo <-> Dimoni identity traceability through bindings.
- Preserve backend scoping by `dimoni_grp_id`.
- Keep credentials in `base.external.dbsource`, never in code.
- Treat fallback matching by `default_code` as a sensitive deduplication rule.
- Be careful with changes that can duplicate records or bind the wrong Odoo
  record to a Dimoni `ROW_ID`.

## Change Policy

- Prefer minimal, low-risk changes.
- Review the real implementation before editing.
- Reuse the module's existing patterns and names.
- Ask before changing functional behavior or external contracts.
- Do not add new dependencies without a clear need.
- Update views, security, and documentation when user-visible scope changes.

## Known Limitations

- Only manual single-record product import exists today.
- Only product templates are integrated.
- Only a small set of external fields is mapped.
- Export scaffolding may exist, but no concrete export flow is implemented.
- No automated tests are present yet.
