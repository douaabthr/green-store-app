import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projetsi.settings")

import django 
django.setup()
from datetime import datetime
import random
from faker import Faker

fake = Faker()

# Assurez-vous d'importer les modèles nécessaires
from app.models import Fournisseur, MatierePremiere, Achat,Transfert,Centre,Client,Produit,VenteM,VenteP,Massrouf,Employe
# Générez des données fictives pour la classe Produit
def generate_fake_produits(num_produits):
    fake_produits = []
    for _ in range(num_produits):
        fake_code = fake.unique.random_number(digits=5)  # Utilisez uniquement si vous voulez des codes uniques
        fake_designation = fake.word()
        fake_prix_unitaire = fake.random.uniform(1, 100)
        fake_created_at = fake.date_time_this_decade()
        fake_quantite_stock = fake.random_int(min=0, max=1000)
        fake_active = fake.boolean()
        fake_produits.append({
            'codeP': fake_code,
            'designation_produit': fake_designation,
            'prix_unitaire_Ven': fake_prix_unitaire,
            'created_at': fake_created_at,
            'quantiteStockPod': fake_quantite_stock,
            'active': fake_active,
        })
    return fake_produits

# Insérez les données fictives dans la base de données
def insert_fake_produits(fake_produits):
    for produit_data in fake_produits:
        Produit.objects.create(**produit_data)
def generate_codeF(car):
    return car + str(Fournisseur.objects.count() + 1)

def generate_codeM(car):
    return car + str(MatierePremiere.objects.count() + 10000)
def generate_fake_clients(num_clients):
    fake_clients = []
    for _ in range(num_clients):
        fake_code = fake.unique.random_number(digits=5)  # Utilisez uniquement si vous voulez des codes uniques
        fake_nom = fake.first_name()
        fake_prenom = fake.last_name()
        fake_adresse = fake.address()
        fake_telephone = fake.phone_number()
        fake_credit = fake.random_int(min=0, max=10000)  # Adaptez la plage selon vos besoins
        fake_clients.append({
            'codeCl': fake_code,
            'nomCl': fake_nom,
            'prenomCl': fake_prenom,
            'adresseCl': fake_adresse,
            'telephoneCl': fake_telephone,
            'credit': fake_credit,
        })
    return fake_clients
def insert_fake_clients(fake_clients):
    for client_data in fake_clients:
        Client.objects.create(**client_data)
# Insérez les données fictives dans la base de données
def insert_fake_clients(fake_clients):
    for client_data in fake_clients:
        Client.objects.create(**client_data)
def populate_fournisseurs(value):
    for i in range(value):
        codeF = generate_codeF("F")
        nomF = fake.name()
        prenomF = fake.last_name()
        adresseF = fake.city()
        telephoneF = fake.phone_number()
        solde = 0
        Fournisseur.objects.get_or_create(
            codeF=codeF,
            nomF=nomF,
            prenomF=prenomF,
            adresseF=adresseF,
            telephoneF=telephoneF,
            solde=solde
        )

def generate_achat(fournisseur, produit):
    prix_unitaire_HT = round(random.uniform(1, 100), 2)
    quantitHT = random.randint(1, 10)
    quantitDispo = random.randint(0, 5)
    montantTotalHT = round(prix_unitaire_HT * quantitHT, 2)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 23)

# Générer une date aléatoire entre start_date et end_date
    buyed_at = fake.date_time_between(start_date=start_date, end_date=end_date)
    return Achat.objects.create(
        fournisseur=fournisseur,
        matiere_achete=produit,
        buyed_at=buyed_at,
        prix_unitaire_HT=prix_unitaire_HT,
        quantitHT=quantitHT,
        quantitDispo=quantitDispo,
        montantTotalHT=montantTotalHT
    )

def populate_achats(fournisseur, produits, value):
    for i in range(value):
        produit = random.choice(produits)
        generate_achat(fournisseur, produit)

def populate_matieres_premieres(value):
    for i in range(value):
        codeM = generate_codeM("M")
        designation_matiere = fake.word()
        prix_unitaire_Ven = round(random.uniform(1, 100), 2)
        created_at = fake.date_this_decade()
        quantiteStockMat = random.randint(1, 1000)
        active = True  # Vous pouvez définir cela comme vous le souhaitez
        MatierePremiere.objects.get_or_create(
            codeM=codeM,
            designation_matiere=designation_matiere,
            prix_unitaire_Ven=prix_unitaire_Ven,
            created_at=created_at,
            quantiteStockMat=quantiteStockMat,
            active=active
        )
def generate_transfert(centre, produit):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 23)
    transfer_at = fake.date_time_between(start_date=start_date, end_date=end_date)
    quantitTran = random.randint(1, 10)
    cout_transfere = round(random.uniform(1, 100), 2)
    
    return Transfert.objects.create(
        centre=centre,
        produit_transfere=produit,
        transfer_at=transfer_at,
        quantitTran=quantitTran,
        cout_transfere=cout_transfere
    )

def populate_transferts(centres, produits, value):
    for i in range(value):
        centre = random.choice(centres)
        produit = random.choice(produits)
        generate_transfert(centre, produit)

def generate_venteP(client, produit, lieu_ventes):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 23)
    salled_at = fake.date_time_between(start_date=start_date, end_date=end_date)
    prix_unitaire_Ven = round(random.uniform(1, 100), 2)
    quantitVen = random.randint(1, 10)
    montantTotalVen = round(prix_unitaire_Ven * quantitVen, 2)

    return VenteP.objects.create(
        client=client,
        produit_vendus=produit,
        salled_at=salled_at,
        prix_unitaire_Ven=prix_unitaire_Ven,
        quantitVen=quantitVen,
        lieu_ventes=lieu_ventes,
        montantTotalVen=montantTotalVen
    )

