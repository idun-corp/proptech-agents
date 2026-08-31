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

## 🔴 08/28 INCIDENT — phantom device twin killed the connector (RESOLVED same day)

**337 of 338 devices dark 05:53–12:38 PDT, zero errors logged.** Plant kept reporting throughout, so
cooling visibility and the no-cooling SMS were never affected.

**Cause:** a device twin whose BACnet instance does not exist at its configured IP answers
BACnet-Error, leaving `segmentationSupported` null, and the resulting NPE in bacnet4j's transport
thread aborts binding for *every other device*. Timeouts are benign; only respond-with-error is
fatal. It cascades — remove one and the next takes over.

**Fixed** by removing 6 phantoms from `iot_edge_config.json` on the PEG and restarting (Erik
authorised; two plain restarts had already failed). Backup at
`/tmp/iot_edge_config.BACKUP-2026-08-28.json` on the PEG.

```
BEFORE     1 device ·   141 sensors
AFTER    352 devices · 1,599 sensors · 574/574 occupancy · 0 errors   <- 100% of configured
```

- [x] **C** — recover the site
- [ ] **E/C** — **Monday: tell Marichka.** The 6 phantoms (10107, 178, 179, 2101, 10115, 161241)
      still exist in ProptechOS and **return at her next deploy**, bringing the crash risk with them.
      The local edit is self-cleaning, so this is not optional.
- [ ] **E/C** — file the PLAT ticket: draft at `experts/hhc/PLAT-draft-phantom-device-npe.md`
      (Atlassian MCP was disconnected 08/28). Core ask: one device's bind failure must not abort the
      rest, and a device that fails to bind must log an ERROR rather than go silent.

---


## 🆕 08/31 — EMBODIED BUILDING AGENT drafted, blocked on two bindings

`1700-pavilion-embodied-agent.md` v0.4 + `1700-embodied-zone-bindings.csv` (286 zones).
The first 1700 agent that watches the **occupied** building rather than the plant: zone
comfort, schedule behaviour, electricity, and a printed daily statement of which senses
this building does not have. **Daily 06:00 PT, exception-based** — silent one-liner unless a rule
trips; the daily report is a `DAILY_REPORT` switch, off by default. EMAIL dispatch on
deviation, SMS reserved for a tenant-affecting event no existing alert covers and shipped
Disabled. 90-call ceiling, 27 sentinel zones — it samples, it does not scan.

⚠️ **It cannot roll up the PdM and the Watch.** No agent in this estate can read another
agent's output — no report store, no run-history tool, and `get-service-objects` is 403
(PLAT-5721). 1-to-1 routing re-runs the target agent (~283k tokens, 7.5 min), so it is an
on-demand escalation, never a daily habit. The agent instead prints a `NOT MINE TODAY` line
naming what the specialists own, and aggregation happens in the reader's inbox.

### ✅ FIRST LIVE RUN 08/31 07:09 PT — it works, and it cost too much

63 calls, **742k tokens, 14m19s** to produce fourteen lines of finding. Three real findings
on the first morning, two of them new classes: **slow startup pulldown** (5 zones 45-80 min
to band, worst Hearst Healthcare 82.4 -> 77.6 F at +79 min), a **cold-side excursion**
(Summerlin Gallery VAV 1-5, 67-69 F for 90 min - nothing at this building has ever looked
below the band), and **Snell & Wilmer released for the first time in 23 days**.
Also observed: **weekday occupied-start is 05:09-05:24 PT, not the ~06:10 on record** - that
06:10 was a Saturday figure. Thresholds table corrected.

**v0.4 fixes what the run exposed:** verdict-first report capped at 20 lines · sentinel sweep
must use hourly aggregation, never raw series (~92 points/sensor was the whole cost) · the
daily `SENSES DARK` and `WATER: ⚪` recitals are gone · a single amber is MINOR, not SEVERE
(v0.3 sent a probably-transient pulldown as `[Severe]`) · Rule 1 gains the cold side and a
pulldown-vs-steady-state split. Target now 40 calls / 250k tokens.

