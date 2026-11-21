# COMPENDIUM21 - current driver reference archive

Download Velluneo_Kompendium_Zasilacza_C16_C17_POWER20.zip, extract the whole
archive and open Velluneo_Kompendium/00_KOMPENDIUM.html. The Polish entry guide
links all four native layer SVG/PNG views, both-face4Krenders, schematic/assembly
PDFs, current BOM and dated purchase routes, source CAD/libraries, C17manufacturing
data, latest POWER20 thermal/loss study, selected LED19/C16calculations, transformer
drawings and retained open holds. It is an offline compendium, not a new release.

Base d89fdec0a59b99eebee64de0c1493af3eb8360b3. Design C16 / manufacturing C17 /
renders VIS18 / LED19 / POWER20. ZIP has153members; see archive-check.json for
exact digest/size and SOURCE_BINDING.json inside ZIP for copy provenance.
F.Cu/In1/In2 are top views; B.Cu is physically mirrored. Generic appearance models
remain illustrative; native editing project is the reviewed production source,
not the VIS18 visualization scene. No full external STEP library is represented.

All contents retain source uncertainty: nominal8.59Winput/6.54WLED/2.05Wheat/
76.2% is calculated; thermal paths, actual component internals and cooling remain
unverified. The same assumed path gives C1~99C in a selected case and fails the
tentative85C reserve goal. Passing sourceERC/DRC is not powered qualification.
Manufacturing/assembly/insulation/fault/life/thermal/process/human holds remain.
No new CAD/BOM/rule/approval, stock check, supplier upload/order or measurement.

build.py reproduces packaging with PyMuPDF and KICAD_CLI pointing to10.0.6.
It reads reviewed repository inputs, exports only to content/, then creates a
ZIP with member hashes/CRC checks. The content directory is build output and is
not duplicated in Git; the downloadable ZIP is the deliverable. Four independent
review reports and integration record identify the final assessed packet.
