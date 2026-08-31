# Summerlin — what the cooling agents need from onboarding

**Corrected 08/31/2026.** An earlier version of this file proposed two NEW tickets. That was
wrong: **every point both agents need is already scoped and already batched** in the existing
handoffs. Nothing new needs filing. What follows are **three comments on existing tickets**
plus one genuine new defect.

---

## 1. One Summerlin Bldg J — comment on PLAT-5581 (cc OTEAM-6740, epic OTEAM-5539)

> Erik here — built with Claude's help, may have misunderstood something, please don't
> hesitate to challenge me. 🙂

**Ask: move 84 rows from W2 to W1, and re-tier 48 rows from 900s to 60s.** No scope change.

We are standing up a refrigeration PdM agent on the 16 Trane self-contained units at Bldg J
(BACnet instances 723101–723124, MS/TP trunk 7231). Two sequencing problems in the current wave
plan, both inside work already ticketed:

**(a) The run-state points land one wave AFTER the data they gate.**

| Point | Object | Wave | Poll |
|---|---|---|---|
| Condensing Saturated Temp Circuit 1–3 | `multi-state`→ `analog-input 42/43/44` | **W1** | 900s |
| Evaporator Leaving Temp Circuit 1–3 | `analog-input 38/39/40` | **W1** | 60s |
| Condenser Water Entering / Leaving | `analog-input 35/46` | **W1** | 60s |
| **Cool Output 1–3** (circuit run state) | `multi-state-input 25/26/27` | **W2** | 900s |
| **Supply Fan Status** | `multi-state-input 41` | **W2** | 300s |
| **Application Mode Status** | `multi-state-input 19` | **W2** | 300s |

(2 of the 16 units are in W0-smoke for all of the above; the other 14 split W1/W2 as shown.)

Without run state the agent must derive it from `sign(CondSat − CW leaving)`, which caps every
finding at P2 and forbids P1 entirely. This is the gap that produced the 9950 Woodloch incident —
a three-hour-old agent recommended calling a contractor for a chiller that had drawn zero power
for the whole window; only run state for the window separated a real precursor from stagnant
water. **Please pull the 84 W2 rows into W1** so the gate arrives with the data it gates.

**(b) The two halves of one calculation are tiered 15× apart.** Condenser approach is
`CondSat − CW leaving`. `CondSat` is proposed at **900s**, `CW leaving` at **60s**. Per the tier
table in the connector playbook, chiller/compressor circuit temperatures belong in the 1-min
tier — the saturated condensing temps look mis-tiered. **Suggest 60s for `analog-input 42/43/44`**
to match. (Tolerable for a daily PdM either way; raising it because it will bite anything hourly.)

**Load impact.** Trunk 7231 currently polls **388 objects** across 36 devices. The 96 run-state
rows take it to 484, **+24.7%**. Small next to the full-keep projection for that trunk (1,616),
but please confirm against the measured cycle rather than this arithmetic.

**Question back:** does the deployed BACnet connector on HHHEG-002 have the per-sensor
`pollingPeriod` support from PLAT-5554? The whole cadence plan assumes it.

---

## 2. One Summerlin Bldg J — NEW DEFECT, storey placement wrong on all 16 units

**This one is genuinely new.** Please file or fold into OTEAM-6740.

The v5 handoff places every AHU-J unit on `LEVEL 01` or `LEVEL 02`. It read the "J1"/"J2" in the
device name as a floor number.

BACnet instances 723101–723124 run in strict `{AHU-J1-n, AHU-J2-n, FPT-Jn}` triplets with n
descending 9 → 2. **The trailing digit is the FLOOR (2–9); "J1"/"J2" is the RISER.** The tower
carries two self-contained units and one fan-powered terminal per floor, floors 2 through 9.

```
723101 AHU-J1-9   723102 AHU J2-9   723103 FPT-J9      <- floor 9
723104 AHU J1-8   723105 AHU J2-8   723106 FPT-J8      <- floor 8
...
723122 AHU J1-2   723123 AHU-J2-2   723124 FPT-J2      <- floor 2
```

Same class as the Meridian "10 storeys to create" bug (OTEAM-6716) — numbers in device names are
equipment ids, not floor numbers — except inverted: here the floor IS in the name and was
discarded. Affects 16 units + 8 FPT terminals.

---

## 3. Two Summerlin — chase OTEAM-6739 / PLAT-5580 (epic OTEAM-5554)

**No new ticket needed. The entire plant is already in W0-smoke** of
`twosummerlin_connector_manifest.csv` — it simply has not been executed:

| Device | Points | Wave |
|---|---|---|
| `UC600-02 CW Plant` | 53 | **W0-smoke** |
| `UC600-01 ERU-01` | 22 | **W0-smoke** |
| `TR-*` × 6 (VFDs) | 24 each | **W0-smoke** |
| `CSC-03/04/05/06` | 64 each | **W0-smoke** |

Zero of it is live today; the 1,437 flowing sensors are the Nov 2025 VAV load. This is the
highest-value 150 points on the campus and it is already first in the queue — it just needs
running. It unblocks a direct port of the two 1700 Pavilion plant agents onto a **richer**
dataset (both heat exchangers instrumented, native wet-bulb, lead/lag as readable state, and six
*named, metered* VFDs where 1700 has to infer drive identity from run-hour matching).

**Three things to fix during onboarding, not in the agent:**

1. **`TR-* analog-value 6 Power` reads 7360.0 kilowatts** on a fan/pump drive — scaleFactor off
   by 1000, true value approx. 7.36 kW. Check `analog-value 7 Kwatt Counter` (186,289 kWh)
   against the same factor before either is used as an energy basis.
2. **The CSC units report Celsius** while the *identical* Trane BCI-I model at One Summerlin
   reports Fahrenheit, with the same object ids. Set `deviceMeasurementUnit` from the scan's
   `bacnet_units` column per device, never from the model name.
3. **`Outdoor Air Temperature Local` reads −40.001 °C** on CSC-03 — unwired sensor sentinel.
   Drop or annotate so it does not read as an outage.

**Not blocking:** `CSC-01`/`CSC-02` are absent from the scan, behind the panel that has been hung
since 2026-06-23 along with all 71 floor-1/2 VAVs and both smoke-purge controllers. Field fix is
a power-cycle (see the Two Summerlin handover). Add those two units afterwards.
