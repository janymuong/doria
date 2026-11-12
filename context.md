# context

more detail on doria: what is in it, where things live, how to run it, and a few notes. the diagram and the tools are in the [readme](README.md). the build story, in order, is in [walkthrough/](walkthrough/00-overview.md).

## what is in it

- **srv**: dhcp and dns (dnsmasq), a file share at `/srv/share`, a nightly backup and a nightly restore test.
- **mon**: prometheus, alertmanager, grafana and the blackbox exporter. alerts are written to the journal by a small local service that stands in for email.
- **client**: a linux machine that gets its address from dhcp, like a staff laptop.
- **scripts/drill**: opens practice tickets by breaking something in the lab.

## files

| directory | contents |
|---|---|
| `ansible/` | inventory, playbook, and one role per component |
| `libvirt/` | the virtual network definition |
| `docs/` | the addressing plan and troubleshooting notes |
| `scripts/` | the drill script |
| `walkthrough/` | what was built, in order, and what went wrong |

## running it

needs a linux host with libvirt, qemu, virt-install and ansible, and about 4 gb of free ram for the vms.

1. define the network: `virsh net-define libvirt/doria-lan.xml`, then `virsh net-start doria-lan` and `virsh net-autostart doria-lan`.
2. install three debian 13 vms (`mon`, `srv`, `client`) with the addresses in `docs/addressing.md`, an `ops` user and an ssh server. details are in `walkthrough/02-vms-and-access.md`.
3. put your own ssh key on each vm, and set the mac address of `client` in `ansible/group_vars/servers.yml` (find it with `virsh domiflist client`).
4. run `cd ansible && ansible-playbook site.yml --ask-become-pass`. run it twice. the second run should change nothing.

## notes

- this is a lab. prometheus, alertmanager and grafana run without tls, and the sudo password is typed at each run.
- the node exporter full dashboard (grafana dashboard 1860) is used under its apache 2.0 licence.
