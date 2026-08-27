# 1700 Pavilion — after-hours HVAC dashboard for Courtney

### Brief v4 · 27 Aug 2026. **Occupancy is now live data, not mock.** Supersedes the Tuesday version.

Scope of this document: building the dashboard that answers Courtney's after-hours question. Nothing
else. Plant, chillers, towers and the energy-efficiency work are out of scope here.

---

## 1. The question

Courtney Holcombe (Director, Office Property Management, Howard Hughes) wants to know whether the
building is **running HVAC outside scheduled hours that nobody ordered and nobody is paying for**.

At 1700 Pavilion after-hours HVAC is **billable**. Tenants request extended hours through a web
portal and are charged. Every hour of after-hours conditioning is therefore one of:

**Requests and billing live in Genea** (`portal.getgenea.com`) — Courtney: *"Genea is the system we
use for on demand overtime HVAC."* Erik has portal access as of 25 Aug.

⚠️ **Genea bills on the request, not on what the BMS actually delivered.** Those are two different
systems and **nobody has ever compared them.** That reconciliation is the product:

| Genea says | BMS says | meaning |
|---|---|---|
| ordered | delivered | correct — revenue confirmed |
| ordered | **not delivered** | **the tenant paid for nothing** — credit exposure and a trust problem |
| nothing | delivered | unordered after-hours running — pure cost to HHH |

The middle row is the one that changes the conversation. It is a billing-integrity question, not
just an energy question, and it is the row nobody can currently see.

**The headline number Courtney is asking for is the size of rows 2 and 3.**

---

## 2. What changed since Tuesday — read this first

The Tuesday brief said every occupancy time series was mock and that no zone reported occupancy.
**That is no longer true.** Oksana onboarded the points on 25 Aug and Marichka's connector deploy
started them on **26 Aug 12:18 UTC**. Verified in the cloud on 27 Aug:

```
584 points live   292 OccupancyStatus · 291 BypassTime · 2 AHU OccupancyCmd
observations       ~96/day per point (900 s poll), landing in ProptechOS
zones do release   sampled zones show 1 (Occupied) by day and 2 (Unoccupied) overnight
```

**Build against the real API now.** Mock only what section 7 still lists as mock.

⚠️ **The v3 retraction still stands.** An earlier draft claimed weekday load returns to 353–411 kW
at 20:00–23:00, worth ~$2,400/month. **That was wrong** — it came from bucketing by the connector's
log-line timestamp instead of `observationTime`. Nine months of correctly-bucketed meter data show
no evening rise in any month. If any of it survives in your code, remove it.

---

## 3. The data model

Every zone is a Distech ECY-VAV controller carrying a standard occupancy model.

### `OccupancyStatus` — BACnet `multi-state-value 15`

```
1  Occupied      normal scheduled hours
2  Unoccupied    setback
3  Bypass        <-- AN AFTER-HOURS REQUEST IS ACTIVE. This is the money state.
4  Standby       occupied schedule, no presence detected
```

**Measured distribution — all 272 reporting zones, 18.2 h, 19,241 observations:**

```
1  Occupied     13,786   71.9%
2  Unoccupied    5,163   26.9%
3  Bypass           22    0.1%     one zone only (device 7172, ~5.2 h)
4  Standby           0    NEVER OCCURS
```

**State 4 never fires, and the controllers explain why.** Read directly off 24 VAVs spanning all
eight subnets:

```
MSV 15  OccupancyStatus   Number_Of_States = 4
                          State_Text = ['Occupied','Unoccupied','Bypass','Standby']   <- 16/16 identical
MSV 17  OccDetection      State_Text = ['On','Off','Uncnfg']
                          value = 3 (Uncnfg)                                          <- 23/23 controllers
BI 5014 ComSensor 1 Motion  value = 0                                                 <- 23/23, permanently
```

**Occupancy detection is unconfigured on every controller in the building.** Standby cannot be
entered, so the zero in 19,241 observations is by design, not coincidence. The state names above are
now confirmed from the hardware rather than assumed — use them verbatim.

