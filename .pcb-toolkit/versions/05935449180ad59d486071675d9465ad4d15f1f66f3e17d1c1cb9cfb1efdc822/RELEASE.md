# 0.7.1-preview.3

Short kickoff prompt and single documented entry point, ruleset 0.7.1.
The README prompt now contains only the idea, user experience and a pointer to
project-start instructions. Workflow/setup/language details live in the guide and
linked project instructions rather than a duplicated prompt. No fork or central
registration is required. Published preview.1 and preview.2 remain unchanged.
README now provides a copyable kickoff prompt and links to a beginner guide; start-here
routes newcomers to the interview before technical commands. Published preview.1
remains unchanged. This package changes documentation and package metadata only.
Runtime/CAD/profile/rule inputs are byte-identical to preview.1; its recorded Windows
and Ubuntu native validation remains prior-code evidence, not a fresh run of preview.2. This contains editable
ERC/DRC configuration, product/interface/connectivity/spatial checks, project and
review-role templates, installation/update/rollback tools and original CAD examples.
Apache-2.0 + NOTICE applies to original material; preserve the separately documented
KiCad terms for derived configuration. No private audit history or customer sources
are included. Users run checks, reviews and approvals in their own project repositories.

## Support and limits

Validated tool baseline: exact KiCad 10.0.6 with matching pcbnew, Windows and
Ubuntu 26.10 amd64 (KiCad package 10.0.6+dfsg-1). Python 3.11+ is required.
The candidate archive protocol is deliberately retained: candidate_only=true and
publication_ready=false describe the protocol's qualification state. Installation
requires --allow-candidate even when this archive is attached to a GitHub prerelease.
These fields do not mean that a published preview is a stable/qualified product.

Checks cover the documented default schematic assembly and supported rectangular
spatial constraints/outer-copper geometry. Supplier/process profiles require confirmation
for the actual service/order. CAD results do not establish physical operation, process
qualification or safety/EMC compliance. Independent recipient trials, separate validated
Claude Code/Codex startup guides and the full community synchronization exercise are
not claimed. Project-specific hardware release gates remain in your project.

## Build and validate the actual release

From an unchanged checkout, choose a fresh output path:

```sh
python scripts/package_toolkit.py build-candidate --root . --output .work/release/pcb-agent-toolkit-0.7.1-preview.3.zip
python scripts/package_toolkit.py verify .work/release/pcb-agent-toolkit-0.7.1-preview.3.zip
python scripts/package_toolkit.py extract .work/release/pcb-agent-toolkit-0.7.1-preview.3.zip .work/release/extracted
cd .work/release/extracted
python -I scripts/validate_candidate.py
```

The archive recipe/manifest excludes Git history and runtime outputs. Validate a clean
extraction, not a checkout containing .git or generated files. Windows locates KiCad's
bundled Python; Linux needs the matching pcbnew module. The pinned Dockerfile permits
the same extracted test without runtime networking. The PR workflow runs that path;
its result is evidence only once the hosted run actually succeeds.

## Maintainer publication

Review the PR and source revision, then merge before creating the public tag/release.
Tag that exact merged revision as v0.7.1-preview.3, rebuild and verify the archive and
run standalone validation. A preview is a GitHub **prerelease**, not a stable latest.
Attach exactly the ZIP, its .sha256 companion and PACKAGE-MANIFEST.json extracted from
that ZIP. Verify the assets match the reviewed source/manifest. GitHub-generated source
archives are not the installable toolkit package. Never upload .private-review.json.
Do not move an existing published tag or replace assets; corrections need a new identity.
The first export PR prepares this release but does not merge or publish it automatically.
