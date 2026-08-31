# OTEAM-6846 — FILED 2026-08-31 — https://idun.atlassian.net/browse/OTEAM-6846

# TICKET 1 of 2 — ProptechOS twins (OTEAM)

**Issue type:** Task · **Project:** OTEAM · **Epic:** OTEAM-5539 (One Summerlin)
**Assignee:** Erik Wallin · **Reporter:** Erik Wallin
**Relates to:** OTEAM-6740 (One Summerlin bulk), OTEAM-6739 (Two Summerlin bulk)
**Paired with:** Ticket 2 — the connector-config request to Marichka. Twins without that are silent.

**Title (Summary):**

```
Summerlin cooling agents: create 96 run-state twins + fix storey placement at One Summerlin Bldg J (in-house), and three twin-property fixes to apply when Two Summerlin loads
```

---

> Erik here — built with Claude's help, may have misunderstood something, please don't hesitate
> to challenge me. 🙂

## Why

We are standing up cooling agents on the Summerlin campus. At **One Summerlin Bldg J** the
refrigerant data an agent needs is **already live** — 22 points × 16 Trane self-contained units,
1,425 sensors at the building. Rule v1 kept it by luck, because Trane puts condenser-water and
per-circuit refrigerant temperatures on `analog-input`.

What is missing is the **run state**, which Trane puts on `multi-state-input`. Rather than wait for
the full 15,544-tag load in OTEAM-6740, **we are creating that 96-point subset ourselves.** This
ticket is the record of what we did and the handshake so it is not done twice.

## A · Create 96 Sensor twins — One Summerlin Bldg J (we do this)

Building `623a9f1d-3506-4144-b82b-ad46430e48b3`. Alias prefix
`https://ns.proptechos.com/bacnet/summerlin/`. All 16 device twins already exist — these are
sensors on existing devices, **no new devices**.

16 devices × 6 points:

| Object | Vendor name | `twin_class` | States |
|---|---|---|---|
| `multi-state-input 25 / 26 / 27` | Cool Output 1 / 2 / 3 | Sensor | 3 |
| `multi-state-input 41` | Supply Fan Status | Sensor | 3 |
| `multi-state-input 19` | Application Mode Status | Sensor | — |
| `multi-state-input 35` | Primary Filter Status | Sensor | 3 |

BACnet instances: 723101, 723102, 723104, 723105, 723107, 723108, 723110, 723111, 723113, 723114,
723116, 723117, 723119, 723120, 723122, 723123.

`multi-state-input 28` (Cool Output 4) reads `Not Present` on this profile — skipped deliberately.

Rows and device-twin UUIDs: handoff v5, and `onesummerlin-bldgJ-refrigeration-bindings.csv`.

**Why it matters.** Without run state the agent must derive it from `sign(CondSat − CW leaving)`,
which caps every finding at P2 and forbids P1 entirely. That is the gap behind the 9950 Woodloch
incident — a three-hour-old agent recommended calling a contractor for a chiller that had drawn
**zero power for the whole window**; only run state for the window separated a real precursor from
stagnant barrel water.

## B · Correct storey placement on 24 twins — One Summerlin Bldg J (we do this)

**Defect.** Handoff v5 places every AHU-J unit on `LEVEL 01` or `LEVEL 02`. It read the "J1"/"J2"
in the device name as a floor number.

Instances 723101–723124 run in strict `{AHU-J1-n, AHU-J2-n, FPT-Jn}` triplets, n descending 9 → 2.
**The trailing digit is the FLOOR (2–9); "J1"/"J2" is the RISER** — two self-contained units and one
fan-powered terminal per floor, floors 2 through 9.

```
723101 AHU-J1-9   723102 AHU J2-9   723103 FPT-J9     <- floor 9
723104 AHU J1-8   723105 AHU J2-8   723106 FPT-J8     <- floor 8
   ...
723122 AHU J1-2   723123 AHU-J2-2   723124 FPT-J2     <- floor 2
```

Same class as the Meridian "10 storeys to create" bug (OTEAM-6716) — numbers in device names are
equipment ids, not floor numbers — except inverted: here the floor **is** in the name and was
discarded. **16 AHU + 8 FPT twins to re-place.**

## C · Dedupe — handled on our side, one heads-up for OTEAM-6740

The 96 rows in (A) are inside OTEAM-6740's scope (currently Backlog, not started), so it is worth
being explicit about how we avoid creating them twice. **This does not block anything.**

**On our side — a step in our own script, not a decision for anyone.** The API supports alias
lookup directly:

```
GET /json/sensor?aliases=<comma-separated alias URIs>&alias_ns_ids=e02cfd90-2ddb-40e2-b878-e435948536e9
```

We query the 96 alias URIs first and skip any that already exist. Idempotent by construction, and it
re-runs safely.

