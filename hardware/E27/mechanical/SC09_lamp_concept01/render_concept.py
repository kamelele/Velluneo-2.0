from pathlib import Path
import subprocess,sys,os
R=Path.cwd();O=R/'outputs/SC09_zarowka_3D';cli=str(Path(sys.executable).with_name('kicad-cli.exe'));os.environ['KICAD_CONFIG_HOME']=str(R/'work/sc08-3d-config')
for name,rot in [('closed','-20,10,-25'),('cutaway','-28,5,-25')]:
 subprocess.run([cli,'pcb','render','--width','2000','--height','1500','--side','top','--rotate',rot,'--zoom','.43','--preset','SC08 Studio','--quality','high','--floor','-o',str(O/f'SC09_lamp_{name}.png'),str(O/f'SC09_lamp_{name}.kicad_pcb')],check=True)
 subprocess.run([cli,'pcb','export','vrml','--units','mm','--force','-o',str(O/f'SC09_lamp_{name}_assembly.wrl'),str(O/f'SC09_lamp_{name}.kicad_pcb')],check=True)
