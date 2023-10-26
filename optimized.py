import csv
import argparse
import os

# Constantes
MAX_BUDGET = 500


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
            price = row.get('price', row.get('Prix', '0.0'))
            profit = row.get('profit', row.get('Profit', '0.0%')).strip('%')
            data.append({'Nom': name, 'Prix': price, 'Profit': profit})

    clean_data = [entry for entry in data if float(entry['Prix']) > 0.0]

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
            cost = round(float(row[1]), 2)  # Arrondir à deux décimales
            profit = round(float(row[2].strip('%')) / 100 * cost, 2)
            actions.append((name, cost, profit))

    return actions


def best_combination_to_purchase(actions: list, max_budget: int) -> tuple:
    n = len(actions)

    # Initialise le tableau de mémorisation pour la programmation dynamique
    memo_table = [[0 for _ in range(max_budget + 1)] for _ in range(n + 1)]

    # Remplit le memo_table en fonction de la valeur maximale possible
    for i in range(n + 1):
        for w in range(max_budget + 1):
            if i == 0 or w == 0:
                memo_table[i][w] = 0
            elif actions[i - 1][1] <= w:
                memo_table[i][w] = max(actions[i - 1][2] + memo_table[i - 1][w - int(actions[i - 1][1])],
                                       memo_table[i - 1][w])
            else:
                memo_table[i][w] = memo_table[i - 1][w]

    # Reconstruit la solution à partir du memo_table en évitant de dépasser le budget
    w = max_budget
    best_actions = []
    for i in range(n, 0, -1):
        if memo_table[i][w] != memo_table[i - 1][w]:
            best_actions.append(actions[i - 1])
            w -= round(actions[i - 1][1])

    return best_actions, memo_table[n][max_budget]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalise et traite un fichier CSV d'actions.")
    parser.add_argument("csvfile", help="Chemin vers le fichier CSV à traiter.")
    args = parser.parse_args()

    normalized_file = normalize_csv(args.csvfile)

    actions = read_actions_from_csv(normalized_file)
    optimal_combination, total_profit = best_combination_to_purchase(actions, MAX_BUDGET)

    # Calcul du coût total en utilisant les coûts individuels des actions sélectionnées
    total_cost = sum(action[1] for action in optimal_combination)
    print(total_cost)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}€)")
    print(f"Coût total de l'achat des actions: {sum(action[1] for action in optimal_combination):.2f}€")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")