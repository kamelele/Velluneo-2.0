$ErrorActionPreference = 'Stop'
$k = 'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
$python = 'C:/Program Files/KiCad/10.0/bin/python.exe'
$name = 'Zasilacz_RevB2_Ochrona'
$dir = "outputs/$name"
$pcb = "$dir/$name.kicad_pcb"
$sch = "$dir/$name.kicad_sch"
$fab = "$dir/Produkcja_DO_PRZEGLADU"
$preview = "$dir/Podglady"

function Export-KiCad {
    & $k @args
    if ($LASTEXITCODE -ne 0) { throw "KiCad $LASTEXITCODE $args" }
}

& $python work/revb2_guard.py
if ($LASTEXITCODE -ne 0) { throw 'Generator' }
& $python work/model_revb2_guard.py
if ($LASTEXITCODE -ne 0) { throw 'Model' }
New-Item -ItemType Directory -Force -Path $fab,$preview | Out-Null
Export-KiCad sch erc --exit-code-violations -o "$dir/ERC.rpt" $sch
Export-KiCad pcb drc --schematic-parity --exit-code-violations -o "$dir/DRC.rpt" $pcb
Export-KiCad sch export netlist --format kicadxml -o work/revb2-netlist.xml $sch
Export-KiCad sch export svg -o "$preview/" $sch
Export-KiCad pcb export gerbers -o "$fab/" -l 'F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts' $pcb
Export-KiCad pcb export drill --excellon-separate-th --generate-map --map-format svg --generate-report --report-path "$dir/Wiercenia.rpt" -o "$fab/" $pcb
Export-KiCad pcb export pos --format csv --units mm --side both --smd-only -o "$fab/CPL_RevB2.csv" $pcb
Export-KiCad pcb render -w 1200 --height 800 --background opaque --rotate '-30,0,12' --zoom .93 -o "$preview/RevB2_gora_3D.png" $pcb
Export-KiCad pcb render -w 1200 --height 800 --side bottom --background opaque --rotate '-26,0,-12' --zoom .93 -o "$preview/RevB2_dol_3D.png" $pcb
foreach ($svg in Get-ChildItem -LiteralPath $fab,$preview -Filter '*.svg' -File) {
    $clean = [IO.File]::ReadAllText($svg.FullName) -replace '(?m)[ \t]+(?=\r?$)', ''
    [IO.File]::WriteAllText($svg.FullName, $clean, [Text.UTF8Encoding]::new($false))
}
& $python work/verify_b2.py
if ($LASTEXITCODE -ne 0) { throw 'Weryfikacja pinów i eksportu' }
