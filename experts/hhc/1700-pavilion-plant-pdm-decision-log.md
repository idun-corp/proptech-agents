# 1700 PAVILION PLANT PdM — DECISION LOG

**This file is never loaded by the agent.** It exists because incident forensics
were accumulating inside the operational prompt, which the agent re-reads on every
model invocation. v0.8.2 reached 58,817 bytes and failed with `Tokens: 0`; the
trail moved here and the prompt went back to 48,287.

Full text of any prior version is in git — `git show <ref>:experts/hhc/1700-pavilion-plant-predictive-maintenance.md`.
Reusable platform facts live in the project memory, not here.

## VERSION HISTORY

```
v0.1   first tick OK (183,601 tok)
v0.2   incident handling + report discipline
v0.3   cut a 400-call bulk pull that had timed out
v0.4   the tool surface is MCP, not the REST endpoints v0.1-v0.3 described, and
       has NO startTime/endTime. Rewritten around the real tools. Rule 1 pinned to
       aggregation=raw: the v0.3 tick ran it on hourly aggregates (5-7 points per
       day-bucket, below the 30-sample guard) because it did not know raw existed.
       Calls cut 37 -> approx 20; long invocations can outlive the runtime's actor
       timeout and return nothing at all.
v0.5   raw is CAPPED AT 1,000 SAMPLES whatever period you ask for, so _7days raw
       returns only about the most recent 1.5 days and Rule 1's 3-weekday test
       cannot run on raw. Rule 1 split: raw for the latest complete weekday,
       hourly for the 7-day shape. Run timing no longer reaches the status light.
v0.6   table output, CALIBRATING is not amber, Rule 6 unblocked
v0.7   FIRST TICK THAT ACTUALLY RAN. The 400 "messages: at least one message is
       required" block cleared. Evaluated 1 of 7 rules — a 401 cascade killed
       every call after approx the ninth.  ref afe7424, 35,678 bytes
v0.8   front-loaded fetch order; abort on first 401; Rule 1 load gate; BLIND status
v0.8.1 abort-on-first-401 made explicit + one-call pre-flight probe
v0.8.2 root cause found (property owner); probe-first recovery replaces abort-fast
       ref aafe498, 58,817 bytes — FAILED with Tokens: 0
v0.8.3 same rules, forensics moved to this file, 48,287 bytes
```

## THE 401 INVESTIGATION — three wrong diagnoses before the right one

Root cause: **the session had the wrong property owner set.** Every 1700 sensor
call was refused until `set-property-owner-id` was called with Howard Hughes
`3edc18ee-9c68-45e5-980c-d2c9bbf66063`. Found by the v0.7 rollback tick, by direct
experiment. Confirmed platform-wide in Slack `#platform` 08/12 — Per Karlberg's
**AFA** agent `9d416bf2-…` had 401'd since **July 1** with its PO set to **Locum**;
Pavlo: *"that is the second time agents have the 'wrong' property owner set…
looks like a problem and not just a human mistake."* Per Pavlo the PO lives in a
**server-side agent-id → PO-id map in the MCP server**, so no prompt can cause it.

The three wrong diagnoses, and why each failed — the pattern matters more than the
answer:

```
1  "token expiry"           tokens do live exactly 3,600 s, but the failures did
                            not track token age
2  "the routine never       killed by v0.7 succeeding at 13:00Z — it demonstrably
    re-mints"               COULD get a token
3  "the prompt edits        correlated PERFECTLY (v0.7 untouched worked, v0.8 and
    broke it"               v0.8.1 re-saved failed) and was pure coincidence
```

⚠️ **Error class, recorded so it is not repeated: rigour on the wrong variable
reads as certainty.** Diagnosis 3 came with bracketed before/after measurements
either side of a failure — genuinely careful work that answered "is the
interactive path alive?" while never varying the thing that had actually changed.
**Before escalating anything, ask "what did we change?" first.**

Erik declined to file a PLAT ticket twice, on the standing rule *"don't bother
PLAT unless we are very certain something broke server-side."* Both refusals were
correct. The real bug surfaced from someone else's better evidence.

Also found: `set-property-owner-id` returned *"Successfully selected property
owner"* while `get-current-property-owner` immediately after still reported the old
value — a set that reports success without persisting. Reported to `#platform`.
And `get-sensor-latest-data` reads across the PO boundary while
`get-sensor-historical-data` and `get-service-objects` enforce it, so PO filtering
is not applied uniformly.

## v0.8.1's ABORT-FAST RULE WAS A MISTAKE

