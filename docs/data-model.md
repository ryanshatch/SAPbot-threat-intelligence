# Public research data format

The case reports and their CSVs are the published records in this repository. They are not a live feed or a generated database. Rows can describe threat-controlled addresses, victim or recovery assets, service infrastructure, transactions, or provisional investigative leads. The case narrative and cited evidence explain each role.

## CSV layouts

CSV schemas vary by case and date. The [catalog](../CATALOG.md) lists published reports. A common dedicated-case address layout has these 16 columns:

```text
case_id,incident_date,network,chain_id,address,indicator_type,entity,role,source_confidence,control_confidence,attribution_scope,monitoring,priority,threat_label,notes,source
```

Other published address layouts use `address_type`, `classification`, `monitoring_action`, or `watchlist_eligible`. Some use `observed_date` or `disclosure_date` instead of `incident_date`; SOL/CYBERLEEK omits a date column. Sweeps and legacy case files also have distinct CSV layouts. Read each file's header and its accompanying README; do not combine columns by position or silently interpret a report date as on-chain activity.

`source_confidence` and `control_confidence` are source text, not probabilities. `threat_label` is a case-specific boolean, not a global blacklist or graph-propagated label. The same EVM account on different networks must remain network-specific. A false label can still represent a useful victim, recovery, or service pivot. Treat network IDs, address spelling, and evidence URLs as supplied by the case; review them against the primary source.

## Repository checks

Run `python scripts/check_research.py`. It checks all committed CSV files for parseable, unique headers and consistent row width. For address files with `threat_label`, it checks explicit true/false values and disallows labeling an explicitly victim/recovery role as a threat. It also checks local documentation links, JSON syntax, and the visual manifest. It does not verify blockchain checksums, source credibility, live balances, address control, or legal status. New schemas should be documented and reviewed before publication.
