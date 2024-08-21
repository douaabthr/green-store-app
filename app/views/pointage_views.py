from django.db.models import Sum
from django.shortcuts import  render
from django.db.models import Q
from datetime import datetime
from ..models import Centre,Employe,Absent,Massrouf,Exit_time,Payed_at,Command
from datetime import datetime, timezone
import json
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import CommandForm
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timezone
import json
from datetime import datetime
from decimal import Decimal
from django.db.models import Sum, F, ExpressionWrapper, DurationField, Case, When, DateTimeField, Value, Func
from django.db.models.functions import ExtractHour, ExtractMinute
from django.utils import timezone
from datetime import datetime, time
from datetime import datetime, time
from django.db.models import Q, Sum
from django.utils.timezone import make_aware, get_current_timezone
from decimal import Decimal
from django.shortcuts import render
from django.utils.timezone import make_aware, get_current_timezone

def systemePointage(request, employe_id):
    E = Employe.objects.get(pk=employe_id)
    print("1",E)
    absents = Absent.objects.filter(employe=employe_id)
    messrofs = Massrouf.objects.filter(employe=employe_id)
    exit_times = Exit_time.objects.filter(employe=employe_id)

    absents_data = []
    for absent in absents:
        date_abcence = absent.date_abcence
        if isinstance(date_abcence, datetime):
            if date_abcence.tzinfo is None:
                date_abcence = date_abcence.replace(tzinfo=timezone.utc)
            date_abcence = date_abcence.isoformat()
        absents_data.append({
            'id': absent.id,
            'employe': absent.employe_id,
            'date_abcence': date_abcence,
        })

    messrofs_data = []
    for messrof in messrofs:
        demende_at = messrof.demende_at.isoformat()
        messrofs_data.append({
            'id': messrof.id,
            'employe': messrof.employe_id,
            'demende_at': demende_at,
            'montant_dem': str(messrof.montant_dem),
        })

    exit_times_data = []
    for exit_time in exit_times:
        date_sortie = exit_time.date_sortie
        if isinstance(date_sortie, datetime):
            if date_sortie.tzinfo is None:
                date_sortie = date_sortie.replace(tzinfo=timezone.utc)
            date_sortie = date_sortie.isoformat()
        exit_times_data.append({
            'id': exit_time.id,
            'employe': exit_time.employe_id,
            'date_sortie': date_sortie,
        })

    if request.method == 'POST':
        integer_input = request.POST.get('integerInput')
        time_input = request.POST.get('timeInput')
        presence_input = request.POST.get('presenceInput')
        selectedDate = request.POST.get('selectedDate')
        deleteExitTime = request.POST.get('deleteExitTime')
        deleteMasrof = request.POST.get('deleteMasrof')
        E = Employe.objects.get(pk=employe_id)

        print("hiiiiiiiiiiiiiii",E )

        selectedDate = datetime.strptime(selectedDate, '%d %B %Y').date() if selectedDate else None


        if deleteExitTime == 'true' : 
            Exit_time.objects.filter(employe=E, date_sortie__date=selectedDate).delete()
            
        if deleteMasrof == 'true' : 
            Massrouf.objects.filter(employe=E, demende_at=selectedDate).delete()


        integer_input = int(integer_input) if integer_input else None
        time_input = datetime.strptime(time_input, '%H:%M').time() if time_input else None
        presence_input = presence_input.lower() == 'true' if presence_input else None
        date = datetime.combine(selectedDate, time_input) if selectedDate and time_input else None

        if integer_input is not None and selectedDate:
            Massrouf.objects.update_or_create(
                employe=E,
                demende_at=selectedDate,
                defaults={'montant_dem': integer_input},
            )

        if presence_input==True  :
            Absent.objects.update_or_create(
                employe=E,
                date_abcence=selectedDate,
            )
        else:
            if deleteMasrof != 'true' and  deleteExitTime != 'true' :
                print(presence_input)
                Absent.objects.filter(employe=E, date_abcence=selectedDate).delete()
        

        if date :
            
            ET, created = Exit_time.objects.update_or_create(
            employe=E,
            date_sortie__date=selectedDate,
            defaults={'date_sortie': date}
          )

            if created:
                print("A new record was created.")
            else:
                print("An existing record was updated.")   


        context = {
            'E':E,
            'absents': json.dumps(absents_data),
            'messrofs': json.dumps(messrofs_data),
            'exit_times': json.dumps(exit_times_data)
        }

        return render(request, "systemePointage.html", context)

    else:

        context = {
            'E': E,
            'absents': json.dumps(absents_data),
            'messrofs': json.dumps(messrofs_data),
            'exit_times': json.dumps(exit_times_data)
        }

        return render(request, "systemePointage.html", context)


