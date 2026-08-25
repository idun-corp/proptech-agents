> **Repo note.** This is a snapshot of what is actually DEPLOYED as of 2026-08-25, taken from the
> live agent output in ProptechOS. **Deployed versions drift from this repo** — Plant Watch is
> v0.16 live vs v0.18 here; Tower Staging Watchdog is v0.4 live vs v0.7 here. Do not assume the
> specs in `experts/hhc/` are what is running.

# HHH × ProptechOS — agents in operation
### Handover pack for the deck build · compiled 25 Aug 2026 from live agent output

---

## 1. What is actually running

Eight agents, all on `claude-sonnet-5`, all running unattended in ProptechOS.

| # | Agent | Building | Version | Cadence | Runtime | Tokens/run |
|---|---|---|---|---|---|---|
| 1 | **Plant Watch** | 1700 Pavilion | v0.16 | **hourly** | 3 s | 53.6 k |
| 2 | **Tower Staging Watchdog** (outage precursor) | 1700 Pavilion | v0.4 | daily 06:00 PT | 2–4 min | 177–199 k |
| 3 | **Condenser Water Plant PdM** | 1700 Pavilion | — | daily ~02:00 | 7 m 34 s | 283 k |
| 4 | **Chiller Plant Failure Detection** | 9950 Woodloch | v1.13 | daily | — | — |
| 5 | **Chiller Plant PdM** | 9950 Woodloch | v1.08 (pilot) | daily | — | — |
| 6 | **After-Hours HVAC Runtime Monitor** | 9950 Woodloch | — | periodic (8 runs so far) | 3 m 16 s | 110.7 k |
| 7 | **Cooling-Plant & Comfort Watch** | 9950 Woodloch | — | periodic | 3 m 35 s | 74.5 k |
| 8 | **Chilled Water Plant Watch** | 1201 Lake Robbins | v1.14 | **hourly** | 4–6 s | 101 k |

Plus **three platform alert rules** at 1700 Pavilion (not agents — trigger engine).

> ⚠️ **Deployed versions differ from the git repo.** Plant Watch is v0.16 live vs v0.18 in `proptech-agents`; Tower Watchdog is v0.4 live vs v0.7 in the repo. Do not quote repo version numbers in the deck.

**Cost note if asked:** Plant Watch at hourly × 53.6 k = ~1.3 M tokens/day. The PdM is 283 k for one daily run. These are not free; the hourly cadence is the dominant cost.

---

## 2. The 1700 Pavilion stack, in plain language

Three layers. Worth keeping them distinct on a slide — they answer different questions.

### Layer 1 — SMS alerts (the trigger engine, not agents)

| Trigger | Fires on | Delivery | Status |
|---|---|---|---|
| **1700 No Cooling — CW Supply** | Building loop supply above **85 °F**, evaluated on a **20-minute median** | SMS + email | Live, validated in both directions |
| **1700 Communication error** | Sensor edge status = ERROR | SMS + email | Live; fires on real faults, all-clear unproven |
| **1700 No Data — CW Plant** | Observation sum collapses (liveness proxy) | SMS + email | Live |

**Why the median matters** — this is the single best technical detail for the deck. The raw signal produces occasional `0.0` garbage readings. A *mean* would be dragged down by them and hide a real event; on the morning of the 5 August outage the hourly mean read **12 °F while the loop was at 105 °F**. The 20-minute median is immune, and it has absorbed three separate bad-data incidents since.

**Honest limits, state them:**
- Worst-case detection latency **≈ 40 min** (20-minute window plus up to 20 min to the next block). Do not claim 20.
- Night headroom is only **~2 °F** — the loop reaches 82.98 °F on normal nights against the 85 °F threshold.
- ⚠️ **SMS delivery is unverified.** Email on this path is confirmed working. Test before promising a text.

### Layer 2 — Plant Watch (hourly agent)

Answers *"is the plant healthy right now, and if I can't see it, whose fault is that?"*

Seven rules. The distinctive one is **Rule 7**, which separates two failure modes that look identical from the cloud:

```
plant devices dark + control set FRESH   -> the site's own electrics. Call them.
plant devices dark + control set DARK    -> our connector. Restart it, don't call.
everything dark                          -> PEG or uplink. Ours.
```

The control set is three sensors on a different connector and a different protocol. This rule was **validated against all 7 plant outages** between 11 July and 19 Aug: 2 genuine precursors, 3 contractor reprogramming, 2 ours.

Latest tick: `🟢 1700 Watch v0.16 · 08/25 03:41 PT · faults 2/2 · 9/11 calls`

### Layer 3 — Tower Staging Watchdog (daily, the outage precursor)

