# HITL Protocol

When proposing actions that require human approval, wrap the proposal in a HITL block using the exact delimiters below. The block is presented to a human supervisor and, once approved, routed to the executing agent.

### Approval scope

Each HITL block is self-contained. Prior approvals or rejections carry no authority over future proposals — every plan requires its own approval.

### Actions requiring approval

- Any actuation changing a device setpoint by >10 %
- Creating or closing work orders
- Modifying alarm thresholds
- Schedule or control-strategy changes

Pre-approved (no HITL needed):

- Read-only data queries (sensor readings, metadata)
- Logging observations or internal notes

When in doubt, require approval.

### Format

Three sections required: **Motivation → Actions → Expected Result** (in that order).
Include only the Action sub-tables that apply; omit empty ones. At least one sub-table must be present.
Use exact system identifiers in Target fields. Write Descriptions in plain language for non-technical supervisors.

````
---Begin HITL---
<!-- @agent: {agentId} -->

## Motivation
**Trigger:** {observation or event}
**Reasoning:** {why these actions are appropriate}
**Supporting data:**
- {key data point 1}
- {key data point 2}

## Actions
### Metadata Operations
| # | Op | Target | Type | Fields | Description |
|---|----|--------|------|--------|-------------|
| 1 | create/update | {id} | {type} | field: val | {plain language} |

### Actuations
| # | Target | Type | Command | Params | Description |
|---|--------|------|---------|--------|-------------|
| 1 | {id} | {type} | {cmd} | param: val | {plain language} |

### Service Objects
| # | Op | Object | Target | Fields | Description |
|---|----|--------|--------|--------|-------------|
| 1 | create | alarm/workOrder/errorReport | {id or "new"} | field: val, relatedTo: {uuid} | {plain language} |

## Expected Result
**Summary:** {expected outcome}
**Quantified impact:**
- {measurable impact 1}
- {measurable impact 2}
**Timeframe:** {when results materialize}

---End HITL---
````

### Example

````
---Begin HITL---
<!-- @agent: hvac-optimization-agent-01 -->

## Motivation
**Trigger:** Sustained temperature deviation — Floor 3 averaging 24.2 °C vs 21 °C setpoint since 2026-02-10.
**Reasoning:** Consistent overshoot despite normal AHU scheduling suggests AHU-03 cooling-coil valve degradation. Immediate setpoint adjustment provides short-term relief while inspection addresses root cause.
**Supporting data:**
- AHU-03 cooling-coil delta-T dropped 30 % over the past month
- 3 comfort complaints from Floor 3 this week
- No recent changes to Floor 3 occupancy or equipment load

## Actions
### Actuations
| # | Target | Type | Command | Params | Description |
|---|--------|------|---------|--------|-------------|
| 1 | a3b1c2d4-e5f6-7890-abcd-ef1234567890 | AirHandlingUnit | setSupplyAirTempSetpoint | value: 18, unit: °C | Lower AHU-03 supply air setpoint from 21 °C to 18 °C |

### Service Objects
| # | Op | Object | Target | Fields | Description |
|---|----|--------|--------|--------|-------------|
| 1 | create | workOrder | new | title: Inspect AHU-03 cooling coil valve, priority: medium, assignee: HVAC maintenance, due: 2026-02-20, relatedTo: a3b1c2d4-e5f6-7890-abcd-ef1234567890 | Schedule cooling-coil valve inspection |

## Expected Result
**Summary:** Restore Floor 3 temperatures to 21 °C target; preempt valve failure.
**Quantified impact:**
- Reduce average from 24.2 °C → 21 °C
- Avoid ~€2 500 emergency repair
**Timeframe:** Temperature improvement within 2 h; inspection within 1 week.

---End HITL---
````
