# 4. Metrics and dashboards

**Built:** node exporter on every VM, Prometheus and Grafana on `mon`.

- **Node exporter** is the Debian package, with a textfile directory at `/var/lib/prometheus/node-exporter`. Any `.prom` file dropped there is published with the other metrics. The package also installs two small helper units (`-apt`, `-nvme`) that write extra metrics about every 15 minutes. They show up in the journal, but they are not the exporter.
- **Prometheus** pulls from every exporter every 15 seconds. The scrape list is a template that loops over the inventory, so a new host in `[lab]` is picked up automatically. The config is checked with `promtool` before it replaces the live file. A changed config triggers a reload, and changed arguments trigger a restart.
- **Grafana** comes from Grafana's own apt repository, with its signing key. The datasource and the dashboards are provisioned from files. The dashboard JSON is in git, and `allowUiUpdates` is off, so the file is the source of truth.

## Checks

    curl -s 192.168.50.11:9100/metrics | head
    curl -s 192.168.50.10:9090/-/ready
    curl -s 192.168.50.10:3000/api/health

In Prometheus, the query `up` shows 1 for every target.

## What it showed

- A metric was checked against reality: `node_memory_MemAvailable_bytes` against `free -b` on `client`.
- "Connection refused" and "timed out" mean different things. Refused: the machine answered and nothing listens on that port. Timed out: nothing answered at all.
- Files with `{{ }}` in them (dashboards, alert rules) are installed with `copy`, not `template`. Jinja would try to evaluate text that belongs to Grafana or Prometheus.
- The Node Exporter Full dashboard is Grafana dashboard 1860, under the Apache 2.0 licence.
