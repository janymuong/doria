# Troubleshooting method

Work from the bottom up and stop at the first layer that fails.

1. **Scope.** Who is affected: one person, one machine, everyone? What changed recently?
2. **Link.** `ip -br link`: is the interface UP? No link, no network.
3. **Address.** `ip -br addr`: right address and mask? From DHCP or typed by hand?
4. **Route.** `ip route`: is there a default route, and does it point at the real gateway?
5. **Reach by IP.** `ping` the gateway, then a LAN server, then 1.1.1.1.
6. **Names.** `dig <name>` and `dig @192.168.50.11 <name>`: does the local DNS answer?
7. **Service.** `systemctl status <unit>` and `ss -tulnp`: running, and listening on the right address and port?
8. **Logs.** `journalctl -u <unit> -n 50`: what did the service say?
9. **Config and permissions.** What changed, and does it match what Ansible would write?

Change one thing at a time. Write down what you tried, including what did not help.
Monitoring tells you that something is wrong. It does not always tell you where, and sometimes it says nothing.

## What should be listening

Compare `ss -tulnp` against this before deciding anything is wrong.

| Host | Port | Service |
|---|---|---|
| all | 22/tcp | sshd |
| all | 9100/tcp | node exporter |
| srv | 53/udp and tcp, 67/udp | dnsmasq (DNS and DHCP) |
| mon | 3000/tcp, 9090/tcp, 9093/tcp | Grafana, Prometheus, Alertmanager |
| mon (loopback only) | 9115/tcp, 9199/tcp | blackbox exporter, alert logger |
