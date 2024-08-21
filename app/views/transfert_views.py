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

def fiche_journal_transferts(request):
    transferts = Transfert.objects.all()
    total_transferts = Transfert.objects.aggregate(total=Sum('cout_transfere'))['total']

    if request.method == 'POST':
        form = FiltreTransfertForm(request.POST)
        if form.is_valid():
            centre = form.cleaned_data.get('centre')
            matiere_transfere = form.cleaned_data.get('produit_transfere')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if centre:
                filtre_requete &= Q(centre=centre)
            if matiere_transfere:
                filtre_requete&= Q(produit_transfere=matiere_transfere)
            if date_debut:
                filtre_requete &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete &= Q(transfer_at__lte=date_fin)

            # Appliquer le filtre
            transferts = Transfert.objects.filter(filtre_requete)
            total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']

    else:
        form = FiltreTransfertForm()

    return render(request, 'Transfert.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'form': form
    })

from ..models import Transfert

def supprimer_transfert(request, transfert_id):
    transfert = Transfert.objects.get(pk=transfert_id)
    
    # Affichage de la page de confirmation
    if request.method == 'POST':
        # Suppression de l'achat
        transfert.delete()
        matiere = transfert.produit_transfere
        matiere.quantiteStockMat += transfert.quantitTran
        matiere.save()
        return redirect('Transfert') 

    return render(request, 'supprimerItem.html', {'matiere': transfert,'msg':'Trasfert'})

def modifier_transfert(request, transfert_id):
    transfert =Transfert.objects.get(pk=transfert_id)

    if request.method == 'POST':
        form = TransfertForm(request.POST, instance=transfert)
        if form.is_valid():
            if form.cleaned_data['quantitTran']>0 and form.cleaned_data['quantitTran']<=form.cleaned_data['produit_transfere'].quantiteStockMat:
                matiere = form.cleaned_data['produit_transfere']
                matiere.quantiteStockMat -= transfert.quantitTran
                matiere.quantiteStockMat += form.cleaned_data['quantitTran']
                matiere.save()
                transfert.save()
                form.save()
                return redirect('Transfert') 
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro et inferieur a la quantite dispo'})
               


    else:
        form = TransfertForm(instance=transfert)
        return render(request, 'modifierItem.html', {'form': form,'msg':'Trasfert'})
    
from ..forms import FiltreTransfertRecuForm 
from ..models import Ingridiant
from decimal import Decimal

def fiche_journal_transferts_recu_centre1(request,center_id):
    transferts = Transfert.objects.filter(centre__codeC=center_id)
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
    else:
        total_transferts=Decimal(0.0)

    ventes = VenteP.objects.filter(lieu_ventes__codeC=center_id)
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] or 0
    else:
        total_ventes =Decimal(0.0)

    if request.method == 'POST':
        form = FiltreTransfertRecuForm(request.POST)
        if form.is_valid():
            matiere_transfere = form.cleaned_data.get('produit_transfere')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if matiere_transfere:
                filtre_requete&= Q(produit_transfere=matiere_transfere)
            if date_debut:
                filtre_requete &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete &= Q(transfer_at__lte=date_fin)


            filtre_requete_ventes = Q()

            if matiere_transfere:
                # Filtrer les Ingridiants par la matière
                ingridiants = Ingridiant.objects.filter(matiere=matiere_transfere)
                # Filtrer les ventes par les produits extraits de la table Ingridiant
                filtre_requete_ventes &= Q(produit_vendus__in=ingridiants.values_list('produit', flat=True))
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)

            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] or 0
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreTransfertRecuForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'TransfertRecuC1.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })


def fiche_journal_transferts_recu_centre2(request):
    transferts = Transfert.objects.filter(centre__codeC='c2')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total']  or 0
    else:
        total_transferts=Decimal(0.0)

    ventes = VenteP.objects.filter(lieu_ventes__codeC='c2')
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total']  or 0
    else:
        total_ventes =Decimal(0.0)

    if request.method == 'POST':
        form = FiltreTransfertRecuForm(request.POST)
        if form.is_valid():
            matiere_transfere = form.cleaned_data.get('produit_transfere')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if matiere_transfere:
                filtre_requete&= Q(produit_transfere=matiere_transfere)
            if date_debut:
                filtre_requete &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete &= Q(transfer_at__lte=date_fin)


            filtre_requete_ventes = Q()

            if matiere_transfere:
                # Filtrer les Ingridiants par la matière
                ingridiants = Ingridiant.objects.filter(matiere=matiere_transfere)
                # Filtrer les ventes par les produits extraits de la table Ingridiant
                filtre_requete_ventes &= Q(produit_vendus__in=ingridiants.values_list('produit', flat=True))
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)

            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total']  or 0
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreTransfertRecuForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'TransfertRecuC2.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })



