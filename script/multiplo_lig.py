# -*- coding: utf-8 -*-
# No local de execução do script será gerado o arquivo resultados_vina.csv
# delimitado por vírgulas com as energias dos ligantes

import os
import subprocess
import platform
import csv

# Certifique que os nomes dos softwares vina (DETECTAR SISTEMA) estão de acordo com o que está usando. 
# ===== DETECTAR SISTEMA =====
if platform.system() == "Windows":
    VINA = "vina_1.2.7_win.exe"
    VINA_SPLIT = "vina_split_1.2.7_win.exe"
else:
    VINA = "./vina_1.2.7_linux_x86_64"
    VINA_SPLIT = "./vina_split_1.2.7_linux_x86_64"

CONF = "conf.txt"
RECEPTOR = "6wx4.pdbqt"

PASTA_LIGANTES = "ligantes_conv"   # Add o diretório
PASTA_RESULTADOS = "resultados"    # Add o diretório

CSV_SAIDA = "resultados_vina.csv"

# ===========================

# Criar pasta de resultados
if not os.path.exists(PASTA_RESULTADOS):
    os.makedirs(PASTA_RESULTADOS)

ligantes = [f for f in os.listdir(PASTA_LIGANTES) if f.endswith(".pdbqt")]

print("Ligantes encontrados:", len(ligantes))

# ===========================
# PARTE 1 — DOCKING
# ===========================

for lig in ligantes:
    nome_lig = os.path.splitext(lig)[0]
    pasta_lig = os.path.join(PASTA_RESULTADOS, nome_lig)

    if not os.path.exists(pasta_lig):
        os.makedirs(pasta_lig)

    lig_path = os.path.join(PASTA_LIGANTES, lig)
    out_path = os.path.join(pasta_lig, "res_out.pdbqt")

    print("\nDocking do ligante:", lig)

    subprocess.run([VINA, "--config", CONF, "--ligand", lig_path, "--out", out_path], check=True)

    print("Separando poses")

    subprocess.run([VINA_SPLIT, "--input", "res_out.pdbqt"], cwd=pasta_lig, check=True)

# ===========================
# PARTE 2 — GERAR CSV
# ===========================

print("\nGerando tabela CSV...")

with open(CSV_SAIDA, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ligante", "affinity_kcal_mol", "rmsd_lb", "rmsd_ub"])

    for lig_dir in sorted(os.listdir(PASTA_RESULTADOS)):
        pasta_lig = os.path.join(PASTA_RESULTADOS, lig_dir)

        if not os.path.isdir(pasta_lig):
            continue

        arquivo_pose1 = os.path.join(pasta_lig, "res_out_ligand_1.pdbqt")

        if not os.path.exists(arquivo_pose1):
            print("Aviso: res_out_ligand_1.pdbqt não encontrado para", lig_dir)
            continue

        with open(arquivo_pose1, "r") as f:
            for linha in f:
                if linha.startswith("REMARK VINA RESULT:"):
                    partes = linha.split()
                    affinity = partes[3]
                    rmsd_lb = partes[4]
                    rmsd_ub = partes[5]

                    writer.writerow([lig_dir, affinity, rmsd_lb, rmsd_ub])
                    break

print("\nCSV gerado com sucesso:", CSV_SAIDA)
print("Docking múltiplo finalizado!")
