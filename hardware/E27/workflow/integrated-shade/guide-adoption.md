# JLCPCB guide adoption

The user explicitly requested both PCB Agent Toolkit and the JLCPCB KiCad MCP article on 2026-11-19. The URL was not found in the inspected pinned toolkit docs/README/manifest, so it is a separate project source, not a claimed built-in toolkit dependency.

Applied principles: datasheet-first circuit review; exact physical pin intent before capture; exported-netlist comparison independent of ERC; footprint/polarity checks; planned courtyards and dimensions; short switching loops and protected sense/feedback; native DRC and parity; direct supplier identity checks; inspect outputs before fabrication.
The article's XL4015, voltage ratings, 63x33mm board, 1.2mm SW keepout and 0.5mm edge distance are example-specific, not this product's safety/layout rules. Do not use the tutorial as qualification evidence or to override pinned KiCad 10.0.6.
No KiCad MCP server is available to this chat. CLI/pcbnew is verified; live MCP edits and autorouting have not occurred. Any new server must be reviewed, pinned, local/stdio and initially read-only, then scoped to this project. No global settings or MCP installation were changed.
Toolkit dependency was reconstructed from the previously verified unmodified tree with its supplied normalized build recipe, yielding the same archive hash as the prior project lock; the original zip with explicit directory entries was rejected by the installer. No toolkit source modification was made.
