# Version, update and support policy

Pin an exact archive and manifest/content identity. Human-friendly package/ruleset
versions aid communication; hashes determine the actual inputs. Never move a published
version/tag to different contents. Corrections require a new version and new review.
No dependency execution fetches latest automatically.

During the current pre-release phase, keep compatible development increments in the
0.7.x series (0.7.1, 0.7.2, ...), including incremental features, fixes and onboarding.
Do not bump VERSION simply because an issue/PR closes; planning/documentation changes
need no bump unless identifying a new package. A minor bump such as 0.8.0 requires an
explicitly agreed substantial milestone or incompatible contract change, with migration
notes. Do not hide incompatibility in a patch. A major release requires a separate
readiness decision; version numbers do not indicate percentage complete.
Candidate suffixes identify successive internal review builds, never production,
manufacturing or redistribution approval. Published versions remain immutable.

Every change records the problem/result, migration/review impact, supported tools,
actual checks and remaining limitations in the changelog. Keep public package identity
distinct from private history; the private release ledger links source/export/public
revisions and community PRs. An unpublished candidate has no public Git revision;
its exact source-content revision is its manifest SHA256. Git/tag provenance can be
added honestly when public release metadata exists.

Installer protocol 1 has a stable project bootstrap. Archives must declare that
protocol and contain matching bootstrap code. Incompatible launcher/lock migrations
need a separate reviewed migration; updates must not overwrite a customized launcher.
The current parser/build/installer accept review-candidate packages only. Public
publication and approved release-format acceptance remain separate follow-up work.

Validated scope is exact KiCad 10.0.6 (Ubuntu package 10.0.6+dfsg-1), Python 3.11+ on
the tested x64 Windows host and headless Ubuntu 26.10 container. Actual reports record
runtime versions. New KiCad/package/platform versions need compatibility tests before
scope expansion; no automatic conversion of ongoing projects. Existing default-assembly,
rectangular spatial, topology/physical/process limitations remain unchanged.

Report issues with pinned versions/manifest hash, platform/tools, reproduction using
non-confidential sources, actual results and scope. Triage source/config/tool failure
separately from project findings. Keep regressions, accepted scope and deferred
requirements explicit. Synthetic reviews are not actual independent agent/human work;
real recipient validation is a separate acceptance step.
