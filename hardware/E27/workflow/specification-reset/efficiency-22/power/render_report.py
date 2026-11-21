"""Render existing results.json; requires matplotlib. Does not recompute physics."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).resolve().parent
j=json.loads((D/'results.json').read_text(encoding='utf-8'));n=j['nominal']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titleweight':'bold'})
fig,ax=plt.subplots(2,2,figsize=(15,10),layout='constrained')
fig.suptitle('Velluneo E22 | power and cooling estimate\nConditional model - no thermal measurements\nCentral +0.41 pp; some hot-leak cases are worse',fontsize=18,fontweight='bold')
loss=n['losses_W'];names=['T1*','Clamp*','Q1','D3','R1','Bleeders','C1','Other']
values=[loss['T1_assumed_allocation'],loss['D1_TVS1_assumed_allocation'],loss['Q1'],loss['D3'],loss['R1'],loss['bulk_bleeders_R2_R3_R14_R15']+loss['output_bleeders_R11_R12'],loss['C1']]
values.append(n['driver_heat_W']-sum(values))
a=ax[0,0];a.barh(names[::-1],values[::-1],color='#1b817e');a.set_xlabel('Driver heat [W]');a.set_title('Central loss budget | total %.2f W'%n['driver_heat_W']);a.text(.98,.06,'* T1/clamp split is assumed',transform=a.transAxes,ha='right',fontsize=9)
a=ax[0,1];a.axis('off')
text='230 Vac | 50 Hz | seven H40 LEDs\n\nInput                 %.2f W\nLED power             %.2f W\nDriver heat           %.2f W\nEfficiency to LEDs    %.1f %%\nInput RMS current     %.1f mA\nPower factor          %.2f\n\nSelected cases: %.2f-%.2f W input\n%.2f-%.2f W driver heat'%(n['input_W'],n['LED_power_W'],n['driver_heat_W'],100*n['efficiency_to_LEDs'],1000*n['line_current_RMS_A'],n['PF_model'],*j['ranges_selected_cases']['input_W'],*j['ranges_selected_cases']['driver_heat_W'])
a.text(.03,.96,text,va='top',family='monospace',fontsize=13);a.set_title('Accounting result | unmeasured')
a=ax[1,0];qs=[q for q in j['cooling_requirements'] if q['ambient_C']==40];a.bar([str(int(100*q['LED_heat_fraction']))+'%'for q in qs],[q['R_cavity_max_K_W']for q in qs],color='#d18c2e');a.set_xlabel('LED electrical power coupled as cavity heat');a.set_ylabel('Maximum effective cavity-to-room R [K/W]');a.set_title('Required cooling at room 40 C\nTransformer surrounding air <=50 C')
a=ax[1,1];qs=[q for q in j['thermal_scenarios'] if q['ambient_C']==40 and q['electrical_case']=='central'];a.bar(['Target path*','Weak closed*','Poor closed*'],[q['cavity_air_C']for q in qs],color=['#1b817e','#d18c2e','#bd5549']);a.axhline(50,color='#8b1529',ls='--',label='T1 air limit 50 C');a.set_ylabel('Driver cavity air [ C]');a.set_title('Illustrative heat-path scenarios\n* Resistances/coupling assumed, not built');a.legend(fontsize=9)
fig.savefig(D/'E22_power_overview.png',dpi=160)
print('Rendered E22_power_overview.png')
