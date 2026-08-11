# 1700 PAVILION — DAILY MANUAL CHECK (DATA-LOSS BACKSTOP)

## [VERSION]

Version:  0.2
Created:  08/11/2026
Updated:  08/11/2026 — first live validation run. All four unknowns resolved
          against real data, and **check 4 was rewritten: it was wrong.** See
          [VALIDATION RECORD].
Status:   **VALIDATED AGAINST LIVE DATA, not yet run as a whole prompt.** Every
          threshold and cadence below is now measured rather than inferred.
Type:     Manual LLM check, run by a human once per day. Not a platform trigger,
          not a scheduled agent. Read-only — it must never actuate anything.

## [WHY THIS EXISTS]

The two deployed SMS alerts share a structural blind spot: **neither can detect
silence.** They are also individually capable of latching into a state that is
indistinguishable from calm.

```
FAILURE MODE                            no-cooling   no-data     THIS CHECK
BAS / controller stops answering reads       —       ✅ ~45 min      ✅
Connector cleanly stopped (silent)           ✗ (1)   ✗ (2)          ✅
ProptechOS aggregation stalls                ✗ (3)   ✗ (4)          ✅
Loop above 85 F                              ✅ ~40 min   —          ✅
An alert is latched open and cannot fire     ✗       ✗              ✅
```

1. For up to 20 min after a feed dies the median still publishes a healthy
   number from pre-stop samples — verified 08/08: **78.61 °F reported four
   minutes into a total outage.**
2. Verified 08/08 by controlled test: 20 min of total data loss, **no alert**. A
   stopped connector emits no ERROR statuses, so an ERROR-count rule has nothing
   to count. Filed as PLAT-5687.
3. The no-cooling trigger watches **only** the 20-min median. If the median
   stalls, that alert goes quiet while looking perfectly healthy.
4. The median is deliberately **not** among the no-data trigger's 17 sensors, so
   the 08/06–08/07 platform blackout (PLAT-5683, 6.8 h) would not have registered.

**This check does not replace the alerts and is slower than all of them** — once
a day means up to 24 h of detection latency. Its job is different: it verifies
the alerts are still armed, and covers the failure modes they cannot see at all.
It exists because PLAT-5687 is the real fix and will not land soon.

## [THE TIMING ADVANTAGE — why a European morning check works]

Las Vegas is **PDT (UTC−7)**; Stockholm is **CEST (UTC+2)**. Nine hours.

```
LV overnight risk window   22:00–05:00 PT
  = in UTC                 05:00–12:00 Z
  = in Stockholm           07:00–14:00 CEST      <- the European working day
```

The overnight window is where the risk actually is: loop supply drifts to
**82.98 °F** on healthy nights, leaving only ~2 °F under the 85 °F alarm, and the
building engineers are asleep. That window is Erik's morning.

**Run the check at 13:00–15:00 CEST (= 04:00–06:00 PT).** At that hour:

- the full LV night has completed, so the night maximum is knowable;
- it coincides with **06:00 PT — the exact hour the 08/05 outage crossed 85 °F**;
- the Vegas engineers are not on site yet, so a finding buys lead time before
  the day load arrives.

An earlier run (08:00 CEST = 23:00 PT) sees only the first hour of the night and
cannot report a night maximum. Prefer the afternoon slot; if you run both, treat
the morning one as freshness-only.

## [THE PROMPT — copy from here]

