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

    print("===== VÉRIFICATION DU SINGLETON =====")
    compte1 = CompteBancaire(100)
    compte2 = CompteBancaire(500)

    print("ID compte1 :", id(compte1))
    print("ID compte2 :", id(compte2))

    if compte1 is compte2:
        print("Tous les modules manipulent le MÊME compte\n")
    else:
        print("Comptes différents\n")

    # Modules
    controle1 = ControleOperations()
    controle2 = ControleOperations()

    affichage = AffichageSolde()
    historique = HistoriqueOperations()
    alerte = AlerteSolde()

    # Utilisation du compte unique
    compte = compte1

    print("===== ACCÈS MULTIPLE 1 =====")
    depot = 1000
    print(f"Dépôt demandé : {depot}")
    if controle1.autoriser_depot(depot):
        compte.depot(depot)
    print(f"Solde après dépôt : {compte.solde}")
    affichage.afficher(compte)

    print("\n===== ACCÈS MULTIPLE 2 =====")
    retrait = 300
    print(f"Retrait demandé : {retrait}")
    if controle2.autoriser_retrait(compte, retrait):
        compte.retrait(retrait)
    print(f"Solde après retrait : {compte.solde}")
    affichage.afficher(compte)

    print("\n===== ACCÈS MULTIPLE 3 =====")
    retrait = 1100
    print(f"Retrait demandé : {retrait}")
    if controle1.autoriser_retrait(compte, retrait):
        compte.retrait(retrait)
    print(f"Solde après retrait : {compte.solde}")
    affichage.afficher(compte)
    alerte.verifier(compte)

    print("\n===== HISTORIQUE FINAL =====")
    historique.afficher(compte)
