# PLAT — a single phantom device twin silently kills an entire BACnet connector

**Site:** 1700 Pavilion (Howard Hughes) · **Connector:** `multi-bacnet-2c28ab21-f7cf-4c82-ba42-abf56a888297`
**Impact:** 337 of 338 devices stopped publishing for **6 h 45 m** on 28 Aug 2026, with **zero errors logged**.

## ⚠️ This is a REGRESSION in the 27 Aug build, not a long-standing gap

```
PRODUCTION jar deployed 2026-08-28 12:52:51Z · classes compiled 27 Aug 09:43 PDT
SIBLING connector (untouched)                 · classes compiled 13 Jul 07:45
BacnetDataReader.class    13,240 B (Jul)  ->  15,516 B (27 Aug)
```

`BacnetDataReader` is the class that issues the `protocol-services-supported` read where the NPE
fires. The same six bad twins had been present and **completely harmless for eleven months** under
the July build. The new build turns them fatal. Please diff that class first.

## TL;DR

One device twin whose BACnet instance does not exist at its configured IP throws an
unhandled NPE inside the bacnet4j transport thread at bind time. That one failure takes down
device binding for **every other device on the connector**. Nothing is logged as an error
afterwards, so the site looks configured-but-idle rather than broken.

**A single bad twin should never be able to silence 337 healthy devices.**

## The crash

```
ERROR c.s.b.transport.DefaultTransport - Error during send: OutgoingConfirmed
  [maxAPDULengthAccepted=-1, segmentationSupported=null,
   service=ReadPropertyRequest [objectIdentifier=device 10107,
                                propertyIdentifier=protocol-services-supported ...]
java.lang.NullPointerException: Cannot invoke
  "com.serotonin.bacnet4j.type.enumerated.Segmentation.intValue()"
  because "this.segmentationSupported" is null
	at com.serotonin.bacnet4j.transport.DefaultTransport$OutgoingConfirmed.sendImpl(DefaultTransport.java:383)
	at com.serotonin.bacnet4j.transport.DefaultTransport$Outgoing.send(DefaultTransport.java:338)
	at com.serotonin.bacnet4j.transport.DefaultTransport.run(DefaultTransport.java:494)
```

The connector reads `protocol-services-supported` to establish device capabilities. The phantom
answers with a BACnet-Error PDU (the IP is live, the *instance* is not), `segmentationSupported`
is left null, and the NPE escapes into the transport thread.

## What a "phantom" is

A device twin pointing at an IP where a **different** instance actually lives. Verified directly:

```
192.168.1.16   device 10106   Object_Name "VAV 1-6", segmentation OK, services OK   <- real
192.168.1.16   device 10107   BACnet-Error on every property                        <- phantom
```

⚠️ Distinct from an unreachable device. A device that simply **times out** is handled correctly and
has never caused a problem — 4 such devices at this site are benign. Only the
**responds-with-error** case triggers the NPE.

## Timeline (UTC)

```
26 Aug 12:18   restart, 0 NPE, 337 devices          fine
27 Aug         0 NPE all day, 337 devices           fine
28 Aug 05:53   restart, NPE on device 10107         -> 1 device, 141 sensors
28 Aug 12:13   restart, NPE on device 10107         -> still 1 device
28 Aug 12:29   removed 10107, restart               -> NPE moved to device 178, still 1 device
28 Aug 12:38   removed all 5 remaining phantoms     -> 352 of 352 devices, 0 errors
```

Two things worth noting. **It is a race, not a certainty** — the same config ran clean for two days
before failing deterministically on the third, and the final restart logged the NPE yet still bound
everything. And **it cascades**: remove one phantom and the next takes its place.

## Mitigation applied on site (please review)

We edited `iot_edge_config.json` on the PEG directly, removing 6 phantom device entries, and
restarted. **We understand this is outside normal connector maintenance** — the site had been dark
6+ hours, a plain restart had twice failed to recover it, and a config deploy was not available on a
Friday afternoon. The edit is self-cleaning: the next deploy overwrites it.

```
backup: /tmp/iot_edge_config.BACKUP-2026-08-28.json   (on the PEG)
removed: device 10107, 178, 179, 2101, 10115, 161241
result:  352/352 devices · 1,599 sensors · 574/574 occupancy points · 0 errors
```

**The 6 phantom twins still exist in ProptechOS and will return at the next deploy**, at which point
the crash risk returns. They need deleting or correcting platform-side.

## Asks

1. **Do not let one device's bind failure abort the others.** Catch the NPE per-device, mark that
   device failed, carry on. This is the actual defect — the bad data merely exposes it.
2. **Treat a null `segmentationSupported` as "assume no segmentation"** rather than dereferencing it.
3. **Log a device that fails to bind as an ERROR.** Today it is completely silent, which is why this
   went unnoticed for hours and why the original 1,769-sensor problem at this site took months to
   find. Same gap as PLAT-5765 ask #4.
4. **Reject or flag a twin at onboarding whose instance does not answer at its configured IP.** All
   6 here would have been caught by a single directed read.

## How to find phantoms at any site

Directed `ReadProperty(Object_Name)` per configured device at its own `bacnetHost`. Classify the
reply: **OK** keep · **timeout** benign · **BACnet-Error PDU** phantom, and a crash trigger.
At 1700 that was 308 OK, 4 timeout, 6 phantom, 40 MS/TP or unaddressed.


---

## Addendum, 28 Aug — one of the six was NOT a phantom

`device 2101` (`MTIII_AHU_02101`, an air handler, 8 sensors) is real and lives at
**192.168.2.101**. Its twin records **192.168.2.67**, which is where `device 2067` lives. The
mapping is systematic — instance `2NNN` belongs at `.NNN` — so this is a wrong address, not a
missing device. It must be corrected rather than deleted.

The other five appear nowhere across all eight subnets and are safe to delete:
`Wynn VAV 10-28`, `Wynn VAV 10-29`, `ECY-VAV-D837F8`, `ECY-VAV-D84D93`, `VAV-8`.

## Addendum — 37 BACnet devices on this network are not in the connector config

A sweep of 1,720 unconfigured addresses (one wildcard device read each, ~1 min, no impact) found:

```
10  MTIII_AHU_*  192.168.2.101-110   air handlers — only 2 are collected
14  ECY-VAV-*    .1.x and .2.x
 4  VAV 1-22, VAV-1-17/18/19
 1  ECY-TU203-B4BB91  192.168.6.70
 1  DIRIS A-40   192.168.0.149       a Socomec power meter, never onboarded
```

Not a PLAT defect, but it belongs with the onboarding-verification ask: a directed read per
configured device, plus a subnet sweep for unconfigured ones, would have surfaced both the six bad
twins and these thirty missing devices at commissioning.
