# 1. The virtual network

**Built:** a libvirt NAT network called `doria-lan`, bridge `virbr50`, 192.168.50.0/24, with the host at 192.168.50.1.

The definition has no DHCP block on purpose. `srv` becomes the DHCP server later, and two DHCP servers on one network cause faults that are hard to trace. The addressing plan is in `docs/addressing.md`.

## Commands

    virsh net-define libvirt/doria-lan.xml
    virsh net-start doria-lan
    virsh net-autostart doria-lan
    ip addr show virbr50

## Subnetting, worked by hand

- A /24 has 254 usable addresses. The broadcast address is 192.168.50.255.
- Split in two, it becomes two /25 networks with mask 255.255.255.128: 192.168.50.0/25 (hosts .1 to .126, broadcast .127) and 192.168.50.128/25 (hosts .129 to .254, broadcast .255).

## What went wrong

- `Unable to create bridge virbr50: Package not installed` meant the running kernel had lost its modules after an update. A reboot fixed it.
- `NO-CARRIER` on `virbr50` is normal while no VM is running.
- `virsh` showed nothing until `LIBVIRT_DEFAULT_URI=qemu:///system` was set. Without it, it looks at the user session instead of the system one.
