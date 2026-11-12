# doria

a small office network that watches itself

> three vms on one linux host, configured with ansible: dhcp and dns, monitoring and alerts, and a nightly backup that is restored and checked every night.  
> **more**z: find files and run the network in [context.md](context.md) and in the [walkthrough](./walkthrough/) directory.

```mermaid
flowchart LR
    ansible["ansible on the host<br/>(ssh to every vm)"]
    net(("internet"))

    subgraph lan["doria-lan  192.168.50.0/24  (libvirt nat, gateway 192.168.50.1)"]
        subgraph mon["mon  192.168.50.10"]
            prom["prometheus :9090"]
            am["alertmanager :9093"]
            logger["alert-logger :9199"]
            graf["grafana :3000"]
            bb["blackbox_exporter :9115"]
            nem["node_exporter :9100"]
        end
        subgraph srv["srv  192.168.50.11"]
            dns["dnsmasq  dhcp :67  dns :53"]
            bkp["backup and restore test<br/>(systemd timers)"]
            nes["node_exporter :9100"]
        end
        subgraph client["client  192.168.50.20"]
            dhcpc["dhcp client"]
            nec["node_exporter :9100"]
        end
    end

    ansible -.-> lan
    prom -->|scrape| nem
    prom -->|scrape| nes
    prom -->|scrape| nec
    prom -->|probes through| bb
    bb -.->|icmp, http, dns| dns
    prom -->|alerts| am
    am -->|webhook| logger
    graf -->|queries| prom
    dhcpc -->|dhcp and dns| dns
    dns -->|forwards names| net
    bkp -->|metrics file| nes
```


| tool | for |
|---|---|
| libvirt, qemu | the virtual machines and the `doria-lan` network |
| debian 13 | the guest operating system |
| ansible | all configuration after the install |
| dnsmasq | dhcp and dns |
| prometheus, node exporter, blackbox exporter | metrics and probes |
| alertmanager | grouping and routing alerts |
| grafana | dashboards, provisioned from files |
| systemd timers, bash | the backup and the restore test |
