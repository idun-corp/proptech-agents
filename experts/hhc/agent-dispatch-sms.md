# AGENT DISPATCH — SMS / EMAIL / SERVICE OBJECT FROM AN AUTONOMOUS AGENT

## [VERSION]

Version:  0.1
Created:  08/11/2026
Source:   ProptechOS release notes **v5.6.3**, 2026-03-16 — *Autonomous Agent
          Service → Dispatch property*. Transcribed here because the hhc agent
          specs are the consumers and the release notes are not in the repo.
Status:   **DOCUMENTED, NOT YET USED BY ANY AGENT IN THIS FOLDER.** The exact
          syntax of the dispatch block is **not given in the release notes** —
          see [OPEN — BLOCKING]. Nothing here has been exercised end to end.

Shared reference for every agent in `hhc/`. Read together with
`1700-pavilion-no-cooling-sms-alert.md`, whose hard-won SMS craft rules still
apply — see [SMS TEXT RULES STILL APPLY].

## [WHAT IT IS]

Until v5.6.3 an agent could not notify a human. Alerting had to be a
platform **trigger + workflow** pair (that is what both 1700 SMS alerts are).
Dispatch lets an **autonomous agent itself** decide that something needs a human
and signal for a message to go out.

```
the agent          detects the issue, chooses the channel, signals dispatch
the orchestration  executes it — resolves recipients, applies the template, sends, logs
```

This sits **alongside** the existing routing system: 1-to-1 agent routing handles
agent-to-agent traffic; **dispatch handles agent-to-human**.

## [DATA MODEL]

```
DispatchConfig {
  "id":                UUID,
  "type":              SERVICE_OBJECT | EMAIL | SMS,
  "recipients":        ["email@example.com"],
  "autonomousAgentId": UUID,      // reference to the AutonomousAgent
  "enabled":           boolean    // kill switch without deleting the config
}
```

- **One agent may hold several configs** — e.g. one EMAIL and one SMS dispatcher.
- **`enabled` is a kill switch.** Use it to silence an agent without destroying
  its recipient list. This is the mechanism to reach for when an agent is
  mis-firing, rather than deleting the config and rebuilding it.
- Severity reuses the existing enum: **`MINOR` · `MAJOR` · `SEVERE`**.

## [THE PART THAT MATTERS MOST — the LLM never sees recipients]

> The system prompt is injected with **available dispatch types only**. No
> client-sensitive information — email addresses, phone numbers — is exposed to
> the LLM. The Agent Troupe holds the full dispatch config and resolves
> recipients at execution time.

Consequences for how these specs are written:

1. **Never put a phone number or email address in an agent prompt** in order to
   make dispatch work. It is not needed and it would defeat the design. The
   numbers in `1700-pavilion-no-cooling-sms-alert.md` are there because that alert
   is a *platform workflow*, configured in the UI — not because an agent prompt
   needs them.
2. **An agent cannot verify who it reached.** It signals a type; the platform
   resolves the list. So an agent must never claim in its report that a specific
   person was notified — only that a dispatch of a given type was signalled.
3. This is also the containment answer for this folder: dispatch adds **no new
   customer data** to any prompt. See `README.md` on the folder's data exception.

## [HOW AN AGENT SIGNALS IT]

The agent emits a **structured block in its response**. **Multiple dispatch blocks
in a single response are supported.** For each block the platform resolves
recipients from the `DispatchConfig` and executes independently:

```
SMS              apply a static SMS template (compact) using SUMMARY + SEVERITY,
                 resolve recipients, send, log the event

EMAIL            apply a static email template using SUMMARY + SEVERITY,
                 resolve recipients, send, log the event

SERVICE_OBJECT   all required data present  -> create the service object via MCP tool, log
                 data missing              -> create a DRAFT service object, save a
                                              HITL_REQUIRED message naming the missing
                                              fields, and the UI surfaces it for review
```

**The template is static and platform-side. The agent supplies `summary` and
`severity`, not formatting.** That is the single most important thing to
understand before writing a dispatching agent: you control the words, not the
layout, and you cannot preview the rendered message.

The `SERVICE_OBJECT` draft + `HITL_REQUIRED` path is worth noting — it means an
agent that is *unsure* has a legitimate third option between silence and paging:
file an incomplete object and let a human finish it.

## [SMS TEXT RULES STILL APPLY — to the summary]

Because the platform interpolates the agent's `summary` into a static SMS
template, **every lesson from the 1700 SMS work now applies to the summary string
an agent produces.** These were learned the hard way; do not relearn them:

- ⚠️ **No em dash (`—`) and no degree sign (`°`).** Both are outside GSM 03.38 and
  force the whole message into UCS-2, **cutting the limit from 160 characters to
  70**. Write `deg F`, or just `F`, and use plain hyphens.
- ⚠️ **No tilde (`~`).** Separately, the agent UI renders text between two tildes
  as strikethrough. Write `approx.`
- **Keep the summary short and put the meaning first.** House format across the
  1700 set is `<building> <STATE>: <detail>. <what to do>` — building first, state
  in capitals, action last, so the first three words of a lock-screen preview
  carry the message. The static template may or may not preserve this; until a
  real send is inspected, **write the summary so it reads correctly on its own.**
- **Name only equipment that exists at the site.** The 1700 alarm text said
  "check chillers" for a building with no chillers, and it took a month to notice.

## [SEVERITY — map onto the house convention]

The platform enum and the convention already used across the 1700 alert set line
up cleanly. Keep using the house meanings:

```
SEVERE   the building has a problem
MAJOR    we cannot see the building        (data loss, comms, BLIND)
MINOR    unmapped at this site — see OPEN
```

A ⚫ BLIND condition in the PdM sense is a **`MAJOR`**, never a `SEVERE`. An agent
that cannot read its sensors must never dispatch as though the plant has failed.

## [WHERE THIS MUST NOT BE USED]

⚠️ **`1700-pavilion-plant-predictive-maintenance.md` must NOT dispatch.** Its
`[CONSTRAINTS]` say *"Never page anyone. This agent writes a report."* The
division of labour in this folder is deliberate:

```
one sample  -> the SMS alerts (platform trigger + workflow), or a watch agent
a slope     -> the PdM agents, which report and never page
```

Adding dispatch to a daily trend agent would page someone about a gradient. If a
PdM finding is urgent enough to wake somebody, the correct move is to **propose a
new threshold for the acute alert**, not to bolt notification onto the trend
agent. Its `[TOOLS — HARD WHITELIST]` deliberately excludes dispatch, and that is
not an oversight to correct.

## [ALSO IN v5.6.3 — worth knowing]

- **`patch-twin` MCP tool.** PATCH (`ADD` / `REPLACE` / `REMOVE`) on single twin
  fields without replacing the whole resource. Paths limited to `/popularName`,
  `/littera`, `/status`, `/source`; `twinRef` accepts UUID **or** popularName;
  works across RealEstate, RealEstateComponent, BuildingComponent, Device, Sensor,
  Actuator, Asset and their subclasses. ⚠️ **A write tool — no agent in this
  folder should hold it.** These are all read-and-report agents.
- **Autonomous agent persistence.** Agent run state now survives service
  redeployments and scheduled routines resume automatically. Previously every
  agent had to be restarted by hand after each deploy. Relevant to the 1700 PdM
  routine: if it stops running, a redeploy is **no longer** the explanation.

## [OPEN — BLOCKING before any agent here dispatches]

1. **⚠️ The dispatch block syntax is not in the release notes.** They say "a
   structured block in its response" and nothing more — no field names, no
   fencing, no example. **This cannot be written into an agent prompt until
   somebody produces one working example.** Ask Pavlo or check a newer release
   note; do not guess a format and ship it.
2. **Is `MINOR` used at this site?** The 1700 convention has only two levels.
   Decide whether `MINOR` means anything here or is simply unused.
3. **Is there de-duplication or a cooldown?** The platform trigger path
   de-duplicates inherently — `Created` fires once per service object, which is
   what keeps a sustained excursion to one SMS. **Dispatch appears to have no
   equivalent**, so an hourly agent that dispatches on a persistent condition may
   send hourly forever. This is the single biggest risk in adopting it: the
   pre-dispatch world produced a 30-SMS flood in 5 hours at this building.
4. **Is there a delivery log the agent or a human can read?** The 1700 work found
   there is no SMS delivery log anywhere in the platform, which is why every alert
   pairs SMS with email. "Logs event" appears in the release notes — establish
   what that log contains and who can see it.
5. **Can dispatch be tested without sending?** No dry-run is mentioned. Until one
   exists, first exercise must go to an internal number only.

## [RELATED]

- `1700-pavilion-no-cooling-sms-alert.md` — the trigger+workflow SMS path, and the
  source of the text rules above
- `1700-pavilion-no-data-sms-alert.md` — the `MAJOR` / "cannot see the building"
  half of the severity convention
- `1700-pavilion-plant-predictive-maintenance.md` — must not dispatch; see above
- `README.md` — this folder's customer-data exception
