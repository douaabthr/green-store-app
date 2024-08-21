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



def fiche_journal_ventes_interport(request):
    ventes = VenteM.objects.all()
    total_ventes = VenteM.objects.aggregate(total=Sum('montantTotalVen'))['total'] 

    if request.method == 'POST':
        form = FiltreVenteForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data.get('client')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if client:
                filtre_requete &= Q(client=client)

            if date_debut:
                filtre_requete &= Q(salled_at__gte=date_debut)

            if date_fin:
                filtre_requete &= Q(salled_at__lte=date_fin)

            # Appliquer le filtre
            ventes = VenteM.objects.filter(filtre_requete) 
            total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 

    else:
        form = FiltreVenteForm()

    return render(request, 'VenteInterpot.html', {
        'ventes': ventes,
        'total_ventes': total_ventes,
        'form': form
    })


def fiche_journal_ventes_centre1(request):
    ventes = VenteP.objects.filter(lieu_ventes__codeC='c1')
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
    else:
        total_ventes =Decimal(0.0)

    transferts = Transfert.objects.filter(centre__codeC='c1')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
    else:
        total_transferts=Decimal(0.0)

    
    if request.method == 'POST':
        form = FiltreVentePForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data.get('produit')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete_ventes = Q()

            if produit:
                filtre_requete_ventes &= Q(produit_vendus=produit)
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)


            filtre_requete_transfert = Q()

            if produit:
                # Filtrer les Ingridiants par le produit
                ingridiants = Ingridiant.objects.filter(produit=produit)
                # Filtrer les transferts par les matieres extraits de la table Ingridiant
                filtre_requete_transfert &= Q(produit_transfere__in=ingridiants.values_list('matiere', flat=True))
            if date_debut:
                filtre_requete_transfert &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete_transfert &= Q(transfer_at__lte=date_fin)


            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete_transfert)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreVentePForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'VenteCentres.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })

def modifier_vente_mat(request, vente_id):
    vente =VenteM.objects.get(pk=vente_id)

    if request.method == 'POST':
        form = VenteMForm(request.POST, instance=vente)
        if form.is_valid():
            
            ancienVente = VenteM.objects.get(pk=vente_id)
            if form.cleaned_data['quantitVen']>0 and form.cleaned_data['quantitVen']<=form.cleaned_data['matiere_vendus'].quantiteStockMat:
                if  ancienVente.quantitVen != form.cleaned_data['quantitVen']:
                    matiere = ancienVente.matiere_vendus
                    matiere.quantiteStockMat -= ancienVente.quantitVen
                    matiere.quantiteStockMat += vente.quantitVen
                    matiere.save()
                    form.save()
                    return redirect('venteI')
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro et inferieure au matiere disponible'})
                

    else:
        form = VenteMForm(instance=vente)
        return render(request, 'modifierItem.html', {'form': form,'msg':'Vente'})

def supprimer_vente_mat(request, vente_id):
    vente = VenteM.objects.get(pk=vente_id)
    
    # Affichage de la page de confirmation
    if request.method == 'POST':
        # Suppression de l'achat
        vente.delete()

        # Déstockage du produit associé (exemple simplifié, adaptez selon votre modèle)
        matiere = vente.matiere_vendus
        matiere.quantiteStockMat += vente.quantitVen
        matiere.save()

        return redirect('venteI')  # Redirection vers la page principale après la suppression

    return render(request, 'supprimerItem.html', {'vente': vente,'msg':'Vente'})

def fiche_journal_ventes_centre1(request,center_id):
    ventes = VenteP.objects.filter(lieu_ventes__codeC=center_id)
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
    else:
        total_ventes =Decimal(0.0)

    transferts = Transfert.objects.filter(centre__codeC=center_id)
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
    else:
        total_transferts=Decimal(0.0)

    
    if request.method == 'POST':
        form = FiltreVentePForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data.get('produit')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete_ventes = Q()

            if produit:
                filtre_requete_ventes &= Q(produit_vendus=produit)
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)


            filtre_requete_transfert = Q()

            if produit:
                # Filtrer les Ingridiants par le produit
                ingridiants = Ingridiant.objects.filter(produit=produit)
                # Filtrer les transferts par les matieres extraits de la table Ingridiant
                filtre_requete_transfert &= Q(produit_transfere__in=ingridiants.values_list('matiere', flat=True))
            if date_debut:
                filtre_requete_transfert &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete_transfert &= Q(transfer_at__lte=date_fin)


            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete_transfert)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreVentePForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'VenteCentres.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })


def fiche_journal_ventes_centre2(request):
    ventes = VenteP.objects.filter(lieu_ventes__codeC='c2')
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
    else:
        total_ventes =Decimal(0.0)

    transferts = Transfert.objects.filter(centre__codeC='c2')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
    else:
        total_transferts=Decimal(0.0)

    
    if request.method == 'POST':
        form = FiltreVentePForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data.get('produit')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete_ventes = Q()

            if produit:
                filtre_requete_ventes &= Q(produit_vendus=produit)
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)


            filtre_requete_transfert = Q()

            if produit:
                # Filtrer les Ingridiants par le produit
                ingridiants = Ingridiant.objects.filter(produit=produit)
                # Filtrer les transferts par les matieres extraits de la table Ingridiant
                filtre_requete_transfert &= Q(produit_transfere__in=ingridiants.values_list('matiere', flat=True))
            if date_debut:
                filtre_requete_transfert &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete_transfert &= Q(transfer_at__lte=date_fin)


            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete_transfert)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreVentePForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'VenteCentres.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })

def fiche_journal_ventes_centre3(request):
    ventes = VenteP.objects.filter(lieu_ventes__codeC='c3')
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
    else:
        total_ventes =Decimal(0.0)

    transferts = Transfert.objects.filter(centre__codeC='c3')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
    else:
        total_transferts=Decimal(0.0)

    
    if request.method == 'POST':
        form = FiltreVentePForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data.get('produit')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete_ventes = Q()

            if produit:
                filtre_requete_ventes &= Q(produit_vendus=produit)
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)


            filtre_requete_transfert = Q()

            if produit:
                # Filtrer les Ingridiants par le produit
                ingridiants = Ingridiant.objects.filter(produit=produit)
                # Filtrer les transferts par les matieres extraits de la table Ingridiant
                filtre_requete_transfert &= Q(produit_transfere__in=ingridiants.values_list('matiere', flat=True))
            if date_debut:
                filtre_requete_transfert &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete_transfert &= Q(transfer_at__lte=date_fin)


            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete_transfert)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] 
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreVentePForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'VenteCentres.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })

def modifier_vente_prod(request, vente_id):
    vente = VenteP.objects.get(pk=vente_id)

    if request.method == 'POST':
        form = VentePForm(request.POST, instance=vente)
        if form.is_valid():
            ancienVente = VenteP.objects.get(pk=vente_id)
            if form.cleaned_data['quantitVen']>0 and form.cleaned_data['quantitVen']<=form.cleaned_data['produit_vendus'].quantiteStockPod:
                if ancienVente.quantitVen != form.cleaned_data['quantitVen']:
                    produit = ancienVente.produit_vendus
                    produit.quantiteStockPod -= ancienVente.quantitVen
                    produit.quantiteStockPod += vente.quantitVen
                    produit.save()
                    form.save()

                if ancienVente.lieu_ventes == 'Centre1':
                    return redirect('venteC1') 
                elif ancienVente.lieu_ventes == 'Centre2':
                    return redirect('venteC2')
                else:
                    return redirect('venteC3')
            
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro et inferieur au quantite disponible'})

def supprimer_vente_prod(request, vente_id):
    vente = VenteP.objects.get(pk=vente_id)
    
    # Affichage de la page de confirmation
    if request.method == 'POST':
        # Suppression de l'achat
        vente.delete()

        # Déstockage du produit associé (exemple simplifié, adaptez selon votre modèle)
        produit = vente.produit_vendus
        produit.quantiteStockPod += vente.quantitVen
        produit.save()

        if vente.lieu_ventes == 'Centre1':
            return redirect('venteC1') 
        elif vente.lieu_ventes == 'Centre2':
            return redirect('venteC2')
        else:
            return redirect('venteC3')  # Redirection vers la page principale après la suppression

    return render(request, 'supprimerItem.html', {'vente': vente,'msg':'Vente'})

