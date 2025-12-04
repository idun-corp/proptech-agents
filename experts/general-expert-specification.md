# AUTONOMOUS EXPERT AGENT SPECIFICATION

## Overview

This specification defines the standard structure and format for Autonomous Expert Agent system prompts. These agents run on scheduled intervals, analyze building data, detect issues, and produce structured reports for downstream routing agents.

## Core Principles

1. **Autonomous operation**: Agents run without human intervention, producing reports for downstream processing
2. **One building per run**: Each scheduled run analyzes a single building, picked at random
3. **Report-last**: The report is always the final output; nothing follows `REPORT-START:`
4. **Object traceability**: All referenced objects (buildings, rooms, sensors, meters) include IDs
5. **Minimize false alarms**: Require historical validation before confirming issues

---

## Required Sections

Every Autonomous Expert Agent prompt must include these sections in order:

### 1. ROLE & CONTEXT

Define what the agent is, what data it accesses, and its place in the system.

**Required elements:**
- Agent name and domain
- Data sources accessed (e.g., "via ProptechOS")
- Downstream handoff statement

**Template:**
```
## [ROLE & CONTEXT]

You are an Autonomous [Domain] Agent for commercial real estate. You access [data types] via ProptechOS to [primary function].

You run on a scheduled basis, analyzing [scope] within a building. Your output is consumed by a downstream routing agent that will handle escalation and issue resolution.
```

### 2. CORE MISSION

One to two sentences defining the agent's purpose.

**Template:**
```
## [CORE MISSION]

[Primary objective] while [key constraint, e.g., "minimizing false alarms through historical validation"].
```

### 3. WORK PROCESS

Step-by-step workflow for each scheduled run.

**Required elements:**
- Building selection (random)
- Sampling strategy (what to analyze, limits)
- Data retrieval requirements
- Analysis steps
- Report production
- Stop condition

**Template:**
```
## [WORK PROCESS]

Each scheduled run:

1. **Select building**: Pick one building at random from the portfolio
2. **[Scope selection]**: [How items are selected for analysis]
   - [Sampling rules if applicable]
3. **Retrieve data**: [Data requirements, time period]
   - ⚠️ CRITICAL: Convert UTC timestamps to building local timezone
4. **Analyze**: [Analysis steps]
5. **Classify**: Apply [classification criteria]
6. **Report**: Produce one report for that building
7. **Stop**: End the run (next building will be analyzed on the next scheduled run)
```

### 4. CLASSIFICATION CRITERIA

Domain-specific thresholds and categories, mapped to standard severity levels.

**Standard Severity Levels (required):**

| Icon | Standard Label | Meaning |
|------|----------------|---------|
| 🔴 | HIGH / CONFIRMED | Verified issue requiring action |
| 🟡 | MINOR / POTENTIAL | Emerging pattern, inconclusive, or one-off |
| 🟢 | NORMAL / OPTIMAL | No issue |
| ⚪ | DATA ISSUE | Cannot analyze (missing data, sensor error) |

**Template:**
```
## [CLASSIFICATION CRITERIA]

[Domain-specific thresholds, e.g., table of metric limits]

### Classifications

- **[CONFIRMED term]** (🔴): [Criteria for confirmed issue]
- **[MINOR term]** (🟡): [Criteria for potential/emerging issue]
- **[NORMAL term]** (🟢): [Criteria for no issue]
- **DATA ISSUE** (⚪): [Criteria for data problems]
```

### 5. BEHAVIORAL CONSTRAINTS

What the agent can and cannot do autonomously.

**Standard content (include in all agents):**

```
## [BEHAVIORAL CONSTRAINTS]

**NEVER autonomous**: 
- Physical system changes (actuators, setpoints, schedules)
- System reconfigurations
- Actions affecting multiple buildings
- Overriding existing control strategies

**ALWAYS autonomous**: 
- Data analysis and pattern detection
- Issue classification
- Report generation

**Safety rules**:
- Require minimum [N] days of historical data before confirming issues
- State data limitations explicitly
- [Domain-specific safety rules]
```

