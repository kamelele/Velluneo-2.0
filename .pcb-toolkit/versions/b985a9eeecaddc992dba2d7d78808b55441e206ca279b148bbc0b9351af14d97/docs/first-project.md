# Your first project

Start here if you have an idea but do not know PCB design. You need a repository
for your device, an agent you can use, and an explanation of what you want to build.
You do not need to arrive with a component list, KiCad files or a PCB manufacturer.

## Agent entry point

The kickoff prompt supplies the user's idea and points here; it is not a second
copy of the workflow. Agent: read this guide, [Start here](start-here.md), and the
[project instructions](../templates/project/AGENTS.md) from the selected toolkit
version. Follow those project instructions for stage gates and required evidence;
use [installation](installation.md) for setup and version pinning. Work in the
user's device repository. Handle setup within available permissions and explain
actual missing access/tools. Ask the user's preferred conversation language and
write project artifacts in English. Prepare a specification, open questions and a
staged plan as the first review packet, before beginning the schematic.

## 1. Open a project and start the conversation

Create/select a repository for your device and open your agent there. Keep it separate
from the toolkit repository. Give the agent access to the toolkit files and copy the
[kickoff prompt in the README](../README.md#start-with-an-idea-and-an-agent).
This brief can be used with Claude Code or Codex. It does not install an agent,
authorize missing tools or prove environment-specific CAD/delegation support.

Describe the outcome in your own words. For example: "I want a light that turns on
when a cupboard opens." You can say "I don't know" to technical questions. Do not
send credentials, customer designs or private project records to toolkit maintainers.
Everything needed for your project belongs in your project repository.
No fork, project registration or disclosure of your use is required.

## 2. Let the agent ask and explain

The agent starts with at most three questions at a time, such as:

- What should the device do, and who will use it?
- Where will it operate and how do you expect to power it, if you know?
- Is the immediate goal to explore an idea, build a prototype or prepare production?

It follows up on your answers, reuses information already provided and explains
technical choices before asking you to choose. It records requirements, proposals
and unknowns separately. Supplier, assembly, parts and mechanical choices are developed
during specification rather than demanded as a completed technical form up front.
Later-stage unknowns need not stop the initial interview; they must be resolved by
their relevant gate. Missing evidence is never filled with an invented value.

## 3. Review a specification before a circuit

The first review packet contains the device's purpose and scope, proposed behavior
and interfaces, known constraints, open questions, how success will be checked,
fabrication/assembly options and the next steps. It explains what you can decide and
what requires competent technical review. Your acceptance of desired behavior does
not certify an electrical design, product safety or suitability for manufacturing.

Only after the specification is ready and genuinely approved does schematic work
begin. Each following stage has its own packet and human review: schematic/libraries,
placement, routing and release. The agent explains progress, actual checks, limitations
and the decisions needed. It does not approve its own work or fabricate independent
reviewers. No order or physical test is authorized by merely starting the conversation.

## 4. Let the agent handle the technical setup

Agent: read [Start here](start-here.md), [installation](installation.md), and
[project instructions](../templates/project/AGENTS.md) before CAD work. Inspect existing
project files and preserve them. Select an actual release or explicitly reviewed preview,
verify its trusted checksum, pin it and use the installed project launcher.

If only a source checkout is available, distinguish it from an installable archive.
An explicitly reviewed preview can be rebuilt with its declared recipe; its expected
digest must come from the trusted review record. Do not silently use an empty default
branch, select latest, invent a release/checksum or request private repository access.
If package/access/tooling is unavailable, explain the actual gap and continue the
requirements discussion where possible. Run environment checks before CAD operations;
never report tool failures as passes. Propose profile choices for approval instead of
silently treating example command arguments as the user's manufacturing decisions.

The technical guide contains commands and file contracts for the agent; you do not
have to type them all manually. Actual CAD access, available delegation contexts and
human reviewers must be established honestly. Validated native KiCad checks are not
proof that every Claude Code/Codex setup can autonomously operate KiCad.

## What to expect next

The agent keeps specifications, decisions, local libraries, sources and evidence in
your repository, using the selected toolkit version. It shows schematic/PCB views,
calculations, check results and open issues at the appropriate stage. It explains
remaining expert review or physical validation needs. Your project does not require
registration with this toolkit or centralized approval by toolkit maintainers.

For a worked CAD example after the initial discussion, see the
[original connector adapter](../examples/connector-adapter/README.md). Its authored
review perspectives and synthetic records are demonstrations, not your approvals.
