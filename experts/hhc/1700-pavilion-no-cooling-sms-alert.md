# 1700 PAVILION — "NO COOLING" SMS ALERT (CW SUPPLY)

## [VERSION]

Version:  1.0
Created:  08/10/2026
Status:   **DEPLOYED AND VALIDATED** — alarm and all-clear both proven end to end.
Type:     ProptechOS platform alert (trigger + 2 workflows). NOT an LLM agent —
          no reasoning, no tool calls. One threshold, one sensor, two SMS.

This is the outcome-based alert built in response to the 08/05/2026 cooling
outage. It answers exactly one question: **is the building loop actually being
cooled?** It deliberately ignores every mechanical cause. Diagnosis belongs to
the plant-watch agents; this alert exists to wake somebody up.

## [ROLE & CONTEXT]

Building **1700 Pavilion**, Summerlin / Las Vegas NV.
ProptechOS Building `1593d0fe-4e3f-4adc-aeae-a4a808323968` (littera 13075).
Property Owner Howard Hughes `3edc18ee-9c68-45e5-980c-d2c9bbf66063`.
Central plant controller **`device 1200`** (Distech ECLYPSE S1000), twin
`be452777-5c1d-481d-8135-7a6284114d16`, room MECH 303
`29c8bf57-f63f-4611-b8c7-89c76ca5355b`.

Water side: 2 cooling towers + 2 heat exchangers feeding a **~75 °F building
loop**. This is NOT a 44 °F chilled-water plant — every threshold must come from
this building's observed data, never from CHW convention.

**Severity convention across the 1700 alert set:**
`Severe` = the building has a problem · `Major` = we cannot see the building.
This alert is **Severe**.

## [SENSOR MAP — full UUIDs]

```
SOURCE (what the trigger watches)
af29d818-3ce9-4a80-83ab-30da08b4527e   device 1200/bldgCwSupply/20minAggregation
                                       littera "analog-input 406/20 min aggregation"
                                       Observation Function = 20 min median
                                       observesSensor -> 0054ec5f-…

UNDERLYING RAW POINT (not watched directly — see LIMITATIONS)
0054ec5f-171d-44e6-83f3-500026cbd0a2   device 1200/bldgCwSupply  (analog-input 406)

CONTEXT ONLY — not part of this alert, for the responder's diagnosis
c4573bc2-f75c-4b7d-95a9-d9d33f916f4f   device 1200/bldgCwReturn
747aaca5-2d3a-4129-883d-ee8101d87ecd   device 1200/osat
71a26aa4-2005-4153-9a81-540c9cc5bce5   device 1200/cwSupplyCt1
04c54689-2a5d-4f36-8d44-c27a0c0874af   device 1200/cwSupplyCt2
38eec171-4324-45db-bb25-4c12927500a3   device 1200/runtimeCt1
a08ea647-2a4b-4e54-b4a3-796681389dc2   device 1200/runtimeCt2
```

**Why a derived median and not the raw point.** The trigger engine has **no
duration field** — an Observation Trigger offers only Min/Max threshold plus a
day schedule. "Above 85 °F sustained 20 minutes" therefore cannot be expressed
directly. The 20-minute median sensor encodes the duration into the value.

## [TRIGGER CONFIGURATION]

```
Trigger name:       1700 No Cooling - CW Supply
Enabled:            yes
Based on:           Sensor Observations
Template:           Observation Trigger
Min Threshold:      (empty)
Max Threshold:      85            <- Fahrenheit; "greater or equal triggers"
Schedule:           Sun–Sat, no start/end window
Source:             af29d818-…  (the 20-min median, ONE sensor)

Service Object
  Service Type:     Alert
  Severity:         Severe
  Smart Alerts:     Enabled
    Service Object action: Update
    Set status:            Closed
```

**Smart Alerts is what makes the all-clear possible.** When the median falls back
below 85, the object is updated and closed, which stamps `Closed At`. Enabling
Smart Alerts also **removes the Cooldown section** — the 1-Day cooldown that
originally suppressed every SMS is gone as a side effect.

