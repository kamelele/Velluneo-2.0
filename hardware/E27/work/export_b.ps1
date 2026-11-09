$ErrorActionPreference = 'Stop'
$k = 'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
$python = 'C:/Program Files/KiCad/10.0/bin/python.exe'
$dir = 'outputs/Zasilacz_RevB'
$pcb = "$dir/Zasilacz_RevB.kicad_pcb"
$sch = "$dir/Zasilacz_RevB.kicad_sch"
$fab = "$dir/Produkcja_DO_PRZEGLADU"
New-Item -ItemType Directory -Force -Path $fab | Out-Null

function Export-KiCad {
    & $k @args
    if ($LASTEXITCODE -ne 0) { throw "KiCad $LASTEXITCODE $args" }
}

Export-KiCad sch erc --exit-code-violations -o "$dir/ERC.rpt" $sch
Export-KiCad pcb drc --schematic-parity --exit-code-violations -o "$dir/DRC.rpt" $pcb
Export-KiCad sch export netlist --format kicadxml -o work/psb.xml $sch
Export-KiCad pcb export gerbers -o "$fab/" -l 'F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts' $pcb
Export-KiCad pcb export drill --excellon-separate-th --generate-map --map-format svg --generate-report --report-path "$dir/Wiercenia.rpt" -o "$fab/" $pcb
Export-KiCad pcb export pos --format csv --units mm --side both --smd-only -o "$fab/CPL_Zasilacz_KiCad.csv" $pcb
Export-KiCad pcb render -w 1400 --height 900 --background opaque --rotate '-38,0,14' --zoom .89 -o "$dir/Zasilacz_RevB_gora_3D.png" $pcb
Export-KiCad pcb render -w 1400 --height 900 --side bottom --background opaque --rotate '-22,0,-12' --zoom .89 -o "$dir/Zasilacz_RevB_dol_3D.png" $pcb
& $python work/bom_b.py
if ($LASTEXITCODE -ne 0) { throw 'BOM' }
& $python work/verify_b.py
if ($LASTEXITCODE -ne 0) { throw 'QA' }
