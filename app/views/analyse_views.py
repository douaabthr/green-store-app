from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Achat
from ..forms import PaymentAchatForm
from ..models import PaymentAchat
from ..forms import FiltreAchatForm
from ..forms import FiltreVenteForm
from ..forms import AchatForm
from ..forms import PaymentVenteForm
from ..forms import PaymentVenteFormForAjout
from ..forms import PaymentAchatFormForAjout
from ..models import PaymentVente
from ..models import Produit
from ..forms import FiltreStockForm
from ..forms import FiltreTransfertForm
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render,redirect
from django.db.models import Sum,Q
from datetime import datetime
from ..forms import ProduitForm1,MatiereForm1,ClientForm1,FournisseurForm1,EmployeForm1,CentreForm1,AchatForm1,tranForm,VendreProduitForm,FiltreTransfereForm,FiltreAchatForm,MonFormulaire,MonFormulaire_centre1,VendreMatiereForm
from ..models import Produit,Client,Fournisseur,Centre,Employe,Achat,Transfert,VenteP,Absent,Massrouf,MatierePremiere,VenteM
from decimal import Decimal
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, redirect
from ..forms import PaymentAchatFormForAjout
from django.shortcuts import render, redirect
from ..forms import PaymentVenteFormForAjout 
from itertools import chain
from django.shortcuts import render
from django.db.models import Q
from ..models import Produit, Achat
from ..forms import FiltreStockForm
from ..models import VenteP
from ..models import VenteM
from ..forms import VentePForm
from ..forms import VenteMForm
from django.shortcuts import render
from django.db.models import Q
from ..models import Produit, Achat
from ..forms import FiltreStockForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Produit, Achat
from ..forms import FiltreStockForm
from django.db.models import Q
from io import BytesIO
from reportlab.pdfgen import canvas
from ..forms import FiltreVentePForm
from ..models import MatierePremiere
from ..models import Fournisseur
from ..forms import FournisseurForm
from ..models import Centre
from ..forms import CentreForm 
from django.shortcuts import render, redirect
from ..models import Employe
from ..forms import EmployeForm
from ..models import Transfert
from ..forms import MatiereForm
from ..models import Transfert
from ..forms import FiltreTransfertRecuForm 
from ..models import Ingridiant
from decimal import Decimal
from ..forms import TransfertForm
from django.contrib.auth.forms import UserCreationForm
from ..forms import UserCreationForm
from ..forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from ..tokens import account_activation_token
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import login
from ..tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..forms import ProduitForm1,MatiereForm1,ClientForm1,FournisseurForm1,EmployeForm1,CentreForm1,AchatForm1,tranForm,VendreProduitForm,FiltreTransfereForm,FiltreAchatForm,MonFormulaire,MonFormulaire_centre1,VendreMatiereForm
from ..models import Produit,Client,Fournisseur,Centre,Employe,Achat,Transfert,VenteP,Absent,Massrouf,MatierePremiere,VenteM
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse

def indexView(request):
    # Récupérer l'année à partir de la date actuelle
    nb_notification=notification1()

    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year

    
        # traitement pour afficher les top fournisseur de annee actuelle 

    # debut
    
    top_fournisseur_anne_actuelle = Achat.objects.filter(
    buyed_at__year=annee_actuelle
                  ).values(
                'fournisseur__nomF',
                'fournisseur__prenomF').annotate(
                total_achats=Sum('montantTotalHT')
                ).order_by(
                '-total_achats'
                )[:5]
    # fin
    Annee_min_pour_top_fournisseur = annee_actuelle-2
    nomber_top_fournisseurs = 5
    Annee_min_Achat=2023
    if request.method == 'POST':
            form = MonFormulaire(request.POST)

    else:
        form = MonFormulaire()

        # traitement pour afficher nb top fournisseur de anne actuel vers annee min
        Annee_min_pour_top_fournisseur = request.POST.get('Annee_min')
        nomber_top_fournisseurs = request.POST.get('nbr_tops')
        Annee_min_Achat=request.POST.get('Annee_min_Achat')
        print("")
        if Annee_min_Achat:
            Annee_min_Achat = int(Annee_min_Achat)
        else :
            Annee_min_Achat=2023
        if Annee_min_pour_top_fournisseur:
            Annee_min_pour_top_fournisseur=int(Annee_min_pour_top_fournisseur)
        else:
            Annee_min_pour_top_fournisseur = annee_actuelle-2
        if nomber_top_fournisseurs:
            nomber_top_fournisseurs=int(nomber_top_fournisseurs)
        else :
            nomber_top_fournisseurs = 5


        # debut
            
    top_fournisseurs = Achat.objects.filter(
    buyed_at__year__gte=Annee_min_pour_top_fournisseur,buyed_at__year__lte=annee_actuelle
            ).values(
            'fournisseur__nomF',
            'fournisseur__prenomF').annotate(
            total_achats=Sum('montantTotalHT')
            ).order_by(
            '-total_achats'
            )[:nomber_top_fournisseurs]
        
        #traitement pour affocher les evaulotions des taux 
    n=12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    print("la tables des cles ",dic)





    annee_analyse=annee_actuelle-Annee_min_Achat
    if annee_analyse==0:
        nombre_mois = 12
        annee_analyse=1
    else :
        nombre_mois = annee_analyse*12
    
    # Recherche de la clé dans le dictionnaire
    for element in dic:
        if element['nombre_de_mois'] == nombre_mois:
            cle = element.get('cle')
    print("",annee_analyse)
    total_achat_precedent=0
    evoluation_taux_sur_annees=[]
    Annee_min_Achat_debut=Annee_min_Achat
    
    intervalle=0
    y=12/cle
    y=int(y)
    for annee_acoule in range(0, annee_analyse):
        fin_periode=0
        for periode in range(0,y):

            debut_periode=fin_periode+1
            fin_periode=fin_periode+cle
            total_achats = Achat.objects.filter(
                buyed_at__month__gte=debut_periode,
                buyed_at__month__lte=fin_periode,
                buyed_at__year=Annee_min_Achat_debut
                ).aggregate(Sum('montantTotalHT'))['montantTotalHT__sum'] or 0
            taux_achat=Decimal('0.00')
            if total_achat_precedent !=0 and total_achats !=0 :
                taux_achat=(total_achats-total_achat_precedent)/total_achat_precedent*100

            total_achat_precedent=total_achats
            intervalle=intervalle+cle
            
            taux={
                'valeur_achat':taux_achat,
                    'mois':intervalle
                    }
            evoluation_taux_sur_annees.append(taux)
        Annee_min_Achat_debut=Annee_min_Achat_debut+1
    
    
    total_achat_precedent=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_sur_annee=[]
    for month in months:
        total_achats=Achat.objects.filter(buyed_at__month=month,buyed_at__year=annee_actuelle).aggregate(Sum('montantTotalHT'))['montantTotalHT__sum']  or 0 
        taux_achat=0
        if total_achat_precedent !=0 and total_achats !=0:
            taux_achat=(total_achats-total_achat_precedent)/total_achat_precedent*100

        total_achat_precedent=total_achats
        taux={
                'valeur_achat':taux_achat,
                'mois':month
            }
        evoluation_taux_sur_annee.append(taux)
        # analyse de ventes 
    annee_actuelle = datetime.now().year
    valeur_presedent_ventes = 0
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    evoluation_taux_ventes_annee = []

    for month in months:
        total_ventes = VenteM.objects.filter(salled_at__month=month, salled_at__year=annee_actuelle).aggregate(
            Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

        taux_vente = 0
        if valeur_presedent_ventes != 0 and total_ventes != 0:
            taux_vente = (total_ventes - valeur_presedent_ventes) / valeur_presedent_ventes * 100

        valeur_presedent_ventes = total_ventes
        taux = {
            'valeur_Vente': taux_vente,
            'mois': month
        }
        evoluation_taux_ventes_annee.append(taux)
    valeur_presedent_benefice = 0
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    evoluation_taux_Benifice_annee = []

    for month in months:
        total_ventes = VenteM.objects.filter(salled_at__month=month, salled_at__year=annee_actuelle).aggregate(
            Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
        total_Transfere = Achat.objects.filter(buyed_at__month=month, buyed_at__year=annee_actuelle).aggregate(
            Sum('montantTotalHT'))['montantTotalHT__sum'] or 0
        valeur_benefice = total_ventes - total_Transfere
        taux_benefice = 0
        if valeur_presedent_benefice != 0 and valeur_benefice != 0:
            taux_benefice = (valeur_benefice - valeur_presedent_benefice) / valeur_presedent_benefice * 100

        valeur_presedent_benefice = valeur_benefice
        taux = {
            'valeur_benefice': taux_benefice,
            'mois': month
        }
        evoluation_taux_Benifice_annee.append(taux)
    top_clients_anne_actuelle = VenteM.objects.filter(
    salled_at__year=annee_actuelle
).values(
    'client__nomCl',
    'client__prenomCl').annotate(
    total_vent=Sum('montantTotalVen')
).order_by(
    '-total_vent'
)[:5]
    
    best_sellers = VenteM.objects.filter(
    salled_at__year=datetime.now().year
).values(
    'matiere_vendus__designation_matiere'
).annotate(
    total_qte=Sum('quantitVen')
).order_by(
    '-total_qte'
)[:5]

# Calculate total sales for the current year
    total_ventes = VenteM.objects.filter(salled_at__year=annee_actuelle).aggregate(total=Sum('montantTotalVen'))['total'] or 0

# Calculate total purchases for the current year
    total_achat = Achat.objects.filter(buyed_at__year=annee_actuelle).aggregate(total=Sum('montantTotalHT'))['total'] or 0
    total_cost_transferred = Transfert.objects.filter(transfer_at__year=annee_actuelle).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

    valeur_benefice=total_ventes-total_achat
    if total_ventes ==0:
         pourCentageBenefice=0
    else :
        pourCentageBenefice=valeur_benefice*100/total_ventes
    
    return render(request,"layout/index.html",{
                                        "nb_notification":nb_notification,
                                        "form":form,"total_ventes":total_ventes,
                                        "total_Achat":total_achat,
                                        "total_Transfere":total_cost_transferred,
                                        "valeur_benefice":valeur_benefice,
                                        "pourCentageBenefice":pourCentageBenefice
                                        ,"Best_seller":best_sellers,"top_clients_anne_actuelle":top_clients_anne_actuelle,"evoluation_taux_Benifice_annee":evoluation_taux_Benifice_annee,"evoluation_taux_ventes_annee":evoluation_taux_ventes_annee,"fournisseurs":top_fournisseur_anne_actuelle,"evoluation_taux_sur_annee":evoluation_taux_sur_annee,"evoluation_taux_sur_annees":evoluation_taux_sur_annees,"top_fournisseur_annees":top_fournisseurs})

def analyse(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    Annee_min_pour_top_fournisseur = annee_actuelle
    nomber_top_fournisseurs = 5
    Annee_min_Achat=annee_actuelle
    Annee_min_pour_best_client=annee_actuelle
    nombre_best_clients=5
    Annee_min_Vente=annee_actuelle
    Annee_min_pour_top_produit=annee_actuelle
    nombre_top_produits=5

    if request.method == 'POST':
        form = MonFormulaire(request.POST)

        if form.is_valid():
            # Accédez aux données du formulaire comme suit
            Annee_min_Achat = form.cleaned_data['date_achats']
            Annee_min_pour_top_fournisseur = form.cleaned_data['date_top_fournisseurs']
            nomber_top_fournisseurs = form.cleaned_data['nb_fournisseur']
            Annee_min_pour_best_client = form.cleaned_data['Annee_min_pour_best_client']
            nombre_best_clients = form.cleaned_data['nombre_best_clients']
            Annee_min_Vente = form.cleaned_data['Annee_min_Vente']
            Annee_min_pour_top_produit = form.cleaned_data['Annee_min_pour_top_produit']
            nombre_top_produits = form.cleaned_data['nombre_top_produits']


            
        form = MonFormulaire()
        if  Annee_min_Achat is None:
            Annee_min_Achat=annee_actuelle
        if not Annee_min_pour_top_fournisseur:
            Annee_min_pour_top_fournisseur = annee_actuelle-2
        if  nomber_top_fournisseurs is None:
            nomber_top_fournisseurs = 5
        if not Annee_min_pour_best_client:
            Annee_min_pour_best_client=annee_actuelle
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=annee_actuelle
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=annee_actuelle
        if not nombre_top_produits:
            nombre_top_produits=5
    n=12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse=annee_actuelle-Annee_min_Achat
    if annee_analyse==0:
        nombre_mois = 12
        annee_analyse=1
    else :
        nombre_mois = annee_analyse*12
    
    # Recherche de la clé dans le dictionnaire
    for element in dic:
        if element['nombre_de_mois'] == nombre_mois:
            cle = element.get('cle')
    total_achat_precedent=0
    evoluation_taux_sur_annees=[]
    Annee_min_Achat_debut=Annee_min_Achat
    
    intervalle=0
    y=12/cle
    y=int(y)
    for annee_acoule in range(0, annee_analyse):
        fin_periode=0
        for periode in range(0,y):

            debut_periode=fin_periode+1
            fin_periode=fin_periode+cle
            total_achats = Achat.objects.filter(
                buyed_at__month__gte=debut_periode,
                buyed_at__month__lte=fin_periode,
                buyed_at__year=Annee_min_Achat_debut
                ).aggregate(Sum('montantTotalHT'))['montantTotalHT__sum'] or 0
            taux_achat=Decimal('0.00')
            if total_achat_precedent !=0 and total_achats !=0 :
                taux_achat=(total_achats-total_achat_precedent)/total_achat_precedent*100

            total_achat_precedent=total_achats
            intervalle=intervalle+cle
            
            taux={
                'valeur_achat':taux_achat,
                    'mois':intervalle
                    }
            evoluation_taux_sur_annees.append(taux)
        Annee_min_Achat_debut=Annee_min_Achat_debut+1
    top_fournisseurs = Achat.objects.filter(
    buyed_at__year__gte=Annee_min_pour_top_fournisseur,buyed_at__year__lte=annee_actuelle
            ).values(
            'fournisseur__nomF',
            'fournisseur__prenomF').annotate(
            total_achats=Sum('montantTotalHT')
            ).order_by(
            '-total_achats'
            )[:nomber_top_fournisseurs]
    best_client = VenteM.objects.filter(
        salled_at__year__gte=Annee_min_pour_best_client,
        salled_at__year__lte=annee_actuelle
    ).values(
        'client__codeCl',
        'client__nomCl',
        'client__prenomCl',
        'client__adresseCl',
        'client__telephoneCl'

    ).annotate(
        total_ventes=Sum('montantTotalVen')
    ).order_by(
        '-total_ventes'
    )[:nombre_best_clients]
    top_produits = VenteM.objects.filter(
        salled_at__year__gte=Annee_min_pour_top_produit,
        salled_at__year__lte=annee_actuelle
    ).values(
        'matiere_vendus__codeM',  
        'matiere_vendus__designation_matiere'
    ).annotate(
        total_quantite_vente=Sum('quantitVen')
    ).order_by(
        '-total_quantite_vente'
    )[:nombre_top_produits]
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_vente_precedente = 0
    evolution_taux_vent_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente
    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteM.objects.filter(
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
                taux_vente = Decimal('0.00')
                if total_vente_precedente != 0 and total_ventes != 0:
                    taux_vente = (total_ventes - total_vente_precedente) / total_vente_precedente * 100

                total_vente_precedente = total_ventes
                intervalle = intervalle + cle

                taux = {
                    'valeur_vente': taux_vente,
                    'mois': intervalle
                }
                
                evolution_taux_vent_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_benefice_precedent = 0
    evolution_taux_benefice_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente

    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteM.objects.filter(
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

                total_achats = Achat.objects.filter(
                    buyed_at__month__gte=debut_periode,
                    buyed_at__month__lte=fin_periode,
                    buyed_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalHT'))['montantTotalHT__sum'] or 0

                benefice = total_ventes - total_achats

                taux_benefice = Decimal('0.00')
                if total_benefice_precedent != 0 and benefice != 0:
                    taux_benefice = (benefice - total_benefice_precedent) / total_benefice_precedent * 100

                total_benefice_precedent = benefice
                intervalle = intervalle + cle

                taux = {
                    'valeur_benefice': taux_benefice,
                    'mois': intervalle
                }
                evolution_taux_benefice_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
        # Calculer le montant total des achats
    montant_total_achats = Achat.objects.filter(buyed_at__year__gte=Annee_min_Vente).aggregate(Sum('montantTotalHT'))['montantTotalHT__sum'] or 0

    # Arrondir le montant total à deux chiffres après la virgule
    montant_total_achats = round(montant_total_achats, 2)
    montant_total_ventes = VenteM.objects.filter(salled_at__year__gte=Annee_min_Vente).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
    montant_total_ventes = round(montant_total_ventes, 2)
    benefice = montant_total_ventes - montant_total_achats
        # Calculer le montant total des transferts
    montant_total_transferts = Transfert.objects.filter(transfer_at__year__gte=Annee_min_Vente).aggregate(Sum('cout_transfere'))['cout_transfere__sum'] or 0

    # Arrondir le montant total à deux chiffres après la virgule
    montant_total_transferts = round(montant_total_transferts, 2)
    form=MonFormulaire()
    return render(request, 'analyse.html', {
        "top_produits":top_produits,
        "evolution_taux_benefice_sur_annees":evolution_taux_benefice_sur_annees,
        "evolution_taux_vent_sur_annees":evolution_taux_vent_sur_annees,
        "best_client":best_client,
        "form":form,
        "montant_total_achats":montant_total_achats,
        "benefice":benefice,
        "montant_total_transferts":montant_total_transferts,
        "montant_total_ventes":montant_total_ventes,
        'top_fournisseurs': top_fournisseurs, 'evoluation_taux_sur_annees': evoluation_taux_sur_annees})    
def centre1(request,center_id):
    annee_actuelle=datetime.now().year

    valeur_presedent_ventes=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_ventes_annee=[]
    centre=Centre.objects.get(codeC=center_id)
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=annee_actuelle).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        taux_vente=0
        if valeur_presedent_ventes !=0 and total_ventes !=0:
            taux_vente=(total_ventes-valeur_presedent_ventes)/valeur_presedent_ventes*100

        valeur_presedent_ventes=total_ventes
        taux={
                'valeur_Vente':taux_vente,
                'mois':month
            }
        evoluation_taux_ventes_annee.append(taux)
    #  analyse de ventes 
        annee_actuelle=datetime.now()
    valeur_presedent_benefice=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_Benifice_annee=[]
    centre=Centre.objects.get(codeC=center_id)
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=annee_actuelle).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        total_Transfere=Transfert.objects.filter(centre__codeC=centre,transfer_at__month=month,transfer_at__year=annee_actuelle.year).aggregate(Sum('cout_transfere'))['cout_transfere__sum']  or 0 
        valeur_benefice=total_ventes-total_Transfere
        taux_benefice=0
        if valeur_presedent_benefice !=0 and valeur_benefice !=0:
            taux_benefice=(valeur_benefice-valeur_presedent_benefice)/valeur_presedent_benefice*100

        valeur_presedent_benefice=valeur_benefice
        taux={
                'valeur_benefice':taux_benefice,
                'mois':month
            }
        evoluation_taux_Benifice_annee.append(taux)
    top_clients_anne_actuelle = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=annee_actuelle
                  ).values(
                'client__nomCl',
                'client__prenomCl').annotate(
                total_vent=Sum('montantTotalVen')
                ).order_by(
                '-total_vent'
                )[:5]
    Best_seller = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=annee_actuelle
                  ).values(
                'produit_vendus__designation_produit'
                ).annotate(
                total_qte=Sum('quantitVen')
                ).order_by(
                '-total_qte'
                )[:5]
    current_year = datetime.now().year

# Replace with the actual center and product IDs
    
    total_cost_transferred = Transfert.objects.filter(centre=centre.id,transfer_at__year=annee_actuelle).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year=annee_actuelle).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request,"Centre1.html",{
        "total_cost_transferred":total_cost_transferred,
        "total_amount_sold":total_amount_sold,
        "total_profit":total_profit,
        "Best_seller":Best_seller,"top_clients_anne_actuelle":top_clients_anne_actuelle,"evoluation_taux_ventes_annee":evoluation_taux_ventes_annee,"evoluation_taux_Benifice_annee":evoluation_taux_Benifice_annee})
