from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).resolve().parent;r=json.loads((D/'results.json').read_text());P=Path(__file__).resolve().parents[2];s=np.array(json.loads((P/'electrical-integration/native-typical-flux-curve.json').read_text())['samples']);I=np.linspace(210,300,400);fig,ax=plt.subplots(figsize=(9,5.3))
ax.axhspan(750,850,color='#deefd9',alpha=.8,label='Whole-lamp target 750–850 lm')
for c,p in r['panels'].items():ax.plot(I,p['count']*p['hot55_reference_lm']*.87*np.interp(I,s[:,0],s[:,1]),label=f"{c} K / {p['count']} LEDs")
a,b=r['common_current_interval_for_unperturbed750to850_A'];ax.axvspan(a*1000,b*1000,color='#aac9ed',alpha=.25,label='Calculated common interval')
star=r['minimax_nominal_family_current_A']*1000;ax.axvline(star,c='k',ls='--',lw=1,label=f'Proposed budget centre {star:.1f} mA')
ax.set(xlabel='LED current (mA)',ylabel='Calculated whole-lamp flux (lm)',title='Conditional optical screening — not measured photometry',ylim=(600,1000),xlim=(210,300));ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.2)
fig.text(.1,.015,'Typical current curve; 85°C LED reference and diffuser transmission 0.87 are hypotheses.\nActual acceptance: 230 V / 50 Hz, ambient 25±1°C, complete lamp, stabilized.',fontsize=8)
fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(D/'flux-current.png',dpi=160);fig.savefig(D/'flux-current.svg');plt.close(fig)
