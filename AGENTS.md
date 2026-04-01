# AGENTS.md

## Purpose

This file contains only repository-level context for the `connector-dimoni`
workspace. General Odoo/OCA rules and detailed Connector architecture rules are
provided by the active skills, especially `odoo-oca-connector`.

## Repository Context

- Technical integration between Odoo 18 Community and Exact Dimoni ERP.
- Built on top of the OCA Connector framework.
- Current implemented scope is manual import of product templates from Dimoni.
- The module-specific source of truth is
  `connector_dimoni/AGENTS.md`.

## Workspace Policy

- Keep changes inside the current integration scope unless explicitly asked to
  extend it.
- Prefer minimal, low-risk edits that preserve traceability between Odoo and
  Dimoni.
- Do not introduce alternative connector architectures at repository level.
