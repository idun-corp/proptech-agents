# 1700 PAVILION — SHARED TODO

Opened 08/17/2026 after the 18-hour blackout. Owners: **E** = Erik · **C** = Claude.
`[ ]` open · `[x]` done · `[~]` blocked.

**Framing: the plant has been healthy throughout.** Loop never came within 5.4 °F of
the 85 °F alarm across a week that included two days above 106 °F; both towers
fault-free; HX effectiveness stable on independent measurement 3 days apart. **Every
failure this week has been in our ability to SEE the building, not in the building.**

---

## ✅ CLOSED OUT 08/17 — see the bottom of this file for detail

The 18 h blackout (connector wedge, fixed by restart) · root cause of the 155 dark
devices (**PLAT-5706**, Pavlo) · "did we miss onboarding?" (no — 139 of 155 are
configured) · the service object (**Closed**, alert armed) · `highCt2` (onboarded,
**in alarm**) · the 41 never-onboarded devices (**OTEAM-6786**, Oksana) · the 08/15
email (an all-clear, not a stale alarm).

## 🟡 `highCt2` — DOWNGRADED 08/17, it tracks the night shutdown

- [ ] **E · Ask the engineers a question, do NOT build an alert yet.**
      `device 1200/highCt2` (binary-input 704) has **no ProptechOS trigger** — its
      siblings `highCt1`, `lowCt1`, `lowCt2`, `filterAlarmCt2` all have one, so it
      was missed rather than paused. Only **one** Alert object exists for 1700 since
      08/10 (`1700 No Cooling - CW Supply`, Closed), confirming nothing fires.

      **But the pattern says nuisance, not fault.** Over 4 days: 9 transitions,
      dwells of 5–16 h, only one under 30 min, 38.1 h in alarm of 97.7 h (39%).
      Converted to LV time it **sets 19:30–23:30 PDT and clears 05:00–07:00 PDT** —
      in alarm overnight, clear all day. That is backwards for a heat-driven high
      limit, and it lines up with the BAS occupancy schedule (Occupied 05:00–18:00
      PT) and the fully idle overnight plant (both CT pumps, both CW pumps and
      Cooling Tower 1 stopped, iso valves closed). Most likely tower 2's water
      stagnates and drifts toward ambient once circulation stops.

      **It has never tripped during the 11:00–16:00 PT peak window in 4 days.**

      So: ask *"is tower 2's high limit meant to trip when the plant is off
      overnight?"* — and if a trigger is ever built, gate it to occupied hours.
      A plain trigger would page someone every single night.

      ⚠️ I first called this "the only real plant item" and pushed to notify the
      engineers. That was over-called on transition count alone, before looking at
      dwell times and time-of-day.

## 🟡 WATCH — CT1 fan has not run in 14 h (opened 08/18 evening)

- [ ] **E · Ask the engineers only if it survives a peak.** CT1's fan duty was **0 %**
      over 14 h to 10:50 PT on 08/18 while CT2 alone held the tower 6.5 F off wet bulb
      on a 95.6 F day. `faultCt1` healthy throughout, and CT2 being lead fits the
      runtime gap converging at ~7 h/day — so **rotation is the likely explanation.**
      **The test: does CT1 stage in during 11:00-16:00 PT?** Rule 2's fan gate checks
      it; read the next PdM tick before raising anything with the site.

## NOW — before the Howard Hughes demo, Tue 08/18

- [ ] **E · Rotate the PEG sudo password.** It is in the 08/17 session transcript and
      does not expire. New value to 1Password only.
- [ ] **E · Confirm the indoor sensors recovered.** Unverified at hand-off — after the
      connector restart at 23:21 PDT, `device 1200` came back within 3 min but
      `device 6078` had not yet produced a read. They sit on the 900 s tier so may
      simply have been slow.
- [ ] **E · Check the 08/08 service object is CLOSED.** If it is still open the no-data
      alert is latched and cannot fire — that is why an 18 h blackout was silent.
- [ ] **E · Fix the agent schedule.** It has fired at 06:00 PT and 11:35 PM PT; the spec
      wants **17:00 PT**, after the 11:00–16:00 peak window closes. You want a fresh
      tick shortly before the demo, not fourteen hours before it.
- [ ] **E · Decide on v0.8.5** (staged, committed, on `chiller_hh`). Adds the Rule 1
      SHAPE trend — the thing that makes a *predictive* maintenance demo compelling,
      since without it Rule 1 reports a number but cannot show a trend. Against that:
      the agent has only just become stable. Your call.
