# PLAT-5788 — FILED 2026-08-31 — https://idun.atlassian.net/browse/PLAT-5788

# TICKET 2 of 2 — PEG connector config (PLAT → Marichka)

**Issue type:** Task · **Project:** PLAT · **Epic:** OTEAM-5539 / OTEAM-5554
**Assignee:** Marichka
**Relates to:** PLAT-5581 (One Summerlin staged rollout), PLAT-5580 (Two Summerlin staged rollout)
**Blocked by:** Ticket 1 (twins must exist before the device-config regen picks them up)

**Title (Summary):**

```
Summerlin connector config: pull 84 Bldg J run-state rows W2 -> W1 and re-tier 48 rows to 60s, and run the Two Summerlin W0 batch that has never executed
```

---

> Erik here — built with Claude's help, may have misunderstood something, please don't hesitate to
> challenge me. 🙂

Two connector asks on the Summerlin campus, both **inside work already batched**. No new scope.
The twins side is Ticket 1; this is the half that actually makes them stream.

---

## A · One Summerlin Bldg J (PEG HHHEG-002, connector `multi-bacnet-8ecb8864-…`)

We are running a refrigeration PdM agent on the 16 Trane self-contained units, MS/TP **trunk 7231**.
Two sequencing problems in the current wave plan.

### A1 — the run-state points land one wave AFTER the data they gate

| Point | Object | Wave | Poll |
|---|---|---|---|
| Condensing Saturated Temp Circuit 1–3 | `analog-input 42/43/44` | **W1** | 900s |
| Evaporator Leaving Temp Circuit 1–3 | `analog-input 38/39/40` | **W1** | 60s |
| Condenser Water Entering / Leaving | `analog-input 35/46` | **W1** | 60s |
| Mixed Air / Discharge Air Temp | `analog-input 25/24` | **W1** | 300s |
| **Cool Output 1–3** | `multi-state-input 25/26/27` | **W2** | 900s |
| **Supply Fan Status** | `multi-state-input 41` | **W2** | 300s |
| **Application Mode Status** | `multi-state-input 19` | **W2** | 300s |
| **Primary Filter Status** | `multi-state-input 35` | **W2** | 300s |

2 of the 16 units sit in W0-smoke for all of the above; the other 14 split W1 / W2 as shown —
so **84 rows are in W2**.

Without run state the agent derives it from `sign(CondSat − CW leaving)`, which caps every finding
at P2 and forbids P1. This is the gap behind the 9950 Woodloch incident: a three-hour-old agent
recommended calling a contractor for a chiller that had drawn **zero power for the whole window**.
Only run state for the window separated a real precursor from stagnant water.

**Ask: pull the 84 W2 rows into W1**, so the gate arrives with the data it gates.

### A2 — the two halves of one calculation are tiered 15× apart

Condenser approach is `CondSat − CW leaving`. `CondSat` is proposed at **900s**, `CW leaving` at
**60s**. Per the tier table in the connector playbook, compressor-circuit temperatures belong in the
**1-min** tier — the saturated condensing temps look mis-tiered. (Per-tag polling rates landed with
**PLAT-5554**, closed Done 2026-08-01, so the connector supports this.)

**Ask: 60s for `analog-input 42/43/44`** (48 rows). Tolerable for a daily PdM either way; raising it
because it will bite anything hourly.

### A3 — load

Trunk 7231 polls **388 objects across 36 devices today**; full-keep for that trunk is 1,616. Adding
the 96 run-state rows takes it to **484, +24.7%**.

**Please confirm against the measured cycle** from `/opt/proptechos/<connector>/log/log.log` rather
than my arithmetic — the playbook is explicit that headroom is measured, not projected.

### A4 — two notes on this PEG specifically

- A connector restart briefly drops **all 22 campus buildings**, not just Bldg J. Worth timing.
- ⚠️ **The watchdog on HHHEG-002 has been stopped and disabled since 2026-07-05**, deliberately,
  because of the PLAT-5578 restart storm — and the One Summerlin handover still says *"do NOT start
  it"*. **PLAT-5578 was closed Done on 2026-07-30.** If the fix is deployed on this PEG, that
  standing instruction is stale and the watchdog has been off for two months for no reason.

  This is not a theoretical risk: 1700 Pavilion lost a whole building for **6 hours** at its first
  reboot in 73 days because connector auto-start had silently lapsed. The Bldg J connector was
  `systemctl enable`d on 07-05, so boot recovery is covered — but runtime crash recovery is still
  only `Restart=on-failure` (approx. 5 retries) without the watchdog.

  **Marichka — is the PLAT-5578 fix on HHHEG-002, and can the watchdog go back on?** Worth doing in
  the same visit as the config regen rather than as a separate intervention.

---

## B · Two Summerlin (PEG HHHEG-003, connector `multi-bacnet-2916c482-…`) — never executed

**The entire mechanical plant is already batched W0-smoke and none of it has ever run.** 480 sensors
across 15 devices in `twosummerlin_connector_manifest.csv`:

| Device | Points | Wave |
|---|---|---|
| `UC600-02 CW Plant` | 53 | W0-smoke |
| `UC600-01 ERU-01` | 22 | W0-smoke |
| `TR-*` × 6 (VFDs) | 24 each | W0-smoke |
| `CSC-03/04/05/06` | 64 each | W0-smoke |

Zero of it is live — the 1,437 sensors currently flowing are the Nov 2025 VAV load.

**This is the highest-value 480 points on the campus and it is already first in the queue.** It
unblocks a direct port of both 1700 Pavilion plant agents onto a **richer** dataset: both plate heat
exchangers instrumented, native outdoor wet-bulb and a computed tower approach, lead/lag as directly
readable state, and **six named, metered VFDs** — where at 1700 the drives carry factory-default
names and we had to infer drive identity by matching run-hours against plant totalisers (every
energy figure in that customer deck is labelled "inferred" for exactly this reason).

**Ask: run the W0 batch.** Twin creation is OTEAM-6739 — Ticket 1 §E carries three twin-property
fixes that must be right at creation (`TR-*` power scaleFactor off by 1000, °C vs °F per device, a
−40 sentinel).

**Not blocking:** `CSC-01` / `CSC-02` are absent from the scan — they sit behind the panel hung
since 2026-06-23, along with all 71 floor-1/2 VAVs and both smoke-purge controllers. Field fix is a
power-cycle (see the Two Summerlin handover). Add those two units afterwards.
