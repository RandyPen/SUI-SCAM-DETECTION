# SUI-SCAM-DETECTION

A tool to detect `SCAM` object in Sui.

## Workflow

```mermaid
flowchart TB
A[Object ID] --> B[Object data]
B --> C{Own Object?}
C -->|yes| D{Coin or NFT}
C -->|no| E[not SCAM]
D -->|coin| F{In coin whitelist?}
D -->|NFT| G{In NFT whitelist?}
F -->|yes| E
G -->|yes| E
F -->|no| H[get coin metadata]
G -->|no| I[get NFT desc etc]
H --> J1{GPT judge}
I --> J2{GPT judge}
J1 -->|not SCAM| E
J2 -->|not SCAM| E
J1 -->|SCAM| L[SCAM]
J2 -->|SCAM| L
```

## Configure

Whitelist in `/data/coin-list.json` and `/data/object-list.json`.

Prompts in `gpt.py`.

## Run

See `process.py`.


## Future test features
- [ ] visual model to analyze image
- [ ] (optional) llama3
- [ ] (optional) [coze](https://www.coze.com/)
