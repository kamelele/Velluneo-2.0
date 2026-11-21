Compatibility candidate: **0.7.2-velluneo.1**, ruleset **0.7.2**. See [bounded scoped policy extension](docs/scoped-policy.md). Not an upstream release or hardware approval.

# pcb-agent-toolkit — first preview

This candidate contains editable rules, tools, instructions, tests and original
demonstrations. Its manifest identifies the exact files and tested tool scope.
Original material is under [Apache-2.0](LICENSE); see [license scope](LICENSES/README.md)
and [third-party notices](THIRD_PARTY_NOTICES.md) for KiCad-derived configuration.
[NOTICE](NOTICE) records project/upstream attribution.
Repository: [wiktor426/pcb-agent-toolkit](https://github.com/wiktor426/pcb-agent-toolkit).
This is the 0.7.1-preview.3 prerelease, using the tested candidate archive protocol.
Read [release notes and reproducible release procedure](RELEASE.md).
There is no central project registration or approval service: keep project requirements,
reviews and evidence in your own project repository. Maintainers distribute the toolkit.

## Start with an idea and an agent

You do not need to know KiCad, PCB manufacturing or which components to buy to begin.

1. Create an empty repository for **your device**, separate from this toolkit.
2. Open your agent in that project repository and give it access to this toolkit.
   You can use Claude Code or Codex; the brief below is shared. Actual tool access
   and environment support must still be checked by the agent.
3. Paste this prompt, replacing the idea in brackets:

```text
I want to build an electronic device: [describe your idea].
I do not know electronics. Use pcb-agent-toolkit and follow its project-start
instructions at https://github.com/wiktor426/pcb-agent-toolkit/blob/main/docs/first-project.md.
Guide me through the process, ask questions and explain the decisions.
```

Your first result should be a specification and plan you understand, with unresolved
questions visible. The agent then proposes schematic, placement, routing and release
work stage by stage. Read [Your first project](docs/first-project.md) for what to expect.
The agent does not gain CAD control or independent reviewers merely from this prompt.

## Installation details for the agent or experienced user

Read [Start here](docs/start-here.md), [existing projects](docs/existing-projects.md),
[contribution guidance](docs/contributing.md) and the
[complete original example](examples/connector-adapter/README.md).

Use Python 3.11+ and the exact pinned KiCad 10.0.6, including its matching pcbnew
Python runtime for CAD checks. Verify the package before using it:

```sh
python scripts/package_toolkit.py verify-tree .
python scripts/toolkit_install.py install ../my_project_repo --archive ../TOOLKIT.zip --sha256 EXPECTED_SHA256 --allow-candidate
```

Create/select the project repository first. From it, use pcb-toolkit.py doctor and
pcb-toolkit.py run init boards/my_board --vendor jlcpcb --assembly inhouse.
See [pinned installation and updates](docs/installation.md),
[version/support policy](docs/version-policy.md) and [changelog](CHANGELOG.md).
Read [project instructions](templates/project/AGENTS.md), then complete the independent
requirements, connectivity and spatial documents, select/confirm the actual product,
fabrication and assembly process, and submit each stage for human review.
init creates drafts and configuration, not a schematic, working PCB or approvals.

- [Local PCBA provider capabilities and rule template](docs/local-pcba-provider.md)
- [Configuration preview/apply/rollback](docs/configuration-adoption.md)
- [Product requirements and interfaces](docs/product-requirements.md)
- [Intended connectivity](docs/intended-connectivity.md)
- [Spatial constraints](docs/spatial-constraints.md)
- [Project contract](docs/project-contract.md) and [review evidence](docs/reviews.md)
- [Coordinator and four review roles](docs/agent-workflow.md)
- [Original requirements example](examples/multi-board/README.md)
- [Synthetic workflow walkthrough](examples/agent-workflow/README.md)
- [Original connectivity fixtures](examples/connectivity/README.md)

## Validate this extracted candidate

```sh
python -I scripts/validate_candidate.py
```

On Windows the runner locates KiCad's bundled Python; --cad-python selects it explicitly.
On Ubuntu use the distribution Python with the matching pcbnew module. Output is in
.work/package-validation and generated reports/. These runtime outputs are not release
inputs. The selected tests intentionally omit audit-only counting tests and require no
private inventory, repository history or authentication.

The bundled Dockerfile pins a headless Ubuntu 26.10 environment and KiCad package
10.0.6+dfsg-1. Build with only infra as context, then test a disposable extracted tree:

```sh
docker build -f infra/Dockerfile.ubuntu-test -t pcb-toolkit-test infra
docker run --rm --network none --mount "type=bind,source=$PWD,target=/workspace" pcb-toolkit-test
```

## Integrity and rebuilding

PACKAGE-MANIFEST.json inventories exact files. The archive checksum must come from a
trusted release/review record; hashes alone do not authenticate an author or approval.
The included normalized recipe can reproduce the same candidate archive from its
unchanged extracted sources:

```sh
python scripts/package_toolkit.py build-candidate --root . --output ../rebuilt.zip
python scripts/package_toolkit.py verify ../rebuilt.zip
```

The companion .private-review.json is maintainer bookkeeping and must not be published
as a release asset. It is never embedded in the archive. This candidate builder cannot
publish releases or grant licenses. Packaging does not install an agent runtime or
qualify any product, manufacturing process, safety/EMC performance or actual approvals.
Installation/update guidance and an original complete example are included. Independent
recipient trials and separate Claude Code/Codex entry guides are not yet validated.
Read [license scope and notices](THIRD_PARTY_NOTICES.md).
