# Releasing

How a maintainer cuts a tagged release of the kit with [`release.py`](../scripts/release.py). The script prepares the release; tagging and pushing stay with the person, by design.

## Where the version lives

A top-level `VERSION` file holds the kit's one version, `MAJOR.MINOR.PATCH`; it was committed at `0.1.0` on 2026-11-25, matching the last tagged release `v0.1.0`, so the next release, `--bump minor`, is `0.2.0`, and the Claude Code plugin's version is built from it by `build-adapters.py`. Were it absent the script takes the current version as `0.0.0` and says so, and it also refuses any version not above the highest `### vX.Y.Z` heading under `## Releases` in [`CHANGELOG.md`](../CHANGELOG.md), so a release is never numbered twice.

## Cutting a release

1. Make sure the `### Unreleased` section under `## Releases` in the changelog summarises what ships.
2. Preview, which writes nothing:

   ```bash
   python scripts/release.py --bump minor --dry-run
   ```

   Use `--bump major`, `--bump patch`, or `--version X.Y.Z` instead as fits, and `--date YYYY-MM-DD` to date it other than today.
3. Run the same command without `--dry-run`. It writes `VERSION` and renames the Unreleased heading to `### vX.Y.Z (date)`, keeping its text, with a fresh `### Unreleased` above it. The task log is never touched.
4. Commit `VERSION` and `CHANGELOG.md` on their own and merge them as usual.
5. Tag the merged commit, naming it by id, and push the tag with the two commands the script printed:

   ```bash
   git tag -a vX.Y.Z -m "Zen Agent Skills vX.Y.Z" <sha>
   git push origin vX.Y.Z
   ```

   `<sha>` is the commit that landed the release on `main`. When `main` takes squash merges, that is the squash commit, not the head of the release branch, so a bare `git tag` run on the branch would tag the wrong commit. For v0.2.0, pull request #119 was squash-merged as `e694817`, and the tag points there.

   A cloud session cannot push the tag: its git proxy refused the `v0.2.0` push with HTTP 403 on 2026-11-25. Run these two commands yourself from your own checkout.
6. When the release was a squash merge, bring `developer` back level with `main`: merge `main` into `developer` on a branch and open a pull request that you merge with a merge commit, not a squash, so `main`'s release commit becomes part of `developer`'s history; a squash here leaves the next release from `developer` diverging again. The squash commit exists only on `main`, so without this step the two trees disagree. For v0.2.0 this was pull request #120, from the branch `zen/rollout-handoff-2026-11-25`.

`python scripts/release.py --check` confirms at any time that `VERSION` is a semantic version and that the changelog has a section for it.

## Exit codes

`0` done, `1` refused (a malformed or non-increasing version, a tag that exists, a changelog with no `## Releases` heading), `2` could not run (a file missing or unreadable). The precedence is the one [`run-checks.py`](../scripts/run-checks.py) uses.
