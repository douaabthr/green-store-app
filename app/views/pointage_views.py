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