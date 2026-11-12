# 11. Rebuilding from nothing

The VMs hold nothing that cannot be recreated. They can be deleted and rebuilt from this repository plus a few things that live outside it. This file lists both, then the rebuild in order.

It was written from the build, not from a rebuild. The first real rebuild is the test of this file: time it, and fix any step you had to improvise.

## What the repository holds

- the network definition (`libvirt/doria-lan.xml`) and the addressing plan (`docs/addressing.md`)
- all configuration after the install (`ansible/`): alert rules, dashboards, the backup scripts and the DHCP reservation for `client`
- the drill script and the troubleshooting notes

## What it does not hold

| Item | Where it lives | On a rebuild |
|---|---|---|
| the `ops` password | your head | choose it again, and use the same one on all three VMs, because `--ask-become-pass` sends one password to every host |
| SSH key `~/.ssh/doria_ed25519` and the aliases in `~/.ssh/config` | the host | keep them, deleting the VMs does not touch them |
| old host keys in `~/.ssh/known_hosts` | the host | remove them first (step 5), or SSH refuses to connect |
| the Debian ISO | `/var/lib/libvirt/images` | keep it, or download it again and verify the checksum |
| the Grafana admin password | Grafana's database on `mon` | lost, the first login is `admin` / `admin` and Grafana asks for a new one |
| files in `/srv/share` | `srv` | lost, recreate them in step 9 |
| metrics history, archives, drill state | the VMs | lost, by design |
| host packages and settings | the host | step 1 |

## The rebuild, in order

### 1. The host (skip if it is the same machine)

    sudo pacman -S qemu-full libvirt virt-manager dnsmasq ansible virt-install virt-viewer jq nmap
    ansible-galaxy collection install community.general
    sudo systemctl enable --now libvirtd
    sudo usermod -aG libvirt $USER
    echo 'export LIBVIRT_DEFAULT_URI=qemu:///system' >> ~/.zshrc

Log out and back in after the group change.

### 2. The network

    virsh net-define libvirt/doria-lan.xml
    virsh net-start doria-lan
    virsh net-autostart doria-lan
    ip addr show virbr50

If `net-start` says `Package not installed`, the kernel was updated since the last boot. Reboot.

### 3. The ISO

Download the current Debian 13 amd64 netinst image and `SHA256SUMS` from `https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/`, then:

    sha256sum --ignore-missing -c SHA256SUMS
    sudo cp debian-13.*-amd64-netinst.iso /var/lib/libvirt/images/

### 4. The three VMs

Replace the ISO name with the real one. `client` gets a fixed MAC, so the DHCP reservation in `ansible/group_vars/servers.yml` matches without editing.

    sudo virt-install --name mon --memory 1536 --vcpus 1 \
      --disk size=10,format=qcow2 \
      --cdrom /var/lib/libvirt/images/debian-13.x.y-amd64-netinst.iso \
      --network network=doria-lan,model=virtio \
      --osinfo detect=on,require=off --graphics spice --noautoconsole

    sudo virt-install --name srv --memory 1024 --vcpus 1 \
      --disk size=10,format=qcow2 \
      --cdrom /var/lib/libvirt/images/debian-13.x.y-amd64-netinst.iso \
      --network network=doria-lan,model=virtio \
      --osinfo detect=on,require=off --graphics spice --noautoconsole

    sudo virt-install --name client --memory 1024 --vcpus 1 \
      --disk size=10,format=qcow2 \
      --cdrom /var/lib/libvirt/images/debian-13.x.y-amd64-netinst.iso \
      --network network=doria-lan,model=virtio,mac=52:54:00:2f:eb:a3 \
      --osinfo detect=on,require=off --graphics spice --noautoconsole

Open each console with `virt-manager` and answer the installer like this:

| Prompt | Answer |
|---|---|
| language, location, keyboard | your choice (the lab used English and a US keyboard) |
| network | when autoconfiguration fails, choose "Configure network manually" |
| IP address | `192.168.50.10` (mon), `192.168.50.11` (srv), `192.168.50.20` (client) |
| netmask, gateway, name server | `255.255.255.0`, `192.168.50.1`, `1.1.1.1` |
| hostname, domain | `mon`, `srv` or `client`, and leave the domain empty |
| root password | leave empty, so `ops` gets sudo |
| user | `ops`, with the same password on all three |
| time zone | Nairobi (Eastern Africa time) |
| partitioning | guided, use the entire disk, all files in one partition, confirm the write |
| mirror | any nearby country, no proxy |
| package survey | no |
| software selection | untick every desktop and the print server, tick only "SSH server" and "standard system utilities" |
| GRUB | yes, to `/dev/vda` |

### 5. SSH access

Remove the old host keys first, then copy the key, then test the aliases:

    for ip in 192.168.50.10 192.168.50.11 192.168.50.20; do ssh-keygen -R "$ip"; done
    for ip in 192.168.50.10 192.168.50.11 192.168.50.20; do ssh-copy-id -i ~/.ssh/doria_ed25519.pub ops@"$ip"; done
    for h in mon srv client; do ssh "$h" hostname; done

If the key or the aliases are gone, recreate them as in `walkthrough/02-vms-and-access.md`.

### 6. Ansible can reach everything

    cd ansible
    ansible all -m ping
    ansible all -m command -a "id" --become --ask-become-pass

### 7. The first full run

    ansible-playbook site.yml --ask-become-pass

This is the long step. The Grafana package is over 100 MB and prints nothing while it downloads. `client` reboots at the end, when it moves to DHCP. Run it a second time: every host should report `changed=0`.

### 8. Check the lab

    curl -s 192.168.50.10:9090/api/v1/targets | jq -r '.data.activeTargets[] | select(.health != "up") | .labels.job'
    curl -s 192.168.50.10:9090/api/v1/rules | jq -r '[.data.groups[].rules[]] | length'
    curl -s 192.168.50.10:3000/api/health
    ssh client 'ip -4 -o addr show enp1s0'

Expected: nothing printed (all 15 targets up), `14`, a JSON block with `"database": "ok"`, and `192.168.50.20` marked `dynamic` with a finite lifetime. In Grafana (first login `admin` / `admin`), the Doria folder should hold two dashboards.

### 9. The sample files, and the first backup

    ssh srv 'mkdir -p /srv/share/hr /srv/share/finance /srv/share/it
    printf "Amina - Juba office\nDavid - Nairobi office\n" > /srv/share/hr/staff-list.txt
    printf "item,serial,assigned_to\nlaptop,A1001,Amina\nprinter,P2002,front desk\n" > /srv/share/it/asset-log.csv
    printf "Q4 budget draft, not final\n" > /srv/share/finance/budget-q4.txt
    dd if=/dev/urandom of=/srv/share/finance/scan-0001.bin bs=1M count=8 status=none'
    ssh -t srv 'sudo systemctl start doria-backup.service; sudo systemctl start doria-restore-test.service'

The "Doria: backups" dashboard should then show PASS.

### 10. The drills

    scripts/drill open

## Where a rebuild goes wrong

- **`client` gets an address in the 100 to 199 range instead of 20:** its MAC does not match the reservation. Compare `virsh domiflist client` with `ansible/group_vars/servers.yml`.
- **`REMOTE HOST IDENTIFICATION HAS CHANGED`:** step 5.
- **`virsh` lists nothing:** `LIBVIRT_DEFAULT_URI` is not set in this shell.
- **`Unable to create bridge virbr50: Package not installed`:** reboot.
- **Sudo fails on some hosts only:** the three passwords differ.
- **The interface is not called `enp1s0`:** the `dnsmasq` and `dhcp_client` roles assume that name. Check `ip -br link`, then change `dnsmasq_interface` and `network_interface`.

## What this does not reproduce

- **Version numbers.** The same playbook installs whatever Debian and Grafana's repository offer on the day, so the structure rebuilds but the versions do not.
- **The install itself.** It is manual. A Debian preseed file, or a cloud image with cloud-init, would remove it. Neither has been tried here.