⚠️ **Treat occupancy here as a schedule, never as a measurement of people.** Anything labelled
"presence" would be fiction: there is no presence input feeding these controllers.

💡 **Footnote, not a recommendation.** The controllers are provisioned for presence-based setback
(`StandbyCoolSP` 78 °F / `StandbyHeatSP` 68 °F against `OccCoolSP` 75 / `OccHeatSP` 71) but the
detection hardware is genuinely absent — the ComSensor accessory's own SpaceTemp and Humidity
inputs read NaN, so it was never fitted. Realising it means **291 new devices plus install and
commissioning in occupied tenant space**. That is a capital project, not a config change, and it
should not be proposed before the two free levers below have been taken.

**The cheap levers come first, and they may capture most of the benefit:**

1. **Fix the 23 zones that never release.** A zone Occupied through the night is a schedule fault.
   Costs nothing, and it is the single clearest waste this data has surfaced.
2. **Tighten the occupied schedule to real hours.** Needs the actual BAS schedule, which we do not
   yet have. Also free.
3. Presence detection only makes sense for zones that are *correctly* scheduled and still empty —
   a different and much smaller population than the 23. Size that population from schedule data
   before anyone prices hardware. A pilot on the worst zones would answer it for a fraction of a
   building-wide fit.

⚠️ Before costing any hardware, ask HHH whether an existing system already knows who is in the
building — access control / badge readers, or the tenant portal itself. Either could give per-tenant
occupancy with no field devices at all.

### `BypassTime` — BACnet `analog-value 47`, **minutes**

How long a single request lasts. Not uniform across the building:

```
30 minutes   162 zones
60 minutes    66 zones
480 minutes   43 zones   <- eight hours from one click
```

⚠️ **The platform stores no unit for this** (`deviceMeasurementUnit` is null) and the value is not
rescaled. Treat the raw number as minutes. A tenant on 480 and a tenant on 30 are having very
different conversations and neither of them knows it — surfacing this is a real finding on its own.

### `OccupancyCmd` — `multi-state-value 1` on AHUs `device 1300` and `device 1400`

Same four states, at air-handler level above the zones. Polls much faster (~1,550 obs/day).

⚠️ **Object-number collision — do not scrape by object ID alone.** The plant controller
(`device 1200`) also carries `analog-value 47`, `multi-state-value 1` and `multi-state-value 15` as
completely unrelated points — its `AV-47` is `cwPumpQty`. **Filter on `popularName` ending in
`/OccupancyStatus`, `/BypassTime`, `/OccupancyCmd`**, never on the BACnet object number. This cost
me a wrong count already.

### Derive these in the app — the platform cannot do it for you

There is **no virtual/calculated sensor in ProptechOS** (`/virtualsensor`, `/calculatedsensor`,
`/derivedsensor` all 404) and **no write path for observations** — `OPTIONS` on
`/sensor/{id}/observations` returns `GET, HEAD, OPTIONS` only. Values enter the platform solely
through the edge ingest from the PEG. A derived point would have to be computed on the PEG and
published as a new BACnet point, which is out of scope and belongs to the connector team.

So derive in the app. Two signals, named for what they actually are:

```python
STATE = {1: "Occupied", 2: "Unoccupied", 3: "Bypass", 4: "Standby"}

def after_hours_request_active(state):
    """A tenant has ordered (and is billed for) extended hours right now."""
    return state == 3

def zone_conditioning(state):
    """The zone is being conditioned. State 4 never occurs at 1700."""
    return state in (1, 3, 4)

def unbilled_after_hours(state, ts_local, schedule):
    """THE headline metric: conditioned outside schedule with no request behind it."""
    return zone_conditioning(state) and not schedule.covers(ts_local) \
           and not after_hours_request_active(state)
```

⚠️ **Do not call any of this "presence" or "occupancy detection".** It is a control mode. Naming it
after people invites every downstream consumer to misread it, and state 4 proves there is no
presence input to justify the name.

