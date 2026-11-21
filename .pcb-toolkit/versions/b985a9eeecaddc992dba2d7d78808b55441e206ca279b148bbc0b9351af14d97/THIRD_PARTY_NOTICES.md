# Third-party notices and attribution

## Original material

Copyright (c) 2026 Wiktor Krzeszewski, YOLO Consulting.
Original toolkit material is licensed under [Apache-2.0](LICENSE), subject to the file-level
exceptions described in [LICENSES/README.md](LICENSES/README.md). The owner selected
this license and attribution for the exported toolkit. [NOTICE](NOTICE) preserves
project/upstream attribution without adding license conditions. Private audit/customer/history
material is outside this export and outside this license scope.

## KiCad-derived project configuration

The following files reuse project/ERC configuration from the Arduino_Mega template
bundled with KiCad 10.0.6:

- templates/kicad/board.kicad_pro
- examples/connector-adapter/board/board.kicad_pro

Upstream author metadata identifies Caleb Reister (2021) and Jonathan Iapicco (2015).
Retain these attributions and the KiCad library contributors' terms. The ERC pin matrix
is unchanged. Project settings were selected/tightened for this toolkit; unrelated
source project settings, stock footprints and board/schematic geometry were not copied
into this template. The fictional example uses original CAD geometry/local libraries.

The upstream CC-BY-SA 4.0 license with the KiCad library exception is reproduced in
[LICENSES/KiCad-Libraries-License.md](LICENSES/KiCad-Libraries-License.md). These two
configuration files are not represented as Apache-2.0-only material. No upstream endorsement
is implied.

Exact upstream sources:
[license](https://gitlab.com/kicad/libraries/kicad-templates/-/raw/10.0.6/LICENSE.md),
[author metadata](https://gitlab.com/kicad/libraries/kicad-templates/-/raw/10.0.6/Projects/Arduino_Mega/meta/info.html),
[project](https://gitlab.com/kicad/libraries/kicad-templates/-/raw/10.0.6/Projects/Arduino_Mega/Arduino_Mega.kicad_pro).
See the [official library license explanation](https://www.kicad.org/libraries/license/).

## Separately installed dependencies and process scope

KiCad/pcbnew, Python, OS/container packages and stock KiCad libraries are installed
separately; their terms apply independently. This archive does not bundle their
binaries or stock component library collections. Supplier profiles cite capability
sources and record candidate settings, not complete supplier documents or qualification.

In-house assembly capabilities remain unknown until the local PCBA provider confirms
them. Record genuine confirmation in assembly.local_pcba_provider_confirmation for
inhouse projects. A license does not establish product/process qualification, stage
approval or authorization to manufacture. Internal reference-project geometry, history
and identifiers are excluded.