def generate_venteM(client, matiere_vendus):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 23)
    salled_at = fake.date_time_between(start_date=start_date, end_date=end_date)
    prix_unitaire_Ven = round(random.uniform(1, 100), 2)
    quantitVen = random.randint(1, 10)
    montantTotalVen = round(prix_unitaire_Ven * quantitVen, 2)

    return VenteM.objects.create(
        client=client,
        matiere_vendus=matiere_vendus,
        salled_at=salled_at,
        prix_unitaire_Ven=prix_unitaire_Ven,
        quantitVen=quantitVen,
        montantTotalVen=montantTotalVen
    )

# ... (le reste du code)

def populate_venteP_clients(clients, produits, centres, value):
    for i in range(value):
        client = random.choice(clients)
        produit = random.choice(produits)
        lieu_ventes = random.choice(centres)
        generate_venteP(client, produit, lieu_ventes)

def populate_venteM_clients(clients, matieres, value):
    for i in range(value):
        client = random.choice(clients)
        matiere_vendus = random.choice(matieres)
        generate_venteM(client, matiere_vendus)
def generate_massrouf(employe):
    demende_at = fake.date_this_decade()
    montant_dem = round(random.uniform(1, 1000), 2)
    
    return Massrouf.objects.create(
        employe=employe,
        demende_at=demende_at,
        montant_dem=montant_dem
    )
def generate_fake_employes(num_employes):
    fake_employes = []
    for _ in range(num_employes):
        fake_code = fake.unique.random_number(digits=5)
        fake_nom = fake.first_name()
        fake_prenom = fake.last_name()
        fake_adresse = fake.address()
        fake_telephone = fake.phone_number()
        fake_salaire_jour = fake.random.uniform(50, 500)
        fake_employes.append({
            'codeEmp': fake_code,
            'nomEmp': fake_nom,
            'prenomEmp': fake_prenom,
            'adresseEmp': fake_adresse,
            'telephoneEmp': fake_telephone,
            'salaire_jour': fake_salaire_jour,
        })
    return fake_employes

def insert_fake_employes(fake_employes):
    for employe_data in fake_employes:
        Employe.objects.create(**employe_data)

def populate_employes(value):
    fake_employes_data = generate_fake_employes(value)
    insert_fake_employes(fake_employes_data)

# ... (previous code)

def populate_employes_for_centers(centres, num_employes_per_center):
    for centre in centres:
        employes = Employe.objects.filter(EmployeCentre=centre)
        if employes.count() < num_employes_per_center:
            num_employes_to_create = num_employes_per_center - employes.count()
            print(f"Creating {num_employes_to_create} employees for {centre.designation_centre}...")
            populate_employes(num_employes_to_create)
            employes = Employe.objects.filter(EmployeCentre=centre)
            print(f"{num_employes_to_create} employees created for {centre.designation_centre}.")
def main():
    no_fournisseurs = int(input("Combien de fournisseurs voulez-vous créer? "))
    no_achats_par_fournisseur = int(input("Combien d'achats par fournisseur voulez-vous créer? "))
    no_matieres_premieres = int(input("Combien de matières premières voulez-vous créer? "))
    no_transferts_par_centre = int(input("Combien de transferts par centre voulez-vous créer? ")) 
    no_ventesP_par_client = int(input("Combien de ventes de produits par client voulez-vous créer? "))
    no_ventesM_par_client = int(input("Combien de ventes de matières premières par client voulez-vous créer? "))
    num_fake_clients = int(input("Combien de clients fictifs voulez-vous créer? "))
    num_fake_produits = int(input("Combien de produits fictifs voulez-vous créer? "))
    num_fake_employes = int(input("Combien d'employés fictifs voulez-vous créer? "))
    fake_produits_data = generate_fake_produits(num_fake_produits)
    insert_fake_produits(fake_produits_data)
    fake_clients_data = generate_fake_clients(num_fake_clients)
    insert_fake_clients(fake_clients_data)

    # Créer des fournisseurs
    populate_fournisseurs(no_fournisseurs)
    fournisseurs = Fournisseur.objects.all()

    # Créer des matières premières
    populate_matieres_premieres(no_matieres_premieres)
    matieres_premieres = MatierePremiere.objects.all()

    # Créer des achats pour chaque fournisseur
    for fournisseur in fournisseurs:
        populate_achats(fournisseur, matieres_premieres, no_achats_par_fournisseur)

    # Récupérer la liste des centres
    centres = Centre.objects.all()

    # Récupérer la liste des produits
    produits=MatierePremiere.objects.all()
    # Créer des transferts pour chaque centre
    for centre in centres:
        populate_transferts([centre], produits, no_transferts_par_centre)
    
    # Récupérer la liste des clients
    clients = Client.objects.all()

# Récupérer la liste des produits
    produits = Produit.objects.all()

# Récupérer la liste des matières premières
    matieres = MatierePremiere.objects.all()

# Récupérer la liste des centres
    centres = Centre.objects.all()

# Créer des ventes de produits pour chaque client
    populate_venteP_clients(clients, produits, centres, no_ventesP_par_client)

# Créer des ventes de matières premières pour chaque client
    populate_venteM_clients(clients, matieres, no_ventesM_par_client)
    populate_employes_for_centers(centres, num_fake_employes)


if __name__ == "__main__":
    main()
