# 8. Backups and restore tests

**Built:** a nightly backup of `/srv/share` on `srv`, and a nightly test that restores the newest backup and checks it.

Ansible can rebuild `srv` from the repo, but not the files people put on it. That is what the backup covers.

## How it works

- `doria-backup backup` writes a `tar.gz` archive, a manifest with a SHA-256 checksum for every file, and a checksum for the archive. Files are written under a temporary name and renamed when complete. The newest 7 sets are kept. An empty source is treated as a failure.
- `doria-backup restore-test` checks the archive checksum, unpacks the newest archive into a temporary directory, and compares every restored file with the manifest. The temporary directory is removed afterwards.
- systemd timers run the backup at 02:00 and the test at 03:00. `Persistent=true` makes a missed run happen after boot, which matters for machines that are off at night.
- Both write metrics through the node exporter textfile directory. A failed run reports 0 but keeps the old "last success" time, so the stale alerts still work.
- Alerts: BackupFailed, BackupStale (over 26 hours), RestoreTestFailed, RestoreTestStale, BackupMetricsMissing (the job never ran).
- The dashboard "Doria: backups" shows the age of the last backup, the age of the last passing test, the test result and the archive size.

## Tests and results

- **Damaged archive:** four bytes of the newest archive were overwritten. The test failed with a checksum mismatch, `RestoreTestFailed` fired about two minutes later, and it resolved after a fresh backup and test.
- **Accidental deletion:** `/srv/share/finance` was deleted and restored from the archive with `tar`. A check against the manifest printed nothing, which means every file matched.
- `tar` run as root keeps the owners and modification times stored in the archive.

## Limits

- The archives are on the same disk as the data. They protect against deleted or damaged files, not against the disk failing.
- Only the newest archive is tested.
- The script picks the "newest" archive by file name, which depends on the clock being right.
