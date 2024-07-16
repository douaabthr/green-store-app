from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F


# Create your models here.

class Produit(models.Model):
    codeP = models.CharField(max_length=10,unique=True)
    designation_produit = models.CharField(max_length=50) 
    prix_unitaire_Ven=models.DecimalField(max_digits=15, decimal_places=2,default='0.0')
    quantiteStockPod=models.IntegerField()
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeP
    
class MatierePremiere(models.Model):
    codeM = models.CharField(max_length=10,unique=True)
    designation_matiere = models.CharField(max_length=50)
    quantiteStockMat=models.IntegerField()
    prix_unitaire_Ven=models.DecimalField(max_digits=15, decimal_places=2,default='0.0')
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeM  
    
class Fournisseur(models.Model):
    codeF= models.CharField(max_length=10,unique=True)
    nomF= models.CharField(max_length=50)
    prenomF= models.CharField(max_length=50)
    adresseF=models.CharField(max_length=100)
    telephoneF=models.CharField(max_length=20)
    solde=models.DecimalField(max_digits=10, decimal_places=2)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeF
    
class Centre(models.Model):
    NOM_CHOICES = [
        ('Centre1', 'centre1'),
        ('Centre2', 'centre2'),
        ('Centre3', 'centre3'),
    ]
    CODE_CHOICES = [
        ('c1', 'c1'),
        ('c2', 'c2'),
        ('c3', 'c3'),
    ]
    codeC=models.CharField(max_length=10,unique=True,choices=CODE_CHOICES)
    designation_centre=models.CharField(max_length=50,choices=NOM_CHOICES)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeC  
     
class Employe(models.Model):
    codeEmp=models.CharField(max_length=50,unique=True)
    nomEmp=models.CharField(max_length=50)
    prenomEmp=models.CharField(max_length=50)
    adresseEmp=models.CharField(max_length=100)
    telephoneEmp=models.CharField(max_length=20)
    salaire_jour=models.DecimalField(max_digits=10, decimal_places=2)
    EmployeCentre = models.ForeignKey(Centre, null= True, on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeEmp
    
class Client(models.Model):
    codeCl=models.CharField(max_length=10,unique=True)
    nomCl=models.CharField(max_length=50)
    prenomCl=models.CharField(max_length=50)
    adresseCl=models.CharField(max_length=100)
    telephoneCl=models.CharField(max_length=20)
    credit=models.DecimalField(max_digits=10, decimal_places=2)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.codeCl 
    
class Achat(models.Model):
    fournisseur= models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    matiere_achete=models.ForeignKey(MatierePremiere, on_delete=models.CASCADE)
    buyed_at=models.DateTimeField()
    prix_unitaire_HT=models.DecimalField(max_digits=10, decimal_places=2)
    quantitHT=models.IntegerField()
    quantitDispo=models.IntegerField(default=0)
    montantTotalHT=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['fournisseur', 'matiere_achete','buyed_at']
    def save(self, *args, **kwargs):
        # Calculer le montant total
        self.montantTotalHT = self.prix_unitaire_HT * self.quantitHT
        super(Achat, self).save(*args, **kwargs)

class VenteP(models.Model):
    LIEU_CHOICES = [
        ('Centre1', 'centre1'),
        ('Centre2', 'centre2'),
        ('Centre3', 'centre3'),
    ]
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    produit_vendus=models.ForeignKey(Produit,on_delete=models.CASCADE)
    salled_at=models.DateTimeField()
    prix_unitaire_Ven=models.DecimalField(max_digits=10, decimal_places=2)
    quantitVen=models.IntegerField()
    lieu_ventes=models.ForeignKey(Centre, on_delete=models.CASCADE)
    montantTotalVen=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['client', 'produit_vendus','salled_at','lieu_ventes']
    def save(self, *args, **kwargs):
        # Calculer le montant total
        self.montantTotalVen = self.prix_unitaire_Ven * self.quantitVen
        super(VenteP, self).save(*args, **kwargs)


class VenteM(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    matiere_vendus=models.ForeignKey(MatierePremiere,on_delete=models.CASCADE)
    salled_at=models.DateTimeField()
    prix_unitaire_Ven=models.DecimalField(max_digits=10, decimal_places=2)
    quantitVen=models.IntegerField()
    montantTotalVen=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ['client', 'matiere_vendus','salled_at']
    def save(self, *args, **kwargs):
        # Calculer le montant total
        self.montantTotalVen = self.prix_unitaire_Ven * self.quantitVen
        super(VenteM, self).save(*args, **kwargs)


class Transfert(models.Model):
    centre=models.ForeignKey(Centre,on_delete=models.CASCADE)
    produit_transfere=models.ForeignKey(MatierePremiere,on_delete=models.CASCADE,default='M001')
    transfer_at=models.DateTimeField()
    quantitTran=models.IntegerField()
    cout_transfere=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['centre', 'produit_transfere','transfer_at']


class PaymentAchat(models.Model):
    fournisseur= models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    pay_at=models.DateTimeField()
    montant_reglement=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['fournisseur', 'pay_at']

class PaymentVente(models.Model):
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    pay_at=models.DateTimeField()
    montant_paye=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['client', 'pay_at']

class Massrouf(models.Model):
    employe= models.ForeignKey(Employe, on_delete=models.CASCADE)
    demende_at=models.DateField()
    montant_dem=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['employe', 'demende_at']

class Ingridiant(models.Model):
    produit= models.ForeignKey(Produit, on_delete=models.CASCADE)
    matiere= models.ForeignKey(MatierePremiere,on_delete=models.CASCADE)
    class Meta:
        unique_together = ['produit', 'matiere']

class Absent(models.Model):
    employe= models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_abcence=models.DateTimeField()
    class Meta:
    # Définir la clé primaire sur la combinaison de client et produit
        unique_together = ['employe', 'date_abcence']


