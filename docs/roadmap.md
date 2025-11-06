# Roadmap & Milestones

- M0 Platform: Bootstrapping, NIC up, outputs and config scaffolding, basic CLI stub
- M1 L2 Base: VLANs, MAC learning, RSTP/MSTP, LACP, LLDP, IGMP snooping
- M2 L3 Base: IPv4/6, ARP/ND, static routes, VRRP, FRR integration, ECMP
- M3 Routing: OSPFv2/v3, BGP v4/v6, VRF, BFD, basic PIM
- M4 Ops: QoS/ACL, SPAN/ERSPAN, sFlow/NetFlow, config rollback, AAA
- M5 HA/Scale: ISSU/NSF/GR strategies, scale targets, perf certification
- M6 ASIC Offload: SAI/SDK mapping, warm-boot, telemetry parity

## Near-Term Tasks
- Create `switchd` orchestrator scaffold
- Add Redis-backed config/state store
- Provide CLI skeleton and gNMI target placeholder
