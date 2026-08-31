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
