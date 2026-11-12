# 2. The virtual machines and SSH access

**Built:** three Debian 13 VMs on `doria-lan`, reachable over SSH with a key.

| VM | RAM | Disk |
|---|---|---|
| mon | 1.5 GB | 10 GB |
| srv | 1 GB | 10 GB |
| client | 1 GB | 10 GB |

That leaves about 4.5 GB for the host on an 8 GB machine.

## Install

- The netinst ISO was checked against `SHA256SUMS` from the ISO directory. The `SHA256SUMS` in the installer `images/` directory lists other files and verifies nothing.
- The ISO lives in `/var/lib/libvirt/images`. QEMU cannot read files inside a home directory. ISOs are in `.gitignore`.
- `doria-lan` has no DHCP at this point, so the installer cannot configure the network by itself. The address, mask, gateway and name server were entered by hand.
- The root password was left empty, which gives the `ops` user sudo. Only the SSH server and standard system utilities were selected.

## Command (shown for `mon`)

    sudo virt-install --name mon --memory 1536 --vcpus 1 \
      --disk size=10,format=qcow2 \
      --cdrom /var/lib/libvirt/images/debian-13.7.0-amd64-netinst.iso \
      --network network=doria-lan,model=virtio \
      --osinfo detect=on,require=off --graphics spice --noautoconsole

## SSH

    ssh-keygen -t ed25519 -f ~/.ssh/doria_ed25519 -C "doria-lab"
    ssh-copy-id -i ~/.ssh/doria_ed25519.pub ops@192.168.50.10

Host aliases for `mon`, `srv` and `client` went into `~/.ssh/config`.

## What went wrong

- A server showing `graphical.target` as its default is normal on Debian. With no display manager installed it does nothing.
- "terminal is not fully functional" means the VM does not know the host's `TERM` value. Use `--no-pager`, or connect with `TERM=xterm-256color ssh srv`.
- `AF_VSOCK` lines on the console are harmless.
