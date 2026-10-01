# Data needs

Each prompt in `/experts` starts with a `dataNeeds` block: **what data a building must have for the agent to run there.** ProptechOS uses it to show, per building, which agents can run there and which could, and how many buildings each agent covers.

```
---
dataNeeds: {
    "version": 1,
    "need": [ ... ],
    "want": [ ... ],
    "notes": "..."
  }
---

# AGENT TITLE
...
```

The value is JSON, which is also valid YAML, so GitHub renders the block. The prompt starts after the closing `---` and one blank line; the block is not part of the prompt.

## Need and want

- **`need`**: what the agent cannot run without. If any need is unmet, the agent cannot run in that building.
- **`want`**: data that improves the result (context, diagnosis, root cause), but the agent runs without it. A building shows as "can run, 2 of 3 wants".

**Keep requirements as simple and permissive as possible.** A need that is too strict wrongly hides buildings where the agent would work; one that is slightly too loose costs nothing. Most agents have one need.

- A need is only what the agent's classification or core output is computed from. Inputs used only for diagnosis or context are wants.
- Where a Tommestok analysis computes the same thing, offer it as an alternative (`anyOf`).
- Properties of the building model (room area, room type, capacity) are not data needs.
- Do not repeat a need as a want; express "more history" with `history` on the need.

## Requirement

| Field | Meaning |
|---|---|
| `label` | Shown in the UI, e.g. "missing: Room temperature" |
| `kind` | `sensor`, `actuator`, `tommestok` (a Tommestok analysis result) or `external` (data outside the building model, e.g. a booking system; shown, never evaluated) |
| `quantityKind` | QuantityKind IRIs; any one matches |
| `placementContext` | PlacementContext IRIs; any one matches. Omitted when the quantity kind alone is enough |
| `scope` | `building` (default) or `room` |
| `roomType` | RoomType IRIs, narrowing a room-scoped requirement |
| `min` | At least this many matches (default 1) |
| `coverage` | For `room` scope: the share of rooms (0–1) that must have it |
| `all` | `{ quantityKind, placementContext }` entries that must all exist, e.g. supply and return temperature |
| `analysis` | For `tommestok`: `ENERGY_SIGNATURE`, `WATER_CONSUMPTION_SIGNATURE`, `SUPPLY_AIR_FILTER_PREDICTION`, `TIME_IN_OPERATION`, `INDOOR_CLIMATE_SIGNATURE` or `SMART_FUNCTIONS` |
| `system` | For `external`: the system, e.g. "room booking system" |
| `history`, `resolution` | `{ "ideal", "minimum" }` ISO 8601 durations. Part of the schema; not evaluated yet |

A `need` entry may instead be `{ "anyOf": [ ... ] }`: alternatives, any one of which satisfies it.

## Vocabulary

IRIs are full and exact, from the ProptechOS API's `/json/quantitykind`, `/json/placementcontext` and `/json/roomtype` (RealEstateCore terms and ProptechOS extensions). Never invent one. Several terms often mean the same thing (district heating supply is both `.../DistrictHeatingFlow` and `.../PrimaryHeatingFlow`): list all of them. In placement contexts, "Flow" means the flow (supply) pipe, not a flow rate.

Where the vocabulary has no term for something, `notes` says so and the nearest term is used.
