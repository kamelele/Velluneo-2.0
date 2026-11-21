# Independent local-toolkit preview review

Reviewer: /root/spec_change. Scope: deterministic source/archive/recipe identity and local installation eligibility only. This is an actual independent agent review, not a human approval, maintainer release authentication, native CAD validation or design-stage approval.

## Result

Supported for **local preview installation** under the owner's explicit request to use pcb-agent-toolkit, provided the installer uses the exact archive identity below and `--allow-candidate`. There is no source/recipe/identity discrepancy blocking that local use. Keep candidate status and all existing project/human gates. Installation is followed by the real pinned launcher `status` and `doctor`; no CAD operation may be reported verified until its actual environment checks pass.

Expected installable-archive SHA-256, independently obtained from a separate deterministic rebuild:

`15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4`

Archive size: 657358 bytes. Package 0.7.1-preview.3; ruleset 0.7.1; candidate_only=true; publication_ready=false. This is a locally rebuilt reviewed preview, **not an asserted public release checksum**.

## Trusted input and actual checks

- Owner-supplied source ZIP SHA-256: b43c4b7a9c331408b66cb56faee56708a464c3d5d23efb9a3c21974c101e6250.
- Recorded project/source manifest SHA-256: 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822. The exact extracted manifest and every declared file match the supplied ZIP, with no extra source files.
- Recipe: distribution/package.json, SHA-256 74788aa631a7686c6c7ce2fcb654e0328ebdd0a0b06482147a19bf6b6659cb9d. The explicit file list, per-file hashes, candidate metadata and installer protocol 1 were inspected. No recipe/source edit was made.
- Actual `package_toolkit.py verify-tree` returned exit 0 with the recorded manifest.
- Actual separate `build-candidate` returned exit 0, writing only this review's temporary directory. Fixed timestamps, sorted members and ZIP_STORED encoding were independently inspected.
- Actual archive `verify --sha256` returned exit 0. Rebuilt archive has the exact source member set and byte-identical files/manifest.
- The independently built archive is byte-for-byte equal to the coordinator's separate archive at tmp/toolkit-package/pcb-toolkit-0.7.1-preview.3.zip. Its digest was compared only after obtaining the independent build's identity.
- LICENSE, NOTICE, THIRD_PARTY_NOTICES.md, LICENSES/README.md and LICENSES/KiCad-Libraries-License.md are all preserved byte-for-byte. Original Apache-2.0 material is not mislabeled as covering the separately identified KiCad-derived configuration terms.

Commands executed from the unchanged separate toolkit tree:

```sh
python scripts/package_toolkit.py verify-tree .
python scripts/package_toolkit.py build-candidate --root /workspace/scratch/d4c1ae92033a/toolkit-reference/pcb-agent-toolkit-main --output /workspace/scratch/d4c1ae92033a/tmp/toolkit-review/independent-0.7.1-preview.3.zip
python scripts/package_toolkit.py verify /workspace/scratch/d4c1ae92033a/tmp/toolkit-review/independent-0.7.1-preview.3.zip --sha256 15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4
```

## Provenance and qualification boundaries

The trust basis is the owner's supplied source snapshot, the recorded matching project manifest and this independent recipe/rebuild record. Hash agreement does not authenticate a maintainer, prove absence of malicious behavior or provide a public signed release. No public release/tag provenance is asserted. The user source archive is not itself the installer package; the reviewed deterministic export is.

The first-project instruction explicitly permits an explicitly reviewed preview rebuilt with its declared recipe and an expected digest from the review record. This report supplies that independently derived digest; it does not invent release authority or demand an unnecessary external maintainer approval. The owner has already requested using this toolkit; the `--allow-candidate` installation expresses that local candidate choice, not electrical/manufacturing approval.

The installation implementation was inspected for content-pinned selection, protocol/bootstrap identity checks, refusal of unowned namespaces/custom launchers, owned launcher/lock/version paths and no automatic CAD migration. No project installation was performed by this reviewer. Inspect destination ownership/state before installation and preserve existing source/configuration.

Supported declared tools remain KiCad 10.0.6 with matching pcbnew, Python 3.11+, tested x64 Windows or headless Ubuntu 26.10. The historical 10.0.8 project context is not automatically migrated or qualified by this review. Full standalone/native-CAD validation, current-host qualification, installed `doctor`, ERC/DRC, connectivity, spatial checks, all four complete design-stage reviews and genuine owner stage approval remain distinct work.

No shared device source, library, CAD, rules, installer destination or approvals were changed. Writes were confined to tmp/toolkit-review. The generated `.private-review.json` is a local build companion; do not publish it as a release asset.

Machine-readable actual identity/check details: independent-checks.json.