def sava_ventes(request):
        if request.method == 'POST':
            form = VendreProduitForm(request.POST)

            if form.is_valid():
                Client = form.cleaned_data['client']
                produit_vendus_id = request.POST.get('prd')
                produit_vendus_id=int(produit_vendus_id)
                salled_at = form.cleaned_data['salled_at']
                produit_vendus = Produit.objects.get(id=produit_vendus_id)
                prix_unitaire_Ven = produit_vendus.prix_unitaire_Ven
                quantitVen = form.cleaned_data['quantitVen']
                lieu_ventes = form.cleaned_data['lieu_ventes']
                mosa3ada = form.cleaned_data['mosa3ada']
                khesara = form.cleaned_data['khesara']

                if prix_unitaire_Ven<=0 or quantitVen <=0 :
                    message1="Quantite doit eter sup a 0  "
                    produits=Produit.objects.all()
                    form = VendreProduitForm()
                    return render(request,"add_vents.html",{"message1":message1,"form":form,"produits":produits})

                if produit_vendus.quantiteStockPod < quantitVen :
                    message="quantite insuffisante"
                    produits=Produit.objects.all()
                    form = VendreProduitForm()
                    return render(request,"add_vents.html",{"form":form,"produits":produits,"message":message})
                produit_vendus.quantiteStockPod=produit_vendus.quantiteStockPod-quantitVen
                produit_vendus.save()
                VenteP.objects.create(
                    client=Client,
                    produit_vendus=produit_vendus,
                    salled_at=salled_at,
                    prix_unitaire_Ven=prix_unitaire_Ven,
                    quantitVen=quantitVen,
                    lieu_ventes=lieu_ventes,
                    mosa3ada=mosa3ada,
                    khesara=khesara,
                )
                produits=Produit.objects.all()
                form = VendreProduitForm()
                message_succe="Vente ajouter avec succe"
                return render(request,"add_vents.html",{"message_succe":message_succe,"form":form,"produits":produits})
        
        else:
            produits=Produit.objects.all()
            form = VendreProduitForm()
            return render(request,"add_vents.html",{"form":form,"produits":produits})


def sava_ventes_matiere(request):
        if request.method == 'POST':
            form = VendreMatiereForm(request.POST)

            if form.is_valid():
                Client = form.cleaned_data['client']
                produit_vendus_id = request.POST.get('prd')
                produit_vendus_id=int(produit_vendus_id)
                salled_at = form.cleaned_data['salled_at']
                prix_unitaire_Ven = form.cleaned_data['prix_unitaire_Ven']
                quantitVen = form.cleaned_data['quantitVen']
                if quantitVen<=0 :
                    message1="Quantite doit eter sup a 0  "
                    produits=MatierePremiere.objects.all()
                    form = VendreMatiereForm()
                    return render(request,"add_vents_matiere.html",{"form":form,"produits":produits,"message1":message1})
                if produit_vendus.quantiteStockMat < quantitVen :
                    message="quantite insuffisante"
                    produits=MatierePremiere.objects.all()
                    form = VendreMatiereForm()
                    return render(request,"add_vents_matiere.html",{"form":form,"produits":produits,"message":message})
                
                montantTotalVen = prix_unitaire_Ven * quantitVen
                produit_vendus.quantiteStockMat=produit_vendus.quantiteStockMat-quantitVen
                produits_from_achat=Achat.objects.filter(matiere_achete=produit_vendus_id)
                for pa in produits_from_achat:
                        if quantitVen !=0:
                            if  pa.quantitDispo !=0 and pa.quantitDispo <quantitVen:
                              quantitVen=quantitVen-pa.quantitDispo
                              pa.quantitDispo=0
                            else :
                              if pa.quantitDispo >=quantitVen:
                                   pa.quantitDispo=pa.quantitDispo-quantitVen
                                   quantitVen=0
                        pa.save()
                produit_vendus.save()
                VenteM.objects.create(
                    client=Client,
                    matiere_vendus=produit_vendus,
                    salled_at=salled_at,
                    prix_unitaire_Ven=prix_unitaire_Ven,
                    quantitVen=quantitVen,
                    montantTotalVen=montantTotalVen,
                )
                produits=MatierePremiere.objects.all()
                form = VendreMatiereForm()
                message_succe="Vente ajouter avec succe"
                return render(request,"add_vents_matiere.html",{"message_succe":message_succe,"form":form,"produits":produits})
        
        else:
            produits=MatierePremiere.objects.all()
            form = VendreMatiereForm()
            return render(request,"add_vents_matiere.html",{"form":form,"produits":produits})