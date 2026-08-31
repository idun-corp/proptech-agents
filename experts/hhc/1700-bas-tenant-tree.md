# 1700 Pavilion — BAS (Niagara) tenant/suite mapping
Sources: Nav-tree screenshots + **oBIX exports** (Drive folder `Obix 2026-08-31`,
`https://drive.google.com/drive/folders/1iQsPyneueaNbNmGwEI9Kgx0mjUgIEJHT`), read 31 Aug 2026.
Path: `/Drivers/BcpBacnetNetwork/<floor>/<tenantFolder>/<vav>`

⚠️ **The oBIX "Object to oBIX" exporter is ONE LEVEL DEEP.** Tenant folders come out as `<ref>`
pointers, not expanded. To get the VAVs inside a tenant, export (or expand) that folder itself.

## Suite <-> tenant, authoritative
Floor 3's folders are named by SUITE with the tenant in `displayName` — the cleanest evidence:
```
Suite300 = Bruin Capital      Suite310 = Snyder Dental     Suite315 = Cirrus Company
Suite320 = Mass Mutual Fin.   Suite330 = Rimini Street     Suite350 = Edelman Financial
```
All six match Genea's Areas export exactly.

## Per floor

```
FLOOR 1  devices: exh_cav1_1/2, osa_cav1_3, vav1_04,06,07*,08*,09,10,11,12,13,14*,15*,16*,22
         folders: [DouglasElliman] -> VAV_1_17..21        (from screenshot)
                  [SummerlinSales1] -> vav1_05, vav1_23   (from screenshot)  = Genea Suite 120
FLOOR 2  devices: exh_cav2_1/2, osa_cav2_3, vav2_4*, vav2_5
         folders: [HowardHughes] [TSGConsumer] [Suite260]           CONTENTS UNKNOWN
FLOOR 3  devices: exh_cav3_1/2, osa_cav3_3, vav3_4, vav3_5, vav3_9
         folders: [Suite300][Suite310][Suite315][Suite320][Suite330][Suite350]  CONTENTS UNKNOWN
FLOOR 4  devices: exh_cav4_2*, osa_cav4_3
         folders: [CapitalGurus][New_York_Life][Northmarq][PNC_Bank]  CONTENTS UNKNOWN
FLOOR 5  devices: exh_cav5_1*, exh_cav5_2*, osa_cav5_3*, vav5_4*, vav5_5*
         folders: [Suite 500] -> vav_500_5_1..10      (screenshot)
                  [Bessemer Trust] -> vav5_1..13      (screenshot)
                  [ER Injury] -> vav-5-1..12          (screenshot)
FLOOR 6  devices: exh_cav6_1/2, osa_cav6_3, vav_14, vav_15
         folders: [Ghost_Lifestyle][Hearst_Health][Northern_Trust][Malibu]  CONTENTS UNKNOWN
FLOOR 7  devices: exh_cav7_1*, exh_cav7_2*, osa_cav7_3*
         folders: [Snell_Wilmer] = the entire floor    CONTENTS UNKNOWN
FLOOR 8  vav_MP_8_01..34   = MP Materials = Genea Suite 800 (MP Mine Operations)
FLOOR 9  vav_Wynn_9_1..13  = Wynn Suite 900 · vav9_4..9 · [TouchstoneLiving] CONTENTS UNKNOWN
FLOOR 10 vav_Wynn_10_1..34 = Wynn Suite 1000 · vav10_5
```
`*` = `status="down"` in the BAS at export time — an independent check on our silent devices.

## ⚠️ Floor 5 collision
`vav5_3` (Bessemer Trust) and `vav-5-3` (ER Injury) are DIFFERENT boxes. BACnet renders both as
"VAV 5-3", so these two tenants cannot be separated from BACnet data alone, and some of the 187
already-mapped ProptechOS zones may be crossed.

## Join key
BAS `vav_Wynn_10_19` == BACnet Object_Name "Wynn VAV 10-19" == ProptechOS `device 169`
BAS `vav1_05`        == BACnet desc "VAV 1-5"              == `device 10105`
Floor + unit, plus the tenant prefix where present.

