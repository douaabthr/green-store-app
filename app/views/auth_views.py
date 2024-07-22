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