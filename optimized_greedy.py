import csv
import argparse
import os

# Constantes
MAX_BUDGET = 500.00


def detect_delimiter(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        first_line = file.readline()
        delimiters = [';', ',', '\t', '|']
        return max(delimiters, key=lambda delim: first_line.count(delim))


def normalize_csv(input_filename):
    # Extraction du nom de base du fichier d'entrée pour le nom du fichier normalisé
    base_name = os.path.basename(input_filename).rsplit('.', 1)[0]
    normalized_file_path = os.path.join("Data", f"normalize_{base_name}.csv")

    delimiter = detect_delimiter(input_filename)
    data = []
    with open(input_filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            name = row.get('name', row.get('Nom', ''))
            price = row.get('price', row.get('Prix', '0.00'))
            profit = row.get('profit', row.get('Profit', '0.0%')).strip('%')
            data.append({'Nom': name, 'Prix': price, 'Profit': profit})

    clean_data = [entry for entry in data if float(entry['Prix']) > 0.00]

    with open(normalized_file_path, 'w', encoding='utf-8-sig', newline='') as file:
        fieldnames = ['Nom', 'Prix', 'Profit']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for entry in clean_data:
            writer.writerow(entry)

    return normalized_file_path


def read_actions_from_csv(filename):
    actions = []

    with open(filename, 'r', encoding='utf-8-sig') as file:
        delimiter = detect_delimiter(filename)
        reader = csv.reader(file, delimiter=delimiter)
        next(reader)  # Ignore l'en-tête

        for row in reader:
            name = row[0]
            cost = float(row[1])
            profit = float(row[2].strip('%')) / 100 * cost
            actions.append((name, cost, profit))

    return actions


def greedy_combination_to_purchase(actions: list, max_budget: float) -> tuple:
    # Trier les actions par rapport profit/coût décroissant
    sorted_actions = sorted(actions, key=lambda x: x[2] / x[1], reverse=True)

    selected_actions = []
    total_cost = 0
    total_profit = 0

    for action in sorted_actions:
        if total_cost + action[1] <= max_budget:
            selected_actions.append(action)
            total_cost += action[1]
            total_profit += action[2]

    return selected_actions, total_profit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalise et traite un fichier CSV d'actions.")
    parser.add_argument("csvfile", help="Chemin vers le fichier CSV à traiter.")
    args = parser.parse_args()
    normalized_file = normalize_csv(args.csvfile)

    actions = read_actions_from_csv(normalized_file)
    optimal_combination, total_profit = greedy_combination_to_purchase(actions, MAX_BUDGET)

    # Calcul du coût total en utilisant les coûts individuels des actions sélectionnées
    total_cost = sum(action[1] for action in optimal_combination)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}€)")
    print(f"Coût total de l'achat des actions: {total_cost:.2f}€")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")