Answers *"is the plant heading for the 5 August failure again?"*

Watches whether the **lag cooling tower is being staged**, using the runtime totaliser rather than temperature. It is **calendar-aware** — weekends are gated out, because both towers legitimately sit at zero then.

Latest ticks:
```
08/23 Sun · lead CT2 +13h · lag CT1 +0h · div 5.93 °F · faults 1/1
08/24 Mon · lead CT2 +12h · lag CT1 +0h · div 7.60 °F · faults 1/1
```

Both 🟢. On Sunday it explicitly declined to judge: *"a weekend → Rule 1's WORKING DAY gate applies: lag-zero is NORMAL, no staging judgement made."* That restraint is the point — an earlier version would have fired red every day on a healthy plant.

### Layer 4 — Condenser Water Plant PdM (daily, ~02:00)

Answers *"is anything degrading slowly?"* Seven rules, all load-normalised.

Latest run, 25 Aug 02:07, 37 tool calls, 7 m 34 s:

| Rule | Result |
|---|---|
| 1 · HX fouling | 🟢 both breach p90 but single-tower gated — **not** fouling |
| 2 · Tower approach | 🟢 8.98 °F, below p90 10.78, elevated from CT2-only operation |
| 3 · Runtime | 🟡 **CT1 3rd stop/start cycle in 6 days, still fault-free** → get eyes on CT1 |
| 4 · Night margin | 🟢 79.83 °F, 2.85 °F below weekend-night baseline |
| 5 · Makeup water | 🟡 **totaliser flat at 0.00 for 2 consecutive days** → confirm meter status |
| 6 · Fan energy | ⚪ calibrating, 15.71 kW (CT2 only) |
| 7 · Data quality | 🟢 dead signals unchanged; 5 h gap 08/21 evening, first seen |

**The load-normalisation point is worth a slide line.** The HX approach looked like fouling for weeks — it climbed from 2.0 to 6.5 °F before 5 August. Dividing by load showed the ratio was **flat the whole time**: the approach rose because load per exchanger rose, not because anything was fouling. Five separate findings at this plant have died to that same check.

---

## 3. Findings — what the agents have actually produced

### 1700 Pavilion — live, open

| Finding | Status |
|---|---|
| **CT1 stop/start cycling** — 3rd cycle in 6 days, no fault reported | 🟡 open, needs a physical look |
| **Makeup water totaliser flat at 0.00** for 2 days | 🟡 open — confirmed dead at the controller (see below) |
| **Blowdown water dead** — 0.0 for all 36,437 samples over 30 days | standing instrumentation gap |
| **`runtimecwp1` = `runtimecwp2` = 22,044** — one register mapped twice | standing data defect |
| **CT1 is an unproven spare** — 2,784 run-hours behind, commanded off nearly always | risk, not fault |

I read the water meters **directly at the controller** over BACnet: `Present_Value 0.0`, `Reliability: no-fault-detected`, `Out_Of_Service FALSE`. The controller is healthy and honestly reporting zero — the fault is upstream of it. A pulse input cannot distinguish "no flow" from "dead meter", so the healthy reliability flag proves nothing either way.

### 1700 Pavilion — the 5 August outage, retrospectively

Three independent warnings the stack would now produce:

```
28 Jul          CT1 stops accruing run hours     -> 8 days of lead
04 Aug 00:50    controller dark 5.3 h overnight  -> 29 hours of lead
05 Aug 06:00    loop crosses 85 °F               -> alarm
05 Aug 06:00    a tenant calls                   -> how it was actually found
```

The outage itself: controller offline 01:53, comms restored 06:45, **cooling not restored until 10:15** because the contractor had to rewrite plant programming first. Tenants sent home, 100+ °F outside.

### 9950 Woodloch — the money is here

**After-Hours HVAC Runtime Monitor, eighth consecutive confirming run:**

- Cold air delivered on **every weekday night** across a 30-day window — 168 hours of 18:00–24:00 and 00:00–04:00 delivery
- ~14,300 kWh ≈ **$1,715/month** at $0.12/kWh — *confirmed*
- **The weekend setback has failed.** Three clean ~41–42 h weekend off-blocks (Jul 31, Aug 7, Aug 14) then nothing — the 22–23 Aug weekend ran with zero shutdown. Now seen across three overlapping windows.
- Adds ~$900–1,100/month → **total exposure $2,600–2,800/month ≈ $31–34k/year**

The pattern — works reliably three weeks, then silently fails to trigger — points to an **intermittent fault** (missed schedule trigger or an override left engaged), not a misconfiguration. Needs the BAS team to check control logs for 21–23 Aug specifically.

