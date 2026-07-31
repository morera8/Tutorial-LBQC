'''
Script para automatizar a execução do AutoDock e AutoGrid em múltiplas pastas de docking geradas pelo Raccoon.
O script substitui a execução do RunVS.bat, que é gerado pelo Raccoon.
Uso: executo no prompt do Windows
python autodock4.py
'''
from pathlib import Path
import subprocess
import logging
import time

# ================= CONFIGURAÇÕES =================

ROOT = Path(r"C:\Users\Moreira\Desktop\test\resultados")  # diretório onde estão as pastas de docking geradas pelo raccoon 

#diretórios dos executáveis do AutoDock e AutoGrid adaptar conforme a instalação do AutoDock no seu computador 
AUTOGRID = r"C:\Program Files (x86)\The Scripps Research Institute\Autodock\4.2.6\autogrid4.exe" # executável do AutoGrid
AUTODOCK = r"C:\Program Files (x86)\The Scripps Research Institute\Autodock\4.2.6\autodock4.exe" # executável do AutoDock

logging.basicConfig(
    filename=ROOT / "docking.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# =================================================

pastas = sorted([p for p in ROOT.iterdir() if p.is_dir()])
total = len(pastas)

inicio_total = time.time()

print(f"\nTotal de dockings: {total}\n")

for indice, pasta in enumerate(pastas, start=1):

    inicio = time.time()

    print("=" * 70)
    print(f"[{indice}/{total}] {pasta.name}")
    print("=" * 70)

    gpf = list(pasta.glob("*.gpf"))
    dpf = list(pasta.glob("*.dpf"))

    if len(gpf) != 1:
        logging.error(f"{pasta.name}: GPF não encontrado.")
        print("ERRO: GPF não encontrado.")
        continue

    if len(dpf) != 1:
        logging.error(f"{pasta.name}: DPF não encontrado.")
        print("ERRO: DPF não encontrado.")
        continue

    glg = gpf[0].with_suffix(".glg")
    dlg = dpf[0].with_suffix(".dlg")

    # ----------------- AUTOGRID -----------------

    print("Executando AutoGrid...")

    r = subprocess.run(
        [
            AUTOGRID,
            "-p", gpf[0].name,
            "-l", glg.name
        ],
        cwd=pasta,
        capture_output=True,
        text=True
    )

    if r.returncode != 0:

        logging.error(f"{pasta.name}: AutoGrid falhou.")
        logging.error(r.stdout)
        logging.error(r.stderr)

        print("FALHOU (AutoGrid)")
        continue

    print("OK")

    # ----------------- AUTODOCK -----------------

    print("Executando AutoDock...")

    r = subprocess.run(
        [
            AUTODOCK,
            "-p", dpf[0].name,
            "-l", dlg.name
        ],
        cwd=pasta,
        capture_output=True,
        text=True
    )

    if r.returncode != 0:

        logging.error(f"{pasta.name}: AutoDock falhou.")
        logging.error(r.stdout)
        logging.error(r.stderr)

        print("FALHOU (AutoDock)")
        continue

    tempo = time.time() - inicio

    print(f"Concluído em {tempo:.1f} s")

fim_total = time.time()

print("\n" + "=" * 70)
print(f"Docking finalizado!")
print(f"Total: {total}")
print(f"Tempo total: {(fim_total - inicio_total)/60:.1f} minutos")
print("=" * 70)