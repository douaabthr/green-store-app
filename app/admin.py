from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produit
from .models import Fournisseur
from .models import Centre
from .models import Employe
from .models import Client
from .models import Achat
from .models import VenteP
from .models import VenteM
from .models import Transfert
from .models import PaymentAchat
from .models import PaymentVente
from .models import Massrouf
from .models import MatierePremiere
from .models import Ingridiant,Absent

# Register your models here.
admin.site.register(Produit)
admin.site.register(MatierePremiere)
admin.site.register(Fournisseur)
admin.site.register(Centre)
admin.site.register(Employe)
admin.site.register(Client)
admin.site.register(Achat)
admin.site.register(VenteP)
admin.site.register(VenteM)
admin.site.register(Transfert)
admin.site.register(PaymentAchat)
admin.site.register(PaymentVente)
admin.site.register(Massrouf)
admin.site.register(Ingridiant)
admin.site.register(Absent)


