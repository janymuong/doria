# 10. Limits and next steps

## What this lab does not cover

- The VMs share one host, and `mon` watches itself. If `mon` dies, nothing alerts.
- Backups sit on the same disk as the data.
- Prometheus, Alertmanager and Grafana have no TLS, and Alertmanager has no authentication.
- Passwords are typed at each run. There is no secrets management.
- Alerts go to a log file, not to email or chat.
- The only client is Linux. There is no Windows or macOS machine, no Active Directory or Group Policy, and no Microsoft 365.
- There is no ticketing system, no patching process and no asset inventory.

## Next steps

- Copy the backups to a second disk or another machine, and test restores from older archives too.
- Add alerts for the alert path itself (Alertmanager down, failed notifications), and a heartbeat that an outside service watches.
- Move the passwords into Ansible Vault.
- Add a Windows VM and practise the same tasks there.
- Keep the asset log and the ticket notes in one place.
