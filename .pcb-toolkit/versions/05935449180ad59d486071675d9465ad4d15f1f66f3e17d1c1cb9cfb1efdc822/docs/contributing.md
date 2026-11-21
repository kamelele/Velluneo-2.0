# Feedback and contributions

Current status: first technical preview. Use the issues and pull requests at
https://github.com/wiktor426/pcb-agent-toolkit. Original material uses Apache-2.0;
preserve the upstream terms in THIRD_PARTY_NOTICES.md for KiCad-derived files.
No private repository access or central project registration is needed. Maintainers
review contributions and integrate accepted changes into their canonical sources
before exporting them again; public author/PR references must be preserved.
The full community intake/release synchronization trial remains unvalidated.

For a bug report, include the package/ruleset version and manifest SHA256, actual
KiCad/Python/platform, steps, expected and observed results, relevant rule/object IDs
and fresh reports. Provide original non-confidential inputs. Remove credentials,
customer designs, Drive inventories and internal links. A CAD pass does not establish
physical product performance or process capability.

For a shared rule/profile change, provide the current rule ID, proposed change,
rationale, authoritative basis/date/scope where applicable, migration/review impact,
positive and intentional negative examples, and actual validation results. Distinguish
historical settings, product needs, supplier limits and organization policy. A local
approved exception does not silently become shared policy.

Planned public contribution flow: fork the public exported toolkit, create a focused
branch, describe/test the change and propose a PR. Maintainers import and integrate
the proposal in the private canonical development repository, review/test it, preserve
author attribution, then reconcile public acceptance and a reviewed export/release.
Contributors need no private access. Maintainers must not overwrite accepted community
changes or export private history. Public contribution templates, concrete URLs,
contribution setup and release automation remain separate publication work; no working
public PR destination or automated bridge is claimed here.

Use the bundled tests and original example to reproduce relevant checks. Do not
fabricate independent reviews, physical measurements or human approvals. Report missing
capabilities as gaps; agents must retain stage gates and explicit release blockers.

When distributing changes to Apache-2.0 material, mark modified files prominently
and preserve applicable attribution/license notices, including the relevant information
from NOTICE. NOTICE is informational and does not add license conditions. Contributions
submitted for inclusion follow Apache-2.0 section 5 unless explicitly stated otherwise
or covered by a separate agreement. Preserve upstream KiCad terms for its derived files.
