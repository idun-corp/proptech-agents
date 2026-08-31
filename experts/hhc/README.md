# `hhc/` — Howard Hughes chiller agents (TEMPORARY EXCEPTION)

> ⚠️ **This folder holds customer data. That is a deliberate, temporary exception to the
> repo rule "no customer data in GitHub" — granted 2026-08-01 while the HHH chiller agents
> are under active development. It must not reach `main` unreviewed.**

Everywhere else in this repo, expert agents are **generic and portable** — see
[`../chiller-efficiency-monitor.md`](../chiller-efficiency-monitor.md) for the normal shape:
rule logic with no site, no UUIDs, no customer. The files here are the opposite: they are
site-bound instances carrying live sensor identity, because the two Trane families at these
buildings name the same signal differently and **binding by UUID is the only safe option**
— name-based selection has already caused two onboarding misses at 1201 (see OTEAM-6766 and
the building's site folder on Drive for the write-up).

## What's in here

| File | What it is | Customer data |
|---|---|---|
| `1201-lake-robbins-chw-plant-watch.md` | Deployed v1.3, 1201 Lake Robbins — hourly ops | Full sensor UUID map, building + PO IDs, names |
| `1201-chiller-predictive-maintenance.md` | v0.1 pilot, 1201 Lake Robbins — daily PdM | Full sensor UUID map (largest), building + PO IDs, names |
| `9950-chiller-failure-detection.md` | Deployed v1.4, 9950 Woodloch — hourly ops | Full sensor UUID map, building + PO IDs, names |
| `9950-chiller-predictive-maintenance.md` | v0.98 pilot, 9950 Woodloch — daily PdM | Full sensor UUID map (largest), building + PO IDs, names |
| `1700-pavilion-no-cooling-sms-alert.md` | v1.1 deployed + validated — the 85 °F acute alert | Sensor UUIDs, building + PO IDs, names, **recipient phone/email** |
| `1700-pavilion-no-data-sms-alert.md` | v1.0 deployed, **needs manual reset** — not for engineers | Sensor UUIDs, building + PO IDs, **recipient phone/email**, PEG host |
| `1700-pavilion-plant-predictive-maintenance.md` | v0.8.1, condenser-water plant — daily PdM, never pages | Full sensor UUID map (largest), building + PO IDs, names |
| [1700-pavilion-plant-watch.md](1700-pavilion-plant-watch.md) | 1700 Pavilion | Daily ops watch — freshness, aggregation liveness, alert arming, last night's max. Owns everything answerable from one sample; the PdM owns slopes. **v0.1, not yet run.** |
| `1700-pavilion-daily-manual-check.md` | v0.2, manual daily data-loss backstop | Sensor UUIDs, building ID, **PEG host + SSH user** |
| `onesummerlin-bldgJ-refrigeration-pdm.md` | v0.1 pilot, One Summerlin Bldg J — daily refrigeration PdM over 16 self-contained units / 48 circuits | Full sensor UUID map (256), building + PO IDs, names, BACnet instances |
| `onesummerlin-bldgJ-refrigeration-bindings.csv` | The 256-row binding table the spec's map is generated from | Sensor + device UUIDs, vendor point names, sample values |
| [1700-pavilion-embodied-agent.md](1700-pavilion-embodied-agent.md) | 1700 Pavilion | The **occupied** building, not the plant — zone comfort, schedule behaviour, electricity, and an explicit daily statement of which senses the building does not have. Instantiates `embodied/buidling-base.md`, replacing its CO2/humidity/TVOC/water sections, which have no counterpart here. **Exception-based** — silent unless a rule trips; verdict-first report capped at 20 lines. EMAIL/SMS dispatch on deviation and on request. **v0.4, one live run 08/31** — electricity still unbound | Sensor UUIDs, building + PO IDs, tenant names, **Erik's test email + mobile** |
| `1700-embodied-zone-bindings.csv` | The 286-zone roster behind that spec — temp / damper / occupancy sensor per zone | Sensor UUIDs, tenant names, **BACnet device IPs** |
| `jira-FILED-OTEAM-6846-oteam-summerlin-twins.md` | **OTEAM-6846** (filed 08/31) — ProptechOS twin work: 96 run-state twins + 24 storey fixes in-house at Bldg J, the OTEAM-6740 dedupe contract, Two Summerlin twin-property fixes | Building UUIDs, device instances |
| `onesummerlin-bldgJ-created-2026-08-31.csv` | Manifest of the 48 Cool Output twins created in PROD 08/31 (OTEAM-6846) | Alias, device UUIDs, names |
| `jira-FILED-PLAT-5788-plat-summerlin-connector.md` | **PLAT-5788** (filed 08/31) — PEG connector config for Marichka: Bldg J wave/cadence reorder, run the Two Summerlin W0 batch | Building UUIDs, PEG + connector names |
| `agent-dispatch-sms.md` | Shared reference — how an agent sends SMS/EMAIL/service object (v5.6.3) | None — dispatch never exposes recipients to the LLM |

⚠️ **Three files above now carry more than sensor identity.** `1700-pavilion-no-data-sms-alert.md`
and `1700-pavilion-daily-manual-check.md` contain the **PEG host, port and SSH user**; both
1700 SMS specs contain **recipient phone numbers and the building engineers' mobiles**; and
`1700-pavilion-embodied-agent.md` v0.3 carries **Erik's own email and mobile** as named test
recipients for the dispatch validation runs. That last one is the easiest to clear — the
addresses are documentation of what to enter in the Dispatch UI, not a functional binding, so
deleting the block costs nothing once the config exists and the channels are proven. That is
outside the exception as originally granted below ("Not in here, and must stay out: IP
addresses, hostnames, PEG identities"). **Strip those before this merges** — they belong in the
site folder on Drive. The containment check in step 4 does not catch them.

⚠️ **And two CSVs carry BACnet device IPs.** `1700-zone-remap-FULL.csv` and
`1700-embodied-zone-bindings.csv` both have an `ip` column of RFC1918 addresses on the customer's
own BAS network. Same rule, same fix: strip the column, or move the file to the site folder on
Drive, before this merges. Neither the agent spec nor the remap review needs the IP to work — it
is there because it made the derivation auditable.

**Note also:** this folder is no longer only chiller agents — 1700 Pavilion is a water-side
plant with no chillers. The folder name and the heading above are both stale.

**Not in here, and must stay out:** IP addresses, hostnames, PEG identities, credentials,
bearer tokens, VPN details. Those live in the building's site folder on Drive
(`Onboarding ProptechOS/8. Building discovery/HHH/<site>/`) per the `peg-discovery`
convention. Verified clean as of 2026-08-01 — keep it that way.

## Before this merges to `main`

1. **Move the sensor UUID maps out** of the prompts — to the site folder, or inject them at
   deploy time. Do **not** "sanitise" by switching the prompts to name-based lookup; that
   reintroduces the exact bug the UUID binding exists to prevent.
2. **Generalise what's generalisable.** The rule logic (power-without-cooling, flow-lost,
   purge-trend, surge, oil, thermal, computed approach) is portable and valuable to the
   generic `experts/` set — it is the *identity* that isn't. Consider promoting a generic
   `chiller-fdd-*.md` upward and leaving thin site bindings behind.
3. **Strip building UUIDs, property-owner UUIDs, and customer/building names** from whatever
   remains here, or move the remainder out of the repo entirely.
4. Re-run the containment check:
   ```
   git grep -lE '1201 Lake Robbins|9950|Howard Hughes|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
   ```
   Anything outside `experts/hhc/` is a leak; anything still inside is a decision.

Until then this work stays on the `chiller_hh` branch.
