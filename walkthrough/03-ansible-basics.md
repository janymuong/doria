# 3. Ansible basics

**Built:** an inventory with groups, a config file, and the `common` role (hostname, timezone, diagnostic tools).

- Groups: `monitoring` (mon), `servers` (srv), `clients` (client), and `lab` made of all three.
- `ansible all -m ping` is not ICMP. It logs in over SSH, finds Python and answers `pong`.
- The `common` role installs `tcpdump`, `traceroute`, `mtr`, `dig` and a few other tools.

## Commands

    ansible all -m ping
    ansible all -m command -a "id" --become --ask-become-pass
    ansible-playbook site.yml --syntax-check
    ansible-playbook site.yml --check --diff --ask-become-pass
    ansible-playbook site.yml --ask-become-pass

## What it showed

- **Idempotency.** The second run reports `changed=0`. The playbook describes a state, and the machines are already in it.
- **Drift correction.** The timezone on `srv` was changed by hand. The next run changed it back, and only on `srv`.
- `--ask-become-pass` sends one password to every host, so the three passwords have to match.
