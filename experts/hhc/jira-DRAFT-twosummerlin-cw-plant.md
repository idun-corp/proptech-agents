# JIRA DRAFT — Two Summerlin: onboard the condenser-water plant + VFDs

**Project / epic:** OTEAM-5539 (or the Two Summerlin epic if one exists)
**Assignee:** Oksana Koval
**Blocks:** Two Summerlin tower-staging watchdog + CW plant PdM (ports of the 1700 Pavilion pair)
**Size:** ~150 sensors. Carve-out from the 12,098-row `twosummerlin_handoff_v3_cadence.csv`.

## Summary

Onboard 3 devices — 53 + 22 points and 6 VFDs × 24 points — from the existing Two Summerlin
handoff, ahead of the VAV bulk. These are the entire mechanical plant and **none of it is
live**: the 1,437 sensors currently flowing are the Nov 2025 VAV load.

## Why this jumps the queue

Two Summerlin's `UC600-02 CW Plant` is a **more complete version of the 1700 Pavilion plant**,
where we already run a tower-staging watchdog and a CW plant PdM in production. 1700's stack
caught the 08/05 outage precursor eight days early. The rules port with the sensor map swapped.

Where Two Summerlin is strictly better than 1700:

- **Both plate heat exchangers fully instrumented** — HX-01 and HX-02, tower water in/out AND
  building water in/out. 1700 has one HX pair and we had to reason around it.
- **`Outdoor Air Wetbulb` and `Outdoor Air Dewpoint` are computed on the controller.** Tower
  approach against wet-bulb is the textbook tower-degradation signal; at 1700 we do not have it.
- **`Cooling Tower Approach Temperature` is a native point** (read 7.0 °F at scan).
- **Lead/lag rotation is exposed as state** — `Building Water Pump Lead`, `Tower Water Pump Lead`,
  `Tower Fan Lead`, plus rotation day and 24 h rotation time. At 9950 a suspected stuck lead/lag
  rotation had to be inferred from run-hour patterns; here it is a directly readable point.
- **Six named, metered VFDs.** At 1700 the six drives carry factory-default names
  (`FC-102100001`…) and we had to *infer* which drive was which by matching run-hours against
  plant totalisers — every energy figure in that deck is labelled "inferred". Here the drives
  report Motor Current, Power, kWh counter, Heatsink Temp, Torque, Motor Thermal and Inverter
  Thermal, and the plant they belong to is unambiguous.

## Devices to onboard

| Device | Instance / model | Points | What it is |
|---|---|---|---|
| `UC600-02 CW Plant` | Trane UC600 | 53 | 2 towers, 2 tower pumps, 2 building pumps, 2 HX, wet-bulb, approach, lead/lag, all setpoints |
| `UC600-01 ERU-01` | Trane UC600 | 22 | energy recovery unit — supply/return static, filter DPs, fan speeds |
| `TR-2001002102/03/04/05/06`, `TR-2001012101` | Trane TR200 | 24 each | the six drives |

Building `1fe2668e-c7a5-46d8-95e0-ad9ada141bf3`. Rows are already REC-encoded in
`raw/scan-2026-06-29/twosummerlin_handoff_v3_cadence.csv` — filter on `device_name`.

## ⚠️ Fix at onboarding, not in the agent

1. **`TR-* analog-value 6 Power` reads 7360.0 kilowatts** on a fan/pump drive. The scale factor
   is off by 1000 — the true value is approx. 7.36 kW. `analog-value 7 Kwatt Counter` (186,289
   kWh) should be checked against the same factor before either is trusted as an energy basis.
2. **The CSC units report Celsius** while the *identical* Trane BCI-I model at One Summerlin
   reports Fahrenheit, with the same object ids. Set `deviceMeasurementUnit` from the scan's
   `bacnet_units` column per device — never from the model name.
3. **`Outdoor Air Temperature Local` reads −40.001 °C** on CSC-03 (unwired sensor sentinel).
   Either drop it or annotate it so it does not look like an outage.

## Related, not blocking

`CSC-01` and `CSC-02` are absent from the scan because they sit behind panel **SC-03**
, hung since 2026-06-23 along with all 71 floor-1/2 VAVs and the two UC400
smoke-purge controllers. Field fix is a power-cycle of SC-03 (see the Two Summerlin handover).
Those two units can be added once the panel is back — they are not a reason to hold this ticket.
