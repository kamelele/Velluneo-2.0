$ErrorActionPreference='Stop'
$k='C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
$p='C:/Program Files/KiCad/10.0/bin/python.exe'
$d='outputs/Studium_RevE'
$preview="$d/Podglady"
$original='outputs/Zasilacz_RevD_JLCPCB/Zasilacz_RevD_JLCPCB'
$scratch='work/reve_render'
if ($args -contains '-Rebuild') {
    & $p work/studium_e.py
    if ($LASTEXITCODE -ne 0) { throw 'Nie udało się wygenerować rozmieszczenia' }
}
& $p work/reve_models.py
if ($LASTEXITCODE -ne 0) { throw 'Nie udało się wygenerować modeli 3D' }
New-Item -Force -ItemType Directory $preview,$scratch | Out-Null
Copy-Item -LiteralPath "$original.kicad_pcb","$original.kicad_pro" -Destination $scratch
Copy-Item -Path "$d/*.wrl" -Destination $scratch
$demo=(Resolve-Path "$scratch/Zasilacz_RevD_JLCPCB.kicad_pcb")
$demoContents=[IO.File]::ReadAllText($demo) -replace '\$\{KICAD10_3DMODEL_DIR\}/Package_SO\.3dshapes/OnSemi_751EP_[^"]+\.step','${KIPRJMOD}/MB10S_751EP.wrl'
[IO.File]::WriteAllText($demo,$demoContents)

function Render-Board($pcb,$file,$side,$angle,$zoom) {
    & $k pcb render --quality high --background opaque --side $side --rotate $angle --zoom $zoom -w 1500 --height 830 -o "$preview/$file.png" $pcb
    if ($LASTEXITCODE -ne 0) { throw "Nie udało się wyrenderować $pcb" }
}
Render-Board "$scratch/Zasilacz_RevD_JLCPCB.kicad_pcb" 'RevD_nowe_modele_gora' 'top' '-34,0,10' 1.28
Render-Board "$scratch/Zasilacz_RevD_JLCPCB.kicad_pcb" 'RevD_nowe_modele_dol' 'bottom' '-30,0,-10' 1.28
Render-Board "$d/E_Jedna.kicad_pcb" 'RevE_jedna_plytka' 'top' '-34,0,10' 1.28
Render-Board "$d/E_Moc.kicad_pcb" 'RevE_plytka_mocy' 'top' '-34,0,10' 1.23
Render-Board "$d/E_Sterowanie.kicad_pcb" 'RevE_plytka_sterowania' 'top' '-34,0,10' 1.03

foreach ($n in @('E_Jedna','E_Moc','E_Sterowanie')) {
    & $k pcb drc -o "$d/${n}_DRC.rpt" "$d/$n.kicad_pcb"
    if ($LASTEXITCODE -ne 0) { throw "Nie udało się wygenerować raportu $n" }
}
& $p work/verify_reve.py
if ($LASTEXITCODE -ne 0) { throw 'Rozmieszczenie nie przeszło kontroli' }