## STILL NEEDED — 6 tenant folders' contents
floors 2, 3, 4, 6, 7 and TouchstoneLiving on 9.
Either expand them in the Nav tree and screenshot, or right-click each folder ->
Export -> "Object to oBIX" (⚠️ writes to the REMOTE Windows machine).

---

# ProptechOS vs the BAS — the mapping is wrong for almost every tenant

Full BAS VAV lists per tenant are in `1700-bas-tenant-vav-map.json`.

```
BAS tenant folder             BAS   P8S   verdict
MP Materials  (Suite 800)      34     -   *** NO ProptechOS ZONE ***
Wynn Suite 1000                34    12   both Wynn suites share ONE zone of 12
Wynn Suite 900                 13    12       -> 47 BAS VAVs vs 12 in ProptechOS
Snell & Wilmer                 22    22   OK
Howard Hughes (Suite 250)      18    15   +3
Touchstone Living              14    12   +2
New York Life                  13    11   +2
Bessemer Trust                 13    12   +1
ER Injury                      12    10   +2
Ghost Lifestyle                12    11   +1
PNC Bank                       10    11   -1
Suite 500                      10     -   *** NO ZONE ***
Northern Trust                 10     8   +2
Bruin Capital (Suite 300)       9     9   OK
Hearst Health                   8     7   +1
Rimini Street (Suite 330)       6     5   +1
Northmarq                       6     6   OK
Malibu                          6     4   +2
Douglas Elliman (Suite 150)     5     -   *** NO ZONE ***
Mass Mutual (Suite 320)         5     5   OK
Capital Gurus                   5     5   OK
Cirrus Company (Suite 315)      4     4   OK
Edelman Financial (Suite 350)   4     4   OK
Summerlin Sales (Suite 120)     2     -   *** NO ZONE ***
Snyder Dental (Suite 310)       2     1   +1
```

**Only 7 of 25 tenants match.** Six have no ProptechOS zone at all. Most others are under by 1-3.

## 🔴 The big one: Wynn has 12 of 47 zones

Wynn Design & Development is **71 % of Genea's after-hours revenue at 1700** (619 h, $27,856
Mar-Aug). ProptechOS maps **12** of their **47** VAVs. Every weekend conclusion involving Wynn was
drawn from a quarter of their space.

## ⚠️ BAS point names are NOT unique — only the full path is

Real collisions found, same name under different tenants:
```
Floor 3   Bruin Capital vav3_12..16   AND   Mass Mutual vav3_12..16
Floor 5   Bessemer vav5_3             AND   ER Injury vav-5-3      (underscore vs hyphen)
Floor 9   TouchstoneLiving VAV9_4     AND   floor-level vav9_4     (case only)
Floor 2   HowardHughes vav2_4..9      AND   floor-level vav2_4..9
```
➡️ **Never match on the point name alone.** The tenant folder path is the only unique key, so the
BACnet Object_Name/Description cannot resolve these — the BAS hierarchy is the sole authority.

## Still collapsed (floor 2)
`Suite_250`, `Suite260`, `TSGConsumer` — contents unknown.

---

## Floor 2, resolved — and a correction

```
Suite_250      vav2_1 .. vav2_18                              18
Suite260       VAV_2_1, VAV_2_2, VAV_2_3                       3
TSGConsumer    VAV_2_5, VAV_2_2A, VAV_2_3A, VAV_2_4, VAV_2_1A  5   (P8S has 4, +1)
HowardHughes   STILL COLLAPSED — contents unknown
floor level    ahu2_1, exh_cav2_1/2, osa_cav2_3, vav2_4..vav2_9
```

⚠️ **Correction to the earlier entry:** I recorded `vav2_1..vav2_18` under **HowardHughes**. A
clearer screenshot shows that list belongs to **Suite_250**, and `HowardHughes` is a *separate,
still-collapsed folder*. Genea's Suite 250 tenant is "Howard Hughes", so these two folders may be
duplicates, or one may be legacy — **do not map either until HowardHughes is expanded.**

⚠️ **`Suite260` (3 VAVs) does not appear in Genea's Areas export at all.** Either a tenant with no
lease area configured in Genea, or a vacant/reconfigured suite. Worth asking about.

