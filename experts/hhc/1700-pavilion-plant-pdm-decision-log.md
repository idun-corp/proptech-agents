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

⚠️ **DO NOT read `Tokens: 0` as "the model never ran."** Erik established the
opposite on 08/10, against Pavlo's dead-letter finding: *"zero tokens meant the
response never came back, not that the model never ran. If akka is treating a
long-unresponsive actor as dead, then a long tool sequence is plausibly the
trigger."* I repeated the corrected-away version of this on 08/12 and used it to
argue no prompt content could be responsible — **wrong, and it nearly sent a fourth
unfounded escalation to platform.** Prompt content is always in scope for this
failure mode, because the prompt determines the tool sequence.

**Which versions have ever COMPLETED a full run:**

```
v0.7     full run, fetch-then-analyse per rule    SUCCESS  1287 s, report produced
v0.8     aborted at 29 calls on 401               n/a      never reached fetch phase
v0.8.1   aborted at 2 calls on 401 (x2)           n/a      never reached fetch phase
v0.8.2   full run attempted, FRONT-LOADED         FAIL     1037 s, Tokens 0
v0.8.3   full run attempted, FRONT-LOADED         FAIL     1030 s, Tokens 0
```

**PROMPT EXONERATED 08/12 15:56 — v0.7 redeployed verbatim and FAILED.** The
identical 35,678-byte prompt that produced a full report at 10:26 CEST now fails at
964 s with `Tokens: 0`. Same prompt, same reset procedure, opposite outcome. So
neither the front-loaded fetch design nor the load gate nor size is the cause.

```
  08/10        fail     16m47s    1007s   -            -
  08/10        fail     16m46s    1006s   -            -
  08/10        fail     16m46s    1006s   -            -
  08/12 10:26  SUCCESS  21m27s    1287s   v0.7    35,678
  --- 14:35:57 CEST   Pavlo: "messages are deleted" ---
  08/12 14:49  fail     17m17s    1037s   v0.8.2  58,817
  08/12 15:19  fail     17m10s    1030s   v0.8.3  48,287
  08/12 15:56  fail     16m04s     964s   v0.7    35,678
```

**Every variable we control is now eliminated:** prompt content (same prompt, both
outcomes), prompt size (35 K / 48 K / 59 K all fail), and reset (three resets today,
three failures — whereas on 08/10 a reset *did* fix this signature). Six failures
across two days span 73 s (964–1037), a fixed timeout near 16–17 minutes.

⚠️ **I withdrew the "reset no longer helps" line too early.** It was wrong when the
14:43:54 reset was routine deploy procedure. It is now supportable on different
grounds: three reset-then-invoke cycles on 08/12 all failed, against a reset that
worked on 08/10.

**The only intervening server-side event between the last success and the first
failure is the message deletion at 14:35:57 CEST.** That is now the leading
hypothesis, and this time it rests on a same-prompt A/B across the boundary rather
than on correlation alone.

Same signature as 08/10. Same
signature Erik reported on 08/10: *"All failures show Tokens: 0 and a blank Model…
Durations: 37m51s, then 16m47s / 16m46s / 16m46s"* — Pavlo found **dead letters**
addressed to the agent and suspected the **agenttroupe akka config** treating a
long-unresponsive actor as dead. An agent reset fixed it then; a reset at 14:43:54
on 08/12 did **not**.

**SIZE IS EXONERATED — tested 08/12.** v0.8.3 at 48,287 bytes failed identically
to v0.8.2 at 58,817. A 10 KB reduction changed nothing.

```
run                  dur        sec    prompt bytes
08/10 fail           16m47s    1007      -
08/10 fail           16m46s    1006      -
08/10 fail           16m46s    1006      -
08/12 v0.7 OK        21m27s    1287    35,678
08/12 v0.8.2 fail    17m17s    1037    58,817
08/12 v0.8.3 fail    17m10s    1030    48,287
```

Five failures across two days span **31 seconds** (1006–1037 s) — a fixed timeout,
not variable work. And **the one success ran 1,287 s, longer than every failure**,
so it is not a cap on how long work may take either.

### Erik resets the agent after EVERY prompt change — so reset is a control

This makes the comparison clean, and corrects two things:

```
CONSTANT   agent reset before every run, success and failure alike
VARIED     the prompt only

  v0.7    interleaved,   35,678 b  ->  SUCCESS
  v0.8.2  front-loaded,  58,817 b  ->  FAIL
  v0.8.3  front-loaded,  48,287 b  ->  FAIL
```

With reset held constant and size ruled out, **the prompt is the only variable that
tracks the outcome.** That is the controlled comparison this investigation had been
missing.

⚠️ **The draft escalation's "reset no longer helps" line was a mischaracterisation
— do not send it.** On 08/10 Pavlo used a reset as a *remedy* and it worked. The
14:43:54 reset was routine deploy procedure, not an attempt to fix a broken agent.
Nobody has tried reset-as-remedy on this failure.

⚠️ **It also weakens the message-deletion hypothesis below.** A reset followed the
deletion (14:35:57 -> reset 14:43:54) and the agent still failed, so if reset clears
conversation state then corrupt state from the deletion is not what is breaking it.
Keep the AFA prediction as a cheap check, but rank it below the prompt hypothesis.

