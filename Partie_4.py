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


class CompteController:
    def __init__(self):
        self.compte = CompteBancaire()

    def controle_depot(self, montant):
        if montant <= 0:
            print("Dépôt refusé : montant invalide")
            return
        self.compte.depot(montant)

    def controle_retrait(self, montant):
        if montant <= 0:
            print("Retrait refusé : montant invalide")
            return

        if self.compte.solde - montant < -500:
            print("Retrait refusé : découvert maximal dépassé")
            return

        self.compte.retrait(montant)


if __name__ == "__main__":
    controller = CompteController()
    compte = controller.compte

    # Observers
    compte.add_observer(VueSolde())
    compte.add_observer(VueHistorique())
    compte.add_observer(VueAlerte())

    print("\n========= OPÉRATION 1 =========")
    depot = 1000
    print(f"Dépôt demandé : {depot}")
    controller.controle_depot(depot)
    print(f"Solde après dépôt : {compte.solde}")

    print("\n========= OPÉRATION 2 =========")
    retrait = 300
    print(f"Retrait demandé : {retrait}")
    controller.controle_retrait(retrait)
    print(f"Solde après retrait : {compte.solde}")

    print("\n========= OPÉRATION 3 =========")
    retrait = 1100
    print(f"Retrait demandé : {retrait}")
    controller.controle_retrait(retrait)
    print(f"Solde après retrait : {compte.solde}")

    print("\n========= OPÉRATION 4 (REFUSÉE) =========")
    retrait = 200
    print(f"Retrait demandé : {retrait}")
    controller.controle_retrait(retrait)
    print(f"Solde inchangé : {compte.solde}")

    print("\n========= OPÉRATION 5 (INVALIDE) =========")
    depot = -50
    print(f"Dépôt demandé : {depot}")
    controller.controle_depot(depot)
    print(f"Solde inchangé : {compte.solde}")