- [ ] **C · Confirm v0.4 lands under budget** on the next run, and that the report fits 20 lines.
- [ ] **E · Does the 05:09 start need chasing?** Either the BAS weekday schedule changed or it
      was never 06:10. Cheap to settle and it feeds Rule 3's outside-schedule maths.
- [~] **C · PM1 + PM2 total-power sensorIds.** Rule 4 (electricity) is ⚪ until these are
      bound. `popularName` is null on all 54 meter sensors (**OTEAM-6827**) so they cannot
      be resolved by name — needs device + littera. The two PAC3220s are at
      `192.168.2.218` / `.219`, total power is register 65.
- [~] **E · Gross area in ft².** Every `kWh/ft²` figure depends on it, and the agent is
      instructed not to guess one. Absolute kWh only until it is filled in.
- [ ] **C · Verify the 27 sentinels report** on first run — 12 of 289 UNITOUCH SpaceTemp
      points are genuinely dark, so a sentinel may need swapping.
- [ ] **C · Do the Northern Trust / ER Injury footfall twins carry observations?**
      `AreaPresence` / `Footfall` / `DirectionInward`-`Outward`, unit `NumPeople`, created
      by taras. They have **no `source`** in the twin, so probably no data path — but if a
      people-counting integration is live, two tenants get a real occupancy sense and the
      "schedule, never people" caveat narrows for them.
- [ ] **E · Create the EMAIL DispatchConfig** with `erik@wallin.se`, and the SMS config with
      `+46704124900`, for the validation runs (same pair as the 08/24-08/27 dispatch tests, so a
      failure is comparable against a known-good run). ⚠️ **Naming them in the prompt does not
      wire them up** — they must be entered in the Dispatch UI or every signalled dispatch
      resolves to whatever the config actually holds, possibly nobody.
      ⚠️ **Then delete the block from the spec** once the channels are proven: personal contact
      details are outside this folder's containment rule.
- [ ] **E/C · Test the ON-REQUEST path, both channels.** v0.3 makes "email me that" / "text me"
      a dispatch trigger in its own right, outside the deviation rules and the repeat limit.
      Ask it in conversation and confirm both arrive — the cheapest end-to-end proof available,
      and it does not require waiting for a real deviation.
- [ ] **E · Create the EMAIL DispatchConfig** (Agent editor -> Behavior -> Dispatch) and
      **Reset the agent** — without a reset the dispatch block never reaches the prompt and
      the agent silently never dispatches. Create the SMS config too but leave it Disabled.
      ⚠️ Do NOT add a Service Object config: on 08/24 it crashed the invocation outright
      (`No ToolCallback found for tool name: none`, 0 tokens), and the fix is unverified.
- [ ] **C · Regenerate the bindings CSV when OTEAM-6845 lands.** Do not hand-patch it.
- [ ] **E · Get the actual BAS weekday schedule.** Saturday (06:10 → 13:12) and Sunday
      (none) are observed; the weekday off-time is not, so Rule 3 has to hedge.

## 📋 08/31 — two tickets out, mapping paused for review

