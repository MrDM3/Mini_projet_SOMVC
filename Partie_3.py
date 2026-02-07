from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, type_operation, montant, solde, historique):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify(self, type_operation, montant, solde, historique):
        for observer in self._observers:
            observer.update(type_operation, montant, solde, historique)


class CompteBancaire(Observable):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            super().__init__()
            self.solde = 0
            self.historique = []
            self._initialized = True

    def depot(self, montant):
        self.solde += montant
        self.historique.append(f"Dépôt : +{montant}")
        self.notify("DEPOT", montant, self.solde, self.historique)

    def retrait(self, montant):
        self.solde -= montant
        self.historique.append(f"Retrait : -{montant}")
        self.notify("RETRAIT", montant, self.solde, self.historique)


class AffichageSolde(Observer):
    def update(self, type_operation, montant, solde, historique):
        print(f"[SOLDE] Solde actuel : {solde}")


class HistoriqueOperations(Observer):
    def update(self, type_operation, montant, solde, historique):
        print("[HISTORIQUE COMPLET]")
        for operation in historique:
            print("-", operation)


class AlerteSolde(Observer):
    def update(self, type_operation, montant, solde, historique):
        if solde < 0:
            print("[ALERTE] Solde négatif !")


class ControleOperations:
    def __init__(self, compte):
        self.compte = compte

    def autoriser_depot(self, montant):
        if montant <= 0:
            print("[CONTROLE] Dépôt refusé : montant invalide")
            return
        self.compte.depot(montant)

    def autoriser_retrait(self, montant):
        if montant <= 0:
            print("[CONTROLE] Retrait refusé : montant invalide")
            return
        if self.compte.solde - montant < -500:
            print("[CONTROLE] Retrait refusé : découvert maximal (-500) dépassé")
            return
        self.compte.retrait(montant)


#Vérifier que l’ajout d’un nouvel observateur ne nécessite aucune modification du modèle
class LoggerOperations(Observer):
    def update(self, type_operation, montant, solde, historique):
        print(f"[LOGGER] {type_operation} | montant={montant} | solde={solde}")



if __name__ == "__main__":

    print("===== TEST AJOUT NOUVEL OBSERVATEUR (SANS MODIFIER LE MODÈLE) =====\n")

    # Création du compte (Singleton)
    compte = CompteBancaire()

    # Ajout des observateurs existants
    compte.add_observer(AffichageSolde())
    compte.add_observer(HistoriqueOperations())
    compte.add_observer(AlerteSolde())

    # 👉 Nouvel observateur ajouté sans toucher au modèle
    compte.add_observer(LoggerOperations())

    # Contrôleur
    controle = ControleOperations(compte)

    print("===== OPÉRATION 1 =====")
    depot = 1000
    print(f"Dépôt demandé : {depot}")
    controle.autoriser_depot(depot)
    print(f"Solde après dépôt : {compte.solde}\n")

    print("===== OPÉRATION 2 =====")
    retrait = 300
    print(f"Retrait demandé : {retrait}")
    controle.autoriser_retrait(retrait)
    print(f"Solde après retrait : {compte.solde}\n")

    print("===== OPÉRATION 3 =====")
    retrait = 1200
    print(f"Retrait demandé : {retrait}")
    controle.autoriser_retrait(retrait)
    print(f"Solde après retrait : {compte.solde}\n")
