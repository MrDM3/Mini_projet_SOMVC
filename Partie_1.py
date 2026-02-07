class CompteBancaire:
    def __init__(self, solde_initial=0):
        self.solde = solde_initial
        self.historique = []

    def depot(self, montant):
        self.solde += montant
        self.historique.append(f"Dépôt : +{montant}")

    def retrait(self, montant):
        self.solde -= montant
        self.historique.append(f"Retrait : -{montant}")


class AffichageSolde:
    def afficher(self, compte):
        print("Solde actuel :", compte.solde)


class HistoriqueOperations:
    def afficher(self, compte):
        print("Historique des opérations :")
        for operation in compte.historique:
            print("-", operation)


class AlerteSolde:
    def verifier(self, compte):
        if compte.solde < 0:
            print("Alerte : solde négatif !")


class ControleOperations:
    def autoriser_depot(self, montant):
        if montant <= 0:
            print("Dépôt refusé : montant invalide")
            return False
        return True

    def autoriser_retrait(self, compte, montant):
        if montant <= 0:
            print("Retrait refusé : montant invalide")
            return False
        if compte.solde - montant < -500:
            print("Retrait refusé : découvert maximal dépassé")
            return False
        return True
    

if __name__ == "__main__":

    compte = CompteBancaire(100)

    affichage = AffichageSolde()
    historique = HistoriqueOperations()
    alerte = AlerteSolde()
    controle = ControleOperations()

    # ===== Dépôt =====
    montant_depot = 50
    if controle.autoriser_depot(montant_depot):
        compte.depot(montant_depot)
        print("Dépôt effectué avec succès")

    affichage.afficher(compte)
    alerte.verifier(compte)

    print("-" * 30)

    # ===== Retrait =====
    montant_retrait = 120
    if controle.autoriser_retrait(compte, montant_retrait):
        compte.retrait(montant_retrait)
        print("Retrait effectué avec succès")

    affichage.afficher(compte)
    alerte.verifier(compte)

    print("-" * 30)

    # ===== Retrait dépassant le découvert =====
    montant_retrait = 600
    if controle.autoriser_retrait(compte, montant_retrait):
        compte.retrait(montant_retrait)

    affichage.afficher(compte)
    alerte.verifier(compte)

    print("-" * 30)

    # ===== Affichage de l'historique =====
    historique.afficher(compte)

