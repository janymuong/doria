# 6. DHCP and DNS

**Built:** dnsmasq on `srv`, and `client` moved from a typed-in address to DHCP.

- **DHCP pool:** 192.168.50.100 to 199, 12-hour leases. `client` has a reservation for 192.168.50.20 tied to its MAC address. The servers keep static addresses.
- **DNS:** names such as `mon.doria.internal` are generated from the Ansible inventory. Other names are forwarded to 1.1.1.1 and 9.9.9.9 and cached. A name that does not exist under `doria.internal` gets `NXDOMAIN` straight away.
- `no-hosts` stops dnsmasq reading `srv`'s own `/etc/hosts`, which maps its name to 127.0.1.1.
- The config is checked with `dnsmasq --test` before it replaces the live file.
- `client` was switched with a role that rewrites `/etc/network/interfaces` (a backup is kept) and reboots.

## Checks

    dig @192.168.50.11 mon.doria.internal +short
    dig @192.168.50.11 nosuch.doria.internal | grep status
    sudo nmap --script broadcast-dhcp-discover -e virbr50
    cat /var/lib/misc/dnsmasq.leases

## What it showed

- The four-step exchange (discover, offer, request, acknowledge) is visible in the journal, in the same second.
- A DHCP lease is not permanent. `ip addr` shows a finite lifetime, and the offer carries a renew time at 6 hours and a rebind time at 10 hours 30 minutes.
- The first lookup took 16 ms and the repeat took 0 ms, because of the cache.
- **First check for "the internet is down":** if `ping 1.1.1.1` works and `ping deb.debian.org` fails, the problem is DNS, not the network.
- An empty `command -v` over non-interactive SSH does not mean a program is missing. `/usr/sbin` was not on the path.
