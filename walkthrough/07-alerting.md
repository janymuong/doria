# 7. Alerting

**Built:** alert rules in Prometheus, Alertmanager on `mon`, and a small service that writes each alert to the journal in place of email.

Prometheus decides that something is wrong. Alertmanager decides who is told and how.

## Rules

| Group | Alerts |
|---|---|
| reachability | HostUnreachable, GatewayUnreachable, InternetUnreachable |
| services | NodeExporterDown, ServiceDown, LocalDnsDown, MirrorUnreachable |
| capacity | DiskAlmostFull (over 85%), MemoryLow (under 10%) |
| backups | see `08-backups-and-restore-tests.md` |

- `for:` means a condition must hold for that long before the alert fires. An alert waits as pending, then fires.
- Severity is a label, and routing can use it later.

## Alertmanager settings

- `group_wait` 10 s, `group_interval` 1 min, `repeat_interval` 4 h.
- **Inhibition:** a dead host explains its silent exporter, so `HostUnreachable` suppresses `NodeExporterDown`. A dead gateway suppresses `InternetUnreachable`. A dead exporter suppresses `BackupMetricsMissing`.
- The config is checked with `amtool check-config` before it replaces the live file.

## Tests and results

- The first alert reached the journal 10 seconds after Alertmanager received it, which is `group_wait`.
- An alert added by hand resolved after 5 minutes, Alertmanager's default timeout for alerts with no end time. Alerts from rules resolve as soon as Prometheus stops sending them.
- A stopped exporter, a suspended VM and a nearly full disk each produced the expected alert.
