# Board-only scope clarification

Owner clarification, 2026-11-19: focus now on designing the power-supply PCB. Enclosure design, bulb-body geometry, mechanical mating and confirmation of fit inside an E27 envelope are deferred. Enclosure fit must not be presented as a prerequisite for investigating or preparing the driver board.

No enclosure-derived board outline or maximum board size is imposed at this stage. Derive and report the outline from the selected circuit, actual footprints, routing, applicable electrical spacing, thermal separation and assembly access. The previous66x58mm rectangle experiment remains historical feasibility evidence; it is not a frozen PCB outline or an accepted layout.

Continue the capacitor-in-base architecture on concept/integrated-shade-nonisolated-buck. The near-term deliverable is the driver circuit and then its native KiCad PCB through the Toolkit stages. Define electrical input/output connection points without inventing the future mechanical connector. LED voltage/current and fault envelope are still required electrical loads even while the LED module mechanics are deferred.

Keep the electrical issues from PR05 visible: operating point and total current, OVP threshold and latch behavior, pulse/continuous loading, full physical pin intent, input surge coordination and process assumptions. Separate calculations needed for schematic/placement acceptance from later prototype and complete-product qualification. No enclosure project, E27-fit confirmation or full product certification is required merely to continue the board engineering; safety-relevant electrical spacing and on-board thermal design remain part of that engineering.

This note changes task scope only. It does not approve the unresolved circuit, a stage transition, manufacturing or physical mains testing. Earlier immutable evidence is retained; enclosure-specific acceptance belongs to the later integration stage. Main remains outside the write scope.