**Cooling-Plant & Comfort Watch, 25 Aug:**
- 🔴 Chiller_02 — 73 straight hours with zero OFF, still running at time of check
- 🟠 Chiller_04 — ran 97 straight hours, then OFF for 71 h and counting
- The Ch04 shutdown at 22 Aug 07:00 coincides with Ch02's start at 06:00 → **suspected stuck lead/lag rotation**

**Chiller PdM v1.08:**
- 🔴 Chiller_03 motor/CT check requested 20–21 Aug — still not scheduled, now idle 3 straight days
- Ch01 phase-current imbalance 3.52 %, **L3 the low phase on all three occasions it has run** — consistent direction, not noise

### 1201 Lake Robbins
- Chiller **11004 frozen since 07 Aug — 19 days** (PLAT-5715), excluded from evaluation
- Plant otherwise healthy, hourly ticks all 🟢

---

## 4. Savings — ranked, with honest confidence

| # | Measure | Value | Confidence |
|---|---|---|---|
| 1 | **9950 after-hours + weekend setback failure** | **$31–34k/yr** | **High** — 8 consecutive confirming runs, metered |
| 2 | **9950 chilled-water setpoint 4 °F low** | $12–22k/yr | Medium — controller config only, no capital |
| 3 | **1700 tower fans run fixed-speed** | $3,500–5,500/yr | Medium — physics solid, two open questions |

**On #3, the finding is more interesting than the number.** Both 1700 tower fans sit at a **fixed 57 Hz (95 % speed)** whenever they run, controlled by switching on and off. They have variable-speed drives and are being used as soft starters. Sharing load across both towers at part speed does the same cooling for roughly a quarter of the fan energy — but it is only ~1 % of the building, so lead with the capability, not the cash.

Two questions before committing to that number: is the fixed 95 % deliberate (resonance band, vibration)? And can both towers be fed through the existing pumps and isolation valves, or does a second pump have to start and eat the saving?

---

## 5. The measurement story — new as of today

Worth a slide, because it is verifiable and it is ours.

**Two Siemens PAC3220 power meters at 1700 that nobody had read now reproduce HHC's own reported consumption to within 1 %:**

```
GRESB 2025, August (Engie bill):   317,042 kWh
Our two meters, weekday/weekend weighted:  320,160 kWh   -> 101.0 %
```

Whole building is **3,456 MWh/yr**. Plant rotating equipment is **833 kWh/day = 8.8 %** of it, now broken out per drive:

| equipment (inferred) | h/day | kW | speed |
|---|---|---|---|
| Tower 2 fan (lead) | 14.6 | 15.5 | fixed 95 % |
| Tower 1 fan (spare) | 1.1 | 14.2 | fixed 95 % |
| Condenser pump A | 14.4 | 15.7 | modulates |
| Condenser pump B | 14.4 | 15.6 | modulates |
| Building pump (+ standby) | 13.4 | 10.9 | modulates |

> ⚠️ Equipment names are **inferred** from run-hour matching against the plant's own totalisers, not confirmed. The six drives carry factory-default names (`FC-102100001`…) in both ProptechOS and BACnet. Label them "inferred" on any slide.

---

## 6. Do NOT put these in a customer deck

- **Sensor coverage.** 549 of 2,318 sensors on the 1700 PEG published in the last 24 h. 283 of 357 BACnet devices return nothing. Real, being worked (OTEAM-6827/6831/6832, PLAT-5741), but airing it without a fix plan turns a value demo into a mea culpa.
- **Agent dispatch is broken** (PLAT-5754) — the agents' own EMAIL/SMS dispatch does not deliver. Platform alert rules are a separate path and do work.
- **The 403 on service objects** — visible as `alerts N/A(403)` in every Plant Watch tick. AAD permission limit, PLAT-5721, months out.
- **Gary's PTO / the one-person dependency.** True and it is the strongest argument for monitoring, but never in writing to the customer.
- **Anything about our own polling changes** to their equipment.

---

## 7. Three questions to put to Josh

1. Did anyone reset a breaker at the plant early on **4 or 5 August**? Still the missing fact behind the outage.
2. Was anything downloaded to the plant controller around **Friday 21 August**? Both water meters went from 1.19 million to zero inside a six-hour window that night.
3. What drives the **cooling tower setpoint reset** — outdoor dry-bulb, wet-bulb, or load?

---

## 8. Framing line for the deck

> Every failure at 1700 since 5 August has been in our ability to **see** the plant — not in the plant itself.

Two visibility outages (16 and 21 August) are root-caused and fixed. The plant kept cooling through both. The building has not come within 5 °F of its alarm threshold across a week that included two days above 106 °F.