```
Run the 1700 Pavilion daily data-loss check. Read-only: do not actuate, do not
patch twins, do not edit triggers. Building 1593d0fe-4e3f-4adc-aeae-a4a808323968.

Work the checks in order. Checks 1-3 gate the rest: if data is not arriving, the
temperatures in check 4 are meaningless and you must say so rather than reporting
them as health.

CHECK 0 - CLOCK
  Run: date -u  and  TZ=America/Los_Angeles date
  State the LV night window just ended (22:00-05:00 PT) in UTC.

CHECK 1 - IS RAW DATA ARRIVING?   (covers the silence gap nothing else sees)
  get-sensor-latest-data on all three:
    0054ec5f-171d-44e6-83f3-500026cbd0a2   bldgCwSupply
    c4573bc2-f75c-4b7d-95a9-d9d33f916f4f   bldgCwReturn
    747aaca5-2d3a-4129-883d-ee8101d87ecd   osat
  Raw cadence is 302 s (measured 08/11: 285 samples/24 h, intervals 302 s exact).
  Age of newest observationTime vs now:
    GREEN  < 15 min      AMBER 15-40 min      RED > 40 min
  If all three are stale by a similar amount, suspect the connector or the
  controller. If one is stale alone, suspect that point.

CHECK 2 - IS THE AGGREGATION ALIVE?   (covers the PLAT-5683 platform failure)
  get-sensor-latest-data on af29d818-3ce9-4a80-83ab-30da08b4527e (20-min median).
  Blocks publish every 1200 s exactly at :07:53 / :27:53 / :47:53 UTC.
    GREEN  < 25 min      AMBER 25-45 min      RED > 45 min
  RED here means THE NO-COOLING SMS ALERT IS CURRENTLY DEAD - say that explicitly.
  Raw fresh (check 1 green) + median stale = platform-side, not building-side.

CHECK 3 - ARE THE ALERTS STILL ARMED?   (covers latching)
  get-service-objects for the building. Look for any OPEN (not Closed) alert
  object from either trigger:
    "1700 No Cooling - CW Supply"     "1700 Communication error"
  An open object means Created cannot fire again and that alert is LATCHED -
  silent for the same reason a calm building is silent. The no-data alert is
  KNOWN to latch and need a manual close (65 h observed 08/08-08/10).
  Report each alert as ARMED or LATCHED. Latched = RED regardless of temperature.

CHECK 4 - DID THE LV NIGHT STAY UNDER 85 F?
  get-sensor-historical-data on af29d818-... (THE MEDIAN), period _1day,
  aggregation raw. That is only ~72 samples/day - small, fast, safe.
  Night window = 05:00-12:00Z (= 22:00-05:00 PT). Take the max in that window.
    GREEN  <= 83.0 F   (inside observed normal; healthy nights reach 82.98)
    AMBER  83.0-85 F   (above any observed normal night - headroom being eaten)
    RED    >= 85 F     (alarm territory; an SMS should exist. If none arrived,
                        that is a SECOND and worse finding - report both.)
  Blocks run 3/hour, 72/day, so the night window holds 21. Count them - MISSING
  BLOCKS ARE THE GAP SIGNAL. Fewer than 21 means data loss; reconcile with 1-2.

  ⚠️ DO NOT use hourly aggregation on the raw point for the VALUE. Hourly is a
  MEAN, and the controller's 0.0 invalid readings poison it. Proven against the
  real 08/05 outage: the 07:00 PT bucket reads 12.33 F while the loop was
  actually near 105 F. An hourly-mean check would have reported the worst outage
  this building has ever had as impossibly cold water rather than as a failure.
  The 20-min median is immune by construction - 1 bad sample in 4 cannot move it.

  Hourly on the raw point IS useful for one thing only: locating gaps, because
  missing buckets come back as null (confirmed - the 08/05 controller blackout
  renders as 4 consecutive nulls). Use it to find gaps, never to read a value.

CHECK 5 - PLANT SANITY (context, not alarms)
  get-sensor-latest-data on:
    71a26aa4-2005-4153-9a81-540c9cc5bce5   cwSupplyCt1
    04c54689-2a5d-4f36-8d44-c27a0c0874af   cwSupplyCt2
    38eec171-4324-45db-bb25-4c12927500a3   runtimeCt1
    a08ea647-2a4b-4e54-b4a3-796681389dc2   runtimeCt2
  Report loop dT = bldgCwReturn - bldgCwSupply.
  NEAR-ZERO OR SLIGHTLY NEGATIVE NIGHT dT IS NORMAL (weekday night median 0.42 F,
  weekend night -0.22). Do not flag it. Flag only: both towers showing no runtime
  accrual while loop supply is rising.

OUTPUT - one table, then one verdict line. No preamble.

| Check | Result | Threshold | Status |
  ...one row per check...

VERDICT: one line, starting with GREEN / AMBER / RED, naming the single most
important thing. If anything is RED, state the recommended action. If everything
is GREEN, say so plainly and stop - do not manufacture concerns.

RULES
- This building is a CONDENSER WATER plant: 2 cooling towers + 2 plate heat
  exchangers, no chillers. A ~75 F loop supply is CORRECT. Never judge these
  temperatures against 44 F chilled-water convention.
- Distinguish "healthy" from "not visible". Silence is only reassuring when
  checks 1-3 are green. Say "cannot see the building" when that is the truth.
- The controller emits 0.0 invalid readings. Treat an exact 0.0 F as invalid, not
  as cold water.
- Report what the data shows. Do not soften a RED and do not escalate a GREEN.
```

