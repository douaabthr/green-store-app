from django.db.models import fields
from django import forms
from .models import PaymentAchat
from .models import PaymentVente
from .models import Fournisseur
from .models import Achat
from .models import VenteP
from .models import VenteM
from .models import Client
from .models import Produit
from .models import Centre
from .models import MatierePremiere
from .models import Transfert

class PaymentAchatForm(forms.ModelForm): 
    class Meta:
        model = PaymentAchat
        fields="__all__"
        labels = {
            'fournisseur': 'Fournisseur',
            'pay_at': 'Date de payement',
            'montant_reglement': 'Montant  reglement',
          }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'client' et 'produit_vendus' en lecture seule
        self.fields['fournisseur'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['fournisseur'].disabled = True

        self.fields['pay_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['pay_at'].disabled = True


class PaymentVenteForm(forms.ModelForm): 
    class Meta:
        model = PaymentVente
        fields="__all__"
        labels = {
            'client': 'Client',
            'pay_at': 'Date de payement',
            'montant_reglement': 'Montant  reglement',
          }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'client' et 'produit_vendus' en lecture seule
        self.fields['client'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['client'].disabled = True

        self.fields['pay_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['pay_at'].disabled = True


class PaymentAchatFormForAjout(forms.ModelForm): 
    pay_at=forms.DateField(label='Date de payement', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = PaymentAchat
        fields="__all__"
        labels = {
            'fournisseur': 'Fournisseur',
            'pay_at': 'Date de payement',
            'montant_reglement': 'Montant  reglement',
          }
        



class PaymentVenteFormForAjout(forms.ModelForm): 
    pay_at=forms.DateField(label='Date de payement', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = PaymentVente
        fields="__all__"
        labels = {
            'client': 'Client',
            'pay_at': 'Date de payement',
            'montant_reglement': 'Montant  reglement',
          }
        



from django import forms
from .models import Fournisseur  # Assurez-vous d'importer votre modèle Fournisseur

from django import forms
from .models import Fournisseur

class FiltreAchatForm(forms.Form):
    fournisseur =forms.ModelChoiceField(queryset=Fournisseur.objects.all(), required=False,label=
    "Fournisseur"
    )

    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_deb'}),
        required=False,
        label='Date de débuts',
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_fin'}),
        required=False,
        label='Date de fin',
    )


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        exclude=['quantitDispo','montantTotalHT']
        labels = {
            'fournisseur': 'Fournisseur',
            'matiere_achete': 'Matiere vendu',
            'buyed_at': 'Date de achat',
            'prix_unitaire_HT': 'Prix unitaire de achat',
            'quantitHT': 'Quantité achete',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'client' et 'produit_vendus' en lecture seule
        self.fields['fournisseur'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['matiere_achete'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['fournisseur'].disabled = True
        self.fields['matiere_achete'].disabled = True

        self.fields['buyed_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['buyed_at'].disabled = True


class FiltreVenteForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False,label="Client")
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_deb'}),
        required=False,
        label='Date de débuts',
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_fin'}),
        required=False,
        label='Date de fin',
    )

class FiltreVentePForm(forms.Form):
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(), required=False,label="Produit")
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_deb'}),
        required=False,
        label='Date de débuts',
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_fin'}),
        required=False,
        label='Date de fin',
    )

from django import forms
from .models import VenteP

class VentePForm(forms.ModelForm):
    class Meta:
        model = VenteP
        exclude=['montantTotalVen']
        labels = {
            'client': 'Client',
            'produit_vendus': 'Produit vendu',
            'salled_at': 'Date de vente',
            'prix_unitaire_Ven': 'Prix unitaire de vente',
            'quantitVen': 'Quantité vendue',
            'lieu_ventes': 'Lieu de vente',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'client' et 'produit_vendus' en lecture seule
        self.fields['client'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['produit_vendus'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['client'].disabled = True
        self.fields['produit_vendus'].disabled = True

        self.fields['salled_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['salled_at'].disabled = True

        self.fields['lieu_ventes'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['lieu_ventes'].disabled = True

        self.fields['prix_unitaire_Ven'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['prix_unitaire_Ven'].disabled = True

class VenteMForm(forms.ModelForm):
    class Meta:
        model = VenteM
        exclude=['montantTotalVen']
        labels = {
            'client': 'Client',
            'matiere_vendus': 'Matière première vendue',
            'salled_at': 'Date de vente',
            'prix_unitaire_Ven': 'Prix unitaire de vente',
            'quantitVen': 'Quantité vendue',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'client' et 'matiere_vendus' en lecture seule
        self.fields['client'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['matiere_vendus'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['client'].disabled = True
        self.fields['matiere_vendus'].disabled = True

        self.fields['salled_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['salled_at'].disabled = True

        self.fields['prix_unitaire_Ven'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['prix_unitaire_Ven'].disabled = True



class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        exclude=['cout_transfere']
        labels = {
            'centre': 'Centre',
            'produit_transfere': 'Matiere transféré',
            'transfer_at': 'Date de transfert',
            'quantitTran': 'Quantité transférée',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rendre les champs 'centre' et 'produit_transfere' en lecture seule
        self.fields['centre'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['produit_transfere'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        

        # Désactiver les champs côté serveur (backend)
        self.fields['centre'].disabled = True
        self.fields['produit_transfere'].disabled = True

        self.fields['transfer_at'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['transfer_at'].disabled = True

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude = ['active']
        labels = {
            'codeP': 'Code du produit',
            'designation_produit': 'Désignation du produit',
            'prix_unitaire_Ven': 'Prix unitaire de vente',
            'created_at': 'Date de création',
            'quantiteStockPod': 'Quantité en stock',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codeP'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['codeP'].disabled = True

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        exclude = ['active']
        labels = {
            'codeF': 'Code du fournisseur',
            'nomF': 'Nom du fournisseur',
            'prenomF': 'Prénom du fournisseur',
            'adresseF': 'Adresse du fournisseur',
            'telephoneF': 'Téléphone du fournisseur',
            'solde': 'Solde du fournisseur',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codeF'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['codeF'].disabled = True

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['active']
        labels = {
            'codeCl': 'Code du client',
            'nomCl': 'Nom du client',
            'prenomCl': 'Prénom du client',
            'adresseCl': 'Adresse du client',
            'telephoneCl': 'Téléphone du client',
            'credit': 'Crédit du client',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codeCl'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['codeCl'].disabled = True

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        exclude = ['active']
        labels = {
            'codeC': 'Code du centre',
            'designation_centre': 'Désignation du centre',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codeC'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['codeC'].disabled = True

from .models import Employe, MatierePremiere

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ['active']
        labels = {
            'codeEmp': 'Code de l\'employé',
            'nomEmp': 'Nom de l\'employé',
            'prenomEmp': 'Prénom de l\'employé',
            'adresseEmp': 'Adresse de l\'employé',
            'telephoneEmp': 'Téléphone de l\'employé',
            'salaire_jour': 'Salaire par jour',
            'EmployeCentre': 'Centre de l\'employé',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codeEmp'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        # Désactiver les champs côté serveur (backend)
        self.fields['codeEmp'].disabled = True

class MatiereForm(forms.ModelForm):
    class Meta:
        model = MatierePremiere
        exclude = ['active']
        labels = {
            'codeM': 'Code de la matière première',
            'designation_matiere': 'Désignation de la matière première',
            'created_at': 'Date de création',
            'quantiteStockMat': 'Quantité en stock',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codeM'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['codeM'].disabled = True
        self.fields['quantiteStockMat'].disabled=True


class FiltreStockForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), required=False, label='Fournisseur')
    date_achat = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False, label='Date d\'Achat')
    codeM = forms.ModelChoiceField(queryset=MatierePremiere.objects.all(), to_field_name='codeM', required=False, label='Matières')

class FiltreTransfertForm(forms.Form):
    centre = forms.ModelChoiceField(queryset=Centre.objects.all(), to_field_name='codeC', required=False, label='Centre')
    produit_transfere = forms.ModelChoiceField(queryset=MatierePremiere.objects.all(), to_field_name='codeM', required=False, label='Matière')
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_deb'}),
        required=False,
        label='Date de débuts',
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_fin'}),
        required=False,
        label='Date de fin',
    )
class FiltreTransfertRecuForm(forms.Form):
    produit_transfere = forms.ModelChoiceField(queryset=MatierePremiere.objects.all(), to_field_name='codeM', required=False, label='Matière')
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_deb'}),
        required=False,
        label='Date de débuts',
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','id': 'id_date_fin'}),
        required=False,
        label='Date de fin',
    )
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


class ProduitForm1(forms.ModelForm):
    class Meta:
        model = Produit
        exclude=['active']
        labels = {
            'codeP':'code produit',
            'designation_produit': 'Désignation du Produit',
            'quantiteStockPod': 'Quantité en Stock',
            'prix_unitair_vente': 'Prix Unitaire de Vente',
        }
class MatiereForm1(forms.ModelForm):
    class Meta:
        model = MatierePremiere
        exclude=['active']
        labels = {
            'codeM':'code matiere',
            'designation_matiere': 'Désignation du matiere',
            'quantiteStockMat': 'Quantité en Stock',
            'prix_unitair_vente': 'Prix Unitaire de Vente',
        }

class ClientForm1(forms.ModelForm):
    class Meta:
        model = Client
        exclude=['active']
        labels = {
            'nomCl': 'Nom du Client',
            'prenomCl': 'Prénom du Client',
            'adresseCl': 'Adresse du Client',
            'telephoneCl': 'Téléphone du Client',
            'credit': 'Crédit du Client',
        }

class FournisseurForm1(forms.ModelForm):
    class Meta:
        model = Fournisseur
        exclude=['active']
        labels = {
            'nomF': 'Nom du Fournisseur',
            'prenomF': 'Prénom du Fournisseur',
            'adresseF': 'Adresse du Fournisseur',
            'telephoneF': 'Téléphone du Fournisseur',
            'solde': 'Solde du Fournisseur',
        }

class CentreForm1(forms.ModelForm):
    class Meta:
        model = Centre
        exclude=['active']
        labels = {
            'designation_centre': 'Désignation du Centre',
        }

class EmployeForm1(forms.ModelForm):
    class Meta:
        model = Employe
        exclude=['active']
        labels = {
            'nomEmp': 'Nom de l\'Employé',
            'prenomEmp': 'Prénom de l\'Employé',
            'adresseEmp': 'Adresse de l\'Employé',
            'telephoneEmp': 'Téléphone de l\'Employé',
            'salaire_jour': 'Salaire par Jour de l\'Employé',
            'EmployeCentre': 'Centre de l\'Employé',
        }

class AchatForm1(forms.ModelForm):
    buyed_at = forms.DateField(label='Date d\'achat', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Achat
        exclude = ['matiere_achete', 'montantTotalHT', 'quantitDispo']
        labels = {
            'fournisseur': 'Fournisseur',
            'prix_unitaire_HT': 'Prix Unitaire HT',
            'quantitHT': 'Quantité HT',

        }

class tranForm(forms.ModelForm):
    transfer_at = forms.DateField(label='Date d\'achat', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Transfert
        exclude = ['cout_transfere']
        labels = {
            'centre': 'Centre de Destination',
            'produit_transfere': 'Produit à Transférer',
            'quantitTran': 'Quantité à Transférer',
        }

from .models import Massrouf

class MassroufForm(forms.ModelForm):
    class Meta:
        model = Massrouf
        fields = "__all__"
        labels = {
            'employe': 'Employé',
            'demende_at': 'Date de la Demande',
            'montant_dem': 'Montant de la Demande',
        }

class VendreProduitForm(forms.ModelForm):
    salled_at = forms.DateField(label='Date d\'achat', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = VenteP
        exclude = ['montantTotalVen','produit_vendus','prix_unitaire_Ven']
        labels = {
            'client': 'Client',
            'salled_at': 'Date de la Vente',
            'lieu_ventes': 'Lieu de la Vente',
        }
class VendreMatiereForm(forms.ModelForm):
    salled_at = forms.DateField(label='Date d\'achat', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = VenteM
        exclude = ['montantTotalVen','matiere_vendus','prix_unitaire_Ven']
        labels = {
            'client': 'Client',
            'salled_at': 'Date de la Vente',
        }
class FiltreTransfereForm(forms.ModelForm):
    date_debut = forms.DateField(label='Date de début', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    date_fin = forms.DateField(label='Date de fin', widget=forms.TextInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Transfert
        exclude = ['transfer_at', 'quantitTran', 'cout_transfere']
        labels = {
            'produit_transfere': 'Produit',
            'centre': 'Centre'
        }
        produit_transfere = forms.CharField(required=False)
        centre = forms.CharField(required=False)
class FiltreAchatForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), to_field_name='codeF',required=False,label='Fournisseur')
    date_debut = forms.DateField(label='Date de début', widget=forms.TextInput(attrs={'type': 'date'}),required=False)
    date_fin = forms.DateField(label='Date de fin', widget=forms.TextInput(attrs={'type': 'date'}),required=False)

class MonFormulaire(forms.Form):
    date_achats = forms.IntegerField(label='Année d\'analyse des achats', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    date_top_fournisseurs = forms.IntegerField(label='Année  meilleurs fournisseurs', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    nb_fournisseur = forms.IntegerField(label='Nombre  meilleurs fournisseurs', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    Annee_min_pour_best_client = forms.IntegerField(label='Année d\'analyse  meilleurs clients', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    if Annee_min_pour_best_client is not None and Annee_min_pour_best_client == 0:
            raise forms.ValidationError("Veuillez entrer une année valide (supérieure à zéro).")
    nombre_best_clients = forms.IntegerField(label='Nombre  meilleurs clients', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    Annee_min_Vente = forms.IntegerField(label='Année d\'analyse des ventes', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    Annee_min_pour_top_produit = forms.IntegerField(label='Année d\'analyse  meilleurs produits', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    nombre_top_produits = forms.IntegerField(label='Nombre  meilleurs produits', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
class MonFormulaire_centre1(forms.Form):
    
    Annee_min_pour_best_client = forms.IntegerField(label='Année d\'analyse  meilleurs clients', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    nombre_best_clients = forms.IntegerField(label='Nombre  meilleurs clients', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    Annee_min_Vente = forms.IntegerField(label='Année d\'analyse des ventes', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    Annee_min_pour_top_produit = forms.IntegerField(label='Année d\'analyse  meilleurs produits', required=False, widget=forms.NumberInput(attrs={'size': '5'}))
    nombre_top_produits = forms.IntegerField(label='Nombre  meilleurs produits', required=False, widget=forms.NumberInput(attrs={'size': '5'}))




