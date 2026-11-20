# Headless Ubuntu candidate checks

infra/Dockerfile.ubuntu-test pins Ubuntu 26.10 and KiCad package 10.0.6+dfsg-1.
The image installs tools only; supply a disposable extracted candidate at runtime.
Run scripts/validate_candidate.py, whose inputs come entirely from this package.
It performs integrity, selected unit tests, real KiCad regressions and original
requirements/workflow demonstrations. No audit metadata or private access is needed.

See [the package README](../README.md) for Docker commands. Disable runtime networking
for the validation run. Building the tool image requires access to Ubuntu packages.
Use the matching Python/pcbnew and CLI; a different tool release/package needs a
separate compatibility decision and validation.

Fresh evidence is written under .work/package-validation and generated reports/.
Record actual tool/platform versions, package manifest hash, counts/skips and limits.
Container checks qualify only the declared headless environment, not every Linux
distribution, GUI behavior, product function or manufacturing process.
