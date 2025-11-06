# NateOS

A network operating system designed to operate as a Layer 2/Layer 3 switch, following a pragmatic NOS-on-Linux approach with clear separation of data, control, and management planes.

## Getting Started

- BMAD config: `bmad/bmm/config.yaml`
- Outputs directory: `outputs/`
- Docs: see `docs/`

## High-Level Components

- Data plane: XDP/DPDK initially; optional SAI/ASIC offload later
- Control plane: FRR (BGP/OSPF/IS-IS/PIM/VRRP), LACP/STP daemons
- Management plane: CLI/API, gNMI/NETCONF (scaffold), telemetry

See `docs/architecture.md` and `docs/roadmap.md` for details.

## Run (dev)

- Initialize workspace: `./scripts/setup-dev.ps1`
- Install dependencies: `pip install -r requirements.txt`
- Start switchd (stub): `./scripts/run-switchd.ps1`
- Start Web GUI: `./scripts/run-web-gui.ps1` (then open http://localhost:8080)
- Start Desktop GUI (Tkinter): `./scripts/run-desktop-gui.ps1` (requires Web GUI running)
- CLI (stub): `python src/mgmt/cli/cli.py --help`

## Authors

- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [Nathan Godin]
- [Daniel Ribeirinha-Braga]()