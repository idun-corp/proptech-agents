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
| `1201-lake-robbins-chw-plant-watch.md` | Deployed v1.2, 1201 Lake Robbins | Full sensor UUID map, building + PO IDs, names |
| `9950-chiller-failure-detection.md` | Deployed v1.4, 9950 Woodloch — hourly ops | Full sensor UUID map, building + PO IDs, names |
| `9950-chiller-predictive-maintenance.md` | v0.98 pilot, 9950 Woodloch — daily PdM | Full sensor UUID map (largest), building + PO IDs, names |

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
