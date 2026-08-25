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

## 4. Building load — nine months of real data

**Whole building (both meters), kW by hour, PT. One sample week per period.**

```
 hr   Dec wd   we    Apr wd   we    Jun wd   we    Aug wd   we
  0      156  145       146  138       160  143       150  150
  1      150  143       145  138       161  141       150  146
  2      146  139       141  133       155  136       150  145
  3      139  136       140  135       152  135       148  144
  4      136  133       137  132       148  136       148  145
  5      171  134       246  131       469  138       602  148
  6      414  144       574  237       557  331       675  331
  7      731  365       595  352       620  343       696  392
  8      709  371       607  374       726  350       736  464
  9      705  359       625  371       742  366       756  446
 10      711  369       641  392       741  417       765  468
 11      707  366       631  396       727  407       763  475
 12      703  372       622  403       724  407       745  476
 13      697  147       615  261       706  244       753  293
 14      682  134       603  278       703  234       751  284
 15      666  135       593  276       705  236       748  285
 16      665  183       580  278       696  240       736  283
 17      656  193       566  171       676  156       703  226
 18      253  191       258  167       262  156       263  197
 19      210  187       228  165       214  152       215  171
 20      170  138       171  169       181  148       176  150
 21      155  135       155  167       172  141       165  148
 22      150  134       146  132       161  140       162  151
 23      153  134       147  130       163  139       155  149
```

**This is a textbook office profile.** Ramp at 05:00-07:00, plateau 07:00-17:00, sharp drop at
18:00, night baseline by 20:00. **There is no evening rise on weekdays** — see the retraction in
section 6 if you saw the earlier version of this brief.

```
night baseline        ~140-160 kW, stable all year, weekday and weekend
weekday plateau       656-765 kW      weekday daily total  ~11,300 kWh (Aug)
weekend plateau       350-476 kW      weekend daily total  ~6,270 kWh (Aug)
whole building        3,456 MWh/yr · ~9,770 kWh/day average
plant motors          833 kWh/day = 8.8 % of the building
```

**Seasonality is in the morning ramp, not the peak.** 05:00 is 171 kW in December and 602 kW in
August — summer pull-down starts hours earlier. Midday peak barely moves (703 → 745).

### The real signal: weekend daytime operation

Weekends run **350-476 kW from 06:00 to 17:00** against a 145 kW night baseline. The building
keeps a substantial weekend schedule, ramping at 06:00 and holding through midday.

```
excess over baseline    ~200-220 kW (Aug)   ~120 kW (Dec)
per weekend day         ~1,400-2,700 kWh
annualised              roughly 200,000-280,000 kWh  =  $22,000-31,000/yr
```

**Whether that is waste is exactly the open question.** Some tenants may legitimately work
Saturdays and the schedule may be deliberate. This is the number to build the dashboard around,
because the occupancy points settle it: weekend hours in `Bypass` are billed, weekend hours in
plain `Occupied` are not.

⚠️ **February 2026 returns no meter data at all.** Unexplained gap, flagged separately.

**Assumed, not measured:** electricity at **$0.11-0.12/kWh** (Nevada commercial, not from an
invoice — every dollar figure inherits it) and the occupied schedule of roughly **05:00-18:00 PT**
(corroborated by the ramp and the 18:00 collapse, not read from the BAS).

**Suggested mock behaviour:**

- Weekdays: zones Occupied 05:00-18:00, Unoccupied otherwise. Match the load shape above.
- Weekends: a real subset of zones Occupied 06:00-17:00 — this is what the meter shows, so the
  mock should reproduce it rather than assume weekends are dark.
- Bypass events: a handful per tenant per week, mostly 18:00-22:00, duration = that zone's
  `BypassTime` (mix 30 / 60 / 480 so the variation is visible).
- **Seed the two cases the dashboard exists to separate**: weekend zones running with Bypass
  (billed) and weekend zones running without it (waste). The second is the finding.

For a real precedent: at 9950 Woodloch the same class of problem is measured at **$1,715/month** of
weekday-night delivery plus a failed weekend setback worth another $900-1,100/month.

---

## 5. Views worth building

**The headline.** After-hours and weekend hours this month, split Authorised vs Waste, with a cost
on each.

**Weekend view.** Given the finding above, weekends deserve their own panel: which zones run, for
how long, with or without Bypass, by tenant.

**By tenant.** Ranked table — after-hours hours, how many were Bypass, how many were not, estimated
cost, and their `BypassTime` allowance. This is the billing conversation.

**Timeline / heatmap.** Day × hour grid per tenant, coloured by state. Bypass and
unauthorised-Occupied must be instantly distinguishable.

**The exceptions list.** Zones Occupied outside schedule with no Bypass, most recent first. The
actionable list an engineer works through.

Worth surfacing `BypassTime` — a tenant on 480 minutes and a tenant on 30 are having very different
conversations and neither knows it.

---

## 6. What is real and what is not

### Measured — trust it

- The four `OccupancyStatus` states and their numbering, read from live controllers
- `BypassTime` = 30 / 60 / 480 minutes, read from 12 sampled VAVs
- All 291 zones and every tenant name and count in section 3
- **The entire load profile in section 4** — nine months, four seasons, from two Siemens PAC3220
  meters whose combined output reproduces HHC's own GRESB-reported consumption to **101 %**
- All three occupancy objects exist and read cleanly on 12 of 12 controllers sampled

### Assumed — label it in the UI

- **$0.11-0.12/kWh.** Not from an invoice. Any dollar figure inherits this.
- **Occupied schedule 05:00-18:00 PT.** Inferred from the load shape, not read from the BAS.

### Entirely mock — none of it exists yet

- Every occupancy time series. No zone reports `OccupancyStatus` or `BypassTime` today
  (**OTEAM-6837**, 584 sensors).
- Every Bypass event. Not one has been observed.
- Every per-tenant hour or cost.

What the VAVs report today is **`VAV Actuator Position`** and **`UNITOUCH SpaceTemp`**. The other
five onboarded inputs return NaN — they are for a ComSensor/UNITOUCH CO₂-and-humidity accessory
that was never fitted (**OTEAM-6836**).

### ⚠️ Retracted from the earlier version of this brief

An earlier draft claimed weekday load **"comes back up to 353-411 kW at 20:00-23:00"**, worth
~$2,400/month. **That was wrong.** It came from bucketing observations by the connector's log-line
timestamp rather than the observation timestamp; the connector batches, so the two diverge. Same
sensor, same days: 20:00 reads 179 kW by log-line time and 115 kW by observation time. The
observation-time figure matches the API exactly.

Nine months of correctly-bucketed data show **no evening rise in any month**. If you built anything
on that claim, remove it.

### Not yet proven

That the tenant portal drives `Bypass` at all, rather than something in the supervisory layer above
BACnet. The mechanism is confirmed; a live Bypass event has never been seen. If after-hours running
appears with **no Bypass ever recorded**, that is a larger finding — requests never reaching the BMS.

**Design for both outcomes.**

---

## 7. Names to get right

Courtney Holcombe — Director, Office Property Management. Joshua Smith and Joshua Chong — Assistant
Chief Engineers. Gary Hornick — Senior Director, Facilities. The building is **1700 Pavilion**,
Summerlin, Las Vegas.
