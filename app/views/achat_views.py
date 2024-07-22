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

def fiche_journal_achats(request):
    achats = Achat.objects.all()
    total_achats = Achat.objects.aggregate(total=Sum('montantTotalHT'))['total'] or 0

    if request.method == 'POST':
        form = FiltreAchatForm(request.POST)
        if form.is_valid():
            fournisseur = form.cleaned_data.get('fournisseur')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')

            # Construire la requête de filtre
            filtre_requete = Q()

            if fournisseur:
                filtre_requete &= Q(fournisseur=fournisseur)

            if date_debut:
                filtre_requete &= Q(buyed_at__gte=date_debut)

            if date_fin:
                filtre_requete &= Q(buyed_at__lte=date_fin)

            # Appliquer le filtre
            achats = Achat.objects.filter(filtre_requete)
            total_achats =achats.aggregate(total=Sum('montantTotalHT'))['total'] or 0
    else:
        form = FiltreAchatForm()

    return render(request, 'Achat.html', {
        'achats': achats,
        'total_achats': total_achats,
        'form': form
    })


def modifier_achat(request, achat_id):
    achat = Achat.objects.get(pk=achat_id)

    if request.method == 'POST':
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            ancien_achat = Achat.objects.get(pk=achat_id)
            if form.cleaned_data['quantitHT']>0:
                if ancien_achat.quantitHT != form.cleaned_data['quantitHT']:
            # Mettez à jour la quantité en stock du produit associé
                    matiere = ancien_achat.matiere_achete
                    matiere.quantiteStockMat -= ancien_achat.quantitHT
                    matiere.quantiteStockMat += form.cleaned_data['quantitHT']
                    matiere.save()

            # Enregistrez la modification de l'achat
                form.save()

                return redirect('achat')
            else:
                return render(request, "modifierItem.html", {'form': form, 'messageexp': 'Le montant doit être supérieur à zéro'})
    else:
        form = AchatForm(instance=achat)
        return render(request, 'modifierItem.html', {'form': form,'msg':'Achat'})

def supprimer_achat(request, achat_id):
    achat = Achat.objects.get(pk=achat_id)
    
    # Affichage de la page de confirmation
    if request.method == 'POST':
        # Suppression de l'achat
        achat.delete()

        # Déstockage du produit associé
        matiere = achat.matiere_achete
        matiere.quantiteStockMat-= achat.quantitHT
        matiere.save()

        return redirect('achat')  # Redirection vers la page principale après la suppression

    return render(request, 'supprimerItem.html', {'achat': achat,'msg':'Achat'})

def sava_achat(request):
    if request.method == 'POST':
        form = AchatForm1(request.POST)
        if form.is_valid():
            fournisseur = form.cleaned_data['fournisseur']
            prix_unitaire_HT = form.cleaned_data['prix_unitaire_HT']
            quantitHT = form.cleaned_data['quantitHT']
            buyed_at = form.cleaned_data['buyed_at']
            produit_achete_id = request.POST.get('prd')
            if quantitHT<=0 or prix_unitaire_HT<=0 :
                message1="Quantite ou prix invalide "
                produits = MatierePremiere.objects.all()
                form = AchatForm1()
                return render(request, "add_achat.html", {"form": form, "produits": produits,"message1":message1})
            produit_achete_id=int(produit_achete_id)
            # Récupérer le produit en fonction de l'ID et ajoueter la quantite acheter
            produit_achete = MatierePremiere.objects.get(id=produit_achete_id)
            produit_achete.quantiteStockMat=produit_achete.quantiteStockMat+quantitHT
            produit_achete.save()

            # Calculer le montant total
            montantTotalHT = quantitHT * prix_unitaire_HT

            # Créer l'objet Achat
            Achat.objects.create(
                fournisseur=fournisseur,
                matiere_achete=produit_achete,
                buyed_at=buyed_at,
                prix_unitaire_HT=prix_unitaire_HT,
                quantitHT=quantitHT,
                quantitDispo=quantitHT,
                montantTotalHT=montantTotalHT
            )
            produits = MatierePremiere.objects.all()
            form = AchatForm1()
            message_succe="Achat effecute avec succe"
            return render(request, "add_achat.html", {"form": form, "produits": produits,"message_succe":message_succe})

    else:
        produits = MatierePremiere.objects.all()
        form = AchatForm1()
        return render(request, "add_achat.html", {"form": form, "produits": produits})
