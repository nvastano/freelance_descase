# Gijs Van Schaik reassignment - run 2026-11-24

| Step | Records | Result |
|---|---|---|
| Accounts | 493 | 493 ok (Barry 365, Jos 123, Guido 5) |
| Contacts | 197 | 197 ok |
| Open opportunities | 19 | 19 ok |
| Leads | 896 | 896 ok (all to Jamal) |
| Task reassigned | 1 | ok (Jos) |
| Tasks deleted (soft, Recycle Bin) | 84 | 84 ok; full export in tasks_open_full_export.csv |
| City__c Hyvinkaa -> Barry | 1 | FAILED: TRANSFER_REQUIRES_READ (Barry has no read on City__c) |

Verified after accounts step: 390 closed opps and 47 cases unchanged (still Gijs).

Still owned by Gijs: 3 accounts with no country (Vollenhoven, Schindler N.V., L.I.S. Hydraulics), 1 contact on them, 8 City__c, 390 closed opps, 47 cases.

Rollback: before_*.csv hold Id + original OwnerId; deleted tasks restorable from Recycle Bin for 15 days.
