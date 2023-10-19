import csv
import itertools


# Lire le fichier contenant les informations sur les actions
def lire_actions():
    actions = []
    with open("Data.csv", 'r', encoding='utf-8-sig') as file:  # Utilisation directe du nom du fichier "Data.csv"
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Ignorer la première ligne (entête)
        for row in reader:
            nom = row[0]
            cout = float(row[1])
            benefice = float(row[2].strip('%'))
            actions.append((nom, cout, benefice))
    return actions


# Calculer le bénéfice pour une combinaison d'actions
def calculer_benefice(combinaison):
    total_cout = sum(action[1] for action in combinaison)
    total_benefice = sum(action[1] + (action[1] * action[2] / 100) for action in combinaison)
    return total_cout, total_benefice - total_cout


# Trouver la meilleure combinaison d'actions
def meilleure_combinaison():
    actions = lire_actions()  # Appel direct à lire_actions() sans arguments
    meilleure_comb = []
    meilleur_benefice = 0

    # Pour chaque taille de combinaison possible
    for r in range(1, len(actions) + 1):
        # Générer toutes les combinaisons de cette taille
        for combinaison in itertools.combinations(actions, r):
            total_cout, benef = calculer_benefice(combinaison)
            # Si le coût total ne dépasse pas 500 et le bénéfice est supérieur au meilleur bénéfice trouvé
            if total_cout <= 500 and benef > meilleur_benefice:
                meilleur_benefice = benef
                meilleure_comb = combinaison
    return meilleure_comb, meilleur_benefice


# Exécuter le programme
if __name__ == "__main__":
    combinaison, benefice = meilleure_combinaison()  # Appel direct à meilleure_combinaison() sans arguments
    print("Meilleure combinaison d'actions à acheter :")
    for action in combinaison:
        print(f"{action[0]} (Coût: {action[1]}€, Bénéfice après 2 ans: {action[2]}%)")
    print(f"Bénéfice total après 2 ans: {benefice:.2f}€")
