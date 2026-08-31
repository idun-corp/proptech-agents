# 1700 Pavilion — BAS (Niagara) tenant tree, read 30 Aug 2026 23:44 PDT
# Source: LogMeIn -> Px View -> Nav, /Drivers/BcpBacnetNetwork/<floor>
# Tenant/suite FOLDERS are the mapping we could not reconstruct from ProptechOS.

FLOOR 1   ahu1_1 · exh_cav1_1/2 · osa_cav1_3
          vav1_04,06,07,08,09,10,11,12,13,14,15,16,22   (floor-level, unassigned)
          [DouglasElliman]        <- Genea Suite 150
          [SummerlinSales]        <- Genea Suite 120, the $630 weekend tenant

FLOOR 2   ahu2_1 · exh_cav2_1/2 · osa_cav2_3 · vav2_4..vav2_9
          [Suite_250] [Suite260] [HowardHughes] [TSGConsumer]

FLOOR 3   ahu3_1 · exh_cav3_1/2 · osa_cav3_3 · vav3_4..vav3_9
          [Bruin Capital] [SnyderDental] [Cirrus Company] [Mass Mutual Finan..]
          [Rimini Street] [Edelman Financial]

FLOOR 4   ahu4_1 · exh_cav4_2 · osa_cav4_3
          [CapitalGurus] [New York Life] [Northmarq] [PNC Bank]

FLOOR 5   ahu5_1 · exh_cav5_1/2 · osa_cav5_3 · vav5_4, vav5_5
          [Suite 500] [Bessemer Trust] [ER Injury]

FLOOR 6   ahu6_1 · exh_cav6_1/2 · osa_cav6_3 · vav_14, vav_15
          [Ghost_Lifestyle] [Hearst_Health] [Northern_Trust] [Malibu]

FLOOR 7   ahu7_1 · exh_cav7_1/2 · osa_cav7_3
          [Snell_Wilmer]          <- whole floor

FLOOR 8   ahu8_1 · exh_cav8_1/2 · osa_cav8_3 · vav8_5, vav8_9
          vav_MP_8_01 .. vav_MP_8_34   <- 34 VAVs, MP Materials = Genea Suite 800
                                          (MP Mine Operations — MISSING from ProptechOS entirely)

FLOOR 9   ahu9_1 · exh_cav9_1/2 · osa_cav9_3 · vav9_4..vav9_9
          vav_Wynn_9_1 .. vav_Wynn_9_13   <- Wynn Suite 900
          [TouchstoneLiving]              <- Suite 950

FLOOR 10  ahu10_1 · exh_cav10_1/2 · osa_cav10_3 · vav10_5
          vav_Wynn_10_1 .. vav_Wynn_10_34 <- Wynn Suite 1000

ALSO: Fan Coils · DOAS · Plant · Power · Schedules · Alarm Console

## Naming joins to our BACnet reads
BAS `vav_Wynn_10_19`  ==  BACnet Object_Name "Wynn VAV 10-19"  ==  ProptechOS device 169
BAS `vav1_10`         ==  BACnet desc "VAV 1-10"
So the join key is floor+unit, with the tenant prefix where present.

## Floor plan labels seen
Floor 1 plan shows "Summerlin Sales" near vav1_22 / the lobby.
