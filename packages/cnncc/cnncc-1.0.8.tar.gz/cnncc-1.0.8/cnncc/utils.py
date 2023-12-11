def pretty_print(output, p, classe):
    class_str = map_classes_to_names(classe)

    # Titre
    print("It looks like your cell is in phase:", class_str)
    print()

    # En-têtes
    print("{:<10} | {:>10}".format("Phase", "Probability"))
    print("-" * 25)

    # Données
    phases = ["G1", "S", "G2", "M"]
    probabilities = [round(100 * output[0][i].item(), 2) for i in range(4)]

    # Trouver la probabilité maximale
    max_prob = max(probabilities)
    max_prob_index = probabilities.index(max_prob)

    # Appliquer des styles pour le texte en gras et la couleur verte
    green_bold = "\033[1;32m"
    reset = "\033[0m"

    for i, (phase, probability) in enumerate(zip(phases, probabilities)):
        if i == max_prob_index:
            # Afficher la probabilité la plus élevée en vert et en gras
            print("{:<10} | {}{:>8.2f} %{}".format(phase, green_bold, probability, reset))
        else:
            # Afficher les autres probabilités normalement
            print("{:<10} | {:>8.2f} %".format(phase, probability))


def map_classes_to_names(classe):
    if classe == 0:
        return "G1"
    elif classe == 1:
        return "S"
    elif classe == 2:
        return "G2"
    else:  
        return "M"