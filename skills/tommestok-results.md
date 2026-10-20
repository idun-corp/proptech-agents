# Tommestok results

Tommestok is ProptechOS's analysis engine. It computes signatures and key figures per
building and writes them back into ProptechOS as ordinary sensors. A result is a
**computed value**, not a measurement (`observationCharacteristics = CalculatedValue`).
Never present one as a live reading.

## 1. The basics: what the observation time means

**A result sensor's observation time is when the analysis last ran.** Its latest value is
the current result, and its history is the run-over-run trend. Use
`get-sensor-latest-data`; the timestamp tells you how fresh the result is. Always state
that age when you use a result.

Exceptions — these sensors are stamped on the period they describe, not on the run:

| Sensor | Stamped on |
|---|---|
| Max Power R12 `…-DAY` | **the peak power day**, 24 values 00:00–23:00 UTC |
| Water `…-WORKDAY_HOURLY_MEDIAN`, `…-NON_WORKDAY_HOURLY_MEDIAN` | the UTC day **before** the run, 24 values 00:00–23:00 UTC |
| Max Power R12 `…-WEEKLY`, Operating Hours `…-HOURS` | Monday 00:00 UTC of each week, one value per week |
| Operating Hours `…-WEEK`, `…-MEDIAN` | the most recent complete UTC week, 168 hourly values |

