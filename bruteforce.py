import csv
import argparse
import os
from itertools import combinations

# Constantes
MAX_BUDGET = 500.00


def detect_delimiter(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        first_line = file.readline()
        delimiters = [';', ',', '\t', '|']
        return max(delimiters, key=lambda delim: first_line.count(delim))


def normalize_csv(input_filename):
    base_name = os.path.basename(input_filename).rsplit('.', 1)[0]
    normalized_file_path = os.path.join("Data", f"normalize_{base_name}.csv")

    delimiter = detect_delimiter(input_filename)
    clean_data = []

    with open(input_filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            price = row.get('price', row.get('Prix', '0.00'))
            if float(price) > 0:
                clean_data.append({
                    'Nom': row.get('name', row.get('Nom', '')),
                    'Prix': price,
                    'Profit': row.get('profit', row.get('Profit', '0.0%')).strip('%')
                })

    with open(normalized_file_path, 'w', encoding='utf-8-sig', newline='') as file:
        fieldnames = ['Nom', 'Prix', 'Profit']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(clean_data)

    return normalized_file_path


def read_actions_from_csv(filename):
    actions = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            cost = float(row[1])
            profit = float(row[2]) * cost / 100
            actions.append((row[0], cost, profit))
    return actions


def best_combination_bruteforce(actions: list, max_budget: float) -> tuple:
    best_profit = 0
    best_combination = []

    for r in range(len(actions) + 1):
        for subset in combinations(actions, r):
            total_cost = sum(action[1] for action in subset)
            total_profit = sum(action[2] for action in subset)
            if total_cost <= max_budget and total_profit > best_profit:
                best_profit = total_profit
                best_combination = subset

    return best_combination, best_profit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalise et traite un fichier CSV d'actions.")
    parser.add_argument("csvfile", help="Chemin vers le fichier CSV à traiter.")
    args = parser.parse_args()
    normalized_file = normalize_csv(args.csvfile)

    actions = read_actions_from_csv(normalized_file)
    optimal_combination, total_profit = best_combination_bruteforce(actions, MAX_BUDGET)

    total_cost = sum(action[1] for action in optimal_combination)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}€)")
    print(f"Coût total de l'achat des actions: {total_cost:.2f}€")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")