⚠️ **Never put an em dash (`—`) or a degree sign (`°`) in the trigger name.**
Both are outside GSM 03.38 and force the SMS into UCS-2, cutting the limit from
160 characters to 70. The trigger name is interpolated into the message.

## [WORKFLOW CONFIGURATION]

Every alert is a **pair** of workflows on one trigger. There is no "Closed"
event — the dropdown offers only Created / Modified / Deleted — so a closure is
detected as a modification that carries a Closed status.

```
WORKFLOW 1 — the alarm
  Name:        1700 - No Cooling - CW Sup
  Event:       Created
  Filter (And)
    Trigger   In   [1700 No Cooling - CW Supply]
  Dispatchers: SMS + Email
    SMS   +46-704-124-900
    Email Trigger template -> erik@proptechos.com, oksana@proptechos.com

WORKFLOW 2 — the all clear
  Name:        1700 - No Cooling - CW Sup — ALL CLEAR
  Event:       Modified
  Filter (And)
    Service Status   Equal   Closed
    Trigger          In      [1700 No Cooling - CW Supply]
  Dispatchers: SMS
    SMS   +46-704-124-900
```

⚠️ **Use `Service Status Equal Closed`, NOT `Closed At Is Not Empty`.** Both
express the same condition, but the `Is Not Empty` operator renders no value
control while `Value` is marked required — the form then shows an error badge
with no tooltip and **refuses to save a workflow that is running correctly in
production**. This is a UI bug; the `Service Status` form is the workaround.

## [MESSAGE TEMPLATES]

```
ALARM
1700 Pavilion COOLING ALARM: {{serviceObject.tags.message}}. Check chillers + cooling towers.

ALL CLEAR
1700 Pavilion ALL CLEAR: {{serviceObject.tags.alertName}} - back below alarm limit. No action needed.
```

House format: `1700 Pavilion [STATE]: [detail]. [what to do]` — building first,
state in capitals, action last, so the first three words of a lock-screen preview
carry the meaning.

Rules that produced these:

1. **The alarm uses `{{...message}}`** — it carries the live value and the current
   threshold, and self-updates if the threshold changes.
2. **The all-clear must NOT use `{{...message}}`.** Tags are snapshotted at object
   creation, so it would render *"is above the maximum threshold value: 85"*
   inside a message headed ALL CLEAR.
3. **Keep at least one `{{...}}` placeholder.** Whether a fully static template
   delivers has never been proven; every template that has ever delivered had one.
4. **"Back below alarm limit", not "cooling restored".** With the limit at 85 and
   a normal peak near 81, closure means the loop is under the alarm line — not
   that the plant is healthy. The duller wording will not send someone back to bed
   on a building that is still struggling.

## [CALIBRATED BASELINE — why 85 °F]

14-day analysis 07/22–08/05/2026, n = 19,442, failure window excluded:

```
median 75.4 · p90 80.1 · p99 82.7 · max 84.0 · samples > 85 °F: ZERO
```

Against the real event (08/05): 85 °F crossed at **06:00 PDT**, max 89.1 that
hour, stayed crossed ~4 h, peaked **113.8 °F at 08:00**. Cooling restored inside
the 10:00 hour. The alert would have fired hours before the plant recovered.

Confirmed in operation 08/08–08/10 (40 h, OSAT 86–107 °F, both towers healthy):
median max **79.94**, raw max **80.53**, **zero alerts**. First real evidence the
threshold does not false-fire.

⚠️ **Only ~4 °F of headroom.** Normal peak is 81; the limit is 85. Watch a few
more hot afternoons before treating 85 as settled.

**Do not use lower values as live thresholds.** 74 sits *on* the loop and flaps
(22 of 32 samples ≥74). 76 fires within an hour or two and then sits in alarm all
night as the loop drifts to 79–81. Both are test values only, and must be
returned to 85 immediately after a test.

## [DETECTION BEHAVIOUR & TIMING]

