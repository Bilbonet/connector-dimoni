# AGENTS.md

Template context file for an **Odoo 18** module.

This document is intended to help automated agents and development assistants
understand **what this module does**, **which dependencies it has**, **which parts are critical**,
and **which constraints must be respected** when analyzing or modifying it.

General repository-wide technical rules (OCA standards, linting, formatting, workflows,
pre-commit, development conventions, etc.) are **not duplicated here**.
Those rules must be obtained from the repository executable configuration
and/or from the applicable Skills.

---

# 1. Module Identification

## Technical Name

`<module_name>`

## Functional Name

`<functional_name>`

## Status

`<draft / active / maintenance / deprecated>`

## Target Version

- Odoo: `18.0`
- Target branch: `18.0`

---

# 2. Module Purpose

## Functional Summary

<Explain in 2 to 5 sentences what the module does and which need it solves.>

## Business Problem Covered

<Describe the actual business problem solved by this module.>

## Expected Outcome

<Describe the expected functional behavior once the module is installed and configured.>

---

# 3. Functional Scope

## Included

- <main_feature_1>
- <main_feature_2>
- <main_feature_3>

## Not Included

- <out_of_scope_1>
- <out_of_scope_2>

## Main Use Cases

- <use_case_1>
- <use_case_2>
- <use_case_3>

---

# 4. Business Objects

## New Models

| Model | Purpose | Comments |
|--------|---------|----------|
| `<model.name>` | <what it represents> | <relevant notes> |
| `<model.name>` | <what it represents> | <relevant notes> |

## Extended Models

| Model | What is added or changed | Functional Impact |
|--------|---------------------------|-------------------|
| `<existing.model>` | <fields / logic / constraints> | <impact> |
| `<existing.model>` | <fields / logic / constraints> | <impact> |

## Object Relationships

<Briefly explain how the main models are related.>

Example:

- `<model.a>` belongs to `<model.b>`
- `<model.c>` is generated from `<model.a>`
- `<model.d>` stores synchronization state

---

# 5. Functional Flow

Describe the main functional flow of the module.

## Main Flow

1. <step_1>
2. <step_2>
3. <step_3>
4. <step_4>

## Alternative or Secondary Flows

- <alternative_flow_1>
- <alternative_flow_2>

## Relevant Events

- <event_1>
- <event_2>
- <event_3>

---

# 6. External Integrations

Complete this section only if the module integrates with external systems.

## Integrated Systems

| System | Type | Flow Direction | Purpose |
|---------|------|----------------|---------|
| `<system>` | `<API / webhook / SOAP / file / email / other>` | `<Odoo -> external / external -> Odoo / bidirectional>` | <objective> |

## Integration Details

### `<system_name>`

- protocol: `<REST / SOAP / XML-RPC / JSON-RPC / SFTP / SMTP / other>`
- authentication: `<none / basic / token / oauth / api key / other>`
- main operation: `<what it does>`
- frequency: `<real time / on demand / cron / manual>`
- external identifier used: `<field or rule>`
- retry tolerance: `<yes/no and how>`

## Integration Constraints

- <constraint_1>
- <constraint_2>

---

# 7. Dependencies

## Odoo Dependencies

Actual dependencies must match `__manifest__.py`.

- `<module_dependency_1>`
- `<module_dependency_2>`
- `<module_dependency_3>`

## Python Dependencies

Complete only if applicable.

- `<library_1>`
- `<library_2>`

## External Functional Dependencies

- <external_service_1>
- <external_service_2>

---

# 8. Required Configuration

## Mandatory Configuration

- <configuration_1>
- <configuration_2>
- <configuration_3>

## Optional Configuration

- <optional_configuration_1>
- <optional_configuration_2>

## Relevant Parameters or Master Data

- <parameter_1>
- <parameter_2>

---

# 9. Automations and Scheduled Processes

## Cron Jobs

| Cron | Purpose | Frequency | Risk If It Fails |
|------|---------|-----------|------------------|
| `<cron_name>` | <what it does> | <frequency> | <impact> |
| `<cron_name>` | <what it does> | <frequency> | <impact> |

## Manual Processes

- <manual_process_1>
- <manual_process_2>

## Event-Triggered Processes

- <trigger_1>
- <trigger_2>

---

# 10. Views and User Interaction

## Main Views

- <view_1>
- <view_2>
- <view_3>

## Relevant Actions

- <action_1>
- <action_2>

## User-Visible Changes

- <visible_change_1>
- <visible_change_2>

---

# 11. Security and Permissions

## Affected Groups or Roles

| Group | Access | Notes |
|-------|--------|-------|
| `<group>` | `<read / write / create / unlink / configure>` | <notes> |
| `<group>` | `<read / write / create / unlink / configure>` | <notes> |

## Important Rules

- <rule_1>
- <rule_2>

## Security Risks

- <risk_1>
- <risk_2>

---

# 12. Critical Data and Side Effects

## Sensitive or Critical Data

- <critical_data_1>
- <critical_data_2>

## Side Effects When Modifying This Module

- <side_effect_1>
- <side_effect_2>
- <side_effect_3>

Typical examples:

- accounting entry changes
- duplicated synchronizations
- third-party data resubmission
- document regeneration
- automatic state changes

---

# 13. Critical Functional Constraints

These rules must not be broken without explicit human review.

- <critical_constraint_1>
- <critical_constraint_2>
- <critical_constraint_3>

Typical examples:

- do not change external integration contracts
- do not alter external identifiers already in use
- do not change accounting logic without functional validation
- do not modify business states without reviewing downstream impacts
- do not introduce automations that may duplicate submissions or processes

---

# 14. Known Limitations

- <limitation_1>
- <limitation_2>
- <limitation_3>

## Module Assumptions

- <assumption_1>
- <assumption_2>

---

# 15. Expectations for Automated Agents

## Agents Must

- understand the functional purpose of the module before changing code
- keep changes limited to the scope of the requested task
- respect existing dependencies, contracts, and integrations
- review the impact on models, security, data, and automations
- update functional documentation if visible behavior changes
- rely on the actual repository configuration for technical rules

## Agents Must Not

- invent functional behavior not described in the module context
- introduce changes outside the scope of the module or task
- break Odoo 18 compatibility
- alter external integrations without reviewing contracts and effects
- modify critical logic without making it explicit
- merge, deploy, or execute destructive actions without human approval

---

# 16. Impact Checklist Before Modifying the Module

Before making changes, review:

- [ ] `__manifest__.py`
- [ ] affected models
- [ ] affected views
- [ ] security (`ir.model.access.csv`, rules, groups)
- [ ] XML data / demo data / configuration
- [ ] cron jobs and automations
- [ ] external integrations
- [ ] side effects
- [ ] functional documentation
- [ ] relevant tests

---

# 17. Module-Specific Information to Complete

Fill this section with the actual context of the current module.

## Executive Summary

<Short and direct summary of the specific module.>

## Change Risk

`<low / medium / high>`

## Especially Sensitive Areas

- <sensitive_area_1>
- <sensitive_area_2>

## Do Not Modify Unless Explicitly Requested

- <restricted_area_1>
- <restricted_area_2>

## Additional Notes

<Free-form notes useful for agents and developers.>

---

# 18. History

| Date | Changes |
|------|---------|
| `<yyyy-mm-dd>` | Creation or update of this AGENTS.md |
