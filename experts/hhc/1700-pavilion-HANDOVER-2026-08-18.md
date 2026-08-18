# HANDOVER — HH agents, 08/18/2026

Paste this into a new tab to continue. Repo `proptech-agents`, branch
`chiller_hh`, everything below is committed and pushed. Specs live in
`experts/hhc/`.

## THE STATE OF THE BUILDING (verified live over REST, 08/18 07:50 CEST)

**1700 Pavilion is healthy. Low risk.** Yesterday was the hottest day of the week
and the plant beat its own baseline.

```
Peak OAT 99.8 F   ·   loop held 74.42 F   ·   alarm 85.00
HX1 approach 0.84 F   baseline med 1.11 / p90 1.91
HX2 approach 2.69 F   baseline med 2.75 / p90 5.60
Tower approach 2.71 F   p90 10.78
Night margin 9.07 F   ·   both fault points clean
280 samples · 302 s cadence · 0 gaps -> UNBROKEN since the 08/16 restart
```

Remaining risk is **the feed, not the plant**: PLAT-5706 is still open, so the
connector can wedge again as it did on 08/16 (13.5 h dark, service still
`active`). Recovery is a 3-minute `systemctl restart`.

## WHAT CHANGED TODAY — five specs swept, one new agent

```
1700 Plant PdM              0.8.9  -> 0.8.11
1700 Plant Watch            NEW    -> 0.3      hourly, EMAIL dispatch
1201 Chiller PdM            0.3    -> 0.5
1201 CHW Plant Watch        1.4    -> 1.6
9950 Failure Detection      1.5    -> 1.7
9950 Chiller PdM            0.99   -> 1.01
agent-dispatch-sms.md       0.1    -> 0.2
```

Three sweeps, in order:

1. **ACTIONS-first report format** on every agent. Nothing may precede the header;
   the top block answers "is it fine / must I do something / what changed";
   ACTIONS is never omitted, written `who — what — by when`, addressed to Erik and
   never to the site. **"none today" is stated as the correct answer on a quiet
   plant** — the failure mode is an agent inventing work until the reader stops
   looking. Perennial open items are explicitly NOT actions.
2. **`set-property-owner-id` added to every TOOLS whitelist.** Self-inflicted bug:
   yesterday's STEP 0 mandated the call while the whitelist said "only these two".
   1201 CHW Watch hit it live and reasoned itself out of the fix.
3. **Pavlo's two 08/17 facts** recorded in all five (below).

## THE FIVE THINGS THAT MATTER MOST

1. ⚠️ **Agent RESET does NOT clear a stale property owner.** It is in redis and
   survives redeploys. Erik asked *"will a reset-agent clear that?"* → **"no"**.
   Only `set-property-owner-id` fixes it. Reset stays valid for prompt changes.
2. ⚠️ **Never trust an agent's claim that it set the PO.** Pavlo: check the
   executed-tool section *"to be sure the tool was executed and that agent is not
   just lying"*. `GET /json/autonomousagent/{id}/message/latest` → `usedTools` is
   the only proof. A report line saying "property owner set correctly" is
   narration.
3. ⚠️ **Two gates for any tool.** It must be on the spec whitelist AND enabled in
   the agent's ProptechOS tool config. **The prompt cannot grant access.**
4. ✅ **Dispatch has no syntax to write.** Pavlo 05/13: *"agenttroupe is adding
   message block to a system prompt by itself if there is a dispatch config"*. The
   old "BLOCKING - syntax unpublished" note was a misreading. **Reset is required
   after adding a DispatchConfig** (Pavlo 07/31). Note the inversion against #1.
5. ⚠️ **Dispatch has no known de-duplication.** An hourly agent could email 24x/day
   on one unresolved condition. 1700 produced a 30-SMS flood in 5 h pre-dispatch.
   Dedup is currently the agent's own job — max 1 per 6 h, reading its own
   previous report.

## THE TWO FAILURE MODES, STILL CLEANLY DISTINGUISHABLE

```
401 on every call, fails in ~80 s          -> wrong property owner
Request failed · Tokens: 0 · ~1000 s       -> the 5-min per-request model timeout
```

