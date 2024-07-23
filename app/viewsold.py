from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from .models import Achat
from .forms import PaymentAchatForm
from .models import PaymentAchat
from .forms import FiltreAchatForm
from .forms import FiltreVenteForm
from .forms import AchatForm
from .forms import PaymentVenteForm
from .forms import PaymentVenteFormForAjout
from .forms import PaymentAchatFormForAjout
from .models import PaymentVente
from .models import Produit
from .forms import FiltreStockForm
from .forms import FiltreTransfertForm
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render,redirect
from django.db.models import Sum,Q
from datetime import datetime
from .forms import ProduitForm1,MatiereForm1,ClientForm1,FournisseurForm1,EmployeForm1,CentreForm1,AchatForm1,tranForm,VendreProduitForm,FiltreTransfereForm,FiltreAchatForm,MonFormulaire,MonFormulaire_centre1,VendreMatiereForm
from .models import Produit,Client,Fournisseur,Centre,Employe,Achat,Transfert,VenteP,Absent,Massrouf,MatierePremiere,VenteM
from decimal import Decimal
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, redirect
from .forms import PaymentAchatFormForAjout
from django.shortcuts import render, redirect
from .forms import PaymentVenteFormForAjout 
from itertools import chain
from django.shortcuts import render
from django.db.models import Q
from .models import Produit, Achat
from .forms import FiltreStockForm
from .models import VenteP
from .models import VenteM
from .forms import VentePForm
from .forms import VenteMForm
from django.shortcuts import render
from django.db.models import Q
from .models import Produit, Achat
from .forms import FiltreStockForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produit, Achat
from .forms import FiltreStockForm
from django.db.models import Q
from io import BytesIO
from reportlab.pdfgen import canvas
from .forms import FiltreVentePForm
from .models import MatierePremiere



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

#*******************ACHAT******************#

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



#***********************************************************************




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
                


    else:
        form = VentePForm(instance=vente)
        return render(request, 'modifierItem.html', {'form': form,'msg':'Vente'})

    
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


def generate_pdf(matieres):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Logique pour générer le contenu du PDF avec ReportLab
    y = 800  # Position verticale initiale
    for matiere in matieres:
        p.drawString(100, y, matiere.designation_matiere)
        y -= 20  # Décalage vertical pour le prochain produit

    p.showPage()
    p.save()

    # Rembobiner le buffer pour lire depuis le début
    buffer.seek(0)

    return buffer



def fiche_journal_Stock(request):
    matieres = MatierePremiere.objects.all()
    achats_concerne = Achat.objects.none()

    if request.method == 'POST':
        form = FiltreStockForm(request.POST)
        if form.is_valid():
            fournisseur = form.cleaned_data.get('fournisseur')
            date_achat = form.cleaned_data.get('date_achat')
            codeM = form.cleaned_data.get('codeM')

            if not fournisseur and not date_achat and not codeM:
                matieres = MatierePremiere.objects.all()
            
            else:

            # Construire la requête de filtre pour les achats
                filtre_achats = Q()
                if fournisseur:
                    filtre_achats &= Q(fournisseur=fournisseur)
                if date_achat:
                    filtre_achats &= Q(buyed_at__year=date_achat.year,buyed_at__month=date_achat.month,buyed_at__day=date_achat.day)

                achats_concerne = Achat.objects.filter(filtre_achats)

            # Construire la requête de filtre pour les produits
                filtre_produits = Q()
                for achat in achats_concerne:
                    filtre_produits |= Q(codeM=achat.matiere_achete.codeM)

                if codeM:
                    filtre_produits &= Q(codeM=codeM)

            # Appliquer le filtre
                matieres = MatierePremiere.objects.filter(filtre_produits).distinct()

            # Si le paramètre 'generate_pdf' est présent dans la requête, générer le PDF
            if 'generate_pdf' in request.POST:
                pdf_buffer = generate_pdf(matieres)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="etat_stock.pdf"'
                response.write(pdf_buffer.getvalue())
                return response
    else:
        form = FiltreStockForm()

    return render(request, 'EtatStock.html', {
        'matieres': matieres,
        'form': form
    })

def supprimer_matiere(request, matiere_id):
    matiere = MatierePremiere.objects.get(pk=matiere_id)
    
    # Affichage de la page de confirmation
    if request.method == 'POST':
        # Suppression de l'achat
        matiere.active=False
        matiere.save()

        return redirect('stock')  # Redirection vers la page principale après la suppression

    return render(request, 'supprimerItem.html', {'matiere': matiere,'msg':'Matiere premiere'})

