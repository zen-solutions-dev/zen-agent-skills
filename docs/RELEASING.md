# Releasing

How a maintainer cuts a tagged release of the kit with [`release.py`](../scripts/release.py). The script prepares the release; tagging and pushing stay with the person, by design.

## Where the version lives

A top-level `VERSION` file holds the kit's one version, `MAJOR.MINOR.PATCH`; it was committed at `0.2.0` on 2026-11-25, and the Claude Code plugin's version is built from it by `build-adapters.py`. Were it absent the script takes the current version as `0.0.0` and says so, and it also refuses any version not above the highest `### vX.Y.Z` heading under `## Releases` in [`CHANGELOG.md`](../CHANGELOG.md), so a release is never numbered twice.

## Cutting a release

1. Make sure the `### Unreleased` section under `## Releases` in the changelog summarises what ships.
2. Preview, which writes nothing:

   ```bash
   python scripts/release.py --bump minor --dry-run
   ```

   Use `--bump major`, `--bump patch`, or `--version X.Y.Z` instead as fits, and `--date YYYY-MM-DD` to date it other than today.
3. Run the same command without `--dry-run`. It writes `VERSION` and renames the Unreleased heading to `### vX.Y.Z (date)`, keeping its text, with a fresh `### Unreleased` above it. The task log is never touched.
4. Commit `VERSION` and `CHANGELOG.md` on their own and merge them as usual.
5. Tag the merged commit and push the tag with the two commands the script printed:

   ```bash
   git tag -a vX.Y.Z -m "Zen Agent Skills vX.Y.Z"
   git push origin vX.Y.Z
   ```

`python scripts/release.py --check` confirms at any time that `VERSION` is a semantic version and that the changelog has a section for it.

## Exit codes

`0` done, `1` refused (a malformed or non-increasing version, a tag that exists, a changelog with no `## Releases` heading), `2` could not run (a file missing or unreadable). The precedence is the one [`run-checks.py`](../scripts/run-checks.py) uses.
