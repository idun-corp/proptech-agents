# 1700 Pavilion — after-hours cooling dashboard
### Brief for the session building it. Mock data for now; the real points are being onboarded.

---

## 1. The question the dashboard answers

Courtney Holcombe (Director, Office Property Management, Howard Hughes) wants to know whether the
building is **running extra cooling that nobody asked for and nobody is paying for**.

At 1700 Pavilion, after-hours HVAC is **billable**. Tenants request extended hours through a web
portal and are charged. So every hour of after-hours cooling falls into one of two buckets:

| | |
|---|---|
| **Authorised** | a tenant requested it, it is billed, it is revenue |
| **Waste** | the plant ran outside schedule with no request behind it — pure cost |

**Today we cannot tell these apart.** The dashboard's whole job is to separate them, per tenant,
per day.

---

## 2. The data model

Every zone is served by a Distech ECY-VAV controller carrying a standard occupancy model.

### `OccupancyStatus` — multi-state, 4 values

```
1  Occupied      normal scheduled hours
2  Unoccupied    setback
3  Bypass        <-- AN AFTER-HOURS REQUEST IS ACTIVE
4  Standby       occupied schedule but no presence detected
```

**State 3 = Bypass is the authorised after-hours state.** It is what a portal request (or a wall
button) produces. When it expires the zone falls back to Unoccupied.

### `BypassTime` — how long one request lasts, in minutes

Not uniform. Observed values across the fleet: **30, 60 and 480 minutes**. Some tenants get an
eight-hour extension from a single request; others get half an hour. This matters for cost
attribution and nobody is tracking it today.

### `OccupancyCmd` — on the two AHUs (`device 1300`, `device 1400`)

Same four states. This is the air-handler-level command, above the individual zones.

---

## 3. The 291 zones, by tenant

Zone counts are real — use them so the mock looks like the building.

| zones | tenant |
|---|---|
| 72 | *MECH. ROOM* — not a tenant, see caveat |
| 32 | *TENANT SPACE* — unattributed, see caveat |
| 22 | Snell & Wilmer |
| 15 | Howard Hughes Holdings |
| 12 | Touchstone Living |
| 12 | Bessemer Trust |
| 12 | Wynn Design & Development |
| 11 | PNC Bank |
| 11 | Ghost Beverages |
| 11 | New York Life Insurance |
| 10 | ER Injury Attorneys |
| 9 | Bruin Capital Partners |
| 9 | Clark Hill |
| 8 | The Northern Trust |
| 7 | Hearst Healthcare |
| 6 | Northmarq |
| 5 | Rimini Street · Capital Gurus · Mass Mutual |
| 4 | Malibu Management · The Cirrus Company · TSG Consumer Partners · Edelman Financial |
| 1 | Dr. Snyder Cosmetic Dentistry |

⚠️ **104 of 291 zones (36 %) are not attributed to a named tenant** — 72 sit in "MECH. ROOM" and 32
in "TENANT SPACE". Do not silently fold these into a total that implies full tenant coverage. Show
them as their own bucket; the gap is real and worth surfacing.

---

## 4. Building facts, for realistic mock data

Everything in this section is **measured**, not invented.

```
whole building        3,456 MWh/yr · 9,766 kWh/day
weekday mean          457 kW          weekend mean   348 kW
weekday peak          755 kW at 08:00 PT
weekday minimum       177 kW at 19:00 PT
plant motors          833 kWh/day = 8.8 % of the building
plant run time        ~14 h/day, CT2 lead, CT1 essentially idle
loop supply           ~75 °F, alarms above 85 °F
Las Vegas             OAT 84-106 °F in August
```

**Whole-building kW by hour (PT), measured 20-24 Aug — use this shape:**

```
hr    weekday  weekend        hr    weekday  weekend
00       360      320         12       492      475
01       363      362         13       475      317
02       367      367         14       470      321
03       378      365         15       459      332
04       377      360         16       461      326
05       656      364         17       447      249
06       702      511         18       243      212
07       715      531         19       177      176
08       755      526         20       406      147
09       535      431         21       411      150
10       496      484         22       356      148
11       504      477         23       353      147
```

⚠️ **Look at 20:00-23:00.** Weekdays run 353-411 kW; weekends run 147-150 kW at the same hours.
A ~250 kW delta for four hours every weeknight is roughly **1,000 kWh/night**, order **$2,400/month**
at $0.11/kWh. The building drops to 177 kW at 19:00 and then *comes back up*.

**That is very likely the thing Courtney is asking about, visible in the meter data before any
occupancy point is onboarded.** Treat it as the headline the dashboard should be able to explain -
but note the caveat in section 6: it is five days of data and the cause is not yet established.

