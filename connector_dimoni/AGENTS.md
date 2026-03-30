# AGENTS.md

Context file for the `connector_dimoni` Odoo 18 module.

This document contains module-specific functional and architectural context for
automated agents. General Odoo, OCA, linting, and repository rules must be taken from
active skills and repository configuration.

---

# 1. Module Identification

## Technical Name

`connector_dimoni`

## Functional Name

`Dimoni Connector`

## Status

`active - alpha`

## Target Version

- Odoo: `18.0`
- Module version: `18.0.1.0.0`
- Target branch: `18.0`

---

# 2. Module Purpose

## Functional Summary

This module connects Odoo 18 Community with Exact Dimoni ERP for product import
operations. It is built on top of the OCA Connector framework and currently implements a
manual import flow for a single product identified by code.

## Business Problem Covered

The module avoids re-entering product master data manually in Odoo when the
authoritative source already exists in Dimoni. It also preserves traceability between
the imported Odoo product and the external Dimoni record.

## Expected Outcome

Users can configure a Dimoni backend linked to an MSSQL external source and a
company-specific `GRP_ID`, launch a manual import by product code, and create or update
an Odoo `product.template` while storing the external binding and last sync timestamp.

---

# 3. Functional Scope

## Included

- Backend configuration for Dimoni connections.
- Manual product import from Dimoni by exact product code.
- Binding storage between `product.template` and Dimoni external identifiers.
- Update of existing products when a matching binding or product code exists.

## Not Included

- Automatic scheduled synchronization.
- Export from Odoo to Dimoni.
- Multi-record batch imports.
- Sales, stock, accounting, or other business logic replication from Dimoni.

## Main Use Cases

- Configure one backend per company and Dimoni `GRP_ID`.
- Import a product from Dimoni into Odoo on demand.
- Re-import a product to refresh description or code data from Dimoni.

---

# 4. Business Objects

## New Models

| Model                          | Purpose                       | Comments                                                                         |
| ------------------------------ | ----------------------------- | -------------------------------------------------------------------------------- |
| `dimoni.backend`               | Connector backend definition  | Inherits `connector.backend`; stores company, dbsource, and Dimoni `GRP_ID`.     |
| `dimoni.product.template`      | External binding for products | Inherits `external.binding` and delegates to `product.template` via `_inherits`. |
| `dimoni.product.import.wizard` | Manual import assistant       | Transient model used from backend form.                                          |

## Extended Models

| Model              | What is added or changed      | Functional Impact                                       |
| ------------------ | ----------------------------- | ------------------------------------------------------- |
| `product.template` | `dimoni_binding_ids` one2many | Allows navigation from Odoo product to Dimoni bindings. |

## Object Relationships

- `dimoni.backend` belongs to one `res.company`.
- `dimoni.backend` uses one `base.external.dbsource` restricted to MSSQL.
- `dimoni.product.template` belongs to one `dimoni.backend`.
- `dimoni.product.template` wraps one `product.template`.
- The backend `GRP_ID` scopes external queries against Dimoni table `PARTI`.

---

# 5. Functional Flow

## Main Flow

1. User opens a `dimoni.backend` record.
2. User launches the `Import product` button.
3. Wizard collects the target backend and the Dimoni product code.
4. The importer queries Dimoni table `PARTI` filtered by backend `GRP_ID` and trimmed
   product code.
5. Mapper converts Dimoni fields `Codigo` and `Descripc` into Odoo values.
6. If an existing binding is found for the external `ROW_ID`, the linked product is
   updated.
7. Otherwise, the module searches `product.template` by `default_code`, updates it if
   found, or creates a new one.
8. The module creates or updates the Dimoni binding and writes `sync_date`.

## Alternative or Secondary Flows

- If no Dimoni row matches the code and backend, the importer raises a `UserError`.
- If multiple rows are returned, only the first row is processed by the current
  implementation.

## Relevant Events

- Manual backend button `action_open_product_import_wizard`.
- Wizard action `action_import`.
- OCA Connector component lookup with `usage="record.importer"`.

---

# 6. External Integrations

## Integrated Systems

| System                                   | Type                 | Flow Direction                     | Purpose                                          |
| ---------------------------------------- | -------------------- | ---------------------------------- | ------------------------------------------------ |
| `Exact Dimoni`                           | `external database`  | `external -> Odoo`                 | Read product master data from Dimoni.            |
| `MSSQL via base_external_dbsource_mssql` | `database connector` | `Odoo -> external` query execution | Execute SQL queries against the Dimoni database. |

## Integration Details

### `Exact Dimoni`

- protocol: `SQL over MSSQL dbsource`
- authentication: `managed by base.external.dbsource configuration`
- main operation: `read product rows from PARTI`
- frequency: `manual / on demand`
- external identifier used: `ROW_ID`
- functional scoping key: `GRP_ID`
- retry tolerance: `no explicit retry mechanism in current module`

## Integration Constraints

- Do not bypass the configured `base.external.dbsource`.
- Do not replace the OCA Connector architecture with ad hoc ORM or SQL logic.
- Preserve `ROW_ID` and backend-scoped bindings as the source of identity.
- Keep `GRP_ID` filtering in place unless a functional change is explicitly requested.

---

# 7. Dependencies

## Odoo Dependencies

These must match `__manifest__.py`.

- `connector`
- `base_external_dbsource_mssql`
- `product`

## Python Dependencies

No direct Python library is declared by this module beyond those required by its Odoo
dependencies.

## External Functional Dependencies

- Access to a Dimoni database exposing table `PARTI`
- A valid MSSQL dbsource configured in Odoo

