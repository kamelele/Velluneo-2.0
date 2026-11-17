# Mechanical space illustration — not PCB placement

MECH-PREVIEW-01,2026-11-17. The owner asked to see the board in the conversation. The current native artifact is a schematic; its incomplete stage does not have an accepted PCB layout. This bounded illustration supports space/footprint discussion without generating a product .kicad_pcb or advancing placement/routing.

The proposed75x40mm green outline is an unapproved planning space budget. It is not the owner's chosen board dimension, verified E27 enclosure fit or an allowable safety envelope. Only six dominant components are depicted;22 other schematic items have no assigned positions. There are no copper paths, pad coordinates, drill files, verified insulation margins, temperature predictions or assembly claims.

F1 and RIN use earlier body-size candidates. CBULK uses maximum10.5mm diameter; complete height can reach22mm. T1 shows only the raw bobbin body projection25.2x26mm inside an allocated30x30mm area. The complete transformer core, yokes, winding, leadouts and insulation must still be qualified; the reserve is not a guaranteed finished size. COUT/DOUT use preliminary space reservations, not accepted land patterns.

The drawing establishes that the present EFD25 and high-voltage capacitor materially constrain compactness. It does not establish that all28 items, insulation and heat paths fit75x40mm, or that this outline fits an ordinary bulb. Exact body size versus a smaller transformer is a later evidence-based tradeoff; no current winding/electrical value is changed here.

Sources: prior source-hashed pin-basis documents and input-stage part table named in space-proposal.json. render_space.py deterministically renders the JSON intoPNG/SVG using standard plotting. No photorealistic generated PCB or fabricated KiCad screenshot is supplied. Existing schematic/library/electrical major findings and all approvals are untouched.