⚠️ Interval-weight everything. Observations arrive every ~900 s and are **not** evenly spaced —
compute hours as the gap between consecutive observations, not as `count x 15 min`. Cap any gap at
a sane ceiling so a connector outage doesn't invent hours of Bypass.

---

## 4. How to get the data

### The REST API — use this

```
base    https://proptechos.com/api/json
auth    Authorization: Bearer <token>
⚠️      the WAF rejects default HTTP client agents — send a curl-like User-Agent
```

```http
GET /sensor/{uuid}
GET /sensor/{uuid}/observations?startTime=2026-08-26T00:00:00Z&endTime=2026-08-27T00:00:00Z&size=2000
```

Observations come back paged:

```json
{ "last": false,
  "nextPageToken": "qsGlF-QM...",
  "content": [ { "observationTime": "2026-08-26T20:08:02.067841722Z", "value": 1.0 } ] }
```

⚠️ Bucket by **`observationTime`** (UTC), never by anything else. This is exactly what produced the
retracted finding above. Convert to **America/Los_Angeles** for anything Courtney reads.

At 900 s polling one zone-day is ~96 rows, so a day fits one page comfortably. 292 zones × 1 day is
292 requests — pull day-by-day in parallel (6–8 concurrent is fine) and cache locally. Do not try to
re-query the API on every dashboard render.

**Identifying the sensors:** `popularName` is `device <instance>/OccupancyStatus`, `littera` is the
BACnet object id, `hasSuperDevice` is the VAV twin, and `isMountedInBuildingComponent` is the tenant
zone (section 5).

### The Genea side — the other half of the join

Confirmed from the portal itself (`portal.getgenea.com`, Erik has admin access).

**`Platform Setup > Areas`** is the join table. For 1700 Pavilion it carries:

```
Id | Name (suite) | Building | Tenant | Lease | HVAC Rate | Lighting Only Rate
```

```
20876  Suite 550   Bessemer Trust                    $45.00/h
20877  Suite 300   Bruin Capital Partners            $45.00/h
20878  Suite 420   Capital Gurus                     $45.00/h
20879  Suite 500   Clark Hill                        $45.00/h
38139  1st Level   Conference Room                    $0.00/h   <- common area
20880  Suite 150   Douglas Elliman                   $45.00/h
20881  Suite 310   Dr. Snyder Cosmetic Dentistry     $45.00/h
20882  Suite 350   Edelman Financial Engines         $45.00/h
20883  Suite 530   ER Injury                         $45.00/h
20884  Suite 630A  Ghost Beverages                   $45.00/h
20885  Suite 640   Ghost Beverages                   $45.00/h
20886  Suite 600   Hearst Healthcare                 $45.00/h
20887  Suite 250   Howard Hughes                     $45.00/h
39780  Suite 120   Howard Hughes Mgmt Svcs           $45.00/h
                                          (list continues alphabetically)
```

### 💰 The after-hours rate is **$45.00 per hour**, flat, per area

**Use this, not a kWh estimate, for anything on the billing side.** Lighting-only is $0.00 and the
common-area Conference Room is $0.00. This is the actual tariff a tenant is charged and it makes
every "was this billed correctly" figure exact rather than modelled. The $0.11–0.12/kWh assumption
still applies to the *energy* side (what it costs HHH to deliver) — the two must not be mixed.

**`On-Demand HVAC > Activity History`** is the request log:

```
Building | Tenant | Area | Request Type | Start Date | Start Time | End Date | End Time | Status
```

Request Type is `Recurring` or one-off; Status includes `Cancelled`. **There is an "Export to Excel"
button** — that is the integration path until an API is confirmed. Header tiles show
`Currently Running Requests`, `Completed Requests Today` and `Runtime This Week` (117 h portfolio-wide
at time of writing).

⚠️ **Cancelled instances appear in the log.** A recurring series generates future rows that may later
be cancelled. **Filter on Status before counting anything**, or the billed total will be inflated.

### ⚠️ The join is on tenant name, and it is not clean

Genea `Tenant` ↔ ProptechOS Zone `popularName`. Mostly they match, but:

```
Genea "ER Injury"                 vs   P8S "ER Injury Attorneys"        fuzzy
Genea "Douglas Elliman"           vs   not present in our 22 Zones      missing
Genea Suite 630A + Suite 640      vs   P8S one "Ghost Beverages" Zone   many-to-one
Genea "Conference Room"           vs   common area, no tenant Zone      no join
```

**Build an explicit mapping table, reviewed by hand.** Do not fuzzy-match tenant names silently —
a wrong join puts one tenant's hours on another tenant's invoice. Genea splits by **suite**;
ProptechOS groups by **tenant**, so several Genea areas legitimately collapse to one Zone. And
remember 105 of our 292 zones have no tenant identity at all, so some Genea requests will have
nothing to join to.

⚠️ **The reconciliation window starts 26 Aug 2026.** ProptechOS has no zone occupancy before the
points went live at 12:18 UTC that day. Genea history goes back further, but there is nothing to
compare it against. Do not present a "last 12 months" reconciliation — it cannot exist yet.

⚠️ **Recurring requests matter enormously and will break a naive dashboard.** A tenant can hold a
standing after-hours schedule for weeks — the 26 Aug notification shows one extended from 8/31 to
9/30. In the BMS that looks exactly like "Occupied outside hours", and it is **fully paid for**.
Flagging it as waste would be wrong and would embarrass us in front of the tenant. **The Genea
request list is not optional context; without it the waste number is unsound.**

⚠️ Genea covers **lighting as well as HVAC**. Do not attribute a whole request's cost to HVAC.

**Open:** whether Genea exposes an API or only CSV export. That is the next thing to establish —
everything in row 2 of the table above depends on getting the request list programmatically.
⚠️ The notification seen so far is for **Two Summerlin**, not 1700 Pavilion. Same portfolio and same
system per Courtney, but confirm 1700's requests appear identically before building against it.

### ⚠️ The ProptechOS MCP tools will NOT do this job

Worth knowing before anyone tries:

- **`get-presence-status-for-rooms-in-building`** reports presence as a **binary 1/0 over Rooms**.
  Our points are **multi-state 1–4 attached to Zones**. Even if it did return them, its convention
  is `1 = occupied, 0 = empty`, whereas our `2` means unoccupied — a silent, dangerous mismatch.
- **`get-tenant-unit-by-building-ref`** will enumerate the tenants, but cannot join them to
  occupancy observations.
- **`patch-twin`** only accepts `/popularName`, `/littera`, `/status`, `/source`.

Use the REST API directly. The MCP layer is built for a different question.

---

## 5. The tenant join — how zones map to tenants

Every one of the 292 sensors has `isMountedInBuildingComponent` populated, but it resolves to only
**33 distinct components**. Placement is **per tenant, not per room**.

```
22 Zones  covering 187 VAVs   named after the tenant   <- the billing join, and it works
11 Rooms  covering 105 VAVs   named only "MECH. ROOM" or "TENANT SPACE"
```

| VAVs | tenant |
|---|---|
| 22 | Snell & Wilmer |
| 15 | Howard Hughes Holdings |
| 12 | Touchstone Living |
| 12 | Wynn Design & Development |
| 12 | Bessemer Trust |
| 11 | New York Life Insurance |
| 11 | PNC Bank |
| 11 | Ghost Beverages |
| 10 | ER Injury Attorneys |
| 9 | Bruin Capital Partners · Clark Hill |
| 8 | The Northern Trust |
| 7 | Hearst Healthcare |
| 6 | Northmarq |
| 5 | Capital Gurus · Mass Mutual · Rimini Street |
| 4 | The Cirrus Company · Malibu Management · Edelman Financial · TSG Consumer Partners |
| 1 | Dr. Snyder Cosmetic Dentistry |

⚠️ **105 of 292 VAVs (36 %) have no tenant identity.** They sit in eight separate components all
named `MECH. ROOM` (73 VAVs) and three named `TENANT SPACE` (32). The components are distinct
records with identical names, so they are indistinguishable in any UI. 73 VAVs serving mechanical
rooms is not credible in a 292-zone office building — this is a placeholder for zones nobody mapped.