## [INTERPRETING THE RESULT]

The single most valuable output is **not** the temperature — it is the
combination of checks 1–3, which answers *"is my alerting actually working right
now?"* Nothing else in the system answers that.

```
1 green · 2 green · 3 armed   → alerts are live; trust tonight's silence
1 green · 2 RED               → platform-side stall; no-cooling alert is DEAD
1 RED   · 2 green (<20 min)   → feed just died; median still faking health
1 RED   · 2 RED               → total data loss; check the PEG connector
3 latched                     → close the object by hand, then re-verify
```

PEG access if needed: `24.234.26.254:1022`, user `orangepi`, key auth, sudo
password in 1Password. The connector holding device 1200 is
`2c28ab21-f7cf-4c82-ba42-abf56a888297`. Do not count
`connector-watchdog.service` as recovery — it stayed `active` through the entire
20-minute test outage without acting.

## [LIMITATIONS]

1. **Up to 24 h detection latency.** This is a coverage backstop, not a fast
   alert. An outage starting just after the check runs is invisible until
   tomorrow. Do not present it to anyone as monitoring.
2. **It depends on a human running it.** A missed day is a silent gap, and there
   is no record of whether it ran. If it proves its worth, the honest next step
   is to schedule it rather than to rely on discipline.
3. **`get-service-objects` behaviour in check 3 is untested by me.** Objects are
   also known to sometimes not appear under the building twin even when
   `Building: 1700 Pavilion` is populated — so an empty result is weak evidence.
   Cross-check in the UI the first few times.
4. **It cannot see BAS-internal faults** — a tower that is commanded off, a valve
   in hand, a failed sensor reading plausibly. Only the plant front-end shows those.

## [VALIDATION RECORD]

**08/11/2026 11:28–11:30Z** — first live validation, via the MCP tools.

```
CONFIRMED
  median block phase    :07:53 / :27:53 / :47:53 UTC, 72/72 blocks over 24 h
                        interval exactly 1200 s, zero missed blocks
  raw cadence           302 s exact; 285 samples / 24 h (286 expected)
  null buckets          CONFIRMED - hourly returns null for missing buckets
  hourly = MEAN         and is poisoned by the 0.0 invalid readings

CORRECTED
  check 4 rewritten     it read the night max from an hourly MEAN. Against the
                        08/05 outage that path yields 12.33 F for the 07:00 PT
                        hour while the loop was near 105 F. Now reads the
                        20-min median's raw blocks instead.

THE 08/05 OUTAGE, as the 7-day hourly array renders it (PT):
  01:00        78.69     last good hour
  02:00-05:00  null x4   controller dark (matches the logged 01:53-06:45 PT)
  06:00        69.08
  07:00        12.33  <- mean poisoned by 0.0 readings; loop was near 105
  08:00        58.38
  09:00       100.61  <- the dead loop, visible at last
  10:00        77.52     cooling restored inside this hour, as documented

BASELINE RUN (the night of 08/10-08/11, window 97% complete at 11:29Z)
  raw freshness         11:27:30Z, ~2 min          GREEN
  median freshness      11:27:53Z, ~1 min          GREEN
  aggregation liveness  72/72 blocks, 0 nulls/24 h GREEN
  night max (median)    78.60 F   vs 82.98 normal, 85 alarm   GREEN
  night max (raw)       78.63 F
  VERDICT: GREEN - 6.4 F under the alarm, data complete.
  Shape note: the loop rose smoothly 72.89 -> 78.63 from 01:02Z to 11:27Z,
  about +0.55 F/h, monotonic. That is the normal overnight ramp, well inside
  the 82.98 F documented night maximum. Not a finding; recorded as the shape a
  healthy night has, so a departure from it is recognisable.
```

Checks 3 and 5 were not exercised — `get-service-objects` still untested (see
LIMITATIONS §3).

## [RELATED]

- `1700-pavilion-no-cooling-sms-alert.md` — the 85 °F Severe alert this backstops
- `1700-pavilion-no-data-sms-alert.md` — the ERROR-count Major alert, and the
  `1700 No Data - CW Plant` appendix explaining why silence detection failed
- `1700-pavilion-plant-predictive-maintenance.md` — the calibrated baseline every
  threshold above is drawn from
- PLAT-5687 — `Count` aggregation on Sensor Observations, the real fix
- PLAT-5683 — the 08/06–08/07 aggregation outage, closed as temporary