⚠️ More name collisions on this floor: `Suite_250/vav2_4..9` vs floor-level `vav2_4..9`, and
`TSGConsumer/VAV_2_4` vs `Suite_250/vav2_4`. Path remains the only unique key.

## ✅ Floor 2 complete — HowardHughes is a DUPLICATE of Suite_250

`HowardHughes` expands to the **same** `vav2_1 .. vav2_18` as `Suite_250`. Two folders, one space,
one set of devices. Genea calls it Suite 250 / "Howard Hughes".

➡️ **Map to ONE zone only.** Whichever is chosen, the other must be ignored or the 18 VAVs get
counted twice. Floor 2 real totals: Howard Hughes 18 · Suite260 3 · TSGConsumer 5.

# ✅ MAPPING COMPLETE — all 10 floors

**285 VAVs assigned to a tenant** across 25 tenant folders (excluding the Suite_250/HowardHughes
duplicate), plus floor-level common/mech units. ProptechOS holds 287 OccupancyStatus devices, so
the BAS accounts for essentially the whole building.

## Next
1. Build the PATCH set — match on **floor + tenant folder + unit**, never on point name alone
   (see the collision list above). Flag ambiguities rather than guessing.
2. Create ProptechOS zones for the 6 tenants that have none: MP Materials/Suite 800 (34),
   Suite 500 (10), Douglas Elliman/Suite 150 (5), Suite260 (3), Summerlin Sales/Suite 120 (2).
3. Fix the 18 tenants whose counts are wrong — Wynn most of all, 12 of 47.
4. **Then redo the weekend reconciliation from scratch.** Summerlin Gallery, Wynn and Touchstone
   were all analysed on wrong or partial zone sets.

---

# ⚠️ WITHDRAWN: "Bessemer and ER Injury cannot be separated"

I warned that `vav5_3` and `vav-5-3` were indistinguishable in BACnet. **That was wrong.** The
punctuation survives into the BACnet Object_Description, and the two tenants sit on entirely
separate IP blocks:

```
192.168.5.51  - .5.63    "VAV 5-1" .. "VAV 5-13"     13   Bessemer Trust   (BAS vav5_1..13)
192.168.5.161 - .5.172   "VAV-5-1" .. "VAV-5-12"     12   ER Injury        (BAS vav-5-1..12)
```

Contiguous, non-overlapping, and the counts match the BAS exactly. **IP contiguity resolves every
collision I flagged** — the tenants occupy distinct address blocks, so floor+unit+IP-block is a
sound key even where the name alone is ambiguous.

# Remap proposal — `1700-zone-remap-proposal.csv`

7 single-device fixes, each justified by falling inside an established contiguous block:

```
device 50560   .5.60    VAV 5-10           MECH. ROOM   -> Bessemer Trust        HIGH
device 5163    .5.163   VAV-5-3            MECH. ROOM   -> ER Injury             HIGH
device 5168    .5.168   VAV-5-8            MECH. ROOM   -> ER Injury             HIGH
device 3034    .3.34    VAV-3-04           none         -> Rimini Street         HIGH
device 115036  .3.62    Procedure Rm 105   none         -> Dr. Snyder            HIGH
device 193231  .2.70    VAV-2-1            TENANT SPACE -> Suite260 (new)        MEDIUM
device 20106   .2.71    VAV-2-2            TENANT SPACE -> Suite260 (new)        MEDIUM
```

These alone correct Bessemer 12->13, ER Injury 10->12, Rimini 5->6, Dr Snyder 1->2.

## Zones that must be CREATED (Genea is authoritative for tenant identity)
```
MP Materials / Suite 800      34   Genea customer, 48 paid hours, no zone at all
Wynn Suite 1000               34   decide: separate zone, or merge with Suite 900?
Suite 500                     10   no matching BACnet devices located yet - investigate
Douglas Elliman / Suite 150    5
Suite260                       3   ⚠️ not in Genea's Areas export - confirm with HHH
Summerlin Sales / Suite 120    2   device 10105 + device 1033
```

⚠️ **Suite 500's 10 VAVs have no BACnet counterpart on floor 5.** The floor-5 address space holds
exactly Bessemer (13) + ER Injury (12) and nothing else. Either they are on another subnet, not
onboarded, or the folder is stale. Resolve before creating that zone.