def centre2(request):
    annee_actuelle=datetime.now()
    valeur_presedent_ventes=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_ventes_annee=[]
    centre=Centre.objects.get(codeC='c2')

    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=annee_actuelle).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        taux_vente=0
        if valeur_presedent_ventes !=0 and total_ventes !=0:
            taux_vente=(total_ventes-valeur_presedent_ventes)/valeur_presedent_ventes*100

        valeur_presedent_ventes=total_ventes
        taux={
                'valeur_Vente':taux_vente,
                'mois':month
            }
        evoluation_taux_ventes_annee.append(taux)
    #  analyse de ventes 
        annee_actuelle=datetime.now()
    valeur_presedent_benefice=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_Benifice_annee=[]
    centre=Centre.objects.get(codeC='c2')
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=2024).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        total_Transfere=Transfert.objects.filter(centre__codeC=centre,transfer_at__month=month,transfer_at__year=annee_actuelle.year).aggregate(Sum('cout_transfere'))['cout_transfere__sum']  or 0 
        valeur_benefice=total_ventes-total_Transfere
        taux_benefice=0
        if valeur_presedent_benefice !=0 and valeur_benefice !=0:
            taux_benefice=(valeur_benefice-valeur_presedent_benefice)/valeur_presedent_benefice*100

        valeur_presedent_benefice=valeur_benefice
        taux={
                'valeur_benefice':taux_benefice,
                'mois':month
            }
        evoluation_taux_Benifice_annee.append(taux)
    top_clients_anne_actuelle = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=2024
                  ).values(
                'client__nomCl',
                'client__prenomCl').annotate(
                total_vent=Sum('montantTotalVen')
                ).order_by(
                '-total_vent'
                )[:5]
    Best_seller = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=2024
                  ).values(
                
                'produit_vendus__designation_produit'
                ).annotate(
                total_qte=Sum('quantitVen')
                ).order_by(
                '-total_qte'
                )[:5]

