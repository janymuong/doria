# <the symptom, in the user's words>

**Reported as:** TICKET: "The dashboard shows an exporter down on srv, but nobody was told."
**Affected:** one machine srv
**Time to resolve:** NN minutes
31 minutes since the ticket was opened

## What I saw
MAIN: Prometheus Alerts Show Node Exporter Down for 1 m(at the time) and severity critical
Prometheus Alerts shows alert for BackupMetrics Missing for srv- but this is tied to the above I supposes
Grafana Dashboard confirms it definitely has to do with node exporter; shows n/a for ram, disk etc(which are showing okay in client and mon)

Commands in the order I ran them, and what each one showed. Include the dead ends.
ssh'd into srv
did this command:
```bash
ops@srv:~$ ss -tulnp                                                                                                                                             
Netid         State          Recv-Q         Send-Q                                    Local Address:Port                 Peer Address:Port        Process         
udp           UNCONN         0              0                                             127.0.0.1:53                        0.0.0.0:*                           
udp           UNCONN         0              0                                         192.168.50.11:53                        0.0.0.0:*                           
udp           UNCONN         0              0                                        0.0.0.0%enp1s0:67                        0.0.0.0:*                           
udp           UNCONN         0              0                      [fe80::5054:ff:fe32:38e4]%enp1s0:53                           [::]:*                           
udp           UNCONN         0              0                                                 [::1]:53                           [::]:*                           
tcp           LISTEN         0              128                                             0.0.0.0:22                        0.0.0.0:*                           
tcp           LISTEN         0              32                                        192.168.50.11:53                        0.0.0.0:*                           
tcp           LISTEN         0              32                                            127.0.0.1:53                        0.0.0.0:*                           
tcp           LISTEN         0              128                                                [::]:22                           [::]:*                           
tcp           LISTEN         0              32                                                [::1]:53                           [::]:*                           
tcp           LISTEN         0              32                     [fe80::5054:ff:fe32:38e4]%enp1s0:53                           [::]:*                           
ops@srv:~$ systemctl status node-exporter
WARNING: terminal is not fully functional
Press RETURN to continue 
Unit node-exporter.service could not be found.
ops@srv:~$ ls
ops@srv:~$ ls -al
```
 couldnt figure anything from this; probably a deadend

I ran the journal command:
```sh
ops@srv:~$ journalctl -u node-exporter -n 50
Hint: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal' can see all messages.
      Pass -q to turn off this notice.
WARNING: terminal is not fully functional
Press RETURN to continue 
-- No entries --
ops@srv:~$ sudo journalctl -u node-exporter -n 50
[sudo] password for ops: 
WARNING: terminal is not fully functional
Press RETURN to continue 
 ESC[A-- No entries --
ops@srv:~$ sudo journalctl -n 50 | grep node-exporter
Nov 12 11:35:56 srv systemd[1]: prometheus-node-exporter-nvme.service: Deactivated successfully.
Nov 12 11:35:56 srv systemd[1]: Finished prometheus-node-exporter-nvme.service - Collect NVMe metrics for prometheus-node-exporter.
Nov 12 11:35:57 srv systemd[1]: prometheus-node-exporter-apt.service: Deactivated successfully.
Nov 12 11:35:57 srv systemd[1]: Finished prometheus-node-exporter-apt.service - Collect apt metrics for prometheus-node-exporter.
Nov 12 11:35:57 srv systemd[1]: prometheus-node-exporter-apt.service: Consumed 1.142s CPU time, 31.9M memory peak.
Nov 12 11:51:27 srv systemd[1]: Starting prometheus-node-exporter-apt.service - Collect apt metrics for prometheus-node-exporter...
Nov 12 11:51:27 srv systemd[1]: Starting prometheus-node-exporter-nvme.service - Collect NVMe metrics for prometheus-node-exporter...
Nov 12 11:51:27 srv systemd[1]: prometheus-node-exporter-nvme.service: Deactivated successfully.
Nov 12 11:51:27 srv systemd[1]: Finished prometheus-node-exporter-nvme.service - Collect NVMe metrics for prometheus-node-exporter.
Nov 12 11:51:29 srv systemd[1]: prometheus-node-exporter-apt.service: Deactivated successfully.
Nov 12 11:51:29 srv systemd[1]: Finished prometheus-node-exporter-apt.service - Collect apt metrics for prometheus-node-exporter.
Nov 12 11:51:29 srv systemd[1]: prometheus-node-exporter-apt.service: Consumed 1.597s CPU time, 32M memory peak.
Nov 12 12:01:33 srv sudo[1021]:      ops : TTY=pts/0 ; PWD=/home/ops ; USER=root ; COMMAND=/usr/bin/journalctl -u node-exporter -n 50
ops@srv:~$ logout
Connection to 192.168.50.11 closed.
```

so from this node exporter was deactivated/service stopped, and so it has to be brought up using systemd (but can be done using ansible for an effective solutin)
## Cause
One or two sentences.
node exporter was stopped

## Fix
The exact commands.
sudo systemctl start prometheus-node-exporter-nvme
ansible-playbook site.yml --ask-become-pass (nuclear fix)

## Check that it worked
Grafana reported mem, cpu, io usage and the the rest of the metrics
saw that the user's side checks out as well
How I confirmed it from the user's side, and from the monitoring side.

## Did monitoring catch it?
two alerts:
1 - NodeExporterDown (1 active)

alert: NodeExporterDown
expr: up{job="node"}
  == 0
for: 1m
labels:
  severity: critical
annotations:
  summary: The exporter on {{ $labels.host }} is not answering

2 - BackupMetricsMissing (1 active)

alert: BackupMetricsMissing
expr: absent(doria_backup_success{host="srv"})
for: 1h
labels:
  severity: warning
annotations:
  summary: srv is not reporting backup metrics, the job may never have run

I am not sure the second one is related to the node exported one; but the point is monitoring caught the problem

Which alert fired and how long it took, or what would have caught it.

## Prevention

What would stop this happening again.

not to stop node exporter service from running