---

# 8. Required Configuration

## Mandatory Configuration

- Create a `dimoni.backend` record.
- Set `company_id`.
- Set `dimoni_grp_id` with the company key used in Dimoni `PARTI`.
- Link `dbsource_id` to an MSSQL `base.external.dbsource`.

## Optional Configuration

- Existing Odoo products with matching `default_code` can be reused instead of creating
  new products.

## Relevant Parameters or Master Data

- Dimoni table `PARTI`
- External fields currently consumed: `ROW_ID`, `GRP_ID`, `Codigo`, `Descripc`

---

# 9. Automations and Scheduled Processes

## Cron Jobs

No cron jobs are defined in the current module.

## Manual Processes

- Create and maintain backend records.
- Launch manual product imports from the backend form.
- Re-import individual products when external data must be refreshed.

## Event-Triggered Processes

- None beyond direct user-triggered wizard execution.

---

# 10. Views and User Interaction

## Main Views

- `dimoni.backend` tree and form views
- `dimoni.product.import.wizard` form view
- `dimoni.product.template` tree view

## Relevant Actions

- Backend window action `action_dimoni_backend`
- Backend form button `action_open_product_import_wizard`
- Wizard button `action_import`

## User-Visible Changes

- New top-level menu `Dimoni Connector`
- Backend maintenance screen
- Manual product import popup from backend form

---

# 11. Security and Permissions

## Affected Groups or Roles

| Group             | Access                                                  | Notes                                                 |
| ----------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| `base.group_user` | `read/write/create/unlink` on `dimoni.backend`          | Can configure backends in current implementation.     |
| `base.group_user` | `read/write/create/unlink` on `dimoni.product.template` | Can manage binding records in current implementation. |

## Important Rules

- Credentials must remain in dbsource configuration, never hardcoded in code.
- Backend records are company-related, but no extra record rules are defined in this
  module.

## Security Risks

- Broad access on backend and binding models may be too permissive for production use.
- External connection details rely on the security of `base.external.dbsource`.

---

# 12. Critical Data and Side Effects

## Sensitive or Critical Data

- External identity link: `dimoni.product.template.external_id`
- Backend scoping key: `dimoni_product_template.dimoni_grp_id` and
  `dimoni.backend.dimoni_grp_id`
- Last synchronization timestamp: `sync_date`
- Product master fields updated on import: currently `default_code` and `name`

## Side Effects When Modifying This Module

- Incorrect binding behavior can duplicate products or break traceability.
- Changes to matching logic can overwrite the wrong `product.template`.
- Removing `GRP_ID` scoping can import cross-company or cross-tenant data.
- Changes in mapper/importer logic can alter re-import behavior silently.

---

# 13. Critical Functional Constraints

These rules must not be broken without explicit human review.

- Do not replace the existing backend + binding + component architecture.
- Do not change the identity contract based on backend + external `ROW_ID`.
- Do not remove or weaken `GRP_ID` filtering without validating business impact.
- Do not hardcode external connection parameters or credentials.
- Do not introduce automatic synchronization without explicit request and impact review.

---

# 14. Known Limitations

- Only manual single-product import is implemented.
- Only product code and description are mapped.
- The importer processes only the first row returned by the external query.
- No export flow exists from Odoo to Dimoni.
- No automated tests are present in this module yet.

## Module Assumptions

- `Codigo` identifies the intended product within the backend `GRP_ID` scope.
- Table `PARTI` and the consumed columns are stable in the external system.
- Reusing an existing `product.template` by `default_code` is acceptable business
  behavior.

---

# 15. Expectations for Automated Agents

## Agents Must

- review `__manifest__.py`, models, components, views, and security before editing
- preserve OCA Connector usage patterns already implemented in this module
- keep changes minimal and low-risk unless broader refactoring is requested
- validate impacts on traceability, bindings, and product matching behavior
- update documentation when visible behavior or configuration changes

## Agents Must Not

- invent new business flows not supported by current code or explicit instructions
- replace connector components with ad hoc SQL or HTTP access
- alter external identifiers or binding rules without review
- add dependencies without clear need
- introduce destructive data migrations without explicit approval

---

# 16. Impact Checklist Before Modifying the Module

Before making changes, review:

- [ ] `__manifest__.py`
- [ ] affected models
- [ ] affected connector components
- [ ] affected views and wizard flow
- [ ] security (`ir.model.access.csv`, rules, groups)
- [ ] dbsource usage and external query contract
- [ ] side effects on binding and product deduplication
- [ ] functional documentation
- [ ] relevant tests or missing test coverage

---

# 17. Module-Specific Information to Complete

## Executive Summary

`connector_dimoni` is an alpha-stage Odoo 18 connector module that imports products
manually from Exact Dimoni through MSSQL, using the OCA Connector framework and
persistent binding records for traceability.

## Change Risk

`medium`

## Especially Sensitive Areas

- `components/product_importer.py`
- `components/product_adapter.py`
- binding uniqueness and matching logic
- backend scoping by company and `GRP_ID`

## Do Not Modify Unless Explicitly Requested

- connector architecture selection
- identity contract based on `ROW_ID`
- search scope on Dimoni `PARTI`
- product matching fallback by `default_code`

## Additional Notes

The repository-level reference AGENTS in the external project states the same core
constraints: preserve backend/binding/mapper/adapter design, keep synchronization
traceability intact, and prefer minimal low-risk changes.

---

# 18. History

| Date         | Changes                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| `2026-03-30` | Replaced template placeholders with module-specific context extracted from code and repository references. |