def fiche_journal_transferts_recu_centre3(request):
    transferts = Transfert.objects.filter(centre__codeC='c3')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
    else:
        total_transferts=Decimal(0.0)

    ventes = VenteP.objects.filter(lieu_ventes__codeC='c3')
    if ventes:
        total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total'] or 0
    else:
        total_ventes =Decimal(0.0)

    if request.method == 'POST':
        form = FiltreTransfertRecuForm(request.POST)
        if form.is_valid():
            matiere_transfere = form.cleaned_data.get('produit_transfere')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if matiere_transfere:
                filtre_requete&= Q(produit_transfere=matiere_transfere)
            if date_debut:
                filtre_requete &= Q(transfer_at__gte=date_debut)
            if date_fin:
                filtre_requete &= Q(transfer_at__lte=date_fin)


            filtre_requete_ventes = Q()

            if matiere_transfere:
                # Filtrer les Ingridiants par la matière
                ingridiants = Ingridiant.objects.filter(matiere=matiere_transfere)
                # Filtrer les ventes par les produits extraits de la table Ingridiant
                filtre_requete_ventes &= Q(produit_vendus__in=ingridiants.values_list('produit', flat=True))
            if date_debut:
                filtre_requete_ventes &= Q(salled_at__gte=date_debut)
            if date_fin:
                filtre_requete_ventes &= Q(salled_at__lte=date_fin)

            # Appliquer le filtre
            transferts = transferts.filter(filtre_requete)
            if transferts:
                total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
            else:
                total_transferts=Decimal(0.0)

            ventes = ventes = ventes.filter(filtre_requete_ventes)
            if ventes:
                total_ventes = ventes.aggregate(total=Sum('montantTotalVen'))['total']  or 0
            else:
                total_ventes =Decimal(0.0)


    else:
        form = FiltreTransfertRecuForm()
    
    benefice = total_ventes - total_transferts

    return render(request, 'TransfertRecuC3.html', {
        'transferts': transferts,
        'total_transferts': total_transferts,
        'ventes': ventes,
        'total_ventes': total_ventes,
        'benefice':benefice,
        'form': form
    })

def save_transfer(request):
        if request.method == 'POST':
            form = tranForm(request.POST)

            if form.is_valid():
                Q=form.cleaned_data['produit_transfere']
                p=MatierePremiere.objects.get(id=Q.id)
                QT=form.cleaned_data['quantitTran']
                transfer_at = form.cleaned_data['transfer_at']
                cout = form.cleaned_data['cout_transfere']

                if QT <=0:
                    message1="Quantite transfere non valide "
                    form = tranForm()
                    return render(request,"add_transfer.html",{"form":form,"message1":message1})
                if QT> p.quantiteStockMat:
                    form=tranForm()
                    message="cette quantite n'est pas disponible"
                    return render(request,"add_transfer.html",{"form":form ,"message":message})
                else :
                    p.quantiteStockMat=p.quantiteStockMat-QT
                    p_quntiteTRan=QT
                    p.save()
                    produits_from_achat=Achat.objects.filter(matiere_achete=Q.id)
                    for pa in produits_from_achat:
                        if QT !=0:
                            if  pa.quantitDispo !=0 and pa.quantitDispo <QT:
                              cout_tan = pa.quantitDispo*(pa.prix_unitaire_HT + cout)
                              QT=QT-pa.quantitDispo
                              pa.quantitDispo=0
                            else :
                              if pa.quantitDispo >=QT:
                                   cout_tan=(pa.prix_unitaire_HT + cout )*QT
                                   pa.quantitDispo=pa.quantitDispo-QT
                                   QT=0
                        pa.save()
                        
                    centre= form.cleaned_data['centre']    
                    Transfert.objects.create(
                      centre=centre,
                      produit_transfere=Q,
                      transfer_at=transfer_at,
                      quantitTran=p_quntiteTRan,
                      cout_transfere=cout_tan,

                )
                    message_succe="Transfere ajouter avec succe"
                    form = tranForm()
                    return render(request,"add_transfer.html",{"form":form,"message_succe":message_succe})
        
        else:
            form = tranForm()
            return render(request,"add_transfer.html",{"form":form})
    