# Replace with the actual center and product IDs


    total_cost_transferred = Transfert.objects.filter(centre=centre.id,transfer_at__year=2024).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id, salled_at__year=2024).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request,"Centre2.html",{
        "total_cost_transferred":total_cost_transferred,
        "total_amount_sold":total_amount_sold,
        "total_profit":total_profit,
        "Best_seller":Best_seller,"top_clients_anne_actuelle":top_clients_anne_actuelle,"evoluation_taux_ventes_annee":evoluation_taux_ventes_annee,"evoluation_taux_Benifice_annee":evoluation_taux_Benifice_annee})
def centre3(request):
    annee_actuelle=datetime.now()
    valeur_presedent_ventes=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_ventes_annee=[]
    centre=Centre.objects.get(codeC='c3')
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre,salled_at__month=month,salled_at__year=2024).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        taux_vente=0
        if valeur_presedent_ventes !=0 and total_ventes !=0:
            taux_vente=(total_ventes-valeur_presedent_ventes)/valeur_presedent_ventes*100

        valeur_presedent_ventes=total_ventes
        taux={
                'valeur_Vente':taux_vente,
                'mois':month
            }
        evoluation_taux_ventes_annee.append(taux)
    #  analyse de ventes 
        annee_actuelle=datetime.now()
    valeur_presedent_benefice=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_Benifice_annee=[]
    centre=Centre.objects.get(codeC='c3')
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=2024).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
        total_Transfere=Transfert.objects.filter(centre__codeC=centre,transfer_at__month=month,transfer_at__year=annee_actuelle.year).aggregate(Sum('cout_transfere'))['cout_transfere__sum']  or 0 
        valeur_benefice=total_ventes-total_Transfere
        taux_benefice=0
        if valeur_presedent_benefice !=0 and valeur_benefice !=0:
            taux_benefice=(valeur_benefice-valeur_presedent_benefice)/valeur_presedent_benefice*100

        valeur_presedent_benefice=valeur_benefice
        taux={
                'valeur_benefice':taux_benefice,
                'mois':month
            }
        evoluation_taux_Benifice_annee.append(taux)
    top_clients_anne_actuelle = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=2024
                  ).values(
                'client__nomCl',
                'client__prenomCl').annotate(
                total_vent=Sum('montantTotalVen')
                ).order_by(
                '-total_vent'
                )[:5]
    Best_seller = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year=2024
                  ).values(
                
                'produit_vendus__designation_produit'
                ).annotate(
                total_qte=Sum('quantitVen')
                ).order_by(
                '-total_qte'
                )[:5]
    current_year = datetime.now().year

