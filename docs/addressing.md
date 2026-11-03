# addressing plan

network: 192.168.50.0/24 (virtual network `doria-lan`, bridge `virbr50`)

| host   | address         | role                                  |
|--------|-----------------|---------------------------------------|
| host   | 192.168.50.1    | gateway (the arch machine)            |
| mon    | 192.168.50.10   | Prometheus, Grafana, Alertmanager     |
| srv    | 192.168.50.11   | DHCP/DNS, file share, backup target   |
| client | 192.168.50.20   | provisioned like a new laptop         |
