# Executed SC07-C coupled output sensitivity

The adjacent script was actually run after changing auxiliary feed to5070ohm and nominalrail12.15V. This is our own limited per-cycle model, not manufacturerSPICE/PIXls.

{
  "cases": 27,
  "max_v": 116.07827492450878,
  "min_v": 104.54637841993227,
  "LEDavg_range": [
    0.04768821440851784,
    0.06148840919865657
  ],
  "max_chargegap_s": 0.002599999999999991,
  "missing20ms_any": false,
  "normal123V_exceedances": 0,
  "lowest_OVP126V_exceedances": 0
}

15 of27 illustrativecases miss the proposed50..60.5mALEDwindow. Actualcurrent/fulltemperature/filter/OVPqualification remainsOPEN. EarlierSC07Bdata is retained under explicitSC07Bfilenameprefixes and must not be called the current run.
