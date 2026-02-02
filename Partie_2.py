class CompteBancaire:
    __instance = None

    def __new__(cls, solde_initial=0):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.solde = solde_initial
            cls.__instance.historique = []
        return cls.__instance

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

    compte1 = CompteBancaire(500)
    compte2 = CompteBancaire(100) 

    print("Même instance ?", compte1 is compte2)

    affichage = AffichageSolde()
    historique = HistoriqueOperations()
    alerte = AlerteSolde()
    controle = ControleOperations()

    print("\n=== Dépôt de 50 ===")
    compte1.depot(50)
    affichage.afficher(compte2)
    historique.afficher(compte2)

    print("\n=== Retrait de 200 ===")
    compte2.retrait(200)
    affichage.afficher(compte1)
    historique.afficher(compte1)
    alerte.verifier(compte1)
    controle.controler(compte1)