**Assumed, not measured:** electricity at **$0.11-0.12/kWh** (Nevada commercial, not taken from an
invoice) and the occupied schedule of roughly **05:00-18:00 PT** (from earlier BAS work, not
re-verified). The 05:00 jump from 377 to 656 kW and the 18:00 collapse to 243 kW both corroborate
that schedule.

**Suggested mock behaviour:**

- Weekdays: zones Occupied 05:00–18:00, Unoccupied otherwise
- Weekends: Unoccupied, with occasional Bypass
- Bypass events: a handful per tenant per week, mostly 18:00–22:00, duration = that zone's
  `BypassTime` (mix 30 / 60 / 480 across tenants so the variation shows)
- **Seed some waste**: a few zones Occupied past 18:00 with no Bypass, and at least one tenant
  where a whole floor stays Occupied all weekend. That is the finding the dashboard exists to
  surface, so it must be visible in the mock.

For a real precedent: at 9950 Woodloch the same class of problem is measured at **$1,715/month**
of weekday-night delivery plus a failed weekend setback worth another $900–1,100/month.

---

## 5. Views worth building

**The headline.** After-hours hours this month split Authorised vs Waste, with a cost on each.
One number the customer cares about: *"you are giving away £X of cooling."*

**By tenant.** Ranked table — after-hours hours, how many were Bypass, how many were not,
estimated cost, and their `BypassTime` allowance. This is the billing conversation.

**Timeline / heatmap.** Day × hour grid per tenant, coloured by state. Bypass and
unauthorised-Occupied should be instantly distinguishable. The eye finds the pattern faster than
a table — a whole weekend running hot shows up immediately.

**The exceptions list.** Zones Occupied outside schedule with no Bypass, most recent first. This
is the actionable list an engineer works through.

Worth showing `BypassTime` prominently somewhere — a tenant on 480 minutes and a tenant on 30 are
having very different conversations, and neither knows it.

---

## 6. What is real and what is not

### Measured today, trust it

- The four `OccupancyStatus` states and their numbering — read from `State_Text` on live controllers
- `BypassTime` = 30 / 60 / 480 minutes — read from 12 sampled VAVs, genuinely varies
- All 291 VAV zones, and every tenant name and zone count in section 3 — from ProptechOS placement
- Every kW figure and the whole hourly profile in section 4 — from two Siemens PAC3220 meters
  whose combined output reproduces HHC's own GRESB-reported consumption to **101 %**
- All three objects exist and read cleanly on 12 of 12 controllers sampled

### Assumed, flag it if the dashboard leans on it

- **$0.11–0.12/kWh.** Nevada commercial rate, not from an invoice. Any dollar figure inherits this.
- **Occupied schedule 05:00–18:00 PT.** From earlier BAS work, not re-verified today — though the
  measured load profile corroborates it closely.

### Entirely mock — none of this exists yet

- **Every occupancy time series.** No zone reports `OccupancyStatus` or `BypassTime` today.
  Tracked as **OTEAM-6837** (584 sensors).
- **Every Bypass event.** Not one has been observed. The mechanism is confirmed to exist; it has
  never been seen firing.
- **Every per-tenant after-hours hour or cost.** There is no per-zone occupancy history to derive
  it from.

What the VAVs actually report today is **`VAV Actuator Position`** and **`UNITOUCH SpaceTemp`** —
two points per controller. The other five onboarded inputs return NaN because they are for a
ComSensor/UNITOUCH CO₂-and-humidity accessory that was never fitted (**OTEAM-6836**).

### Not yet proven

That the tenant portal drives `Bypass` at all, rather than something in the supervisory layer above
BACnet. If, once data flows, after-hours running appears with **no Bypass ever recorded**, that is a
larger finding than the one we expect — it would mean requests never reach the BMS.

**Design for both outcomes.** The dashboard should be equally informative if Bypass never appears.

### The one real signal available now

The 20:00–23:00 weekday-vs-weekend gap in section 4 is measured, not modelled. It is five days of
data and the cause is unestablished — it could be tenants legitimately buying hours, a schedule
that does not release, or a night purge. But it is a real number from real meters, and it is the
only piece of the after-hours story that does not depend on OTEAM-6837 landing first.

## 7. Names to get right

Courtney Holcombe — Director, Office Property Management. Joshua Smith and Joshua Chong — Assistant
Chief Engineers. Gary Hornick — Senior Director, Facilities. The building is **1700 Pavilion**,
Summerlin, Las Vegas.
