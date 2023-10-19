import csv

# Constantes
FILENAME = "Data.csv"
MAX_BUDGET = 500


def read_actions_from_csv(filename):
    """
    Lit les actions depuis un fichier CSV.

    Args :
    - filename : Nom du fichier CSV.

    Returns :
    - list de tuples : Chaque tuple contient le nom, le coût et le bénéfice calculé d'une action.
    """
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
    """
    Détermine la meilleure combinaison d'actions pour maximiser le bénéfice sans dépasser max_budget.

    Args:
    - actions (list): Liste des actions disponibles.
    - max_budget (int): Capacité maximale (budget) pour acheter des actions.

    Returns:
    - tuple: Une liste des meilleures actions et le bénéfice total correspondant.
    """
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

    # Reconstruit la solution à partir du memo_table
    w = max_budget
    best_actions = []
    for i in range(n, 0, -1):
        if memo_table[i][w] != memo_table[i - 1][w]:
            best_actions.append(actions[i - 1])
            w -= int(actions[i - 1][1])

    return best_actions, memo_table[n][max_budget]


if __name__ == "__main__":
    actions = read_actions_from_csv(FILENAME)
    optimal_combination, total_profit = best_combination_to_purchase(actions, MAX_BUDGET)

    print("Meilleure combinaison d'actions à acheter :")
    for action in optimal_combination:
        print(f"{action[0]} (Coût: {action[1]:.2f}€, Bénéfice après 2 ans: {action[2]:.2f}€)")
    print(f"Bénéfice total après 2 ans: {total_profit:.2f}€")