`abort on the first 401` turned a **one-call fix** into three consecutive ⚫ BLIND
ticks. v0.7, which had no such rule, blundered through approximately 100 retries
and **found the cause**. **Fail fast is only correct when the failure is
unrecoverable.** Replaced in v0.8.2 by probe-first recovery, which also logs
whether the PO context was wrong — so the fault stays observable for platform
instead of being silently self-healed.

## THE HX2 "FLOW FAULT" — raised, then retracted

A single snapshot at 06:18 PT showed HX2 energy balance 0.50 against HX1's 1.03,
read as tower-side flow through HX2 running at half the building-side flow.
Tested against the **08/10 weekday peak window** (5 hourly buckets) it **inverts**:

```
                08/10 PEAK WINDOW      06:18 PT snapshot
                  HX1     HX2            HX1     HX2
approach          0.81    2.77           1.95    5.87
tower rise        4.55    5.88           8.04    8.94
building drop     7.45    5.53           8.27    4.43
effectiveness     0.901   0.666          0.81    0.43
energy balance    1.64    0.94           1.03    0.50
```

A real flow fault does not swap exchangers. **The spec already forbade what I
did** — the ANCHOR discipline says the headline figure comes from a complete
weekday peak window, and the alarm was raised from one off-window sample at an
hour no baseline covers. Surviving finding, now the effectiveness baseline seed:
HX2 is stably less effective than HX1 while **both approaches sit at or below
their own baselines** — a fixed characteristic difference, not fouling.

## TOKEN COST — measured, and one wrong inference

```
v0.7    approx 100 calls (401 retries)  21m27s  1,257,179 tok   1 of 7 rules
v0.8     29 calls, all 401               1m45s     81,348 tok   BLIND
v0.8.1    2 calls, probe + retry           19s    103,359 tok   BLIND
v0.8.1    2 calls, identical                9s     35,629 tok   BLIND
v0.8.2    0 calls, model never ran      17m17s          0 tok   Request failed
```

⚠️ I told Erik the v0.8.1 spec growth "cost more than the protocol saved", from the
single 103,359 figure. The next identical tick came in at **35,629** — so that was
an outlier and the protocol saved roughly 55%. **Token-count claims need n > 1.**

**The real lever is fetch payload, not call count.** Raw returns
`{"time":"…","value":x}` per sample at approximately 17 tokens; hourly returns a
dense `values:[…]` array at approximately 1.8. Combined with 1,000 samples vs 25
buckets that is roughly **370× per point-day** — and every payload is re-sent on
each subsequent call, so cost scales with payload × remaining calls. Rule 1's raw
anchor is justified (hourly means are poisoned by the invalid `0.0` readings) but
the load gate only needs "is tower rise above 2.0 °F", which hourly answers.

## THE `Tokens: 0` FAILURE MODE

```
2026-08-12 14:49:30  run -> "Request failed", 17m17s, blank Model, Tokens: 0
```

**The model was never invoked**, so no prompt content can be responsible. Same
signature Erik reported on 08/10: *"All failures show Tokens: 0 and a blank Model…
Durations: 37m51s, then 16m47s / 16m46s / 16m46s"* — Pavlo found **dead letters**
addressed to the agent and suspected the **agenttroupe akka config** treating a
long-unresponsive actor as dead. An agent reset fixed it then; a reset at 14:43:54
on 08/12 did **not**.

Open size correlation, which is why v0.8.3 exists: 35,678 ✅ · 49,800 ✅ ·
**58,817 ❌**. Untested, and worth testing before escalating, because it is our
variable. Note v0.7 ran 21m27s (1,287 s) successfully, longer than the 1,037 s
that failed — so a fixed duration timeout does not explain it on its own.

## STANDING OPEN QUESTIONS FOR PLATFORM

1. Does `set-property-owner-id` write **per agent** or **for the current user**?
   The tool description says *"for the current user"*, which complicates Pavlo's
   agent-id → PO-id map and would be a cross-agent contamination route.
2. Why does a successful-looking `set-property-owner-id` not persist?
3. Is `aggregation: "hourly"` a mean or a median? (Asked 08/10, unanswered. The
   08/05 evidence says mean: the 07:00 PT bucket read 12.33 °F while the loop was
   near 105 °F.)
4. Is there a documented ceiling on invocation duration or tool-call count?
5. Per's proposed sweep: check every autonomous agent, across customers, for
   working state and correct PO — plus whether scheduled triggers disengaged over
   the summer. 1700's routine fires approximately 06:00 PT against a 17:00 PT
   schedule.
