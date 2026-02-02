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

    def notify_observers(self, type_operation, montant, solde, historique):
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
        self.notify_observers("DEPOT", montant, self.solde, self.historique)

    def retrait(self, montant):
        self.solde -= montant
        self.historique.append(f"Retrait : -{montant}")
        self.notify_observers("RETRAIT", montant, self.solde, self.historique)


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


class ControleOperations(Observer):
    def update(self, type_operation, montant, solde, historique):
        if solde < -500:
            print("[CONTROLE] Découvert excessif !")


if __name__ == "__main__":
    compte = CompteBancaire()

    print("Même instance ?", compte is CompteBancaire())

    vue_solde = AffichageSolde()
    vue_historique = HistoriqueOperations()
    vue_alerte = AlerteSolde()
    vue_controle = ControleOperations()

    compte.add_observer(vue_solde)
    compte.add_observer(vue_historique)
    compte.add_observer(vue_alerte)
    compte.add_observer(vue_controle)

    print("\n=== Dépôt de 300 ===")
    compte.depot(300)

    print("\n=== Retrait de 200 ===")
    compte.retrait(200)

    print("\n=== Retrait de 200 (solde négatif) ===")
    compte.retrait(200)

    print("\n=== Retrait de 500 (découvert excessif) ===")
    compte.retrait(500)