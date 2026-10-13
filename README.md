<div align="center">
  <img alt="Conceptual blockchain investigation illustration; not transaction evidence" src="./assets/blockchain-investigation-hero.jpg" width="1200">
  <h1>SAPbot - Security Analysis Platform</h1>
  <p><strong>Public blockchain threat intelligence research</strong><br>Originally published as <em>Blockchain Analysis on Threat Actors</em>.</p>
  <p><a href="https://sapbot.org">SAPbot.org</a> · <a href="./CATALOG.md">Case catalog</a> · <a href="./wallets.md">Wallet index</a> · <a href="./CONTRIBUTING.md">Contribute or request a correction</a></p>
</div>

## About this repository

This is the public, research-only edition of SAPbot. It contains selected case reports, chain-specific indicators, transaction and incident CSVs, and an index of published wallet research. The SAPbot application, private review material, development tools, and unpublished cases live separately. This repository does not include a runnable web app, a Python package, or a generated database.

Browse the [complete public case catalog](CATALOG.md) or start with:

| Area | Research |
| --- | --- |
| [Ethereum and EVM](EVM/README.md) | Exploits, proceeds, contracts, and attribution boundaries |
| [Solana](SOL/README.md) | Protocol incidents, compromised wallets, and campaigns |
| [TRON](TRON/README.md) | Sanctions and threat-finance records |
| [Multi-chain](Multi-Chain/README.md) | Cross-chain incidents and security sweeps |
| [1VPNS](1VPNS/README.md) | OFAC designation and multi-network addresses |
| [FTX](FTX/readme.md) | Historical wallet snapshot |
| [Lazarus](Lazarus/readme.md) | DPRK wallet research |

The [wallet index](wallets.md) is a historical research document. Some referenced cases may be absent from this curated public edition; the [catalog](CATALOG.md) lists only published case files.

## How to read the evidence

Records combine official disclosures, explorer transactions, researcher analysis, and provisional leads. Read the case narrative and cited source before using an address. The same address can have different roles across networks or cases. A victim, recovery wallet, exchange, bridge, or service intermediary does not become attacker-controlled merely because it appears in a flow.

CSV files use several documented layouts. [Data format and validation](docs/data-model.md) explains the supported structure and its limits. The repository check runs with Python's standard library:

```sh
python scripts/check_research.py
```

This checks local documentation links, JSON syntax and visual references, CSV structure, and basic role/label consistency. It does **not** verify an address on-chain or prove an attribution.

## Publication and corrections

Research enters this public edition after review of sources, complete identifiers, chain and address role, uncertainty, and unintended disclosure. An unpublished folder in the private research workspace is not automatically mirrored here. [Submit intelligence](https://github.com/ryanshatch/SAPbot-threat-intelligence/issues/new?template=new-intelligence.yml) or [request a correction](https://github.com/ryanshatch/SAPbot-threat-intelligence/issues/new?template=attribution-correction.yml). See [CONTRIBUTING.md](CONTRIBUTING.md) for the review criteria.

For changes over time, use the [commit history](https://github.com/ryanshatch/SAPbot-threat-intelligence/commits/main) and [public release notes](CHANGELOG.md). Inclusion does not establish criminal activity or current sanctions status. Check the current primary source for time-sensitive designations and balances.

© Ryanshatch. See [LICENSE](LICENSE) for reuse terms.
