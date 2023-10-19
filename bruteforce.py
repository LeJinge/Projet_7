import csv
import itertools

# Constantes
FILENAME = "Data.csv"
MAX_BUDGET = 500


def read_actions_from_csv(filename):
    """
    Lit les détails des actions depuis le fichier CSV.

    Args :
    - filename : Nom du fichier CSV.

    Returns :
    - list de tuples : Chaque tuple contient le nom, le coût et le pourcentage de bénéfice d'une action.
    """
    actions = []

    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Ignore l'en-tête

        for row in reader:
            name = row[0]
            cost = float(row[1])
            profit_percentage = float(row[2].strip('%'))
            actions.append((name, cost, profit_percentage))

    return actions


def calculate_profit(combination):
    """
    Calcule le coût total et le bénéfice pour une combinaison d'actions donnée.

    Args :
    - combination : Liste de tuples représentant une combinaison d'actions.

    Returns :
    - tuple : Coût total et bénéfice de la combinaison.
    """
    total_cost = sum(action[1] for action in combination)
    total_profit = sum(action[1] + (action[1] * action[2] / 100) for action in combination)
    return total_cost, total_profit - total_cost


def find_best_combination(actions):
    """
    Détermine la meilleure combinaison d'actions pour maximiser le bénéfice.

    Args :
    - actions : Liste des actions disponibles.

    Returns :
    - tuple : Une liste des meilleures actions et le bénéfice total correspondant.
    """
    best_comb = []
    highest_profit = 0

    for r in range(1, len(actions) + 1):
        for comb in itertools.combinations(actions, r):
            total_cost, profit = calculate_profit(comb)
            if total_cost <= MAX_BUDGET and profit > highest_profit:
                highest_profit = profit
                best_comb = comb

    return best_comb, highest_profit


if __name__ == "__main__":
    actions = read_actions_from_csv(FILENAME)
    optimal_combination, total_profit = find_best_combination(actions)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}%)")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")
