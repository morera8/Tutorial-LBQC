# No local de execução do script será gerado o arquivo docking_results.csv 
# delimitado por vírgulas com ligante, pose, energia (kcal/mol) e Ki (nM)

import os
import csv

# =========================================================
# CONFIGURAÇÃO PRINCIPAL
# =========================================================
BASE_DIR = " ../Dock4/resutados"   # Add o diretório
OUTPUT_FILE = "docking_results.csv"
# =========================================================
# FUNÇÕES DE PARSING
# =========================================================
def parse_dlg(file_path):
    poses = []
    current_pose = None

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()

                if line.startswith("DOCKED: MODEL"):
                    if current_pose:
                        poses.append(current_pose)

                    current_pose = {"model": int(line.split()[2]), "energy": float("inf"), "Ki": float("inf")}

                elif line.startswith("DOCKED: USER") and current_pose:
                    if "Estimated Free Energy of Binding" in line:
                        try:
                            current_pose["energy"] = float(line.split("=")[1].split()[0])
                        except ValueError:
                            current_pose["energy"] = float("inf")

                    elif "Estimated Inhibition Constant, Ki" in line:
                        try:
                            current_pose["Ki"] = float(line.split("=")[1].split()[0])
                        except ValueError:
                            current_pose["Ki"] = float("inf")

        if current_pose:
            poses.append(current_pose)

    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")

    return poses


def find_best_pose(poses):
    if not poses:
        return None
    return min(poses, key=lambda x: (x["energy"], x["Ki"]))


def process_folder(folder_path):
    best_poses = {}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".dlg"):
            file_path = os.path.join(folder_path, filename)
            poses = parse_dlg(file_path)

            if not poses:
                print(f"Aviso: nenhuma pose encontrada em {filename}")
                continue

            best_pose = find_best_pose(poses)
            if best_pose:
                best_poses[filename] = best_pose

    return best_poses

# =========================================================
# SCRIPT PRINCIPAL
# =========================================================
def main():
    print("Analisando resultados de docking...\n")

    all_results = []

    for folder_name in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder_name)

        if not os.path.isdir(folder_path):
            continue

        best_poses = process_folder(folder_path)

        for filename, pose in best_poses.items():
            all_results.append({"Ligante": folder_name, "Arquivo": filename, "Modelo": pose["model"], "Energia (kcal/mol)": pose["energy"],"Ki (nM)": pose["Ki"]})

    if not all_results:
        print("Nenhum resultado encontrado.")
        return

    # Ordenar pela melhor energia
    all_results.sort(key=lambda x: x["Energia (kcal/mol)"])

    # Salvar CSV no diretório de execução
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Ligante", "Arquivo", "Modelo", "Energia (kcal/mol)", "Ki (nM)"])
        writer.writeheader()
        writer.writerows(all_results)

    print("Análise concluída com sucesso!")
    print(f"Arquivo gerado: {os.path.abspath(OUTPUT_FILE)}\n")

    # Mostrar os 10 melhores resultados no terminal
    print("Top 10 melhores poses:")
    for result in all_results[:10]:
        print(f"{result['Ligante']} | {result['Arquivo']} | "f"Modelo {result['Modelo']} | "f"E = {result['Energia (kcal/mol)']:.2f} kcal/mol | "f"Ki = {result['Ki (nM)']:.2f} nM")

if __name__ == "__main__":
    main()