Eight timeout failures span 964-1041 s (77 s spread). **Possibly relevant and not
yet tested:** v5.6.8 raised the memory compaction trigger from 100k toward ~400k
tokens *"so agents no longer compact mid-run"*. The 1700 PdM runs 200-316k tokens
— right in the old danger band. Worth checking whether the ~1000 s crashes stop.

## OPEN — ERIK

```
🔴 Deploy the specs. Erik holds current copies of 1700 PdM v0.8.11, 1201 PdM
   v0.5, 1201 Watch v1.6. He holds a STALE 9950 PdM (v0.99, now v1.01) and has
   never received 9950 FD v1.7. 1700 Plant Watch v0.3 is new and undeployed.
🔴 Enable set-property-owner-id in each agent's ProptechOS tool config.
   1700 PdM evidently already has it; the four chiller agents may never have.
🟡 Pull usedTools on the last 1700 tick — everything green rests on it.
🟡 Rotate the PEG sudo password (in the 08/17 transcript, does not expire).
🟡 SMS template still says "check chillers" in the live dispatcher. No chillers here.
🟡 Engineers still not SMS recipients. Blocks go-live.
🟡 highCt2 — ask whether the high limit is meant to trip when the plant is off
   overnight. Do NOT build a plain trigger; it would page every night.
```

## OPEN — CLAUDE

```
- 1700 Plant Watch v0.3 has NEVER RUN. Two thresholds unvalidated:
  get-service-objects behaviour in Rule 3, and the cross-tenant temp guard.
- Paired-implausibility guard, deferred. 08/15 sample: supply -2.4 F and return
  +13.1 F in ONE poll, dT 18.47 vs observed max 9.82. Passes both existing guards.
- Ask Pavlo: does dispatch de-duplicate? Is the "logs event" log readable? Is
  there a dry-run? If it dedups, the 6-hour rule can relax.
- v5.6.8 added REC classes we now need: PlateHeatExchanger, HeatExchanger,
  CondenserWaterFlow/Return, Effectiveness, TemperatureDifference. Relevant to
  OTEAM-6786 (Oksana) — the exact classes for this plant now exist.
```

## BLOCKED ON OTHERS

```
PLAT-5706  Pavlo, Highest. PEG has no IP on 4 of 8 subnets; 155 devices dark;
           root cause of the 08/16 wedge. Also gates 17 onboarding items.
OTEAM-6786 Oksana, High. 41 devices + three REC-mapping fixes.
PLAT-5687  Count aggregation. Blocks all silence detection.
Open Q     Is `aggregation: hourly` a mean or a median? Asked 08/10 and 08/12,
           still unanswered, and load-bearing: if median, Rule 1 drops raw
           entirely. Evidence it is a MEAN: the 08/05 outage hour read 12.33 F
           while the loop was near 105 F.
```

## SCHEDULES (all CEST; US and EU clocks diverge 25 Oct - 1 Nov)

```
02:00   1700 Plant PdM            17:00 PT
hourly  1700 Plant Watch          + full report at the 05:00 PT tick = 14:00 CEST
14:00   1201 CHW Watch daily      07:00 CT
14:30   9950 Failure Det. daily   07:30 CT
22:00   1201 Chiller PdM          15:00 CT
22:30   9950 Chiller PdM          15:30 CT
```

⚠️ 1700 Plant Watch's daily lands at 14:00 CEST and collides with 1201 CHW Watch.
Move one by 30 minutes.

## STANDING RULES (Erik's, both proven right repeatedly)

- **Do not bother PLAT unless we are very certain something broke server-side.**
  Four of my diagnoses in one week were wrong; no PLAT ticket was ever warranted
  for the 401s. The recurring error class is *rigour on the wrong variable* —
  careful measurement of something that was not the thing that changed.
- **Do not touch the PEG network config.** *"we should not try to fix it (we will
  then mess up the maintenance of the connectors)"*.
- **A live BAS with a dead feed means the problem is ours, not the building's.**

## KEY FILES

```
experts/hhc/1700-pavilion-plant-predictive-maintenance.md   the trend agent
experts/hhc/1700-pavilion-plant-watch.md                    the new hourly watch
experts/hhc/1700-pavilion-plant-pdm-decision-log.md         why things are as they are
experts/hhc/agent-dispatch-sms.md                           dispatch, v0.2
experts/hhc/1700-pavilion-TODO.md                           shared todo
memory/hhh-1700-pavilion-plant.md · proptechos-agent-platform.md
```