def CalculerSalaire(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        filtre_centre = request.POST.get('browser')
        date_debut_de_mois = request.POST.get('date_debut')
        date_fin_de_mois = request.POST.get('date_fin')
        
        # Conversion des dates en objets datetime.date
        date_debut_de_mois = datetime.strptime(date_debut_de_mois, '%Y-%m-%d').date()
        date_fin_de_mois = datetime.strptime(date_fin_de_mois, '%Y-%m-%d').date()
        
        # Filtrage des employés selon le centre, si spécifié
        if filtre_centre:
            employes_centres = Employe.objects.filter(EmployeCentre=filtre_centre)
        else:
            employes_centres = Employe.objects.all()
        
        resultat_employes = []
        nb_jour = (date_fin_de_mois - date_debut_de_mois).days
        tz = get_current_timezone()

        for emp in employes_centres:
            # Initialisation des variables pour chaque employé
            total_masrouf = Decimal('0.0')
            nb_absent = 0
            heures_travaillees_totales = Decimal('0.0')
            heure_debut_journee = time(8, 0)
            
            # Calcul des heures travaillées pour l'employé dans la période donnée
            exit_times = Exit_time.objects.filter(
                Q(employe=emp) & 
                Q(date_sortie__gte=date_debut_de_mois) & 
                Q(date_sortie__lte=date_fin_de_mois)
            )

            for exit_time in exit_times:
                date_sortie = make_aware(exit_time.date_sortie, timezone=tz) if exit_time.date_sortie.tzinfo is None else exit_time.date_sortie
                heure_debut = make_aware(datetime.combine(date_sortie.date(), heure_debut_journee), timezone=tz)
                difference = date_sortie - heure_debut
                heures_travaillees = Decimal(difference.total_seconds()) / Decimal(3600)  # Convertir les secondes en heures
                heures_travaillees_totales += heures_travaillees
            print(heures_travaillees_totales)

            # Calcul du nombre de jours d'absence
            nb_absent = Absent.objects.filter(
                Q(employe=emp) &
                Q(date_abcence__gte=date_debut_de_mois) & 
                Q(date_abcence__lte=date_fin_de_mois)
            ).count()

            # Ajustement du nombre de jours de travail avec les jours d'absence
            nb_avec_exit_time = exit_times.count()
            if nb_avec_exit_time != 0:
                nb_jour = nb_jour-nb_absent
                print(nb_jour)
            
            # Calcul du montant total des masroufs
            total_masrouf = Massrouf.objects.filter(
                Q(employe=emp) & 
                Q(demende_at__gte=date_debut_de_mois) & 
                Q(demende_at__lte=date_fin_de_mois)
            ).aggregate(total=Sum('montant_dem'))['total'] or Decimal('0.0')

            # Calcul du salaire
            salaire = (nb_jour - nb_absent) * emp.salaire_base - total_masrouf + (heures_travaillees_totales * (emp.salaire_base / Decimal(8)))

            # Création du dictionnaire de résultat pour chaque employé
            resultat_employe = {
                'codeEmp': emp.codeEmp,
                'nomEmp': emp.nomEmp,
                'prenomEmp': emp.prenomEmp,
                'nb_absent': nb_absent,
                'total_masrouf': total_masrouf,
                'salaire': salaire,
            }
            resultat_employes.append(resultat_employe)

        # Récupération des centres pour l'affichage
        centre = Centre.objects.all()
        return render(request, "Salaire.html", {"resultat_employes": resultat_employes, "centre": centre})

    else:
        # Si ce n'est pas une requête POST, afficher une page vide avec les centres disponibles
        resultat_employes = []
        employes_centres = Employe.objects.all()
        for emp in employes_centres:
            resultat_employe = {
                'codeEmp': emp.codeEmp,
                'nomEmp': emp.nomEmp,
                'prenomEmp': emp.prenomEmp,
                'nb_absent': 0,
                'total_masrouf': Decimal('0.0'),
                'salaire': Decimal('0.0'),
            }
            resultat_employes.append(resultat_employe)

        centre = Centre.objects.all()
        return render(request, "Salaire.html", {"resultat_employes": resultat_employes, "centre": centre})

def fiche_jornal_command(request):
    commandes = Command.objects.all()

    context = {
        'commandes': commandes,
    }

    return render(request, 'Commande.html', context)

def inserer_commande(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listCommand')  # Redirige vers la liste des commandes
    else:
        form = CommandForm()

    return render(request, 'ajouter_command.html', {'form': form, 'msg': 'Ajouter une Commande'})

def modifier_command(request, commande_id):
    commande = get_object_or_404(Command, pk=commande_id)  # Utilise get_object_or_404 pour une meilleure gestion des erreurs

    if request.method == 'POST':
        form = CommandForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('listCommand')  # Redirige vers la liste des commandes
    else:
        form = CommandForm(instance=commande)

    return render(request, 'modifier_command.html', {'form': form, 'commande': commande, 'msg': 'Modifier une Commande'})

def supprimer_command(request, commande_id):
    commande = get_object_or_404(Command, pk=commande_id)  # Utilise get_object_or_404

    if request.method == 'POST':
        commande.delete()  # Supprime la commande
        return redirect('listCommand')  # Redirige vers la liste des commandes

    return render(request, 'supprimer_command.html', {'commande': commande, 'msg':commande})