$ErrorActionPreference='Stop'
$k='C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
$p='C:/Program Files/KiCad/10.0/bin/python.exe'
function Run-KiCad {
    & $k @args
    if ($LASTEXITCODE -ne 0) { throw "KiCad $LASTEXITCODE $args" }
}
function Run-Python {
    & $p @args
    if ($LASTEXITCODE -ne 0) { throw "Python $LASTEXITCODE $args" }
}
if ($args -contains '-RebuildPower') {
    Run-Python work/revf_power.py
    Run-Python work/trim_revf_stubs.py outputs/Zasilacz_RevF_Moc/Zasilacz_RevF_Moc.kicad_pcb
}
$revision='F'
$types=@('Moc','Sterowanie')
if ($args -contains '-RevGPower') {
    $revision='G'
    $types=@('Moc')
    if ($args -contains '-Rebuild') { Run-Python work/revg_power.py }
    Run-Python work/model_revf_rcd.py
}
foreach ($type in $types) {
    $name="Zasilacz_Rev${revision}_$type"
    $dir="outputs/$name"
    $pcb="$dir/$name.kicad_pcb"
    $sch="$dir/$name.kicad_sch"
    $review="work/revf_exports/$revision/$type"
    New-Item -Force -ItemType Directory "$dir/Podglady",$review | Out-Null
    Run-KiCad sch erc --exit-code-violations -o "$dir/ERC.rpt" $sch
    Run-KiCad pcb drc --refill-zones --save-board --schematic-parity --exit-code-violations -o "$dir/DRC.rpt" $pcb
    Run-KiCad sch export netlist --format kicadxml -o "$review/netlist.xml" $sch
    Run-KiCad sch export svg -o "$dir/Podglady/" $sch
    $svg=(Resolve-Path "$dir/Podglady/$name.svg")
    $clean=[IO.File]::ReadAllText($svg) -replace '(?m)[ \t]+(?=\r?$)',''
    [IO.File]::WriteAllText($svg,$clean)
    Run-KiCad pcb render --quality high --background opaque --rotate '-29,0,8' --zoom 1.05 -w 1400 --height 920 -o "$dir/Podglady/Rev${revision}_3D.png" $pcb
    $layers='F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts'
    if ($type -eq 'Sterowanie') { $layers += ',In1.Cu,In2.Cu' }
    Run-KiCad pcb export gerbers --use-drill-file-origin --subtract-soldermask -o "$review/" -l $layers $pcb
    Run-KiCad pcb export drill --drill-origin plot --excellon-separate-th --generate-report --report-path "$dir/Wiercenia.rpt" -o "$review/" $pcb
    Run-KiCad pcb export pos --format csv --units mm --side both --smd-only --use-drill-file-origin -o "$review/smd.csv" $pcb
    if ($revision -eq 'G') {
        Run-Python work/verify_revg_power.py "$review/netlist.xml"
    } elseif ($type -eq 'Moc') {
        Run-Python work/verify_revf_power.py "$review/netlist.xml"
    } else {
        Run-Python work/model_revf_control.py
        Run-Python work/verify_revf_control.py "$review/netlist.xml"
    }
    Run-Python work/revf_jlc.py $name $review
}
