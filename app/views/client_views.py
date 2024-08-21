from ..models import Client
from ..forms import ClientForm  
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


def fiche_jornal_clients(request):
    clients = Client.objects.all()
    solde_total = sum(client.credit for client in clients if client.active)

    context = {
        'clients': clients,
        'solde_total':solde_total,
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
        