**The one heads-up:** after our write, `existing_sensor_twin_id` in handoff v5 is **stale for those
96 rows** — the CSV was built 07/05. `onboard_bacnet.py` checks whether the *building* exists but
does not do a per-sensor alias lookup before creating, so a bulk load driven purely off the stale
CSV column would recreate them. Re-deriving that column against the live model before the bulk run
fixes it — the same dedupe step the Meridian v4 handoff did for all 658 live twins.

**Oksana — no action needed now.** We will regenerate the column after our write and say so on this
ticket, so v5 is correct by the time OTEAM-6740 runs. Flagging it only so it is on the record.

**Open (empirical, we will answer it ourselves):** whether ProptechOS *enforces* alias uniqueness
within a namespace, or whether it is a convention the writer maintains. The convention doc says
site-tags "must be globally unique across HHH PO so aliases don't collide", which reads like a rule
for the writer rather than a database constraint. We will find out on the first write by attempting
one create twice, and record the answer here.

## D · Question: should `analog-output` readings be `Sensor`?

Bldg J's condenser-loop supply and return temperatures live on `AS_2187664` (Schneider SmartX AS-P)
as `CWSTmp` / `CWRTmp` — read 74.25 / 74.89 °F in the July scan.

Both are `analog-output`, so the handoff classes them **`twin_class = Actuator`** — and the
connector playbook records that **actuator twins are not supported by the BACnet connector**. The
`AS_2187664` device twin does not exist either. Created as-is, they would be silent.

They are plainly *readings* — an AS-P publishing a computed loop value outward, not a command.
Classing by BACnet object type alone mislabels them.

**Should these be `Sensor` despite the object type, and does that unblock the connector?** Worth
settling: with them the agent measures the condenser loop directly instead of reconstructing it
from 16 units. This is very likely why the same recommendation in the (unfiled) May RefCalc gap
analysis is still open — it was scoped there as "easy, software-only", and it is not.

Naming note: the May draft calls them `BldgSupTmp`/`BldgRetTmp`; the July v5 scan has
`CWSTmp`/`CWRTmp` on the same device. Same pair, renamed between scans.

## E · Three twin-property fixes to apply when Two Summerlin loads (OTEAM-6739)

Two Summerlin's 480 plant sensors stay with **OTEAM-6739** — we are not doing those in-house.
These three are **twin properties, not connector config**, so they must be right at creation:

1. **`TR-* analog-value 6 Power` reads 7360.0 kilowatts** on a fan/pump drive — `scaleFactor` off by
   1000, true value approx. 7.36 kW. Check `analog-value 7 Kwatt Counter` (186,289 kWh) against the
   same factor before either is used as an energy basis.
2. **The CSC units report Celsius** while the *identical* Trane BCI-I model at One Summerlin reports
   **Fahrenheit**, same object ids. Set `deviceMeasurementUnit` from the scan's `bacnet_units`
   column **per device**, never from the model name.
3. **`Outdoor Air Temperature Local` reads −40.001 °C** on CSC-03 — unwired-sensor sentinel, not a
   measurement. Drop or annotate so it does not read as an outage.

⚠️ **These need to reach whoever actually executes OTEAM-6739.** Linking may not be enough — please
make sure they land.

## F · Aside — the RefCalc gap analysis for these same 16 AHUs has two errors

`jira_NEW_refcalc_gap_analysis_one_summerlin.md` (Drive, One Summerlin, drafted 05/10) was
**apparently never filed**. Before it is filed or discarded, two corrections:

1. It lists `Evaporator Leaving Temperature Circuit N` as **"water-side leaving evap temp"**. It is
   **refrigerant-side** — there are **three per unit**, one per refrigerant circuit; water-side
   would be one per unit. These are self-contained DX units with no evaporator water.
2. It **misses `Condensing Saturated Temperature Circuit 1/2/3` entirely** — not in its coverage
   table at all, though it is on all 16 units (`analog-input 42/43/44`) and **already live**. That
   is the saturated high-side condition: for a pure refrigerant, the same state variable as
   high-side pressure, expressed as a temperature.

**So part of the $25–40k capex that draft scopes for refrigerant pressure transducers may already be
on the wire.** ⚠️ A question, not a conclusion — it depends on (a) whether RefCalc can consume a
saturation temperature in place of `PT_RHP`, and (b) the refrigerant, since a blend with temperature
glide breaks the clean P↔T equivalence. The refrigerant type is not in the scan for these units.
**Worth answering before anyone quotes that number to Gary.**

## Not in scope

**No connector work in this ticket.** Twins are metadata and cost the field bus nothing; the
connector is the only thing that generates BAS load. Until Ticket 2 lands, these 96 twins **will
exist and stay silent** — that is expected, and is the point of "onboard-all, poll-gradual".