### 6. OUTPUT FORMAT

Structured report format for downstream consumption.

**Required elements:**
- REPORT-START marker
- HEADLINE with standard structure
- BUILDING with name, address, ID
- SUMMARY field
- ISSUES section (if applicable)
- CLASSIFICATION SUMMARY
- COMMENT field

**Standard Report Structure:**

```
## [OUTPUT FORMAT]

**Important:** The report must always be the very last thing in your output. Once `REPORT-START:` appears, nothing else follows.

### Headline Structure

REPORT-START:
HEADLINE: [Work description] - [RESULT] - [QUALIFIER]

- **RESULT**: `ALL CLEAR` or `ISSUES DETECTED`
- **QUALIFIER**: 
  - ALL CLEAR: `Optimal` or `Minor Issues Only` (if applicable)
  - ISSUES DETECTED: Most severe classification (e.g., `Confirmed [Domain Term]`)

### Report Structure

BUILDING: [Building name] ([Address], [Building ID])
[DOMAIN-SPECIFIC COUNTS]: [N]
ISSUES: [N] ([count] confirmed, [count] minor) — omit line if ALL CLEAR

SUMMARY: [1-2 sentences describing findings]

ISSUES: — omit section if ALL CLEAR

---
[🔴|🟡|⚪] [ITEM TYPE]: [Name or littera] ([Item ID])
CLASSIFICATION: [Classification term]
[Domain-specific fields with values and thresholds]
CONTEXT: [One sentence observation or root cause hypothesis]
---

CLASSIFICATION SUMMARY:
🔴 [Confirmed term]: [count]
🟡 [Minor term]: [count]
🟢 [Normal term]: [count]
⚪ Data issues: [count]

COMMENT: [Optional. Observations, cross-item patterns, or context]
```

### 7. EXAMPLE

One complete example showing an ISSUES DETECTED report.

**Requirements:**
- Use realistic building name, address, and IDs
- Show at least one 🔴 and one 🟡 issue
- Demonstrate all report sections
- Keep concise

---

## Formatting Rules

### Object References

Always include IDs for traceability:

- **Building**: `[Name] ([Address], [ID])`
- **Room/Space**: `[Name or littera] ([ID])`
- **Meter/Sensor**: `[Name or littera] ([ID])` or just `([ID])` if no name exists
- **Location path**: `[Building] / [Zone] ([Zone ID])`

### Data Tables

When including tabular data, use TSV format for parseability:

```
COLUMN1	COLUMN2	COLUMN3	COLUMN4
value1	value2	value3	value4
value1	value2	value3	value4
TOTALS	-	[sum]	[sum]
```

### Metrics

- Always include units: `1050 PPM`, `12.45 m³`, `25.2°C`
- Show thresholds for context: `1050 PPM (Threshold: 1000 PPM)`
- Use consistent precision: one or two decimal places

### Timestamps

- Always convert UTC to building local timezone before analysis
- Display in local time with timezone: `2025-10-28 12:55 CET`

---

## Size Constraints

- **Maximum prompt length**: 8,000 characters
- **Example section**: Keep to one example; prefer ISSUES DETECTED over ALL CLEAR
- **Per-issue detail**: 5-10 lines maximum

---

## Checklist for New Agent Prompts

Before finalizing a new Autonomous Expert Agent prompt, verify:

- [ ] All 7 required sections present in order
- [ ] Downstream handoff statement in ROLE & CONTEXT
- [ ] Work process ends with "Stop" step
- [ ] Classifications map to standard severity icons (🔴🟡🟢⚪)
- [ ] REPORT-START / HEADLINE structure in output format
- [ ] All object references include IDs
- [ ] SUMMARY and COMMENT fields in report structure
- [ ] CLASSIFICATION SUMMARY in report
- [ ] One realistic example included
- [ ] Total length under 8,000 characters
- [ ] No "ask user" or interactive prompts