def modifier_matiere(request, matiere_id):
    matiere = MatierePremiere.objects.get(pk=matiere_id)

    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            matiere.save()
            form.save()
            return redirect('stock')

    else:
        form = MatiereForm(instance=matiere)
        return render(request, 'modifierItem.html', {'form': form,'msg':'Matiere premiere'})



def fiche_jornal_produits(request):
    produits = Produit.objects.all()

    context = {
        'produits': produits
    }

    return render(request, 'Produit.html', context)

from .forms import ProduitForm

def inserer_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listProduits')
    else:
        form = ProduitForm()

    return render(request, 'insererItem.html', {'form': form,'msg':'Produits'})

def modifier_produit(request,produit_id):
    produit = Produit.objects.get(pk=produit_id)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('listProduits')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'modifierItem.html', {'form': form, 'produit': produit,'msg':'Produits'})

def supprimer_produit(request,produit_id):
    produit = Produit.objects.get(pk=produit_id)
    
    if request.method == 'POST':
        # Suppression de l'achat
        produit.active = False
        produit.save()
        return redirect('listProduits')
    
    return render(request, 'supprimerItem.html', {'produit': produit,'msg':'Produits'})



##############FOURNISEUR#############################################
from .models import Fournisseur
from .forms import FournisseurForm
from .models import Centre
from .forms import CentreForm 
from django.shortcuts import render, redirect
from .models import Employe
from .forms import EmployeForm 

def fiche_jornal_fournisseurs(request):
    produits = Fournisseur.objects.all()

    context = {
        'fournisseurs': produits
    }

    return render(request, 'Fournisseur.html', context)


def inserer_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listFournisseurs')
    else:
        form = FournisseurForm()

    return render(request, 'insererItem.html', {'form': form,'msg':'Fournisseur'})