**Show them as their own bucket. Never fold them into a tenant total.** If after-hours running
concentrates in that bucket, the honest answer to Courtney is "we cannot yet say whose it is", and
that itself is the argument for closing the gap.

⚠️ **There is no floor and no room number.** `isPartOfBuildingComponent` is empty on every component
including the Zones. You can group by tenant. You cannot build a floor plan or a per-room view.

---

## 6. Views to build

**The headline.** After-hours hours this month, split **Authorised (Bypass)** vs **Unbilled**, with
a dollar figure on each. This is the number Courtney opens the page for.

**By tenant.** Ranked table: after-hours hours, how many were Bypass, how many were not, estimated
cost, and that tenant's `BypassTime` allowance. This is the billing conversation, and the allowance
column is the part nobody has seen before.

**Weekend panel.** Weekends run 350–476 kW from 06:00 to 17:00 against a ~145 kW night baseline.

⚠️ **An earlier draft called this ~$22–31k/yr of probable waste. The Genea export shows most of it
is paid for.** Weekend requests account for **678.8 of the 865.9 billable hours** at 1700 —
$30,547 of $38,964. Wynn Design & Development holds a standing recurring booking, Saturdays
08:00–17:00 and Sundays 10:00–17:00, across Suites 900 and 1000.

**The sharper question is margin, not waste.** Wynn pays 2 × $45 = $90/h. Serving two suites means
running central plant for the whole building: the weekend excess of ~200–220 kW over baseline costs
roughly $23–25/h in energy at $0.115/kWh. **So it looks profitable — but nobody has ever checked**,
and that ratio is now computable per booking. Build the panel around margin per request.

⚠️ Do not attribute the whole weekend load to the requesting tenant — base building, lighting and
lifts are inside that 350–476 kW too. Bound the claim.

**Timeline heatmap.** Day × hour grid per tenant, coloured by state. Bypass and
unauthorised-Occupied must be instantly distinguishable — they are the whole point.

**Exceptions list.** Zones Occupied outside schedule with no Bypass, most recent first. The
actionable queue an engineer works through.

### ⭐ "Zones stuck in Occupied" — build this as a permanent panel

The strongest thing in the data so far, and the only finding with a fix that costs nothing.

**23 of 271 zones never report Unoccupied.** Not once in 18 hours, overnight included. Verified
against the controllers at 23:50 local:

```
                        damper position      space temp
23 stuck zones          100.0%  (22 of 22)      75.4 F
25 control zones         44.0%  (0-60% mix)     77.1 F
```

Every stuck zone is pinned wide open against a 75 °F occupied setpoint at midnight, while normal
zones have closed down and drifted to setback.

⚠️ **This is NOT currently burning energy overnight, and the panel must not claim it is.** At the
same moment both AHUs report `OccupancyCmd = 0` and measured `ActFlow` is ~15 across *both* groups —
the air handlers are off, so a wide-open damper delivers nothing. The zones are stuck in the
occupied *mode*, not being actively conditioned.

**It still matters, for three reasons — and the second is the one Courtney cares about:**

1. **Waste whenever the AHU does run.** Any morning warm-up, weekend run, or Bypass-triggered start
   will condition these 23 zones to a 75 °F occupied setpoint with dampers at 100 %, pulling far
   more air than the space needs. The cost is real but intermittent — it must be measured against
   actual AHU runtime, never assumed from damper position alone.
2. **A tenant in one of these zones can be billed for nothing.** Genea bills on the request; the
   zone is already in state 1 permanently, so the request changes nothing and can never even
   register as Bypass. **The tenant pays for conditioning they would have received anyway.** That is
   credit exposure and a trust problem for HHH — the opposite of the lost-revenue reading, and worse.
   These 23 zones are where that failure is *guaranteed* rather than possible.
3. **It is a straightforward configuration fault.** A schedule fix in the BAS, no hardware, no capital.