# Replace with the actual center and product IDs


    total_cost_transferred = Transfert.objects.filter(centre=centre.id,transfer_at__year=2024).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id ,salled_at__year=2024).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request,"Centre3.html",{
        "total_cost_transferred":total_cost_transferred,
        "total_amount_sold":total_amount_sold,
        "total_profit":total_profit,
        "Best_seller":Best_seller,"top_clients_anne_actuelle":top_clients_anne_actuelle,"evoluation_taux_ventes_annee":evoluation_taux_ventes_annee,"evoluation_taux_Benifice_annee":evoluation_taux_Benifice_annee})
def analyse_centre1(request,center_id):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    centre=Centre.objects.get(codeC=center_id)
    Annee_min_pour_best_client=date_actuelle.year
    nombre_best_clients=5
    Annee_min_Vente=date_actuelle.year
    Annee_min_pour_top_produit=date_actuelle.year
    nombre_top_produits=5

    if request.method == 'POST':
        form = MonFormulaire_centre1(request.POST)

        if form.is_valid():
            # Accédez aux données du formulaire comme suit
            Annee_min_pour_best_client = form.cleaned_data['Annee_min_pour_best_client']
            nombre_best_clients = form.cleaned_data['nombre_best_clients']
            Annee_min_Vente = form.cleaned_data['Annee_min_Vente']
            Annee_min_pour_top_produit = form.cleaned_data['Annee_min_pour_top_produit']
            nombre_top_produits = form.cleaned_data['nombre_top_produits']
        form = MonFormulaire_centre1()

        if not  Annee_min_pour_best_client:
            Annee_min_pour_best_client=date_actuelle.year
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=date_actuelle.year
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=date_actuelle.year
        if not nombre_top_produits:
            nombre_top_produits=5
        
    best_client = VenteP.objects.filter(
        lieu_ventes=centre.id,
        salled_at__year__gte=Annee_min_pour_best_client,
        salled_at__year__lte=annee_actuelle
    ).values(
        'client__codeCl',
        'client__nomCl',
        'client__prenomCl',
        'client__adresseCl',
        'client__telephoneCl'

    ).annotate(
        total_ventes=Sum('montantTotalVen')
    ).order_by(
        '-total_ventes'
    )[:nombre_best_clients]
    
    top_produits = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year__gte=Annee_min_pour_top_produit,
    salled_at__year__lte=annee_actuelle
).values(
    'produit_vendus__codeP',  
    'produit_vendus__designation_produit'

).annotate(
    total_quantite_vente=Sum('quantitVen')
).order_by(
    '-total_quantite_vente'
)[:nombre_top_produits]
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_vente_precedente = 0
    evolution_taux_vent_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente
    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
                taux_vente = Decimal('0.00')
                if total_vente_precedente != 0 and total_ventes != 0:
                    taux_vente = (total_ventes - total_vente_precedente) / total_vente_precedente * 100

                total_vente_precedente = total_ventes
                intervalle = intervalle + cle

                taux = {
                    'valeur_vente': taux_vente,
                    'mois': intervalle
                }
                evolution_taux_vent_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_benefice_precedent = 0
    evolution_taux_benefice_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente

    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

                total_Transfere = Transfert.objects.filter(
                    centre=centre.id,
                    transfer_at__month__gte=debut_periode,
                    transfer_at__month__lte=fin_periode,
                    transfer_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('cout_transfere'))['cout_transfere__sum'] or 0

                benefice = total_ventes - total_Transfere

                taux_benefice = Decimal('0.00')
                if total_benefice_precedent != 0 and benefice != 0:
                    taux_benefice = (benefice - total_benefice_precedent) / total_benefice_precedent * 100

                total_benefice_precedent = benefice
                intervalle = intervalle + cle

                taux = {
                    'valeur_benefice': taux_benefice,
                    'mois': intervalle
                }
                evolution_taux_benefice_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    form=MonFormulaire_centre1()
    current_year=datetime.now().year
    total_cost_transferred = Transfert.objects.filter(centre=centre,transfer_at__year__lte=date_actuelle.year,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year__lte=date_actuelle.year,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request, 'analyse_centre1.html', {
         "total_cost_transferred":total_cost_transferred,
         "total_amount_sold":total_amount_sold,
         "total_profit":total_profit,
        "top_produits":top_produits,
        "evolution_taux_benefice_sur_annees":evolution_taux_benefice_sur_annees,
        "evolution_taux_vent_sur_annees":evolution_taux_vent_sur_annees,
        "best_client":best_client,
        "form":form})

