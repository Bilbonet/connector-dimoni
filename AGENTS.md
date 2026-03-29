# AGENTS.md

## Purpose

This file contains only module-specific rules. General Odoo/OCA coding, security, and
style rules are already provided by active skills.

## Module context

- Technical integration module between Odoo 18 Community and Exact Dimoni ERP.
- Built on top of the OCA Connector framework.
- Scope is data synchronization, not replacing business logic in Odoo or Velneo.

References:

- https://odoo-connector.com/
- https://github.com/OCA/connector

## Current functional scope

- Developing....

Out of scope by default:

- New business features not explicitly requested.
- UI customization not required for integration operations.

## Connector framework usage to preserve

Follow the connector patterns already implemented in this module. Do not replace them
with ad hoc ORM or HTTP logic.

## Architecture constraints

- Do not replace OCA Connector with custom architecture.
- Keep the existing backend + binding + mapper/adapter design.
- Do not reorganize module structure unless explicitly requested.

## Data invariants

- Preserve Odoo <-> Dimoni identity links in binding models.
- Preserve synchronization state integrity.
- Never hardcode credentials; use backend configuration.

## Change policy

- Prefer minimal, low-risk changes.
- Ask for clarification before applying changes that alter integration
  behavior/contracts.
- Do not add new dependencies without clear need.

## Agent checklist

1. Confirm the request is inside this module's scope.
2. Review existing implementation before editing.
3. Reuse existing connector usage patterns from this module.
4. Validate Odoo <-> Dimoni traceability is preserved.
5. If business behavior is ambiguous, ask before implementing.
