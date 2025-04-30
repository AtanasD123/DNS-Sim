# DNS-SIM &nbsp;

A minimal, **Python 3** implementation of a toy Domain-Name-System that mirrors the hierarchy and message-flow of the real Internet DNS.  
Four independent programs work together:

| Program | Role | Listens on |
|---------|------|------------|
| `rs.py` | **Root Server (RS)** — first stop for every query; redirects or resolves | `<RU_DNS_PORT>` |
| `ts1.py` | **TLD Server 1 (TS1)** — authoritative for first TLD in `rsdatabase.txt` | `<RU_DNS_PORT>` |
| `ts2.py` | **TLD Server 2 (TS2)** — authoritative for second TLD in `rsdatabase.txt` | `<RU_DNS_PORT>` |
| `client.py` | **Client / Resolver** — takes hostnames from `hostnames.txt` and queries RS | *(outbound only)* |

Each server maintains its own flat text database (`*.txt`) and writes every outgoing DNS response to a log file.

---

## 📦 Contents

```txt
.
├── client.py              # iterative / recursive resolver
├── rs.py                  # root server
├── ts1.py                 # top-level domain server #1
├── ts2.py                 # top-level domain server #2
├── rsdatabase.txt         # RS mappings + TS hostnames (1st 2 lines)
├── ts1database.txt        # TS1 authoritative mappings
├── ts2database.txt        # TS2 authoritative mappings
├── hostnames.txt          # <domain> <rd|it> input for client
├── resolved.txt           # (auto-generated) client log
├── rsresponses.txt        # (auto-generated) RS log
├── ts1responses.txt       # (auto-generated) TS1 log
└── ts2responses.txt       # (auto-generated) TS2 log
