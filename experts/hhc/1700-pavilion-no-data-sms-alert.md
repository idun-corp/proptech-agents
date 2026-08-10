# 1700 PAVILION — "NO DATA" SMS ALERT (COMMUNICATION / MONITORING BLIND)

## [VERSION]

Version:  1.0
Created:  08/10/2026
Status:   **DEPLOYED, PARTIALLY VALIDATED — NOT READY FOR BUILDING ENGINEERS.**
          Fires correctly on real read failures. Requires a **manual reset**
          after every alarm (see LIMITATIONS §1). Keep internal until PLAT-5687
          and the sticky-edge-status question are resolved.
Type:     ProptechOS platform alert (trigger + 2 workflows). NOT an LLM agent.

This is the companion to `1700-pavilion-no-cooling-sms-alert.md`. That alert
answers *"is the building being cooled?"*. This one answers the question that
must be true for the first answer to mean anything: **are we still receiving
data at all?**

The 08/05/2026 outage ran roughly eleven hours partly because nothing flagged
the data loss. The temperature alert alone cannot close that gap — for up to
20 minutes after a feed dies it reports a healthy-looking number.

## [ROLE & CONTEXT]

Building **1700 Pavilion** `1593d0fe-4e3f-4adc-aeae-a4a808323968` (littera 13075),
PO Howard Hughes `3edc18ee-9c68-45e5-980c-d2c9bbf66063`, plant controller
**`device 1200`** `be452777-5c1d-481d-8135-7a6284114d16`, room MECH 303.

**Severity convention:** `Severe` = the building has a problem · `Major` = we
cannot see the building. This alert is **Major**.

Message wording deliberately says **"monitoring blind"**, never that the plant has
failed. On the two occasions this failure mode has actually occurred, the plant
controller was healthy both times — 07/10 was the connector, 08/06 was a
ProptechOS-side outage. An alert that repeatedly sends technicians to a healthy
controller loses credibility fast.

The recipient is a **BAS technician who does not know what a PEG is.** The only
action always valid regardless of cause is: *look at the plant on your own
front-end, because ours cannot see it.*

## [SENSOR MAP]

The trigger watches **17 sensors on `device 1200`** by edge status. Sixteen are
identified; one was not captured during configuration.

```
analog-input 707   device 1200/osat                747aaca5-2d3a-4129-883d-ee8101d87ecd
analog-input 708   device 1200/osah
analog-input 406   device 1200/bldgCwSupply        0054ec5f-171d-44e6-83f3-500026cbd0a2
analog-input 407   device 1200/bldgCwReturn        c4573bc2-f75c-4b7d-95a9-d9d33f916f4f
analog-input 101   device 1200/cwSupplyCt1         71a26aa4-2005-4153-9a81-540c9cc5bce5
analog-input 201   device 1200/cwSupplyCt2         04c54689-2a5d-4f36-8d44-c27a0c0874af
analog-input 405   device 1200/ctCwSupplyTemp
analog-input 504   device 1200/bldgSupplyFlow
analog-input 505   device 1200/ctSupplyFlow
analog-value 3     device 1200/runtimeCt1          38eec171-4324-45db-bb25-4c12927500a3
analog-value 4     device 1200/runtimeCt2          a08ea647-2a4b-4e54-b4a3-796681389dc2
binary-input 102   device 1200/fanStatCt1          c261c495-d378-4bf6-935e-fb9694a7b982
binary-input 202   device 1200/fanStatCt2          1bd06ed8-5615-4c58-8c91-6b3e3726a7e5
binary-input 401   device 1200/statusCwp1
binary-input 402   device 1200/statusCwp2
multi-state-value 25  device 1200/orderCwp1        e3506d2d-de72-44f0-9948-b0c92fe3176c
multi-state-value 26  device 1200/orderCwp2        af77b720-7d5a-4205-8100-5500e075e1a7
```

⚠️ **The 20-min median sensor is NOT in this list.** Consequence: the 08/06–08/07
blackout, where the aggregation stalled while raw data kept flowing, would not
have registered here.

## [TRIGGER CONFIGURATION]