**How to detect it:** a zone with no state-2 observation across a full night window (00:00–04:00
local) for N consecutive nights. Report zone, tenant, consecutive nights, and — separately —
estimated cost using AHU runtime, not damper position.

⚠️ **Guard against false positives.** Some zones legitimately run 24/7 (server rooms, comms closets).
The panel needs an acknowledge/whitelist action so a known-good zone stops reappearing, otherwise it
becomes noise and gets ignored.

**Why it belongs on the page permanently rather than as a one-off report:** schedule faults
accumulate silently — one zone at a time, after a controller swap or a tenant fit-out — and nothing
in the BAS surfaces them. A standing panel turns an invisible drift into a short weekly work list.

**Zones that never release.** At least one zone (`device 153067`) read Occupied across every sample
in 24 h. A zone that never drops to Unoccupied is continuous unbilled conditioning and is the
cheapest win on the page. Sweep all 292 for this and give it its own panel.

---

## 6b. What the Genea export already tells us (397 rows, Oct 2025 – Sep 2026)

Exported 27 Aug from `On-Demand HVAC > Activity History`. 182 rows are 1700 Pavilion.

### The business, Mar–Aug 2026

```
   619.0 h   $27,856    81 req   Wynn Design & Development      <- 71% of everything
    90.3 h    $4,065    21 req   Snell & Wilmer
    63.0 h    $2,835     9 req   Howard Hughes Mgmt Svcs (Summerlin Gallery)
    48.0 h    $2,160    12 req   MP Mine Operations
    17.0 h      $765    17 req   New York Life                  <- every Monday 18:00–19:00
    15.5 h      $698     3 req   Clark Hill
   (11 more tenants, all under $120 each)
   865.9 h   $38,964   165 req   TOTAL billable
```

**Status matters:** 138 Completed, 27 Early Stop, 17 Cancelled. `Early Stop` is billable and must be
counted at *actual* duration; `Cancelled` must be excluded entirely.

### ⚠️ Reconciliation is not yet possible — there is no overlap

```
last billable 1700 request     24 Aug 2026, 18:00–19:00, New York Life
BMS occupancy data begins      26 Aug 2026, 05:18 PT
overlap                        NONE
```

The only 1700 row on or after 26 Aug is a **cancelled** request for 28 Aug. Wynn's recurring weekend
series appears to have ended after 23 Aug, so **nothing is currently scheduled** to reconcile against.

**This also resolves the single-Bypass mystery.** There were no Genea requests at 1700 during the
18-hour observation window at all — so near-zero Bypass is the *expected* result, not an anomaly. An
earlier draft treated it as evidence that requests were not reaching the BMS. That inference was
unsupported: we were comparing against an empty request list.

### 🎯 A test available this weekend, with no new access

**No Genea request exists for 1700 on Sat 29 or Sun 30 Aug.** If the building still runs its
350–476 kW weekend profile with zones reporting Occupied, that is unordered conditioning — row 3 of
the table in section 1 — measured against a confirmed-empty request list. If instead it stays near
baseline with zones Unoccupied, the weekend load was Wynn's all along and the schedule works.

**Both outcomes are worth having, and both come from data we already collect.**

### The join is built — 25 of 28, and it is good

Full mapping in **`1700-genea-p8s-join.csv`** (Desktop): Genea area id, suite, tenant, $/h, matched
ProptechOS zone, VAV count, paid hours Mar–Aug. **Use this file, do not fuzzy-match at runtime.**

```
Genea lease areas at 1700          28
matched to a ProptechOS zone       25
ProptechOS zones with no Genea area 0     <- every tenant zone is billable
```

**The three unmatched, and what to do with each:**

```
1st Level   Conference Room        $0/h    common area — correctly has no tenant zone, ignore
Suite 150   Douglas Elliman        1.0 h paid    <- MISSING from ProptechOS
Suite 800   MP Mine Operations    48.0 h paid    <- MISSING, and a real user ($2,160)
```

**Those two are almost certainly inside the 105 VAVs parked in `TENANT SPACE` / `MECH. ROOM`.**
That turns the vague "36 % unattributed" problem into a specific, cheap ask: map Suite 150 and
Suite 800. Everything else already reconciles.