def analyse_centre2(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    centre=Centre.objects.get(codeC='c2')
    Annee_min_pour_best_client=2023
    nombre_best_clients=5
    Annee_min_Vente=2023
    Annee_min_pour_top_produit=2023
    nombre_top_produits=5

    if request.method == 'POST':
        form = MonFormulaire_centre1(request.POST)

        if form.is_valid():
            # Accédez aux données du formulaire comme suit
            Annee_min_pour_best_client = form.cleaned_data['Annee_min_pour_best_client']
            nombre_best_clients = form.cleaned_data['nombre_best_clients']
            Annee_min_Vente = form.cleaned_data['Annee_min_Vente']
            Annee_min_pour_top_produit = form.cleaned_data['Annee_min_pour_top_produit']
            nombre_top_produits = form.cleaned_data['nombre_top_produits']
        form = MonFormulaire_centre1()

        if not  Annee_min_pour_best_client:
            Annee_min_pour_best_client=2023
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=2023
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=2023
        if not nombre_top_produits:
            nombre_top_produits=5
        
    best_client = VenteP.objects.filter(
        lieu_ventes=centre.id,
        salled_at__year__gte=Annee_min_pour_best_client,
        salled_at__year__lte=annee_actuelle
    ).values(
        'client__codeCl',
        'client__nomCl',
        'client__prenomCl',
        'client__adresseCl',
        'client__telephoneCl'

    ).annotate(
        total_ventes=Sum('montantTotalVen')
    ).order_by(
        '-total_ventes'
    )[:nombre_best_clients]
    
    top_produits = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year__gte=Annee_min_pour_top_produit,
    salled_at__year__lte=annee_actuelle
).values(
    'produit_vendus__codeP',  
    'produit_vendus__designation_produit'

).annotate(
    total_quantite_vente=Sum('quantitVen')
).order_by(
    '-total_quantite_vente'
)[:nombre_top_produits]
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_vente_precedente = 0
    evolution_taux_vent_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente
    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
                taux_vente = Decimal('0.00')
                if total_vente_precedente != 0 and total_ventes != 0:
                    taux_vente = (total_ventes - total_vente_precedente) / total_vente_precedente * 100

                total_vente_precedente = total_ventes
                intervalle = intervalle + cle

                taux = {
                    'valeur_vente': taux_vente,
                    'mois': intervalle
                }
                evolution_taux_vent_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_benefice_precedent = 0
    evolution_taux_benefice_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente

    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

                total_Transfere = Transfert.objects.filter(
                    centre=centre.id,
                    transfer_at__month__gte=debut_periode,
                    transfer_at__month__lte=fin_periode,
                    transfer_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('cout_transfere'))['cout_transfere__sum'] or 0

                benefice = total_ventes - total_Transfere

                taux_benefice = Decimal('0.00')
                if total_benefice_precedent != 0 and benefice != 0:
                    taux_benefice = (benefice - total_benefice_precedent) / total_benefice_precedent * 100

                total_benefice_precedent = benefice
                intervalle = intervalle + cle

                taux = {
                    'valeur_benefice': taux_benefice,
                    'mois': intervalle
                }
                evolution_taux_benefice_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    form=MonFormulaire_centre1()
    current_year=datetime.now().year
    total_cost_transferred = Transfert.objects.filter(centre=centre.id,transfer_at__year__lte=2024,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year__lte=2024,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request, 'analyse_centre2.html', {
         "total_cost_transferred":total_cost_transferred,
         "total_amount_sold":total_amount_sold,
         "total_profit":total_profit,
        "top_produits":top_produits,
        "evolution_taux_benefice_sur_annees":evolution_taux_benefice_sur_annees,
        "evolution_taux_vent_sur_annees":evolution_taux_vent_sur_annees,
        "best_client":best_client,
        "form":form})
