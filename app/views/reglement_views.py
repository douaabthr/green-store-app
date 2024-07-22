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

def payerAchat(request):
    if request.method == 'POST':
        form = PaymentAchatFormForAjout(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            fournisseur = payment.fournisseur

            # Vérifier si le montant de règlement est supérieur à zéro
            if payment.montant_reglement > Decimal(0.0):
                fournisseur.solde += payment.montant_reglement
                fournisseur.save()
                form.save()
                return redirect('histpymtachat')
            else:
                # Afficher un message d'erreur si le montant est inférieur ou égal à zéro
                return render(request, "paymentAchat.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro'})
    else:
        form = PaymentAchatFormForAjout()

    return render(request, "paymentAchat.html", {'form': form})


def payerVente(request):
    if request.method == 'POST':
        form = PaymentVenteFormForAjout(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            client = payment.client

            # Vérifier si le montant payé est supérieur à zéro
            if payment.montant_paye > 0:
                client.credit += payment.montant_paye
                client.save()
                form.save()
                return redirect('histpymtvente')
            else:
                return render(request, "paymentVente.html", {'form': form, 'messageexp': 'Le montant payé doit être supérieur à zéro'})
    else:
        form = PaymentVenteFormForAjout()

    return render(request, "paymentVente.html", {'form': form})

def liste_paiemens_achat(request):
    payments = PaymentAchat.objects.all()

    context = {
        'payments': payments,
    }

    return render(request, 'HistoriquePymtAchat.html', context)

def liste_paiements_vente(request):
    payments = PaymentVente.objects.all()

    context = {
        'payments': payments,
    }

    return render(request, 'HistoriquePymtVente.html', context)

def modifier_paymentht(request, payment_id):
    payment = get_object_or_404(PaymentAchat, pk=payment_id)
    fournisseur = payment.fournisseur

    ancien_montant_reglement = payment.montant_reglement  # Sauvegarde de l'ancien montant pour mise à jour du solde

    if request.method == 'POST':
        form = PaymentAchatForm(request.POST, instance=payment)
        if form.is_valid():
            
            if payment.montant_reglement > 0:
                form.save()
            # Soustraire l'ancien montant du solde du fournisseur
                fournisseur.solde -= ancien_montant_reglement
                fournisseur.save()

            # Ajouter le nouveau montant du paiement au solde du fournisseur
                fournisseur.solde += payment.montant_reglement
                fournisseur.save()

                return redirect('histpymtachat')
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro'})
    else:
        form = PaymentAchatForm(instance=payment)

    context = {
        'form': form,
        'fournisseur': fournisseur,
        'msg':'Payment'
    }

    return render(request, 'modifierItem.html', context)


def supprimer_paymentht(request, payment_id):
    payment = PaymentAchat.objects.get(pk=payment_id)
    fournisseur = payment.fournisseur

    if request.method == 'POST':
    # Supprimer le paiement
        payment.delete()

    # Mettre à jour le solde du fournisseur en soustrayant le montant du paiement supprimé
        fournisseur.solde -= payment.montant_reglement
        fournisseur.save()

        return redirect('histpymtachat')
    
    return render(request, 'supprimerItem.html', {'msg':'reglementation'})





def modifier_paymentvt(request, payment_id):
    payment = get_object_or_404(PaymentVente, pk=payment_id)
    client = payment.client

    ancien_montant_paye = payment.montant_paye  # Sauvegarde de l'ancien montant pour mise à jour du solde

    if request.method == 'POST':
        form = PaymentVenteForm(request.POST, instance=payment)
        if form.is_valid():
            if payment.montant_paye > 0:
                form.save()

            # Soustraire l'ancien montant du solde du client
                client.credit -= ancien_montant_paye
                client.save()

            # Ajouter le nouveau montant du paiement au solde du client
                client.credit += payment.montant_paye
                client.save()

                return redirect('histpymtvente')  # Assurez-vous que la redirection est correcte
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro'})
    else:
        form = PaymentVenteForm(instance=payment)

    context = {
        'form': form,
        'client': client,
        'msg': 'Payment'  # Assurez-vous que le message est correct
    }

    return render(request, 'modifierItem.html', context)

def supprimer_paymentvt(request, payment_id):
    payment = get_object_or_404(PaymentVente, pk=payment_id)
    client = payment.client

    if request.method == 'POST':
    
    # Supprimer le paiement
        payment.delete()

    # Mettre à jour le solde du client en soustrayant le montant du paiement supprimé
        client.credit -= payment.montant_paye
        client.save()

        return redirect('histpymtvente')

    return render(request, 'supprimerItem.html', {'msg':'reglementation'})