⚠️ Genea books by *suite*, ProptechOS groups by *tenant* — Wynn's Suites 900 and 1000 both point at
one 12-VAV Zone, and Ghost Beverages has Suites 630A and 640 against one Zone. **Aggregate Genea
hours to tenant level before joining**, or you will double-count.

⚠️ Every area is **$45/h except the Conference Room at $0**. No per-tenant rate variation to model.

---

## 7. What is real, what is assumed, what is still mock

### Measured — trust it

- **Every occupancy time series.** Live in ProptechOS since 26 Aug 12:18 UTC.
- The four states and their numbering, read from the controllers' `State_Text`.
- `BypassTime` = 30 / 60 / 480 minutes, across all 291 zones.
- The tenant table and all VAV counts in section 5, from the twin graph.
- **The building load profile** — nine months, four seasons, two Siemens PAC3220 meters whose
  combined output reproduces HHC's own GRESB-reported consumption to **101 %**.

### Assumed — label it in the UI

- **$0.11–0.12/kWh** for the *energy* side (what delivery costs HHH). Nevada commercial, **not** from
  an invoice. The *billing* side is exact — $45.00/h from Genea — and the two must never be mixed.
- **Occupied schedule ~05:00–18:00 PT.** Inferred from the load shape, not read from the BAS.
  Getting the real schedule out of the BAS would firm up every "outside schedule" number.

### Still mock or absent

- **Billing records.** We have no portal data, so we cannot yet prove a Bypass was actually invoiced
  — only that the zone entered Bypass. Model the billing side.

### ⚠️ First real result — and it reframes the whole dashboard

Sweeping all 292 zones over the 18.2 h since they started:

```
zones that used Bypass at all        1 of 271     device 7172, ~5.2 h
zones that NEVER released            23 of 271    Occupied straight through the night
zones that behaved as scheduled     248 of 271
```

**23 zones are conditioned around the clock and essentially none of the building's after-hours
running goes through Bypass.** That is the larger of the two outcomes section 7 warned about: either
tenants are not using the portal, or **portal requests are not reaching the BMS at all**. Build the
"no Bypass ever recorded" case as a first-class view, not an edge case — right now it is the norm.

⚠️ **This is 18.2 hours — one weekday night, all the data that exists.** One day proves very little
about a billing pattern and some of those 23 zones may have a legitimately continuous schedule.
Treat it as the shape of the answer, not the answer. It needs a week.
- **20 zones** of the 292 are not publishing (their controllers are alive but the connector is not
  polling them — 21 devices in total, being raised with the connector team). Show as "no data",
  not as zero.

### Not yet proven — design for both outcomes

That Genea actually drives `Bypass`, rather than acting on the supervisory layer above BACnet — or
on nothing at all. One live Bypass has been observed, so the state is real and reachable. But only
**one zone in the entire building** has ever entered it, which is hard to square with a portfolio
that runs on-demand overtime HVAC as a paid service.

**If Genea requests are being billed while the BMS shows no corresponding Bypass, that is the
finding** — bigger than waste, and it points at reconciliation rather than efficiency. Get the
Genea request list for a few known dates and check them against zone state first; it is the fastest
way to establish which world we are in.

---

## 8. Open questions worth putting to Howard Hughes

1. **Genea request export for 1700** — portal access is granted; what is needed now is the request
   list (tenant, area, start, end, recurring flag) in a form we can join. API or CSV, either works.
2. **The real occupied schedule** from the BAS, per zone or per AHU.
3. **The after-hours tariff** — what a tenant is actually charged per hour.
4. **Who owns the 105 unattributed zones**, and why 73 are labelled MECH. ROOM.

---

## 9. Names to get right

**Courtney Holcombe** — Director, Office Property Management. **Joshua Smith** and **Joshua Chong** —
Assistant Chief Engineers. **Gary Hornick** — Senior Director, Facilities.
The building is **1700 Pavilion**, Summerlin, Las Vegas.
