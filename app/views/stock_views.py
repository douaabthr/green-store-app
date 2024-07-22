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