- [~] **C · Temperature readings.** BLOCKED — MCP connector needs re-authorisation and
      the REST bearer token expired. Reconnect at claude.ai/settings/connectors, or
      paste a fresh token, and I will report loop + indoor temps immediately.

## 🟡 BLIND SPOT — we cannot currently verify our own alerting

- [~] **ANSWERED 08/19 — not fixable by us, and it was never an RPP.**
      Pavlo: *"there is no way (at least for now) to allow autonomous agent to allow
      use service object API — can be granted only via AAD."* Yaroslav: *"there is no
      connection between RPPs and Service Objects."* So Oksana was never the right
      ask, and neither was the agent's Permissions tab — the grant lives in Azure AD.

      ⚠️ **But two accounts disagree.** Yaroslav also said it *"has been working for
      some time already for other agents, which sounds like improper agent
      configuration or latest MCP changes"*, and that a 403 also arises when the
      caller lacks access to the Property Owner in the headers. **If it works for
      other agents it is not impossible** — worth one more question if Rule 3 ever
      matters enough.

      **Now tracked: PLAT-5721** *"Support Service Object API scope in P8S
      Applications(Agents)"* — Pavlo, **Medium, Backlog, empty description.** A
      recognised gap, not a refusal. But Medium+Backlog+no-context means months, so
      treat Rule 3 as permanently unavailable and design around it.

      - [ ] **E · Add the use case to PLAT-5721.** It has no description. The one
            thing that moves a Backlog ticket is a concrete cost: this is the only
            automated check on whether our own alerting is armed, and the no-data
            alert has latched for 65 h before.

      **Handled in the agent:** v0.9 stops calling it hourly (24 guaranteed failures a
      day), attempts once on the daily tick, and reports ⚪ NOT EVALUATED — never
      amber, never colouring the plant.

- [x] **E · Checked manually in the UI, 08/18 — BOTH ARMED, nothing latched.**
      Every service object reads `Closed`:

      ```
      1700 No Cooling - CW Supply   2026-08-10 10:47   Closed
      1700 Communication error      2026-08-08 14:47   Closed
      1700 No Cooling - CW Supply   2026-08-08 11:07   Closed
      1700 lowCt1                   2026-08-08 02:13   Closed
      1700 lowCt1                   2026-08-08 01:06   Closed
      ```

      **So the 403 is a reporting gap, not an exposure.** Re-check by hand after any
      alert fires, until the RPP lands.

      Two things worth noting from the list. **`1700 lowCt1` fires and closes on its
      own** — two events on 08/08 — so that trigger is live and self-clearing, unlike
      `highCt2`, which has no trigger at all. And **nothing has fired since 08/10**,
      which includes the 13.5 h blackout on 08/16: consistent with the known
      silence-detection gap (PLAT-5687), not evidence of a new one.

## NEXT — the monitoring gap this outage exposed

- [ ] **E+C · Connector health check.** `All device tasks completed` stopped appearing
      for 13 hours and nothing noticed; `connector-watchdog.service` was running the
      whole time and never acted (it watches IoT Hub *status*, and a wedged connector
      still publishes some devices, so status stayed OK). **That single log line is the
      cheapest reliable health signal we have.** Per-device freshness is the other.
- [ ] **E · Push PLAT-5687** (`Count` aggregation on Sensor Observations, Pavlo).
      Erik's proposed "dead / flatlining sensor" workflow needs it. Until then:
      **flatline is buildable today** (derived range/stddev sensor + `Max ≈ 0`
      threshold, if such an Observation Function exists); **silence is not buildable
      at all** — an empty window produces no evaluation, which is exactly why
      `1700 No Data - CW Plant` never fired.
- [ ] **E · Decide whether BAS alarm integration is a project.** Arguably the biggest
      gap found. The BAS Alarm Console shows **82 sources / 500 alarms**, including
      `highCt2` Offnormal (16-Aug 19:31, 12 unacked) and five AHU `dischAirTemp`
      alarms accumulating. **None of this reaches ProptechOS.** Note `highCt2` is one
      of the triggers deliberately paused on 08/08 pending validation.

## BACKLOG — data model / onboarding

- [ ] **C · Add the VAV tag** so the BAS floor plans join our data. **Source is already
      in Drive** — `point list/px/SummaryFloor1-9.px` contain
      `.../BcpBacnetNetwork/firstFloor/vav1_4` style ords, giving floor → VAV tag.
      The remaining hop (VAV tag → BACnet instance) should be in the `Bcp` folder.
      One sensor already uses the convention: littera `Wynn VAV N-N_EffectSpaceTemp`.
      **No site visit needed.**
