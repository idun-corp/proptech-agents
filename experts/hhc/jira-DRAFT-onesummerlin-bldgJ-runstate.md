# JIRA DRAFT — One Summerlin Bldg J: onboard self-contained unit run-state points

**Project / epic:** OTEAM-5539 "One Summerlin"
**Assignee:** Oksana Koval
**Blocks:** deployment of the Bldg J Refrigeration PdM agent at full confidence
**Size:** ~96 sensors (16 devices × 6 points). Carve-out from OTEAM-6740, not new scope.

## Summary

Onboard six `multi-state-input` points on each of the 16 Trane BCI-I self-contained units at
One Summerlin (Bldg J) so the refrigeration PdM agent has a **vendor-reported run state**
instead of a derived one.

## Why

The Bldg J AHU-J units are water-cooled Vertical Self-Contained machines with three
refrigerant circuits each — 48 circuits on one condenser-water loop. Rule v1 (analog-input
only) already put the entire refrigeration dataset live: condenser water entering/leaving and
per-circuit saturated condensing + evaporator leaving temperatures, 22 points × 16 units.

What rule v1 drops is the **run state**, because Trane puts it on `multi-state-input`.

Without it the agent must derive circuit run state from `sign(CondSat − CW leaving)`. That
derivation is sound and was validated against the vendor state in the 07/05 scan on all three
circuits of AHU-J1-3 — but it is a derivation, so every finding that rests on it is capped at
P2 / Medium confidence and can never escalate to P1.

This is the exact gap that produced the 9950 Woodloch incident: a three-hour-old agent raised
a P2 and recommended calling a contractor for a chiller that had drawn **zero power for the
entire window**. Only run state for the window separated a genuine precursor from stagnant
water. Rule v2 already classes `multi-state-input` as ~95% signal.

## Points to onboard (per device, all 16)

| Object | Name | Use |
|---|---|---|
| `multi-state-input 25` | Cool Output 1 | circuit 1 run state |
| `multi-state-input 26` | Cool Output 2 | circuit 2 run state |
| `multi-state-input 27` | Cool Output 3 | circuit 3 run state |
| `multi-state-input 41` | Supply Fan Status | airflow gate (replaces a duct-static proxy) |
| `multi-state-input 19` | Application Mode Status | Cooling / Heating / Off |
| `multi-state-input 35` | Primary Filter Status | Clean / Dirty — standalone value |

`multi-state-input 28` (Cool Output 4) reads `Not Present` on this profile — skip.

## Devices

BACnet instances 723101, 723102, 723104, 723105, 723107, 723108, 723110, 723111, 723113,
723114, 723116, 723117, 723119, 723120, 723122, 723123.
Building `623a9f1d-3506-4144-b82b-ad46430e48b3`. Alias prefix
`https://ns.proptechos.com/bacnet/summerlin/`. Existing device twin UUIDs are in
`experts/hhc/onesummerlin-bldgJ-refrigeration-bindings.csv`.

## ⚠️ Second defect, same devices — placement is wrong on all 16

The v5 handoff places every AHU-J unit on `LEVEL 01` or `LEVEL 02`. It read the "J1"/"J2" in
the device name as a floor number.

The BACnet instances run 723101–723124 in strict `{AHU-J1-n, AHU-J2-n, FPT-Jn}` triplets with
n descending 9 → 2. **The trailing digit is the FLOOR (2–9); "J1"/"J2" is the RISER.** The
tower has two self-contained units and one fan-powered terminal per floor, floors 2 through 9.

Same class of bug as the Meridian "10 storeys to create" error (OTEAM-6716) — numbers in device
names are equipment ids, not floor numbers — except inverted: here the floor IS in the name and
was discarded. Please correct storey placement for all 16 units and the 8 FPT-Jn terminals in
the same pass.
