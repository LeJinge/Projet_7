import csv
import argparse
import os

# Constantes
MAX_BUDGET_CENTS = 50000  # En centimes, car nous avons multiplié par 100


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
            # Conversion des données en centimes
            cost = int(float(row[1]) * 100)
            profit = int(float(row[2]) * cost / 100)
            actions.append((row[0], cost, profit))
    return actions


def best_combination_to_purchase(actions: list, max_budget: int) -> tuple:
    n = len(actions)
    memo_table = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, max_budget + 1):
            cost, profit = actions[i - 1][1], actions[i - 1][2]
            if cost <= w:
                memo_table[i][w] = max(profit + memo_table[i - 1][w - cost], memo_table[i - 1][w])
            else:
                memo_table[i][w] = memo_table[i - 1][w]

    w, best_actions = max_budget, []
    for i in range(n, 0, -1):
        if memo_table[i][w] != memo_table[i - 1][w]:
            best_actions.append(actions[i - 1])
            w -= actions[i - 1][1]

    return best_actions, memo_table[n][max_budget]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalise et traite un fichier CSV d'actions.")
    parser.add_argument("csvfile", help="Chemin vers le fichier CSV à traiter.")
    args = parser.parse_args()
    normalized_file = normalize_csv(args.csvfile)

    actions = read_actions_from_csv(normalized_file)
    optimal_combination, total_profit_cents = best_combination_to_purchase(actions, MAX_BUDGET_CENTS)

    total_cost_cents = sum(action[1] for action in optimal_combination)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1] / 100:.2f}€, Bénéfice après 2 ans: {action[2] / 100:.2f}€)")
    print(f"Coût total de l'achat des actions: {total_cost_cents / 100:.2f}€")
    print(f"Bénéfice total après 2 ans: {total_profit_cents / 100:.2f}€")