def modifier_fournisseur(request,fourniseur_id):
    fournisseur = Fournisseur.objects.get(pk=fourniseur_id)

    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('listFournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)

    return render(request, 'modifierItem.html', {'form': form, 'fournisseur': fournisseur,'msg':'Fournisseur'})

def supprimer_fournisseur(request,fourniseur_id):
    fournisseur = Fournisseur.objects.get(pk=fourniseur_id)
    
    if request.method == 'POST':
        # Suppression de l'achat
        fournisseur.active = False
        fournisseur.save()
        return redirect('listFournisseurs')
    
    return render(request, 'supprimerItem.html', {'fournisseur': fournisseur,'msg':'Fournisseur'})

###################CLIENT########################


from .models import Client
from .forms import ClientForm  

def fiche_jornal_clients(request):
    clients = Client.objects.all()

    context = {
        'clients': clients,
    }

    return render(request, 'Client.html', context)

def inserer_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listClients')
    else:
        form = ClientForm()

    return render(request, 'insererItem.html', {'form': form},{'msg':'Client'})

def modifier_client(request, client_id):
    client = Client.objects.get(pk=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('listClients')
    else:
        form = ClientForm(instance=client)

    return render(request, 'modifierItem.html', {'form': form, 'client': client,'msg':'Client'})

def supprimer_client(request, client_id):
    client = Client.objects.get(pk=client_id)

    if request.method == 'POST':
        client.active = False
        client.save()
        return redirect('listClients')

    return render(request, 'supprimerItem.html', {'client': client,'msg':'Client'})

#####################CENTRE##########################


def fiche_jornal_centres(request):
    centres = Centre.objects.all()

    context = {
        'centres': centres,
        'msg':'Centre'
    }

    return render(request, 'info_centre.html', context)

def inserer_centre(request):
    if request.method == 'POST':
        form = CentreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listCentres')
    else:
        form = CentreForm()

    return render(request, 'insererItem.html', {'form': form,'msg':'Centre'})

def modifier_centre(request, centre_id):
    centre = Centre.objects.get(pk=centre_id)

    if request.method == 'POST':
        form = CentreForm(request.POST, instance=centre)
        if form.is_valid():
            form.save()
            return redirect('listCentres')
    else:
        form = CentreForm(instance=centre)

    return render(request, 'modifierItem.html', {'form': form, 'centre': centre,'msg':'Centre'})

def supprimer_centre(request, centre_id):
    centre = Centre.objects.get(pk=centre_id)

    if request.method == 'POST':
        centre.active = False
        centre.save()
        return redirect('listCentres')

    return render(request, 'supprimerItem.html', {'centre': centre,'msg':'Centre'})




# views.py

 # Assurez-vous d'avoir un formulaire approprié défini dans forms.py

def fiche_jornal_employes(request):
    employes = Employe.objects.all()

    context = {
        'employes': employes,
    }

    return render(request, 'Employe.html', context)

def inserer_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listEmployes')
    else:
        form = EmployeForm()

    return render(request, 'insererItem.html', {'form': form, 'msg': 'Employe'})

def modifier_employe(request, employe_id):
    employe = Employe.objects.get(pk=employe_id)

    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('listEmployes')
    else:
        form = EmployeForm(instance=employe)

    return render(request, 'modifierItem.html', {'form': form, 'employe': employe, 'msg': 'Employe'})

def supprimer_employe(request, employe_id):
    employe = Employe.objects.get(pk=employe_id)

    if request.method == 'POST':
        employe.active = False
        employe.save()
        return redirect('listEmployes')

    return render(request, 'supprimerItem.html', {'employe': employe, 'msg': 'Employe'})



from .models import Transfert
from .forms import MatiereForm
from .models import Transfert
from .forms import FiltreTransfertRecuForm 
from .models import Ingridiant
from decimal import Decimal

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
    


def fiche_journal_transferts_recu_centre1(request):
    transferts = Transfert.objects.filter(centre__codeC='c1')
    if transferts:
        total_transferts = transferts.aggregate(total=Sum('cout_transfere'))['total'] or 0
    else:
        total_transferts=Decimal(0.0)

    ventes = VenteP.objects.filter(lieu_ventes__codeC='c1')
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



from .forms import TransfertForm
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Vérifier si l'e-mail est déjà utilisé par un autre utilisateur
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Cet e-mail est déjà utilisé par un autre utilisateur.')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, email)
                return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    context = {'form': form}
    return render(request, 'Register.html', context)
def login_page(request):

    if request.method =='POST':
        username = request.POST.get('username')  # Correction ici
        password = request.POST.get('password')  # Correction ici

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Userrname or password is incorrect')

    return render(request,'Login.html')

def logout_page(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request,"Home.html")

def h(request):
    return render(request,"h.html")

# django_project/users/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import login
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link. Please contact support.')
        return redirect('login')

from .forms import ProduitForm1,MatiereForm1,ClientForm1,FournisseurForm1,EmployeForm1,CentreForm1,AchatForm1,tranForm,VendreProduitForm,FiltreTransfereForm,FiltreAchatForm,MonFormulaire,MonFormulaire_centre1,VendreMatiereForm
from .models import Produit,Client,Fournisseur,Centre,Employe,Achat,Transfert,VenteP,Absent,Massrouf,MatierePremiere,VenteM


#ANALYSE################################
def indexView(request):
    # Récupérer l'année à partir de la date actuelle
    nb_notification=notification1()

    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year

    
        # traitement pour afficher les top fournisseur de annee actuelle 

    # debut
    
    top_fournisseur_anne_actuelle = Achat.objects.filter(
    buyed_at__year=2024
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
    annee_actuelle = datetime.now()
    valeur_presedent_ventes = 0
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    evoluation_taux_ventes_annee = []

    for month in months:
        total_ventes = VenteM.objects.filter(salled_at__month=month, salled_at__year=2024).aggregate(
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
    annee_actuelle = datetime.now()
    valeur_presedent_benefice = 0
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    evoluation_taux_Benifice_annee = []

    for month in months:
        total_ventes = VenteM.objects.filter(salled_at__month=month, salled_at__year=2024).aggregate(
            Sum('montantTotalVen'))['montantTotalVen__sum'] or 0
        total_Transfere = Achat.objects.filter(buyed_at__month=month, buyed_at__year=annee_actuelle.year).aggregate(
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
    salled_at__year=2024
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
    total_ventes = VenteM.objects.filter(salled_at__year=2024).aggregate(total=Sum('montantTotalVen'))['total'] or 0

# Calculate total purchases for the current year
    total_achat = Achat.objects.filter(buyed_at__year=2024).aggregate(total=Sum('montantTotalHT'))['total'] or 0
    total_cost_transferred = Transfert.objects.filter(transfer_at__year=2024).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

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
def analyse(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    Annee_min_pour_top_fournisseur = 2023
    nomber_top_fournisseurs = 5
    Annee_min_Achat=2023
    Annee_min_pour_best_client=2023
    nombre_best_clients=5
    Annee_min_Vente=2023
    Annee_min_pour_top_produit=2023
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
            Annee_min_Achat=2023
        if not Annee_min_pour_top_fournisseur:
            Annee_min_pour_top_fournisseur = annee_actuelle-2
        if  nomber_top_fournisseurs is None:
            nomber_top_fournisseurs = 5
        if not Annee_min_pour_best_client:
            Annee_min_pour_best_client=2023
        if not nombre_best_clients:
            nombre_best_clients=5
        if not Annee_min_Vente:
            Annee_min_Vente=2023
        if not Annee_min_pour_top_produit:
            Annee_min_pour_top_produit=2023
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
def centre1(request):
    annee_actuelle=datetime.now().year

    valeur_presedent_ventes=0
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    evoluation_taux_ventes_annee=[]
    centre=Centre.objects.get(codeC='c1')
    for month in months:
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=2024).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
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
    centre=Centre.objects.get(codeC='c1')
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
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year=2024).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

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
        total_ventes=VenteP.objects.filter(lieu_ventes=centre.id,salled_at__month=month,salled_at__year=2024).aggregate(Sum('montantTotalVen'))['montantTotalVen__sum']  or 0 
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
def analyse_centre1(request):
    date_actuelle = datetime.now()
    annee_actuelle = date_actuelle.year
    centre=Centre.objects.get(codeC='c1')
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
    total_cost_transferred = Transfert.objects.filter(centre=centre,transfer_at__year__lte=2024,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(lieu_ventes=centre.id,salled_at__year__lte=2024,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

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
    total_cost_transferred = Transfert.objects.filter(transfer_at__year__lte=2024,transfer_at__year__gte=Annee_min_Vente).aggregate(total_cost=Sum('cout_transfere'))['total_cost'] or 0

# Calculate total quantity and amount of sales for the specified center and product in the current year
    total_amount_sold = VenteP.objects.filter(salled_at__year__lte=2024,salled_at__year__gte=Annee_min_Vente).aggregate(total_amount=Sum('montantTotalVen'))['total_amount'] or 0

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

def save_produit(request):
    if request.method == 'POST':
        form = ProduitForm1(request.POST)

        if form.is_valid():
            form.save()
            form = ProduitForm1()
            message_succe="Produit ajouter avec succe"
            return render(request,"add_produits.html",{"message_succe":message_succe,"form":form}) 
        else :
            message="Cette Code exist deja!"
            form = ProduitForm1()
            message_succe="Produit ajouter avec succe"
            return render(request,"add_produits.html",{"message":message,"form":form}) 
    else:
        form = ProduitForm1()
        return render(request,"add_produits.html",{"form":form})
def save_matiere(request):
    if request.method == 'POST':
        form = MatiereForm1(request.POST)

        if form.is_valid():
            form.save()
            form = MatiereForm1()
            message_succe="Produit ajouter avec succe"
            return render(request,"add_matiere.html",{"message_succe":message_succe,"form":form}) 
        else :
            form = MatiereForm1()
            message="Cette Code exist deja!"
            return render(request,"add_matiere.html",{"message":message,"form":form}) 

                   
    else:
        form = MatiereForm1()
        return render(request,"add_matiere.html",{"form":form})   



        ####SAVE#######################
def save_client(request):
    if request.method == 'POST':
        form = ClientForm1(request.POST)

        if form.is_valid():
            form.save()
            form = ClientForm1()
            message_succe="Client ajouter avec succe"
            return render(request,"add_client.html",{"message_succe":message_succe,"form":form}) 
        else :
            form = ClientForm1()
            message="Cette Code exist deja!"
            return render(request,"add_client.html",{"message":message,"form":form}) 

        
    else:
        form = ClientForm1()
        return render(request,"add_client.html",{"form":form}) 
        
def save_fournisseur(request):

        if request.method == 'POST':
            form = FournisseurForm1(request.POST)
            if form.is_valid():
                form.save()
                form = FournisseurForm1()
                message_succe="Fournisseur ajouter avec succe"
                return render(request,"add_fournisseur.html",{"message_succe":message_succe,"form":form}) 
            else :
                message="Cette Code exist deja!"
                form = FournisseurForm1()
                return render(request,"add_fournisseur.html",{"form":form,"message":message}) 

        else:

            form = FournisseurForm1()
            return render(request,"add_fournisseur.html",{"form":form}) 

def save_employe(request):
        if request.method == 'POST':
            form = EmployeForm1(request.POST)

            if form.is_valid():
                form.save()
                form = EmployeForm1()
                message_succe="Employe ajouter avec succe"
                return render(request,"add_employe.html",{"message_succe":message_succe,"form":form}) 
            else :
                message="Cette Code exist deja!"
                form = EmployeForm1()
                return render(request,"add_employe.html",{"form":form,"message":message}) 

        
        else:
            form = EmployeForm1()
            return render(request,"add_employe.html",{"form":form})

def save_centre(request):
        if request.method == 'POST':
            form = CentreForm1(request.POST)
            if form.is_valid():
                form.save()
                form = CentreForm1()
                message_succe="Centre ajouter avec succe"
                return render(request,"add_centre.html",{"message_succe":message_succe,"form":form}) 
            else :
                message="Cette Code exist deja!"
                form = CentreForm1()
                return render(request,"add_centre.html",{"form":form,"message":message}) 
        
        else:
            form = CentreForm1()
            return render(request,"add_centre.html",{"form":form})

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



def save_transfer(request):
        if request.method == 'POST':
            form = tranForm(request.POST)

            if form.is_valid():
                Q=form.cleaned_data['produit_transfere']
                p=MatierePremiere.objects.get(id=Q.id)
                QT=form.cleaned_data['quantitTran']
                transfer_at = form.cleaned_data['transfer_at']
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
                    cout_tan = 0
                    produits_from_achat=Achat.objects.filter(matiere_achete=Q.id)
                    for pa in produits_from_achat:
                        if QT !=0:
                            if  pa.quantitDispo !=0 and pa.quantitDispo <QT:
                              cout_tan=cout_tan+pa.quantitDispo*pa.prix_unitaire_HT
                              QT=QT-pa.quantitDispo
                              pa.quantitDispo=0
                            else :
                              if pa.quantitDispo >=QT:
                                   cout_tan=cout_tan+pa.prix_unitaire_HT*QT
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
                montantTotalVen = prix_unitaire_Ven * quantitVen
                produit_vendus.quantiteStockPod=produit_vendus.quantiteStockPod-quantitVen
                produit_vendus.save()
                VenteP.objects.create(
                    client=Client,
                    produit_vendus=produit_vendus,
                    salled_at=salled_at,
                    prix_unitaire_Ven=prix_unitaire_Ven,
                    quantitVen=quantitVen,
                    lieu_ventes=lieu_ventes,
                    montantTotalVen=montantTotalVen,
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
                produit_vendus = MatierePremiere.objects.get(id=produit_vendus_id)
                prix_unitaire_Ven = produit_vendus.prix_unitaire_Ven
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
def systemePointage(request):
    if request.method=='POST':
        code_emp = request.POST.get('code_emp')
        date_emp = request.POST.get('date')
        browser_choice = request.POST.get('browser')
        massrof = request.POST.get('massrof')
        codes_employes = request.POST.get('codes_employes')
        # Maintenant, codes_employes contient la liste des codes d'employés envoyés depuis le formulaire
        employe=Employe.objects.get(codeEmp=code_emp)
        if browser_choice=="absent":
            if date_emp =="" :
                employes_data=[]
                c=""
                for emp in codes_employes :
                    if emp !="," :
                        c=c+emp
                    else:
                        emp=Employe.objects.get(codeEmp=c)
                        e = {
                        'codeEmp': emp.codeEmp,
                        'nomEmp': emp.nomEmp,
                        'prenomEmp': emp.prenomEmp,
                        'EmployeCentre': emp.EmployeCentre,
                        }
                        employes_data.append(e)
                        c=""
                message = "Veuillez entrer la date d'absence"
                return render(request,"systemePointage.html", {"message":message,'employes': employes_data})

            else :
                Absent.objects.create(
                employe=employe,
                date_abcence=date_emp,
                )
        if massrof :
            massrof=int(massrof)   
        if  massrof and massrof !=0:
            
            if date_emp =="" :
                employes_data=[]
                c=""
                for emp in codes_employes :
                    if emp !="," :
                        c=c+emp
                    else:
                        emp=Employe.objects.get(codeEmp=c)
                        e = {
                        'codeEmp': emp.codeEmp,
                        'nomEmp': emp.nomEmp,
                        'prenomEmp': emp.prenomEmp,
                        'EmployeCentre': emp.EmployeCentre,
                        }
                        employes_data.append(e)
                        c=""
                message = "Veuillez entrer la date demande de massrofe"
                return render(request,"systemePointage.html", {"message":message,'employes': employes_data})

            else :
                Massrouf.objects.create(
                employe=employe,
                demende_at=date_emp,
                montant_dem=massrof,
            )
        c="" # cette prtie pou retorner les employes rester sans pointage
        employes_data=[]
        for emp in codes_employes :
            if emp !="," :
                c=c+emp
            else:
                emp=Employe.objects.get(codeEmp=c)
                if c!=code_emp :
                    e = {
                    'codeEmp': emp.codeEmp,
                    'nomEmp': emp.nomEmp,
                    'prenomEmp': emp.prenomEmp,
                    'EmployeCentre': emp.EmployeCentre,
                    }
                    employes_data.append(e)
                c=""

        return render(request,"systemePointage.html", {'employes': employes_data})
    else:
        employes=Employe.objects.all()
        employes_data=[]
        for emp in employes :
            e = {
            'codeEmp': emp.codeEmp,
            'nomEmp': emp.nomEmp,
            'prenomEmp': emp.prenomEmp,
            'EmployeCentre': emp.EmployeCentre,
            }
            employes_data.append(e)

        return render(request,"systemePointage.html",{"employes":employes_data})

def CalculerSalaire (request):
    if request.method == 'POST' :
        filtre_centre = request.POST.get('browser')
        date_debut_de_mois=request.POST.get('date_debut')
        date_fin_de_mois=request.POST.get('date_fin')
        date_fin_de_mois = datetime.strptime(date_fin_de_mois, '%Y-%m-%d').date()
        date_debut_de_mois = datetime.strptime(date_debut_de_mois, '%Y-%m-%d').date()
        if filtre_centre :
            employes_centres=Employe.objects.filter(EmployeCentre=filtre_centre)
        else :
            employes_centres=Employe.objects.all()

        resultat_employes=[]
        nb_jour=(date_fin_de_mois-date_debut_de_mois).days
        for emp in  employes_centres :
            total_masrouf=0
            nb_absent=0
            nb_absent=Absent.objects.filter(Q(employe=emp) & (Q(date_abcence__lte=date_fin_de_mois) |
                                                               Q(date_abcence__gte=date_debut_de_mois))).count()
            total_masrouf = Massrouf.objects.filter(Q(employe=emp) & (Q(demende_at__lte=date_fin_de_mois) |
                                                                       Q(demende_at__gte=date_debut_de_mois))).values('montant_dem').aggregate(Sum('montant_dem'))['montant_dem__sum']
            total_masrouf = total_masrouf if total_masrouf is not None else Decimal('0.0')
            nb_absent = nb_absent if nb_absent is not None else 0
            salaire=(nb_jour-nb_absent)*emp.salaire_jour-total_masrouf
            resultat_employe = {
            'codeEmp': emp.codeEmp,
            'nomEmp': emp.nomEmp,
            'prenomEmp': emp.prenomEmp,
            'nb_absent': nb_absent,
            'total_masrouf': total_masrouf,
            'salaire': salaire,
                }
            resultat_employes.append(resultat_employe)
        centre=Centre.objects.all()
        return render(request,"Salaire.html",{"resultat_employes":resultat_employes,"centre":centre})
    else :
        resultat_employes=[]
        employes_centres=Employe.objects.all()
        for emp in  employes_centres :
            total_masrouf=0
            nb_absent=0
            salaire=0
            resultat_employe = {
            'codeEmp': emp.codeEmp,
            'nomEmp': emp.nomEmp,
            'prenomEmp': emp.prenomEmp,
            'nb_absent': nb_absent,
            'total_masrouf': total_masrouf,
            'salaire': salaire,
                }
            resultat_employes.append(resultat_employe)
        centre=Centre.objects.all()
        return render(request,"Salaire.html",{"resultat_employes":resultat_employes,"centre":centre})
from django.core.mail import send_mail
from django.shortcuts import render

def envoyer_email(request):
    destinataire = ['douaaboutehra19@gmail.com']
    sujet = 'DEMENDE MAJ APP GREEN STORE (AJOUT CENTRE)'
    message = 's\'il vous plait ajouter moi un nouveau centre'
    message1="Email Envoyé avec Succès"
    message2="Merci, votre demande a été traitée. Vous allez recevoir une confirmation par e-mail"
    send_mail(sujet, message, 'wafaaberrais2@gmail.com', destinataire, fail_silently=False)
    return render(request, 'notification.html',{"message1":message1,"message2":message2,})