def analyse_centre3(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    centre=Centre.objects.get(codeC='c3')
    Annee_min_pour_best_client=2023
    nombre_best_clients=5
    Annee_min_Vente=2023
    Annee_min_pour_top_produit=2023
    nombre_top_produits=5

    if request.method == 'POST':
        form = MonFormulaire_centre1(request.POST)

        if form.is_valid():
            # Accédez aux données du formulaire comme suit
            Annee_min_pour_best_client = form.cleaned_data['Annee_min_pour_best_client']
            nombre_best_clients = form.cleaned_data['nombre_best_clients']
            Annee_min_Vente = form.cleaned_data['Annee_min_Vente']
            Annee_min_pour_top_produit = form.cleaned_data['Annee_min_pour_top_produit']
            nombre_top_produits = form.cleaned_data['nombre_top_produits']
        form = MonFormulaire_centre1()

        if not  Annee_min_pour_best_client:
            Annee_min_pour_best_client=2023
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=2023
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=2023
        if not nombre_top_produits:
            nombre_top_produits=5
        
    best_client = VenteP.objects.filter(
        lieu_ventes=centre,
        salled_at__year__gte=Annee_min_pour_best_client,
        salled_at__year__lte=annee_actuelle
    ).values(
        'client__codeCl',
        'client__nomCl',
        'client__prenomCl',
        'client__adresseCl',
        'client__telephoneCl'

    ).annotate(
        total_ventes=Sum('montantTotalVen')
    ).order_by(
        '-total_ventes'
    )[:nombre_best_clients]
    
    top_produits = VenteP.objects.filter(
    lieu_ventes=centre.id,
    salled_at__year__gte=Annee_min_pour_top_produit,
    salled_at__year__lte=annee_actuelle
).values(
    'produit_vendus__codeP',  
    'produit_vendus__designation_produit'

).annotate(
    total_quantite_vente=Sum('quantitVen')
).order_by(
    '-total_quantite_vente'
)[:nombre_top_produits]
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_vente_precedente = 0
    evolution_taux_vent_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente
    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
                taux_vente = Decimal('0.00')
                if total_vente_precedente != 0 and total_ventes != 0:
                    taux_vente = (total_ventes - total_vente_precedente) / total_vente_precedente * 100

                total_vente_precedente = total_ventes
                intervalle = intervalle + cle

                taux = {
                    'valeur_vente': taux_vente,
                    'mois': intervalle
                }
                evolution_taux_vent_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_benefice_precedent = 0
    evolution_taux_benefice_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente

    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    lieu_ventes=centre.id,
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

                total_Transfere = Transfert.objects.filter(
                    centre=centre.id,
                    transfer_at__month__gte=debut_periode,
                    transfer_at__month__lte=fin_periode,
                    transfer_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('cout_transfere'))['cout_transfere__sum'] or 0

                benefice = total_ventes - total_Transfere

                taux_benefice = Decimal('0.00')
                if total_benefice_precedent != 0 and benefice != 0:
                    taux_benefice = (benefice - total_benefice_precedent) / total_benefice_precedent * 100

                total_benefice_precedent = benefice
                intervalle = intervalle + cle

                taux = {
                    'valeur_benefice': taux_benefice,
                    'mois': intervalle
                }
                evolution_taux_benefice_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    form=MonFormulaire_centre1()
    current_year=datetime.now().year
    total_cost_transferred = Transfert.objects.filter(centre=centre.id,transfer_at__year__lte=2024,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year__lte=2024,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request, 'analyse_centre3.html', {
         "total_cost_transferred":total_cost_transferred,
         "total_amount_sold":total_amount_sold,
         "total_profit":total_profit,
        "top_produits":top_produits,
        "evolution_taux_benefice_sur_annees":evolution_taux_benefice_sur_annees,
        "evolution_taux_vent_sur_annees":evolution_taux_vent_sur_annees,
        "best_client":best_client,
        "form":form})
def analyseCentres(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    Annee_min_pour_best_client=2023
    nombre_best_clients=5
    Annee_min_Vente=2023
    Annee_min_pour_top_produit=2023
    nombre_top_produits=5

    if request.method == 'POST':
        form = MonFormulaire_centre1(request.POST)

        if form.is_valid():
            # Accédez aux données du formulaire comme suit
            Annee_min_pour_best_client = form.cleaned_data['Annee_min_pour_best_client']
            nombre_best_clients = form.cleaned_data['nombre_best_clients']
            Annee_min_Vente = form.cleaned_data['Annee_min_Vente']
            Annee_min_pour_top_produit = form.cleaned_data['Annee_min_pour_top_produit']
            nombre_top_produits = form.cleaned_data['nombre_top_produits']
        form = MonFormulaire_centre1()

        if not  Annee_min_pour_best_client:
            Annee_min_pour_best_client=2023
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=2023
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=2023
        if not nombre_top_produits:
            nombre_top_produits=5
        
    best_client = VenteP.objects.filter(
        salled_at__year__gte=Annee_min_pour_best_client,
        salled_at__year__lte=annee_actuelle
    ).values(
        'client__codeCl',
        'client__nomCl',
        'client__prenomCl',
        'client__adresseCl',
        'client__telephoneCl'

    ).annotate(
        total_ventes=Sum('montantTotalVen')
    ).order_by(
        '-total_ventes'
    )[:nombre_best_clients]
    
    top_produits = VenteP.objects.filter(
    salled_at__year__gte=Annee_min_pour_top_produit,
    salled_at__year__lte=annee_actuelle
).values(
    'produit_vendus__codeP',  
    'produit_vendus__designation_produit'

).annotate(
    total_quantite_vente=Sum('quantitVen')
).order_by(
    '-total_quantite_vente'
)[:nombre_top_produits]
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_vente_precedente = 0
    evolution_taux_vent_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente
    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
                taux_vente = Decimal('0.00')
                if total_vente_precedente != 0 and total_ventes != 0:
                    taux_vente = (total_ventes - total_vente_precedente) / total_vente_precedente * 100

                total_vente_precedente = total_ventes
                intervalle = intervalle + cle

                taux = {
                    'valeur_vente': taux_vente,
                    'mois': intervalle
                }
                evolution_taux_vent_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    n = 12
    dic = [{'cle': i + 1, 'nombre_de_mois': (i + 1) * 12} for i in range(n)]
    annee_analyse = annee_actuelle - Annee_min_Vente
    if annee_analyse == 0:
            nombre_mois = 12
            annee_analyse = 1
    else:
            nombre_mois = annee_analyse * 12

        # Recherche de la clé dans le dictionnaire
    for element in dic:
            if element['nombre_de_mois'] == nombre_mois:
                cle = element.get('cle')

    total_benefice_precedent = 0
    evolution_taux_benefice_sur_annees = []
    Annee_min_Vente_debut = Annee_min_Vente

    intervalle = 0
    y = 12 / cle
    y = int(y)
    for annee_ecoulee in range(0, annee_analyse):
            fin_periode = 0
            for periode in range(0, y):
                debut_periode = fin_periode + 1
                fin_periode = fin_periode + cle

                total_ventes = VenteP.objects.filter(
                    salled_at__month__gte=debut_periode,
                    salled_at__month__lte=fin_periode,
                    salled_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum'] or 0

                total_Transfere = Transfert.objects.filter(
                    transfer_at__month__gte=debut_periode,
                    transfer_at__month__lte=fin_periode,
                    transfer_at__year=Annee_min_Vente_debut
                ).aggregate(Sum('cout_transfere'))['cout_transfere__sum'] or 0

                benefice = total_ventes - total_Transfere

                taux_benefice = Decimal('0.00')
                if total_benefice_precedent != 0 and benefice != 0:
                    taux_benefice = (benefice - total_benefice_precedent) / total_benefice_precedent * 100

                total_benefice_precedent = benefice
                intervalle = intervalle + cle

                taux = {
                    'valeur_benefice': taux_benefice,
                    'mois': intervalle
                }
                evolution_taux_benefice_sur_annees.append(taux)
            Annee_min_Vente_debut = Annee_min_Vente_debut + 1
    form=MonFormulaire_centre1()
    total_cost_transferred = Transfert.objects.filter(transfer_at__year__lte=annee_actuelle,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(salled_at__year__lte=annee_actuelle,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

# Calculate total profit for the specified center and product in the current year
    total_profit = total_amount_sold - total_cost_transferred
    return render(request, 'Centre.html', {
         "total_cost_transferred":total_cost_transferred,
         "total_amount_sold":total_amount_sold,
         "total_profit":total_profit,
        "top_produits":top_produits,
        "evolution_taux_benefice_sur_annees":evolution_taux_benefice_sur_annees,
        "evolution_taux_vent_sur_annees":evolution_taux_vent_sur_annees,
        "best_client":best_client,
        "form":form})

def InventryView(request):
    produits= Produit.objects.all()
    return render(request,"Inventry.html",{"produits":produits})

def sidebar_view(request):
    if request.method == 'GET':
        centers = Centre.objects.all()
        
        # Sérialiser les objets Centre pour les convertir en données JSON
        centers_list = list(centers.values())  # Convertir les queryset en liste de dictionnaires

        data = {
            'centers': centers_list
        }
        
        return JsonResponse(data)
def notification(request):
    produits = Produit.objects.filter(quantiteStockPod__lte=20)
    matieres_premieres = MatierePremiere.objects.filter(quantiteStockMat__lte=20)
    nb_notification=produits.count()+matieres_premieres.count()
    return render(request, 'notification.html', {"nb_notification":nb_notification,'produits': produits, 'matieres_premieres': matieres_premieres})
def notification1():
    produits = Produit.objects.filter(quantiteStockPod__lte=20)
    matieres_premieres = MatierePremiere.objects.filter(quantiteStockMat__lte=20)
    nb_notification=produits.count()+matieres_premieres.count()
    return nb_notification