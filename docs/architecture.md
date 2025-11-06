# NateOS Architecture (v0)

## Overview
NateOS is a NOS-on-Linux targeting L2/L3 switching. It separates planes and favors proven components to accelerate delivery.

## Planes
- Data Plane: XDP/AF_XDP (CPU fast path), optional DPDK; future ASIC via SAI
- Control Plane: FRR for routing; MSTP/RSTP, LACP, LLDP, IGMP/MLD snooping
- Management Plane: Transactional config store, CLI, gNMI/NETCONF, telemetry

## Abstractions
- Switch Abstraction: SAI (future) or vendor SDK mapping module
- Platform: OpenBMC integration (future), platform sensors/LEDs drivers

## Initial Feature Scope
- L2: VLANs, MAC learning/aging, RSTP/MSTP, LACP, LLDP, IGMP snooping
- L3: IPv4/IPv6 static + OSPF/BGP via FRR, ECMP, VRRP, ARP/ND
- Mgmt: CLI skeleton, state datastore, basic telemetry, AAA

## Process Model
- Orchestrator `switchd` (scaffold)
- Protocol daemons (FRR, lldpd, mstpd, lacpd)
- State bus: Redis (or gNMI target process) for config/state

## Data Path Concept
- Ingress: parse → L2 table (FDB/VLAN) → L3 lookup (optional) → QoS/ACL → egress
- Misses to CPU via XDP redirect; control plane programs FIB/ACL/QoS tables

## Performance Targets (initial)
- CPU-only dev: 10–40GbE line-rate per NIC with XDP where possible
- Latency: sub-100µs best-effort; optimize later with pinning/NUMA/hugepages

## Security
- Signed images, secure boot (future), RBAC/AAA, TLS for mgmt

## Delivery Approach
- Start software-only; add ASIC offload (SAI) after functional parity
