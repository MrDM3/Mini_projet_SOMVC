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
    def controler(self, compte):
        if compte.solde < -500:
            print("Attention : découvert excessif !")


if __name__ == "__main__":

    compte = CompteBancaire(100)

    affichage = AffichageSolde()
    historique = HistoriqueOperations()
    alerte = AlerteSolde()
    controle = ControleOperations()

    print("=== Dépôt de 50 ===")
    compte.depot(50)
    affichage.afficher(compte)
    historique.afficher(compte)
    alerte.verifier(compte)
    controle.controler(compte)

    print("\n=== Retrait de 200 ===")
    compte.retrait(200)
    affichage.afficher(compte)
    historique.afficher(compte)
    alerte.verifier(compte)
    controle.controler(compte)