The median sensor publishes **per block, every 1200 s exactly**, at
`:07:53 / :27:53 / :47:53` UTC. It is **not rolling**. 3 samples/hour.
Each value is the median of the trailing 4 raw samples.

```
worst-case detection ≈ 40 min   (20 min window + up to 20 min to the next block)
SMS dispatch          ≈ 1 min after the block
```

Give the customer **40 minutes**, never 20.

`> 85` on a median means **"more than half of the last 20 minutes was above 85"**
— looser than the literal spec, and far safer than a mean. The median is the
right statistic here: it is robust to the `0.0` invalid readings this controller
emits (up to 1 bad sample in 4 cannot shift it) and it filters single-sample
spikes. A mean would be dragged *down* by zeros — that is how the outage hour
averaged approximately 12 °F while the loop sat at 105 °F.

**De-duplication is inherent.** `Created` fires once per service object, so a
sustained excursion produces exactly one SMS however long it lasts. Verified:
1 message across 18 continuous blocks above threshold.

## [VALIDATION RECORD]

All timestamps CEST; block times UTC.

```
08/07 11:09   ALARM      77.48 °F   block 09:07:53Z = 77.4808   threshold 70 (test)
08/07 11:28   ALL CLEAR             block 09:27:53Z = 77.6263   threshold 85
08/07 16:48   ALL CLEAR             (earlier cycle, threshold 85)
08/07 17:08   ALARM      77.33 °F   block 15:07:53Z = 77.3315   threshold 70 (test)
08/07 17:28   ALL CLEAR             (earlier cycle)
08/08–08/10   silent                40 h, OSAT to 107 °F, max 80.53 — correct
08/10 10:48   ALARM      78.10 °F   block 08:47:53Z              threshold 70 (test)
08/10 11:08   ALL CLEAR             block 09:07:53Z              threshold 85
              ^ final pre-handover run on the exact production configuration
```

Every SMS value matches its median block to 2 decimal places, and each arrived
about one minute after the block — confirming genuine threshold evaluation rather
than an artifact of saving the trigger.

## [LIMITATIONS — state these plainly in any handover]

1. **This alert cannot distinguish "cooling is fine" from "we have no data."**
   Verified 08/08: with the connector stopped at 12:03:37Z, the median published a
   normal-looking **78.61 °F at 12:07:53Z — four minutes into a total outage**,
   because the block was computed from pre-stop samples. For up to 20 minutes
   after a data loss this alert actively reports health. **Silence here is only
   meaningful while the data-loss alert is also quiet.** See the companion spec.

2. **An open service object silences the alert.** `Created` fires once per object.
   While one is open, a new excursion produces nothing. If an object is left open
   (test threshold, stuck state), the alert is dead and looks identical to calm.

3. **Editing the trigger closes and recreates its object**, firing a spurious
   all-clear followed by a spurious alarm. Expect a pair on every save, and warn
   recipients before they are added.

4. **Platform-side data loss is invisible to it.** ProptechOS lost 6.8 h of
   aggregation on 08/06–08/07 (PLAT-5683, closed as a temporary outage) while the
   PEG published normally. No building-side alert catches that.

5. **Renaming the trigger changes the text of future SMS** but not of objects
   already open — their `alertName` tag is snapshotted at creation.

## [OPERATING NOTES]

- **Recipients today: Erik only** (SMS) plus erik@/oksana@ (email). The three
  building engineers — Joshua Smith 702-278-7255, Joshua Chong 725-270-2861,
  Gary Hornick 702-427-0083 — are **not yet added; none of the numbers are
  confirmed**, and that blocks go-live. All three get every alert simultaneously;
  no rotation is possible and none should be offered.
- **Testing procedure:** raise the threshold above the current value first (proves
  the all-clear, the untested direction), then lower it to force an alarm, then
  return to 85 — so the sequence *ends* at the production value and cannot be left
  wrong. Change nothing else between saves.
- An SMS arriving within seconds of a save is the edit artifact; one arriving at
  `:08 / :28 / :48` is a genuine evaluation.
- Companion alert: `1700-pavilion-no-data-sms-alert.md`.