```
Trigger name:       1700 Communication error
Enabled:            yes
Based on:           Sensor Edge Status
Template:           Aggregate By Count
Edge Status:        ERROR
Min Threshold:      (empty)
Max Threshold:      1             <- "greater or equal triggers" = 1 or more sensors erroring
Source:             Filter Scope Twins, 17 sensors above

Service Object
  Service Type:     Alert
  Severity:         Major
  Smart Alerts:     Enabled
    Service Object action: Update
    Set status:            Closed
```

⚠️ **Threshold direction flips by what you count.** Counting *errors* → `Max = 1`
("one or more fires"). Counting *observations* → `Min = 0` ("zero or fewer
fires"). This trigger shipped originally as `Min = 1`, which reads as "fire when
one or fewer sensors are erroring" — true whenever the plant is healthy. It never
produced a visible alert, masked further by a 7-Day cooldown.

⚠️ Enabling Smart Alerts **removes the Cooldown section**. The original 7-Day
cooldown is gone as a side effect; do not re-introduce one.

Sensitivity: 1 of 17 sensors ≈ **6% degradation** trips it. That is deliberate —
it is the only alert in the set that detects *partial* data loss.

## [WORKFLOW CONFIGURATION]

```
WORKFLOW 1 — the alarm
  Name:        1700 Communication error
  Event:       Created
  Filter (And)
    Trigger   In   [1700 Communication error]
  Dispatchers: SMS + Email
    SMS   +46-704-124-900
    Email Trigger template -> erik@proptechos.com, support@proptechos.com

WORKFLOW 2 — the all clear
  Name:        1700 Communication error - ALL CLEAR
  Event:       Modified
  Filter (And)
    Service Status   Equal   Closed
    Trigger          In      [1700 Communication error]
  Dispatchers: SMS + Email  (same recipients)
```

⚠️ Use `Service Status Equal Closed`, **not** `Closed At Is Not Empty` — the
latter renders no value control while `Value` is required, so the form refuses to
save with an error badge and no tooltip, even for a workflow running correctly.

**`support@` rather than a named person** — it lands in a queue, not one inbox.

**Email is not optional here.** The alarm email carries a `details_1.csv` naming
the exact Twin IDs and littera of every erroring sensor; the SMS can only say
"2 sensors". Email is also the only way to notice that an SMS workflow has
silently stopped delivering — there is no delivery log anywhere in the platform.

## [MESSAGE TEMPLATES]

```
ALARM
1700 Pavilion NO DATA: {{serviceObject.tags.message}}. Monitoring blind - check plant on BAS.

ALL CLEAR
1700 Pavilion DATA OK: {{serviceObject.tags.alertName}} cleared. Monitoring back online, no action needed.
```

`{{...message}}` renders as e.g. `"2 Sensors in Error status."` — short; total
message approximately 89 characters, single SMS.

## [DETECTION BEHAVIOUR & TIMING]

```
evaluation cycle    approximately 20 min (observed)
edge-status lag     substantial — see the validation record
observed latency    approximately 45 min from fault onset to SMS
```

**What it catches**

- Read failures against a live controller — `Failed to read PresentValue for
  Sensor <uuid>: null`. This is the 07/10 and probable 08/05 failure mode.
- **Partial / intermittent loss.** Edge status is per sensor, so if a controller
  answers only half the reads, roughly half the sensors flag and the count is
  well above 1. This is the *only* alert in the set that detects degradation
  rather than total failure.

**What it does NOT catch**

- **A cleanly stopped connector.** Verified by controlled test 08/08,
  12:03:37Z → 12:23:33Z: 20 minutes of total data loss, **no alert**. A stopped
  connector is *silent*, not erroring — it emits no ERROR statuses, so an
  ERROR-count rule has nothing to count.
- **ProptechOS-side loss**, where the PEG publishes normally.

## [VALIDATION RECORD]

```
08/08 06:36–06:40Z   ~15 device-1200 points log read failures, one per ~18 s
08/08 12:47:52Z      ALARM "2 Sensors in Error status." (cwSupplyCt1, orderCwp1)
                     -> approximately 45 min after fault onset
08/08 12:03–12:23Z   controlled connector stop, 20 min total data loss -> NO ALERT
08/08–08/10          both sensors reading normally throughout; edge status stayed ERROR
08/10 08:15 CEST     service object closed MANUALLY by erik@idun.tech
08/10 08:16 CEST     ALL CLEAR delivered -> all-clear workflow PROVEN
```

**Edge status remained ERROR for approximately 65 hours** after the underlying
reads recovered. 13 of the original ~15 sensors cleared; 2 did not. Smart Alerts
never closed the object. The object carries a field **`Edge Status Related: Yes`**,
suggesting edge-derived objects follow a different code path from
observation-derived ones — likely where the clearing logic is missing.

Note also: an intermediate change to `Acknowledged` (08:13) correctly produced no
SMS, confirming the all-clear filter discriminates properly on status rather than
firing on any modification.

## [LIMITATIONS — read before handing this to anyone]

1. **⚠️ MANUAL RESET REQUIRED. This is the blocking issue.** Edge status does not
   reliably self-clear, so the object stays open indefinitely and **`Created`
   cannot fire again while it is open.** A latched alert is indistinguishable
   from a quiet one. Until fixed, someone must close the object by hand after
   every alarm, and this alert must not be presented to the building engineers as
   working coverage.

2. **Approximately 45-minute detection.** Adequate for an overnight failure; not
   for a fast one.

3. **Does not detect silence** — only errors. See PLAT-5687.

4. **Reports faults that have already resolved.** The message means "something
   failed recently", not "something is failing now".

5. **Objects may not appear under the building twin** in the Service Objects list
   even though `Building: 1700 Pavilion` is populated.

## [APPENDIX — `1700 No Data - CW Plant`: attempted, does not work]

A third trigger was built 08/08 to cover the gap in §3 (silence rather than
errors), and **does not fire**. Documented so nobody rebuilds it.

```
Based on:            Sensor Observations
Template:            Aggregate By Observations
Aggregation Function: Sum For All Sensors
Min Threshold:       50            Max Threshold: 100000
Source:              af29d818-…   (the 20-min median)
Schedule:            Interval 1, Frequency Hour
Aggregation Period:  Period Hour, Quantity 1
Service Object:      Alert / Major / Smart Alerts Update -> Closed
```

**The reasoning:** there is **no `Count` aggregation function** for observations —
only Average and Sum. The median sensor yields approximately 3 observations/hour
at approximately 77 °F, so a healthy hour sums to approximately 231; a totally
empty hour sums to 0; `Min 50` would catch only true silence, since even one
surviving observation gives 77.

**Why it fails:** an empty window appears to produce **no evaluation at all**
rather than a sum of 0. Tested 08/08 with the aggregation period cut to 5 minutes
against a sensor publishing every 20 minutes — a guaranteed-empty window at every
execution — and no service object was created.

Additional constraint found: **Schedule Frequency minimum is `Hour`**
(Hour/Day/Week/Month), so even a working rule of this shape detects in 1–2 h.

**Filed as [PLAT-5687](https://idun.atlassian.net/browse/PLAT-5687)** — feature
request for a `Count` aggregation on Sensor Observations, so a rule can read
`count <= 0 over N minutes`. Assigned to Pavlo Konietin.

**This trigger should be disabled** rather than left enabled and non-functional.

## [OPERATING NOTES]

- Useful zero-data-loss test trick: shrink the Aggregation Period **below the
  sensor's publishing cadence** to manufacture a guaranteed-empty window. The
  median publishes at `:07 / :27 / :47` and executions run at `:34`, so a
  **5-minute** window (`:29–:34`) is always empty; a 10-minute one always catches
  the `:27` block and proves nothing.
- **`connector-watchdog.service` on the PEG is inert** — it is designed to
  `sudo systemctl restart` a connector after 5 consecutive non-OK events, stayed
  `active` through the entire 20-minute test outage without acting, and has
  **1 journal line in 30 days**. Do not count it as recovery.
- Idun-internal Slack **`#edge_modules_alerting`** (Alertmanager) detected the
  test outage in approximately 30 min, but is chronically noisy — 8 customer
  connectors firing simultaneously on 08/08. Not a dependable backstop.
- PEG access: `24.234.26.254:1022`, user `orangepi`, key auth; sudo password in
  1Password. Two connectors run there — **`2c28ab21-f7cf-4c82-ba42-abf56a888297`**
  is the one holding device 1200.
