# Model qualification task and reproduction contract

DRV-MODEL-01 / VEL-MODEL-01. Sole writer/coordinator /root; allowed repository writes driver-study/model-qualification/* and driver-study/README.md only. Baseline draftc78cbf4e0d4d7d977ac5e7017a00244db7a63773; productr11 blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b confirmed unchanged. Requirements R-SUPPLY/R-LIGHT/R-COMPAT/R-FAULT/R-OFFLINE and their existing unknowns are retained; exact requirement IDs in productr11 govern. No CAD ownership, requirement changes, physical tests, orders, supplier messages, merges or human gate approval.

Acceptance: source-pinned native-POLY execution; separate engine smoke, DC, AC and failed transient; retain numeric model parameters; distinguish typical/source conditions and charge/energy definitions; bounded one-part comparison, explicit open findings and four independent read-only reviews. This is preliminary investigation acceptance only.

## Reproduce

Python3 with NumPy2.3.5 was used. Obtain the reference-only ST model archive and matching Debian44.2+ds-1 amd64 package from sources.json; verify archive hashes before extracting the module. The script independently asserts model-ZIP/module/shared-library hashes and refuses unknown binaries. No vendor PDF, model or runtime is redistributed here. The local shared runtime identity is pinned; other operating systems/versions require a separately recorded compatibility check.

```sh
python run_checks.py --model-zip /path/stn1nk80z_spice.zip --code-model /path/spice2poly.cm --library /path/libngspice.so.0 --out-dir /path/isolated-output
```

Use a fresh isolated output directory. Expected current outcome: results.json and numeric traces written, followed by exit1 because the native component transient fails. Review full-run.log and native-transient.log; never interpret output-file presence as successful transient execution. Compare numeric fields and failure endpoint; full warning histories can contain local paths. Existing published results are never overwritten during review. No UCC model or converter simulation occurs. The physical pins must still be verified independently before CAD; model terminals are D/G/S, not a physical-footprint contract.

Frozen inputs exclude review/index/manifest to avoid cycles. Four read-only reviewers: Reality /root/spec_reality, Overengineering /root/spec_simplicity, Completeness /root/spec_completeness, Change /root/spec_change. Diagnostic implementer /root/model_compatibility supplied native-POLY compatibility evidence only, not independent review or human approval. Coordinator maintains finding ledger and index; owner alone approves product stages.
