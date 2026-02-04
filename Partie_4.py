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


class VueSolde(Observer):
    def update(self, type_operation, montant, solde, historique):
        print(f"[VUE SOLDE] Solde actuel : {solde}")


class VueHistorique(Observer):
    def update(self, type_operation, montant, solde, historique):
        print("[VUE HISTORIQUE] Historique des opérations :")
        for operation in historique:
            print("-", operation)


class VueAlerte(Observer):
    def update(self, type_operation, montant, solde, historique):
        if solde < 0:
            print("[VUE ALERTE] Solde négatif !")


class VueControle(Observer):
    def update(self, type_operation, montant, solde, historique):
        if solde < -500:
            print("[VUE CONTROLE] Découvert excessif !")


class CompteController:
    def __init__(self):
        self.compte = CompteBancaire()

    def depot(self, montant):
        if montant > 0: self.compte.depot(montant)

    def retrait(self, montant):
        if montant > 0: self.compte.retrait(montant)


if __name__ == "__main__":
    controller = CompteController()
    compte = CompteBancaire()

    print("Même instance ?", compte is CompteBancaire())

    vue_solde = VueSolde()
    vue_historique = VueHistorique()
    vue_alerte = VueAlerte()
    vue_controle = VueControle()

    compte.add_observer(vue_solde)
    compte.add_observer(vue_historique)
    compte.add_observer(vue_alerte)
    compte.add_observer(vue_controle)

    print("\n=== Dépôt de 500 ===")
    controller.depot(500)

    print("\n=== Retrait de 200 ===")
    controller.retrait(200)

    print("\n=== Retrait de 400 ===")
    controller.retrait(400)

    print("\n=== Retrait de 500 ===")

    controller.retrait(500)
