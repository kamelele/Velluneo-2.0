$ErrorActionPreference = 'Stop'
$k = 'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
$python = 'C:/Program Files/KiCad/10.0/bin/python.exe'
$name = 'Zasilacz_RevD_JLCPCB'
$dir = "outputs/$name"
$pcb = "$dir/$name.kicad_pcb"
$sch = "$dir/$name.kicad_sch"
$fab = 'work/revd_gerber'
$preview = "$dir/Podglady"

function Export-KiCad {
    & $k @args
    if ($LASTEXITCODE -ne 0) { throw "KiCad $LASTEXITCODE $args" }
}

if ($args -contains '-Rebuild') {
    & $python work/revd_integrate.py
    if ($LASTEXITCODE -ne 0) { throw 'Generator' }
}
New-Item -ItemType Directory -Force -Path $fab,$preview | Out-Null
Export-KiCad sch erc --exit-code-violations -o "$dir/ERC.rpt" $sch
Export-KiCad pcb drc --refill-zones --save-board --schematic-parity --exit-code-violations -o "$dir/DRC.rpt" $pcb
Export-KiCad sch export netlist --format kicadxml -o work/revd_netlist.xml $sch
Export-KiCad sch export svg -o "$preview/" $sch
Export-KiCad pcb export gerbers --use-drill-file-origin --subtract-soldermask -o "$fab/" -l 'F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts' $pcb
Export-KiCad pcb export drill --drill-origin plot --excellon-separate-th --generate-report --report-path "$dir/Wiercenia.rpt" -o "$fab/" $pcb
Export-KiCad pcb export pos --format csv --units mm --side both --smd-only --use-drill-file-origin -o work/revd_cpl.csv $pcb
Export-KiCad pcb render -w 1400 --height 750 --background opaque --rotate '-30,0,10' --zoom .92 -o "$preview/RevD_gora_3D.png" $pcb
Export-KiCad pcb render -w 1400 --height 750 --side bottom --background opaque --rotate '-26,0,-10' --zoom .92 -o "$preview/RevD_dol_3D.png" $pcb
foreach ($svg in Get-ChildItem -LiteralPath $preview -Filter '*.svg' -File) {
    $clean = [IO.File]::ReadAllText($svg.FullName) -replace '(?m)[ \t]+(?=\r?$)', ''
    [IO.File]::WriteAllText($svg.FullName, $clean, [Text.UTF8Encoding]::new($false))
}
& $python work/revd_jlc.py
if ($LASTEXITCODE -ne 0) { throw 'BOM, CPL i weryfikacja' }
