# Actual implementation research; not final review

Coordinator and sole writer: /root. Three distinct read-only implementer contexts
researched manufacturer/distributor evidence. They did not approve the resulting ECO.

* /root/cat15_transformer:74215 vs obsolete74015; authentic pins/turns/dots,19.5mm
 height, stock routes and bias/current adaptation. The stronger74032 and74087 were
 rejected as clean replacements because their lower Lp exceeds the controller's
 available frequency range under the declared20..27V/250mA conditions. This is a
 bounded search, not proof that no other catalogue transformer can ever work.
 Source: https://myrra.com/wp-content/uploads/2021/03/Catalogue-Myrra-2026-Final_compressed.pdf
* /root/cat15_smt_sourcing:26 historical SMT references/20MPNs; exact manufacturer,
 small-lot distributor stock, dielectric/B-value/rating restrictions, DBVT packing,
 Littelfuse TVS candidate. Stock readings may be cached/regional, not reservations.
 Root independently read actual settled JLCPCB UI rows; JLC inventory is not LCSC.
 Root also resolved499k cut-tape MOQ1 from the exact DigiKey price table.
* /root/cat15_power_sourcing:factory WSZ R1, SDB107 bridge, DPAK Q1, C1 vent/body,
 orderable wire raw material. Later TO247 STW3N150 research found stock, but29.3nC
 gate charge, exposed drain tab and lead shoulders prevent calling it a drop-in
 solution to the3mm rule. It was not selected. No further variant is active.
 Source: https://www.st.com/resource/en/datasheet/stp3n150.pdf

Root retained one preferred ECO basis with open physics/geometry holds, rather than
manufacturing an accepted electrical selection from catalogue stock alone. No CAD,
global clearance rule, toolkit payload or historic approval was changed.
