import csv

# Constantes
FILENAME = "Data.csv"
MAX_BUDGET = 500


def read_actions_from_csv(filename):
    actions = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Ignore l'en-tête
        for row in reader:
            name = row[0]
            cost = round(float(row[1]), 2)
            profit = round(float(row[2].strip('%')) / 100 * cost, 2)
            actions.append((name, cost, profit))
    return actions


def best_combination_to_purchase(actions: list, max_budget: int) -> tuple:
    # Calcul du ratio bénéfice/coût pour chaque action
    actions_with_ratio = [(name, cost, profit, profit / cost) for name, cost, profit in actions]

    # Trier les actions par ratio en ordre décroissant
    sorted_actions = sorted(actions_with_ratio, key=lambda x: x[3], reverse=True)

    best_actions = []
    total_profit = 0
    remaining_budget = max_budget

    # Sélectionner les actions à partir du haut de la liste
    for action in sorted_actions:
        name, cost, profit, _ = action
        if cost <= remaining_budget:
            best_actions.append((name, cost, profit))
            remaining_budget -= cost
            total_profit += profit

    return best_actions, total_profit


if __name__ == "__main__":
    actions = read_actions_from_csv(FILENAME)
    optimal_combination, total_profit = best_combination_to_purchase(actions, MAX_BUDGET)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}€)")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")
