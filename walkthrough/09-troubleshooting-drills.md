# 9. Troubleshooting drills

**Built:** `scripts/drill`, which opens a practice ticket by breaking something in the lab. Every fault is temporary, and `scripts/drill close` undoes it and re-runs the playbook.

    scripts/drill open [1-6]
    scripts/drill time
    scripts/drill close

The method is in `docs/troubleshooting/README.md`: work from the bottom up (link, address, route, reach by IP, names, service, logs, config) and change one thing at a time. The same file lists which ports should be listening on each machine.

## How a ticket is worked

1. Read the complaint, and check whether it is one person, one machine or everyone.
2. Use only the tools a support person has: dashboards, SSH or the console, `ip`, `ss`, `ping`, `dig`, `tcpdump`, `journalctl`.
3. Fix it, then confirm from the user's side as well as from the dashboard.
4. Write a note from `docs/troubleshooting/TEMPLATE.md`, including the dead ends.

The notes are in `docs/troubleshooting/`.

## What the drills showed

- Monitoring checks from one place, so a user can be broken while every panel is green.
- A running process is not the same as a reachable service.
- Detection and notification are separate. A broken alert pipeline looks like a quiet day.
- Fix the notification path before the fault, or you never learn whether anyone would have been told.