### Weakened hypothesis: the message deletion broke the agent's state

```
10:26 CEST  v0.7 tick SUCCEEDS
14:35:57    Pavlo: "messages are deleted"   (hidden endpoint,
            2026-07-01 -> 2026-08-12T09:00Z)
14:43:54    agent reset
14:49:30    invocation FAILS   Tokens: 0
15:19:11    invocation FAILS   Tokens: 0
```

**Every failure is after the deletion; the last success is before it.** The reset
at 14:43:54 came *after* the deletion and did not repair it, which fits state
corrupted in a way a reset does not clear — and on 08/10 a reset *did* fix this
same signature.

**Falsifiable prediction: Per's AFA agent `9d416bf2-…` had its messages deleted in
the same operation, so it should now fail the same way — `Tokens: 0`, blank Model,
approximately 1,030 s.** If it does, the deletion is the cause. If it invokes
normally, this hypothesis is dead and the akka dead-letter theory stands alone.
Cheap to check and it decides the question.

⚠️ Correlation, not proof — server state is not visible from here, and this is the
fourth hypothesis in this investigation. State it as a prediction to test, not a
finding.

## 08/12 EVENING — v0.8.4 CUT THE PAYLOAD 3.2x AND STILL FAILED

Pavlo's diagnosis (5-minute timeout **per HTTP request to the model**, not per run;
`ClaudeAgenticClient .timeout(Duration.ofMinutes(5))`) is the right mechanism for
*a* timeout. His explanation of *why* the round got slow — context inflated by four
raw `_7days` fetches — is now in doubt, because we removed them and nothing changed.

```
              fetched   +spec   peak ctx   result
  v0.7         70.9k    14.0k     84.9k    FAIL 964 s
  v0.8.4       22.5k    14.0k     36.5k    FAIL 992 s
```

**Time-to-first-token on a 36 k-token input should be seconds, not 300.** So either
the request is not reaching the model at all, or the slowness is not context-driven.

### The retry arithmetic fits better than context size

```
failures (s): 1007 1006 1006 1037 1030 964 992
n=7  min 964  max 1037  spread 73 s  mean 1006

3 attempts x 300 s = 900 s  -> residual work +106 s   <- fits
2 attempts x 300 s = 600 s  -> residual +406 s
4 attempts x 300 s = 1200 s -> residual -194 s
```

**Seven failures across two days, two prompt versions and a 3.2x payload
difference, all inside a 73-second band.** Variable context would not cluster that
tightly; a fixed number of fixed-length timeouts would. Working hypothesis:
**initial attempt + 2 SDK retries, each hitting the 300 s ceiling.** Unverified —
ask whether the SDK retries on timeout.

The one success ran **1,287 s**, longer than every failure, with no round crossing
the ceiling.

⚠️ Still unconfirmed: that the v0.8.4 run actually emitted `_1day` raw calls. The
`usedTools` dump settles it and is the only reliable identifier for these runs —
the failing reports print no version, no model, no tokens.

## 08/13 — PLATFORM CONFIRMS THE ROOT CAUSE. WAIT FOR THE FIX.

Pavlo: **the MCP server can confuse property-owner ids.** A request for Howard
Hughes data can go out under another PO (e.g. Dachser) and security correctly
refuses it. He is fixing it; **1–2 days**. The refusal is the system working as
designed — the bug is upstream of it.

### This explains the one thing that never fit

`set-property-owner-id` returned *"Successfully selected property owner"* while
`get-current-property-owner` immediately after still reported the old value. That
is the same confusion. **Consequence: our Step 0 workaround is unreliable** — it
cannot be trusted to set the PO if the layer that records it is the broken one. It
was added to all four chiller specs on 08/13 in good faith; **review it once the fix
lands, and do not treat a "corrected" log line as proof the context is right.**

### It may also be upstream of the 1700 `Tokens: 0` timeout

⚠️ **Hypothesis, unconfirmed — this is the fifth in this investigation, treat it as
such.** PO confusion produces 401s; 401s make the agent retry; retries inflate the
tool sequence and the accumulated context; a later model round then crosses the
5-minute per-request ceiling and the run dies. The v0.7 tick that *succeeded* made
**approximately 100 tool invocations** precisely because it was retrying 401s — so
the mechanism for an inflated run is already demonstrated at this building.

If that holds, **fixing the PO confusion may fix the timeout too**, and every
prompt version we tested was fighting a symptom. What would confirm it: the
`usedTools` dump for the 18:02:30 run showing repeated or 401-ing calls rather than
the clean 16–30 the call plan specifies.

### Posture

**Stop deploying prompt versions until the fix lands.** Each test tick costs
approximately 17 minutes for no information, and testing against a known-broken
dependency is how confounds got introduced all week. Versions are staged and ready:
`v0.8.4` (payload fix) and `v0.9.0-min` (rounds bisection).

What is still worth doing during the wait: get answers to the two design questions
below, because **if `hourly` is a median, Rule 1 drops raw entirely** and payload
stops being a constraint permanently.

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
