# 5. Probes

**Built:** blackbox exporter on `mon`, listening on loopback only.

Node exporter says what a machine reports about itself. Probes check from the outside, the way a user would.

| Module | Checks |
|---|---|
| `icmp` | ping to the three VMs, the gateway and 1.1.1.1 |
| `http_2xx` | Prometheus and Grafana health pages |
| `http_head_2xx` | the Debian mirror, using HEAD so little data is fetched |
| `dns_a` | a lookup through 1.1.1.1 |
| `dns_local` | a lookup of `mon.doria.internal` through `srv` |

Prometheus passes each target to the exporter with a relabel rule, so the graphs show the real target and not `localhost:9115`.

## What it showed

- **Layers fail separately.** With Grafana stopped, the HTTP probe for Grafana went to 0 while the ping probe and the exporter for `mon` stayed at 1. The host and its exporter were fine, and one service on it was down.
- Probe durations were close to `ping` times, a little higher because a probe includes socket setup.