- [ ] **E · Placement granularity.** 539 IndoorAir temp sensors map to only **39**
      building components (median 10 each) — tenant-suite level, not room.
      `servesBuildingComponent` is **0% populated**.
- [ ] **E · 42 of 80 sampled indoor sensors have NO data at all** — predates the
      outage, separate coverage gap.
- [ ] **E · Bad points.** Several read `0.0 °F`; `vav4_74` reads **888.0 °F**. Our
      30–130 °F guard catches both, but they corrupt any BAS-side average.
- [ ] **C · Paired-implausibility guard** (deferred past the demo). A sample on 08/15
      had supply −2.4 °F and return +13.1 °F in the *same* poll, dT 18.47 against an
      observed max of 9.82, recovering next poll. Passes both existing guards.
      Applies to the 1201/9950 approach rules too, where deltas are smaller and a bad
      read distorts proportionally more.

## CARRIED — unchanged, from earlier work

- [ ] HX runtime never equalises — 4,806 h gap, ≈10 h/day widening. Rotation disabled
      or Hx1 hard-set lead? Best question to put to the site.
- [ ] `hxRuntimeAlmSp` flat at 0 — configured, or dead?
- [ ] `runtimecwp1` / `runtimecwp2` byte-identical — one register mapped twice, needs
      a BAS correction. Do not report the zero imbalance as healthy.
- [ ] `blowdownWater` dead across 36,437 samples — instrumentation ask; water chemistry
      unmonitorable without it.
- [ ] `bldgSupplyFlow` 41% zeros — genuine cycling or broken point? Not usable as a
      denominator either way.
- [ ] `device 100005` VFD — confirm what it drives and whether `Power` is W or kW.
- [ ] `device 118010` + three never-reporting devices (`153067`, `53036`, `6207`).
- [ ] **SMS alarm template still says "check chillers"** in the live dispatcher. The
      spec was corrected to "cooling towers + heat exchangers" on 08/11; ProptechOS
      was never updated. **This building has no chillers.**
- [ ] **Engineers still not SMS recipients** — Josh Smith 702-278-7255, Josh Chong
      725-270-2861, Gary Hornick 702-427-0083, none confirmed. Blocks go-live.
      Gary was on PTO to 08/20.

## ASKS OF PLATFORM

- [ ] **PO thread-local fix** — Pavlo, targeted ≈08/18. Cross-tenant isolation defect;
      identity held in thread-local on a pool shared across all customers.
- [ ] **PLAT-5687** — `Count` aggregation. Blocks all silence detection.
- [ ] **Is `aggregation: "hourly"` a mean or a median?** Asked 08/10 and 08/12, still
      unanswered, and it is load-bearing: **if median, Rule 1 drops `raw` entirely**
      and the payload problem disappears permanently. Evidence it is a mean: the
      08/05 outage hour read **12.33 °F while the loop was near 105 °F**.
- [ ] **Azure AD client secret is visible in plain `ps`** on the PEG — it sits in the
      `ExecStart` line of all three connector services. Suggest an environment file
      or systemd credential.

---

## RESOLVED THIS WEEK — for the record

- [x] **18 h blackout 08/16 09:49 → 08/17 23:21 PDT.** The connector's polling loop
      wedged; it stayed `active`, kept logging and kept publishing *some* devices, but
      never completed a cycle. A restart fixed it in 3 minutes. **The Distech
      controller was never at fault** — the BAS was reading it live throughout, which
      is what disproved my "controller down, send someone to the plant" call. The
      reprogramming Joshua mentioned is also exonerated: no objects were renumbered.
- [x] **The 401 cascade** — wrong property owner, a platform cross-tenant defect. Not
      token expiry, not "never re-mints", not prompt edits. All three of those were my
      diagnoses and all three were wrong; **no PLAT ticket was ever warranted.**
- [x] **The 1700 PdM agent works again** — v0.8.4 ran clean, 6m36s / 201 K tokens /
      31 calls, against v0.7's 21m27s / 1.26 M. Payload fix validated.
- [x] **HX2 "flow fault" retracted** — raised from one off-window sample, inverted when
      tested against a full weekday peak window. Effectiveness seed since confirmed
      independently (HX1 0.895 vs seed 0.90; HX2 0.670 vs 0.67).
