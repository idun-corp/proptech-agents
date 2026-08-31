# Summerlin cooling agents — the twin work, consolidated

**Status 08/31/2026.** ONE new ticket to file (§1). Everything else is comments on tickets that
already exist (§2–§4). An earlier version of this file proposed two new tickets — that was wrong,
the work was already scoped, and it has been replaced.

## Where the twin work currently lives — three places, which is why we consolidate

| Ticket | Covers | State |
|---|---|---|
| **OTEAM-6740** (Oksana) | One Summerlin — all 15,544 tags from handoff v5, incl. our 96 | open, epic OTEAM-5539 |
| **OTEAM-6739** | Two Summerlin — all tags, plant already batched W0-smoke | open, epic OTEAM-5554 |
| `jira_NEW_refcalc_gap_analysis_one_summerlin.md` | The same 16 Trane AHUs, RefCalc tag coverage | **drafted 05/10, apparently never filed** |

The third one matters: its "category A — easy fix, software-only, **Recommended**" item (onboard the
loop supply/return temps at `AS_2187664`) is **still not done four months later**, and §4 below
explains why — it is not actually easy.

---

## §1 — NEW TICKET (the only one to file)

**Issue type:** Task · **Project:** OTEAM · **Epic:** OTEAM-5539 (One Summerlin)
**Assignee:** Erik Wallin · **Relates to:** OTEAM-6740, PLAT-5581

**Title:**

```
One Summerlin Bldg J: create 96 run-state twins + correct storey placement on 24 twins, in-house, ahead of OTEAM-6740
```

> Erik here — built with Claude's help, may have misunderstood something, please don't hesitate
> to challenge me. 🙂

**What this is.** We are standing up a refrigeration PdM agent on the 16 Trane self-contained
units at Bldg J. The refrigerant data it needs is already live (22 points × 16 units — rule v1
happened to keep it, because Trane puts it on `analog-input`). What is missing is the **run
state**. Rather than wait for the 15,544-tag bulk load, we are creating that subset ourselves.
This ticket is the record of what we did.

### Scope A — create 96 Sensor twins

16 devices (BACnet instances 723101, 723102, 723104, 723105, 723107, 723108, 723110, 723111,
723113, 723114, 723116, 723117, 723119, 723120, 723122, 723123) × 6 points:

| Object | Vendor name | `twin_class` | States |
|---|---|---|---|
| `multi-state-input 25/26/27` | Cool Output 1 / 2 / 3 | Sensor | 3 |
| `multi-state-input 41` | Supply Fan Status | Sensor | 3 |
| `multi-state-input 19` | Application Mode Status | Sensor | — |
| `multi-state-input 35` | Primary Filter Status | Sensor | 3 |

All 16 device twins already exist — these are sensors on existing devices, no new devices.
Building `623a9f1d-3506-4144-b82b-ad46430e48b3`, alias prefix
`https://ns.proptechos.com/bacnet/summerlin/`. Rows and device twin UUIDs are in handoff v5 and
in `experts/hhc/onesummerlin-bldgJ-refrigeration-bindings.csv`.

`multi-state-input 28` (Cool Output 4) reads `Not Present` on this profile — skipped deliberately.

### Scope B — correct storey placement on 24 twins

The v5 handoff places every AHU-J unit on `LEVEL 01` / `LEVEL 02`. It read the "J1"/"J2" in the
device name as a floor number.

Instances 723101–723124 run in strict `{AHU-J1-n, AHU-J2-n, FPT-Jn}` triplets, n descending 9 → 2.
**The trailing digit is the FLOOR (2–9); "J1"/"J2" is the RISER** — two self-contained units and
one fan-powered terminal per floor, floors 2 through 9.

```
723101 AHU-J1-9   723102 AHU J2-9   723103 FPT-J9     <- floor 9
723104 AHU J1-8   723105 AHU J2-8   723106 FPT-J8     <- floor 8
...
723122 AHU J1-2   723123 AHU-J2-2   723124 FPT-J2     <- floor 2
```

Same class as the Meridian "10 storeys to create" bug (OTEAM-6716) — numbers in device names are
equipment ids, not floor numbers — except inverted: here the floor IS in the name and was
discarded. 16 AHU + 8 FPT twins to re-place.

### ⚠️ Dedupe contract — the one thing that can go wrong

These 96 rows are **inside OTEAM-6740's scope**. If we create them and the bulk load later runs
against the current v5 CSV, it will create them **again**.

**Before OTEAM-6740 runs, `existing_sensor_twin_id` must be re-derived** against the live model —
the same dedupe step the Meridian v4 handoff did for all 658 live twins. Either we regenerate v5's
column after our run and re-upload the CSV, or Oksana re-derives at her end. **Please confirm which,
Oksana** — this is the only real risk in doing it ourselves.

### Not in scope

**No connector work.** Creating twins is metadata and costs the field bus nothing; the connector
is the only thing that generates BAS load, and it is a separate config regen against PEG HHHEG-002
whose watchdog is deliberately disabled (PLAT-5578). Polling rides PLAT-5581 — see §2.

**Twins alone do not report.** These 96 will exist and stay silent until the connector regen. That
is expected and is the point of "onboard-all, poll-gradual".

---

## §2 — Comment on PLAT-5581 (One Summerlin connector)

**Two sequencing problems, both inside work already ticketed. No scope change.**

**(a) The run-state points land one wave AFTER the data they gate.**

| Point | Wave | Poll |
|---|---|---|
| Condensing Saturated Temp Circuit 1–3 (`analog-input 42/43/44`) | **W1** | 900s |
| Evaporator Leaving Temp Circuit 1–3 (`analog-input 38/39/40`) | **W1** | 60s |
| Condenser Water Entering / Leaving (`analog-input 35/46`) | **W1** | 60s |
| **Cool Output 1–3** (`multi-state-input 25/26/27`) | **W2** | 900s |
| **Supply Fan / Application Mode / Filter Status** (`41/19/35`) | **W2** | 300s |

