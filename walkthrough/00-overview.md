# Overview

Doria is a practice lab for first-line ICT work in a small office: addresses and names, monitoring, backups, and finding faults. Three virtual machines run on one host.

| Machine | Address | Job |
|---|---|---|
| srv | 192.168.50.11 | DHCP and DNS, file share, backups |
| mon | 192.168.50.10 | Prometheus, Alertmanager, Grafana, blackbox exporter |
| client | 192.168.50.20 | a staff laptop that gets its address from DHCP |

The host is the gateway (192.168.50.1) and runs Ansible.

## Order of the build

`01-virtual-network.md`  
`02-vms-and-access.md`  
`03-ansible-basics.md`  
`04-metrics-and-dashboards.md`  
`05-probes.md`  
`06-dhcp-and-dns.md`  
`07-alerting.md`  
`08-backups-and-restore-tests.md`  
`09-troubleshooting-drills.md`  
`10-limits-and-next-steps.md`  
`11-rebuilding.md`  

Each file says what was built, how to check it, and what went wrong. The troubleshooting notes are in `docs/troubleshooting/`.
