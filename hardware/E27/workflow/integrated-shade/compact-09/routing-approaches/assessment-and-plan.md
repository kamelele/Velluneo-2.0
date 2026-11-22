# ROUTE04: endpoint approach simplification

The owner explicitly requested shortening the lower Kelvin receiver-via approach and a whole-board inspection for similar avoidable bends. The source is preserved at commit27674de71c9e1eec702d3ba235e44f3229676547, nativePCBfc2bf0f2e865e23579180fee47f635079a686d576bb84a882f9e91ac462f29fc. Before hashes are in before.json; main remains outside scope.

The F.Cu receiver approach currently runs horizontally to(22.2,6.6), then vertically0.4mm to the via at(22.2,6.2). It is an electrically deliberate separate sense path, but its geometric elbow can be simplified. Replacing its end by a45degree approach can shorten the path while keeping both vias and the force/sense topology unchanged. Inspect the corresponding left Kelvin bend and other two-track90degree elbows, excluding necessary branch junctions and physical terminal-contained geometry.

The SOURCE Yjunction previously shown by the owner joins necessary branches and is not a staircase defect. Preserve its electrical branch function. Do not confuse a normal branch or a required mains-spacing detour with an avoidable two-track elbow.

The private implementer alone edits its isolated candidate. Consume the unchanged actual routing contract, inventory corner decisions, simplify supported approaches with deliberate chamfers, and update the exact protected-purpose map. Root independently verifies topology, native clearance,55pair bounded spacing, spatial/placement invariance, saved-fill freshness and all via/junction checks before adoption. Four distinct read-only roles inspect one frozen engineering packet. Refresh actual native copper/assembly/3D and fabrication exports; publish on the same branch. No stage approval, physical result, order or powered test is invented.