For the water profiles, the run time is on the scalar water sensors of the same building
(same run, a few hours later than the profile's last stamp).

Other rules:

- **Absent is not zero.** A sensor with no observations has not been computed. Say "not
  computed", never 0.
- **Not found is not "does not exist".** A sensor the agent's access policy hides looks
  exactly like a missing one. Report "not found or not accessible to this agent", with
  the littera you tried.
- A result older than about two run intervals is stale. Say so.
- Units come from the sensor's measurement unit. Do not infer them.

## 2. Finding a result sensor

Every result sensor is named from the **building's littera** plus a fixed tail:

```
sensor littera = {building littera}-{TAIL}
```

The tails per analysis are in section 3. To find a sensor:

1. `get-buildings-by-name` → read the building's `littera` (e.g. `AB1234501`). Never use
   the building name in the sensor littera.
2. Build the sensor littera, e.g. `AB1234501-WATER-DAILY_AVERAGE_M3`.
3. `fetch("<sensor littera>")` → the sensor twin and its `id`.
4. **Check that the returned `littera` equals the one you asked for, character for
   character.** Littera matching is substring-based, so a short building littera can
   match another building's sensor. If it differs, you have the wrong sensor.
5. Use the `id` with `get-sensor-latest-data` or `get-sensor-historical-data`.

Rules:

- **Never look up a result sensor by popular name.** Popular names ("Water Signature -
  Baseload M3H") are identical in every building.
- If the system prompt gives a sensor ID, use it directly and skip the lookup.
- If a building has no littera, the results cannot be found this way. Say so.
- Twins that have been replaced are archived, and lookups return only valid ones. If you
  nevertheless see two sensors with the same littera, use the one with the newest
  observation and mention the duplicate.

## 3. The analyses

`{L}` is the building littera.

### Water signature

How the building normally uses cold water. Typically computed monthly over a ~45-day
window.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-WATER-DAILY_AVERAGE_M3` | m³ | Average daily consumption |
| `{L}-WATER-BASELOAD_M3H` | m³/h | Median flow 02:00–03:59 UTC — what runs when nothing should |
| `{L}-WATER-NIGHT_FLOW_RATIO` | ratio | Mean night flow / mean hourly flow |
| `{L}-WATER-PEAK_TO_AVERAGE_RATIO` | ratio | Highest hour / average hour |
| `{L}-WATER-WEEKDAY_WEEKEND_RATIO` | ratio | Workday consumption / non-workday consumption |
| `{L}-WATER-WORKDAY_HOURLY_MEDIAN` | m³/h × 24 | Profile: typical workday, per hour |
| `{L}-WATER-NON_WORKDAY_HOURLY_MEDIAN` | m³/h × 24 | Profile: weekends and holidays, per hour |

For most questions the five scalar figures are enough. Read the two profiles only when
you must compare measured consumption **hour by hour** with a typical day (section 4).
Quality check: if the signature's daily level (`DAILY_AVERAGE_M3`, or a profile's 24-hour
sum) is far from the building's recent real daily totals, say so before drawing
conclusions.

### Energy signature

How the building's energy use depends on outdoor temperature (a change-point regression).

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-{STREAM}-{MODE}-BASE_LOAD` | kW | Load independent of outdoor temperature |
| `{L}-{STREAM}-{MODE}-WEATHER_SLOPE` | kW/°C | Load change per degree of outdoor temperature |
| `{L}-{STREAM}-{MODE}-BALANCE_POINT` | °C | Outdoor temperature where weather-driven load starts |
| `{L}-{STREAM}-{MODE}-HEATING_SLOPE`, `-HEATING_BALANCE_POINT`, `-COOLING_SLOPE`, `-COOLING_BALANCE_POINT` | kW/°C, °C | Present when the model has separate heating and cooling branches |

- `{STREAM}`: `HEATING`, `COOLING`, `ELECTRICITY`.
- `{MODE}`: `OCCUPIED` (workdays), `UNOCCUPIED` (weekends, holidays, bridge days), `ALL`.
- Which metrics exist depends on the fitted model. **Use what is present; do not assume
  the full set.**
- Each sensor also has a `…-HOURLY` twin (e.g. `{L}-HEATING-OCCUPIED-BASE_LOAD-HOURLY`)
  fitted on hourly instead of daily data. Use the sensor without `-HOURLY` unless asked.
  When matching by keyword, exclude `-HOURLY`.
- Quality check: fit quality is in the sensor's `source` properties (`r2`, `cv-rmse`).
  Always report it. A signature with r² around 0.2 is noise.

### Peak power (Max Power R12)

The highest hourly power over the last 12 months, per stream.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-MAX-POWER-R12-{STREAM}` | kW | Rolling 12-month peak. Replaced by each run (no trend) |
| `{L}-MAX-POWER-R12-{STREAM}-DAY` | kW × 24 | Profile of the peak day, **stamped on that day** |
| `{L}-MAX-POWER-R12-{STREAM}-WEEKLY` | kW | Peak of each closed ISO week, stamped Monday 00:00 UTC |

- **When** the peak occurred: `get-sensor-latest-data` on `-DAY`; the timestamp's date is
  the peak day. That one call is usually enough. Read the day's 24 values (section 4)
  only if the shape of the peak day is needed.
- `-WEEKLY` is the history. Gaps are real (weeks with under 80 % data are not
  published) and never zero. The current week is always absent.
- A building with little history may have `-WEEKLY` but no `{STREAM}` value.

### Indoor climate signature

A **snapshot** of indoor temperature across the building, taken once per run. Tommestok
reads the latest value of every indoor-air temperature sensor in the building, drops
readings that are not fresh, and computes statistics **across sensors** at that moment.
It is not an average over a period: each value describes one moment, and the series of
daily snapshots is the trend.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-INDOOR-MEAN`, `{L}-INDOOR-MEDIAN` | °C | Typical indoor temperature at the snapshot |
| `{L}-INDOOR-P5`, `{L}-INDOOR-P95` | °C | The coldest and warmest 5 % of sensors at the snapshot |
| `{L}-INDOOR-SD` | °C | Room-to-room spread at the snapshot |
| `{L}-INDOOR-N_SENSORS` | count | Number of sensors with a fresh reading at the snapshot |

- The snapshot time is the observation time, so the time of day matters. A snapshot
  taken at night says nothing about afternoon overheating. Compare snapshots taken at
  about the same hour.
- For the trend, read `get-sensor-historical-data` with `aggregation: "raw"` over
  `_30days` or `_90days`: one value per run, so the series is small.
- Temperature only: no CO2 or humidity. No per-room values are published, so the
  signature cannot tell **which** rooms are warm or cold, or for how long.
- Quality check: always report `N_SENSORS`. A figure from a handful of sensors is weak,
  and a sudden drop in `N_SENSORS` means sensors stopped reporting.

### Operating hours

The building's typical weekly operating schedule, derived from its energy pattern.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-OPERATING-HOURS-WEEK` | 0/1 × 168 | Typical week: in operation (1) or not (0), per hour |
| `{L}-OPERATING-HOURS-MEDIAN` | index × 168 | Typical week: relative activity per hour |
| `{L}-OPERATING-HOURS-HOURS` | hours | Operating hours per week, one value per week |

These describe a **typical** week, not observed presence. Each run adds one week, so the
history shows how the schedule changes.

### Pump runtime

Daily runtime per pump or fan, from its runtime counter (or an electricity meter used as a
proxy), and the 30-day share of each duty/standby pair. **One value per complete local day,
stamped at that day's local midnight** (22:00 or 23:00 UTC the day before for
Europe/Stockholm). The newest value is **yesterday**; each run re-states the last three
days. Today is never in the result — for "right now", read the pump's live signals.

`{T}` is the letters and digits of the input counter's littera, e.g. `B52KB21PK1ADT` for
`B52_KB21_PK1A_DT`.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-PUMP-RUNTIME-{T}-RUNTIME` | hours | Hours the pump ran that day (at most the day's length) |
| `{L}-PUMP-RUNTIME-{T}-STUCK` | 1 / 0 | 1 = at least 20 h of readings and no rise: did not run, or the counter is stuck |
| `{L}-PUMP-RUNTIME-{T}-RESETS` | count | Counter resets that day (they contribute nothing) |
| `{L}-PUMP-RUNTIME-{T}-COVERAGE` | hours | Hours of the day with readings |
| `{L}-PUMP-RUNTIME-{T}-LONGEST-STOP` | hours | Longest stop that day |
| `{L}-PUMP-RUNTIME-{TA}-{TB}-PARITY` | % | Pump A's share of the pair's runtime over the 30 days ending that day |

- **STUCK = 1 is not a fault by itself.** A standby pump off all day reads the same. Compare
  with its sister pump and with demand: sister ≈ 24 h and PARITY between about 30 and 70 %
  = normal duty/standby rotation.
- **LONGEST-STOP is absent** where the counter is too coarse to show a stop (e.g. a counter
  in whole hours). Absent is not zero; use RUNTIME instead.
- **PARITY is absent** unless both counters have all 30 days. A is the counter whose
  littera sorts first.
- Low COVERAGE means missing readings: a short RUNTIME on such a day is not a stop.
- For a trend, read `get-sensor-historical-data` on RUNTIME with `aggregation: "raw"`
  over `_7days` or `_30days`: one value per day.

### Simultaneous heating and cooling

Daily hours when a supply unit's heating coil valve and cooling coil valve (or
dehumidification coil valve, as a pair of its own) were open at the same time. Same daily
stamp as pump runtime: newest value = yesterday.

| Sensor littera | Unit | Meaning |
|---|---|---|
| `{L}-SIMULT-HC-{UNIT}-{FAN}[-DEHUM]-{IDS}-HOURS` | hours | Hours both valves were open |
| `…-STARTUP` | hours | The part of HOURS inside the start-up window (04–08 local), **included in** HOURS |
| `…-LONGEST` | hours | Longest continuous stretch |
| `…-COVERAGE` | hours | Hours of the day with readings on both valves |
| `…-OUTDOOR` | °C | Mean outdoor temperature during the simultaneous minutes (absent on a day with none) |

- Start-up hours are usually normal (re-heat while a unit starts); judge HOURS − STARTUP.
- `-DEHUM` pairs (heating + dehumidification) are often intended: dehumidify, then re-heat.

## 4. Profiles and time zones

Profiles are the water hourly medians and the peak power `-DAY` (24 values), and the
operating hours `-WEEK` and `-MEDIAN` (168 values).

**Read a profile only when the task needs the hour-by-hour shape** — comparing measured
hourly data with a typical day, showing when in the day something happens, or drawing the
shape. For key figures, trends, summaries and portfolio overviews, use the scalar
sensors: one `get-sensor-latest-data` call each, instead of a history read per profile.

**Reading the current profile:**

1. `get-sensor-latest-data` → its timestamp falls in the profile's day (or week). Never
   use that single value on its own — it is one hour of a shape that may be old.
2. `get-sensor-historical-data` with `aggregation: "raw"` and the smallest period that
   contains that day (`_30days`, `_90days` or `_365days`). Profiles are sparse, so raw is
   small. An hourly grid over 90 days would be thousands of mostly empty buckets.
3. Take the values on that UTC day (or week), in time order. Everything earlier is an
   older version of the profile; ignore it. Do not group the whole series by date.
4. A profile must be complete (24 or 168 values). If not, the latest write was
   incomplete — use the previous one and say so.

**The index is the UTC hour, not local time.** The value stamped `07:00Z` belongs to the
UTC clock hour 07:00–07:59. In Sweden that is 08:00 local in winter (CET, UTC+1) and
09:00 local in summer (CEST, UTC+2).

```
local hour = (UTC hour + offset) mod 24       offset = +1 in winter, +2 in summer
```

- To compare a profile with a given date, use **that date's** offset, not today's. A
  profile computed in summer applied to a winter day still needs the winter offset.
- Never apply a fixed offset across a daylight-saving change.
- Weekly profiles start Monday 00:00 **UTC**, which is Monday 01:00 or 02:00 local.
- A `0` in a profile may mean that hour had no data.

**Comparing with meter data.** `get-sensor-historical-data` with `aggregation: "hourly"`
returns UTC buckets that start on the hour. Before comparing a meter with a profile, make
sure both refer to the same clock hour. A calculated hourly-sum meter stamps each value a
few minutes after the hour and the value covers the 60 minutes *before* the stamp, so its
bucket `hh:00` holds the consumption of hour `hh−1`. Such a meter already gives volume per
hour — never take differences of it.

## 5. Checklist

1. Building littera → `{L}-{TAIL}` → `fetch` → verify the exact littera.
2. Never popular names.
3. State the age of each result; observation time = last run, except the profiles and
   weekly series in section 1.
4. Scalars first. Profiles only when an hour-by-hour shape is needed: latest stamp → raw
   history for that day → convert UTC hours to local with the offset of the date in
   question.
5. Absent ≠ zero. Not found ≠ does not exist.
6. Daily results (pump runtime, simultaneous heating/cooling) end yesterday; use live
   signals for today.
