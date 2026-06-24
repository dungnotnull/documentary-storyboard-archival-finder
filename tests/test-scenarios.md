# Test Scenarios — Documentary Storyboard & Archival Finder (Idea 227)

## Scenario 1 — Apollo program short doc
**Input:** 10-min expository doc, public-domain only.
**Expected:** Structure + storyboard/shot list; NASA/LoC public-domain footage with sources; rights noted.
**Pass:** Shot list + assets with license status.

## Scenario 2 — Rights unclear
**Input:** A found clip with no clear license.
**Expected:** Flagged "do not use without clearance"; alternatives suggested.
**Pass:** Unclear rights flagged.

## Scenario 3 — Fair use request
**Input:** User wants to use a copyrighted news clip under fair use.
**Expected:** Notes fair use is fact-specific, recommends legal review; does not assert it.
**Pass:** No fair-use assertion; legal review advised.

## Scenario 4 — Coverage gap
**Input:** A beat with no available archival footage.
**Expected:** Gap flagged; original B-roll or animation suggested.
**Pass:** Gap identified with plan.

## Scenario 5 — Attribution license
**Input:** A CC-BY image selected.
**Expected:** Attribution requirement recorded in asset table.
**Pass:** Attribution noted.

## Scenario 6 — Archive offline
**Input:** Archive sites unreachable.
**Expected:** Uses cached archive directory; flags staleness; still records rights caution.
**Pass:** Staleness noted.