- **[OTEAM-6845](https://idun.atlassian.net/browse/OTEAM-6845)** (Erik) — 41-device zone remap ready
  for Oksana's review. CSV: `1700-zone-remap-FULL.csv`. 26 Wynn Suite 1000 + 5 MP Mine Operations +
  2 Summerlin Gallery need zones **created** first.
- **[PLAT-5787](https://idun.atlassian.net/browse/PLAT-5787)** (Marichka) — owns the PEG config edit,
  asks her to fix the 6 twins before her next deploy.

⚠️ **`device 2101` is in BOTH tickets.** It is a real air handler needing its IP corrected
(`192.168.2.67` → `192.168.2.101`), not deleted. If Oksana and Marichka act independently they can
collide — tell whoever moves first.

⚠️ **84 unassigned devices are deliberately NOT in the CSV.** An IP-range auto-match produced
nonsense (Touchstone's block swallowed 91 sensors that are not theirs) and was discarded. They need
the BAS folder walked device by device. **Never auto-match by IP range alone** — only contiguous
blocks anchored on an already-correct assignment are safe.

- [ ] **E** — unblock or run `apply_zones.py` yourself. The safety classifier refuses production
      writes from the session, and refuses to let Claude grant itself the permission (correctly).
      Either add `"Bash(python3 <scratchpad>/apply_zones.py:*)"` to `permissions.allow`, or run it.
      Script is committed here as `apply_zones.py`: `snapshot | plan | apply-one | apply | rollback`.
- [ ] **C** — build `plan.json` (not done yet).
- [ ] **C** — redo the weekend reconciliation on the corrected Summerlin Gallery zones
      (`device 10105`, `device 1033`) — does not depend on the remap landing.

---

## ✅ 08/31 — CORRECTED: the portal DOES reach the BMS, but not for the booked duration

⚠️ **The 08/30 finding below is WITHDRAWN.** It analysed 187 of 292 zones and used the wrong ones
for Summerlin Gallery. Erik challenged it; he was right.

**The BAS Nav tree groups every VAV by tenant/suite** — see `1700-bas-tenant-tree.md`. Reached via
LogMeIn → Px View. That is the mapping we could not rebuild from ProptechOS.

**Suite 120 = Summerlin Gallery = 2 VAVs only:** `vav1_05` (device 10105), `vav1_23` (device 1033).
The 15-zone "Howard Hughes Holdings" group is **Suite 250**, a different tenant.

```
SUNDAY   $450 / 07:00-17:00   vav1_23 on 06:56 -> off 10:04  (3h08 of 10h) · vav1_05 never on
SATURDAY $180 / 13:00-17:00   vav1_23 on 06:10 -> off 17:07  (covers it)   · vav1_05 off 13:12
```

- The portal **does** reach the BMS — Sunday had no base schedule and vav1_23 came on at 06:56,
  four minutes before a 07:00 booking.
- The **duration is not honoured** — that is the actual defect.
- It is **not Bypass**: neither zone entered state 3, the request shows as *Occupied*.
  BypassTime is 30 min on one and 480 on the other. **The dashboard's Bypass-based detection
  design will not work.**
- Physically partial: vav1_05 held 68-70 °F regardless, which is why nobody complained.

- [ ] **E** — finish the mapping: expand tenant folders on floors 2, 3, 4, 6, 7 + TouchstoneLiving,
      or export (right-click floor → Export → "Object to oBIX"; ⚠️ writes to the REMOTE machine).
- [ ] **C** — then confirm on floor 7: Snell & Wilmer is the whole floor, zero ambiguity.
- [ ] **C** — apply the mapping. `PATCH /sensor/{id}` with `/isMountedInBuildingComponent`
      is confirmed working (405 on a bad path, 409 on a bad value).
- [ ] **C** — rewrite the dashboard brief: detection must be "Occupied outside the base schedule",
      not Bypass.
- [ ] ⚠️ **Nothing to Josh or Courtney until the mapping is finished.**

⚠️ Floor 5 trap: `vav5_3` (Bessemer) and `vav-5-3` (ER Injury) are different boxes. BACnet renders
both "VAV 5-3", so the 187 already-mapped zones may already be crossed.

---

## 🔴 08/30 — SATURDAY RECONCILIATION: the tenant portal is not reaching the BMS

First hard evidence, both failure modes in one day. Every tenant's Saturday on/off mapped:

```
21 of 24 tenants   ON 06:10 PDT  OFF 13:12 PDT   base Saturday schedule
Snell & Wilmer     always Occupied, never releases
Touchstone Living  ON 06:10      OFF 17:07 PDT   4 h longer
Wynn Design & Dev  ON 06:10      OFF 17:07 PDT   4 h longer
Howard Hughes      ON 06:10      OFF 13:12 PDT   same as everyone
```

- **PAID, NOT DELIVERED** — Summerlin Gallery paid **$180** for 13:00–17:00. Zones shut off at
  **13:12**, twelve minutes in, and stayed off for the whole paid window.
- **DELIVERED, NOT PAID** — Touchstone Living and Wynn ran 4 h past the base schedule, 24 zones,
  no booking in the weekend emails.
- **ZERO Bypass across all 287 zones.** Only state-3 was `device 1200`, the known object-number
  collision. Power 380 kW vs 390 / 354 the two previous Saturdays — no trace of the paid bookings.

- [ ] **C** — Monday: re-run with the **full weekend**, incl. Sunday's 10 h / $450 booking.
      `scratchpad/bypasscheck.py <token> sun`. Two failures in a row makes this unarguable.
- [ ] **E/C** — check the portal whether Touchstone / Wynn had active bookings. ⚠️ The Activity
      History export **cannot show future active bookings**, so absence there proves nothing.
- [ ] **E** — then take it to Josh and Courtney. This is a billing-integrity finding, not an
      energy one: a tenant paid for HVAC they did not receive.

⚠️ Snell & Wilmer's $270 is **unverifiable** — 22 zones locked in Occupied can never show Bypass.
The "stuck in Occupied" defect is corrupting the measurement, as predicted.

---

## ⚠️ 08/30 — the cooling margin was being OVERSTATED in daily reports

```
bldgCwSupply peak vs the 85 F alarm, 14 days:  worst 3.3 F (21 Aug, 81.7 F)
typical peak margin 4-6 F · daily mean stable 75.5-76.4 F
```

Reports quoting "8–9 F margin" used **overnight** readings, when the building is idle. **Quote the
daytime peak.** Never breached; mean rock-steady.

**And CT1 is not untested** — correcting a claim repeated for days:

```
CT1  +19 h over 14 days (ran ~24 Aug)   fan ON 0.3% of last 7 days
CT2 +189 h over 14 days                 fan ON 53.6% of last 7 days
```

**Cooling failure risk: LOW.** CT1 is proven functional within the fortnight, CT2 at 54 % duty has
headroom. Residual: peak margin tighter than assumed, CT2 does ~90 % of the work, CT1's isolation
valves have not cycled in 7 days.

⚠️ `ctMakeupWater` stepped 0 → 8200 on 29 Aug and has been **flat ever since, including while CT2
ran**. A register that changed state, not consumption. **Not a leak.**

---

## 🟠 OPENED 08/28 — follow-ups from the phantom-twin outage

- [ ] **E/C** — **restore `device 2101`** with `bacnetHost=192.168.2.101`. A real air handler
      (`MTIII_AHU_02101`, 8 sensors) whose twin records `192.168.2.67` — a wrong address, not a
      phantom. Removed in the outage fix; this is collateral damage to repair.
      ⚠️ The permission classifier blocked PEG config edits three times, so this needs a Bash
      permission rule or a manual edit. Backup on the PEG:
      `/tmp/iot_edge_config.BACKUP-2026-08-28.json`.
- [ ] **E/C** — Oksana: delete the 5 genuinely-stale twins (`Wynn VAV 10-28`, `Wynn VAV 10-29`,
      `ECY-VAV-D837F8`, `ECY-VAV-D84D93`, `VAV-8`) — none appear anywhere across 8 subnets.
- [ ] **E/C** — Oksana: **onboard the ~30 discovered devices**. Ten `MTIII_AHU_*` air handlers at
      `192.168.2.101–110` (we collect 2 of ~10, and they drive the after-hours question), ~14 more
      `ECY-VAV-*`, and a **DIRIS A-40 power meter** at `192.168.0.149` that has never been counted.
- [ ] **E** — decide on `bacnet-test-3.0.jar`, still running under `screen` (PID 51347) bound to
      `192.168.7.50`, the production connector's own address, with COV listening enabled.
- [ ] **E** — two credential exposures left on the PEG: an IoT Hub policy key and Azure AD client
      secret in `/opt/proptechos/test-connector/application.properties` (mode 664), and an Azure
      storage account key in plaintext in `.bash_history`. Both `idun-dev-*`, on a customer site.
- [ ] **C** — chase the 12 of 289 `UNITOUCH SpaceTemp` (`analog-input 9011`) not reporting. Real
      wired points, unlike the ~1,053 unfitted accessory points that make the UI look 60 % dead
      when the site is at 99.1 %.

⚠️ **Our config fix is self-erasing.** Any deploy to `2c28ab21` restores the six bad twins and the
site goes dark again, silently. Marichka has to fix them platform-side before that happens.

---

## 📌 MONDAY 08/31 — the weekend reconciliation test (opened 08/27)

**Genea has NO request for 1700 on Sat 08/29 or Sun 08/30.** Clean natural experiment: the
occupancy points are live, and the request list is confirmed empty.

- [ ] **C** — pull `OccupancyStatus` for all 292 sensors, 08/29 00:00 → 08/31 00:00 PT
- [ ] **C** — count zones showing state 1 during 06:00–17:00 PT each weekend day
- [ ] **C** — compare PM1+PM2 against the 350–476 kW weekend profile vs ~145 kW baseline
- [ ] **C** — re-export Genea Activity History; confirm nothing was booked retroactively
- [ ] **E** — supply a fresh bearer token (1 h lifetime; a scheduled job cannot do this)

**Zones ran** → unordered conditioning, headline is unbilled cost.
**Baseline + Unoccupied** → weekend load was always Wynn's, headline is margin per booking.
Either result decides which panel leads the Courtney dashboard. Full procedure in memory
`hhh-1700-pavilion-plant.md`.

Also due Monday:
- [ ] **C** — re-check the 21 devices the connector still will not poll (alive, 84 real values)
- [ ] **C** — confirm whether Wynn's recurring weekend series actually ended after 08/23

---

## 🟢 CHEAP ASK, independent of the test — two suites missing from ProptechOS

- [ ] **E/C** — ask Oksana to map **Suite 150 (Douglas Elliman)** and **Suite 800 (MP Mine
      Operations, 48 paid hours / $2,160)**. Both are almost certainly inside the 105 VAVs parked
      in `TENANT SPACE` / `MECH. ROOM`. Every other Genea area already reconciles — see
      `1700-genea-p8s-join.csv`. This turns the vague "36 % unattributed" into two named suites.

---


## 🔁 PENDING 2026-08-26 — reboot test to prove the network fix persists

- [ ] **C · Controlled reboot of the 1700 PEG, early afternoon PT.** Deferred from 25 Aug: the
      plant was at its morning peak (424-442 kW, 06:00-08:00 PT) and Erik had a customer demo, so
      the tail risk of a PEG that does not come back was badly timed. Best window is after the
      morning pull-down, before the evening peak.

      **Why:** on 25 Aug we added five IP addresses to close a gap that had 171 devices / 1,040
      sensors dark. Publishing devices went 75 -> 353 of 357, errors 1,942/h -> 0. The addresses are
      persisted in the NetworkManager profile on disk (`method=manual`, 8 x `addressN=`), which is
      exactly what was missing on 21 Aug when a reboot cost 6 h 09 m of cooling visibility. Evidence
      is strong; the reboot converts "very likely" into "proven".

      **Pre-flight (all verified 25 Aug, re-check before rebooting):**
      8 addresses in `/etc/NetworkManager/system-connections/Wired connection 1.nmconnection` ·
      4 connectors + watchdog `enabled` · one NM profile per interface · SSH is on `enP4p65s0`
      (192.168.50.52), field network is `enP3p49s0` so the reboot does not cut the management path.

      ⚠️ **Copy the connector logs off the box first** — `/var/log` is on zram (`/dev/zram1`), so a
      failed boot destroys the evidence of why.

      **Checklist:**
      1. capture baseline: publishing devices + distinct sensors on `2c28ab21`
      2. `sudo reboot`
      3. SSH back — 51 s on the 22 Aug test
      4. verify 8 addresses live, 4 connectors active, device 1200 returning real values
      5. verify publishing count returns to ~353 devices — 90 s on 22 Aug

      **If the addresses are missing after boot**, the profile was not applied: check
      `nmcli -g GENERAL.STATE device show enP3p49s0` and whether another profile claimed the
      interface. Rollback is not needed; re-add with `nmcli connection up "Wired connection 1"`.

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
- [x] **`device 100005` is CT2's FAN VFD — settled 08/19.** 97.2 % agreement between
      `Drive Running` and `fanStatCt2`, against 82.1 % for `fanStatCt1`, over 3,967
      paired samples. `Power` is declared kW but reports **W** — divide by 1,000.
      Every kW and amp figure we have ever quoted for "the tower fan" is **CT2's**.
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