(2 of the 16 units sit in W0-smoke for all of the above; the other 14 split W1/W2 as shown.)

Without run state the agent derives it from `sign(CondSat − CW leaving)`, which caps every finding
at P2 and forbids P1. This is the gap behind the 9950 Woodloch incident — a three-hour-old agent
recommended calling a contractor for a chiller that had drawn zero power for the whole window; only
run state for the window separated a real precursor from stagnant water. **Please pull the 84 W2
rows into W1.**

**(b) The two halves of one calculation are tiered 15× apart.** Condenser approach is
`CondSat − CW leaving`. `CondSat` is proposed at **900s**, `CW leaving` at **60s**. Per the tier
table in the connector playbook, compressor-circuit temperatures belong in the 1-min tier — the
saturated condensing temps look mis-tiered. **Suggest 60s for `analog-input 42/43/44`.** Tolerable
for a daily PdM either way; raising it because it will bite anything hourly.

**Load.** Trunk 7231 polls **388 objects** across 36 devices today; +96 takes it to 484, **+24.7%**
(full-keep for that trunk is 1,616). Please confirm against the measured cycle, not my arithmetic.

**Question back:** does the connector deployed on HHHEG-002 have the per-sensor `pollingPeriod`
support from PLAT-5554? The whole cadence plan assumes it.

---

## §3 — Comment on OTEAM-6739 / PLAT-5580 (Two Summerlin) — chase, don't re-file

**The entire plant is already in W0-smoke** — 480 sensors across 15 devices (`UC600-02 CW Plant` 53,
`UC600-01 ERU-01` 22, six `TR-*` VFDs 24 each, four `CSC-*` 64 each). Zero is live; the 1,437
flowing sensors are the Nov 2025 VAV load. It is the highest-value 480 points on the campus, it is
already first in the queue, and it just needs running.

It unblocks a direct port of both 1700 Pavilion plant agents onto a **richer** dataset: both heat
exchangers instrumented, native wet-bulb and tower approach, lead/lag as readable state, and six
*named, metered* VFDs where 1700 has to infer drive identity from run-hour matching.

**We are deliberately NOT doing this one in-house** — 480 sensors across a different PEG (HHHEG-003)
and a different connector is a bulk load, not a carve-out.

**Fix during onboarding, not in the agent:**

1. **`TR-* analog-value 6 Power` reads 7360.0 kilowatts** on a fan/pump drive — scaleFactor off by
   1000, true value approx. 7.36 kW. Check `analog-value 7 Kwatt Counter` (186,289 kWh) against the
   same factor before either is used as an energy basis.
2. **The CSC units report Celsius** while the *identical* Trane BCI-I model at One Summerlin reports
   Fahrenheit, same object ids. Set `deviceMeasurementUnit` from the scan's `bacnet_units` per
   device, never from the model name.
3. **`Outdoor Air Temperature Local` reads −40.001 °C** on CSC-03 — unwired sentinel. Drop or annotate.

**Not blocking:** `CSC-01`/`CSC-02` are absent from the scan, behind the panel hung since 2026-06-23
along with all 71 floor-1/2 VAVs and both smoke-purge controllers. Add them after the power-cycle.

---

## §4 — Corrections to the RefCalc gap analysis (never filed; file or discard, but fix first)

That draft concluded ~208 RefCalc data points missing on the 16 AHUs, with `PT_RHP`/`PT_RLP` needing
**$25–40k of capex**. Two things in it are wrong, and one of them affects that number.

**1. `Evaporator Leaving Temperature Circuit N` is refrigerant-side, not water-side.** The doc lists
it as "water-side leaving evap temp". There are **three per unit**, one per refrigerant circuit —
water-side would be one per unit. These are self-contained DX units; there is no evaporator water.

**2. `Condensing Saturated Temperature Circuit 1/2/3` was missed entirely.** It is not in the
crosscheck table at all, but it is on all 16 units (`analog-input 42/43/44`) and it is **already
live**. That is the saturated high-side condition — for a pure refrigerant the same state variable
as high-side pressure, just expressed as a temperature.

**So part of the capex may already be on the wire.** ⚠️ Stated as a question, not a conclusion —
it depends on (a) whether RefCalc can consume a saturation temperature in place of `PT_RHP`, and
(b) the refrigerant, since a blend with temperature glide breaks the clean P↔T equivalence. The
refrigerant type is not in the scan for these units. **Worth answering before anyone quotes $25–40k.**

**3. The category-A "easy fix" is not easy.** The doc recommends onboarding the loop supply/return
temps at `AS_2187664` (Schneider SmartX AS-P). Two obstacles it did not see:

- Both points are `analog-output`, so the handoff classes them **`twin_class = Actuator`** — and the
  connector playbook records that **actuator twins are not supported by the BACnet connector**. They
  would be created and never stream.
- The `AS_2187664` **device twin does not exist** either (VBC "Central Plant").

They are plainly *readings* — an AS-P publishing a computed loop value outward, not a command — so
classing them by BACnet object type alone mislabels them. **Marichka / Oksana: should these be
`Sensor` despite being `analog-output`, and does that unblock the connector?** This is the loop
supply/return pair, so it is worth the question — with it the agent measures the condenser loop
directly instead of reconstructing it from 16 units.

(Naming note: the May draft calls these `BldgSupTmp`/`BldgRetTmp`; the July v5 scan has them as
`CWSTmp`/`CWRTmp` on the same device. Same pair, renamed between scans.)
