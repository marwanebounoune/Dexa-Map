from account.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import table_devis
import re
from smtplib import SMTPException
from django.conf import settings
from threading import Thread
from api_map.models import Documents

#gestion du formulaire de demande de devis
def quotation(request):
    if request.method == 'GET':
        return render(request, 'quotes/quote.html')
    if request.method == 'POST':

        #Variable
        erreur = 0
        devis_validation = table_devis()
        valid_email=0
        valid_phone=0
        #Récupération de la Data
        nom = request.POST['nom']
        mail = request.POST['email']
        telephone = request.POST['telephone']
        societe = request.POST['societe']
        secteur = request.POST['secteur']
        message = request.POST['message']
        
        #Vérification de la Data
        if len(nom) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au nom complet')
        elif len(nom)>50:
            erreur = 1
            messages.error(request, 'Le champs relatif au nom ne doit pas dépasser 50 caractères')
        if len(mail) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif à l\'email')
        else:
            if len(mail) > 254:
                erreur = 1
                messages.error(request, 'Le champs relatif à l\'email ne doit pas dépasser 254 caractères')
            if validateEmail(mail) == 0:
                valid_email=1
                erreur = 1
                messages.error(request, "Format de l'adresse e-mail est non valide")
        if len(telephone) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au telephone')
        else:
            if validateTelephone(telephone) == 0:
                valid_phone=1
                erreur = 1
                messages.error(request, 'Numero de telephone non valide (doit contenir 10 chiffre et commencer par 0)')
        if len(societe) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif à la société')
        elif len(societe) > 200:
            erreur = 1
            messages.error(request, 'Le champs relatif à la société ne doit pas dépasser 200 caractères')      
        if len(secteur) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au activité de la société')
        if len(message) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au message')
        if erreur == 0:
            #Enregistrer le devis
            devis = table_devis(nom=nom, email=mail, telephone=telephone, societe=societe, secteur=secteur, message=message)
            devis.save()
            #Envoyer une email  
            html_content = render_to_string("email_template.html",{'Title':'Demande de devis','Content': 'message content'})   
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                #subject
                "Demande de devis",
                #content
                text_content,
                #from_email
                settings.EMAIL_HOST_USER,
                #recepient
                {mail},
                #fail_silently=True
            )
            try:
                email.attach_alternative(html_content, "text/html")
                EmailThread(email).start()
            except SMTPException as e:
                print('There was an error sending an email: ', e)
            messages.success(request, 'Votre demande a été bien enregistrée, Une confirmation vous sera envoyée à l\'adresse email indiquée,  Merci de bien vouloir vérifier votre boîte de réception: '+ mail)
            return redirect('login')
        if erreur == 1:
            devis_validation = table_devis(nom=nom, email=mail, telephone=telephone, societe=societe, secteur=secteur, message=message)
            context = {
                'devis_validation': devis_validation,
                'valid_phone': valid_phone,
                'valid_email': valid_email,
                'erreur': erreur
                }
            return render(request, 'quotes/quote.html',context)
    

#regex mail
def validateEmail(email):
    if len(email) > 6:
        if re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email) != None:
            return 1
    return 0
#regex telephone
def validateTelephone(tel):
    if re.match(r'^0[0-9]{9}$', tel) != None:
        return 1
    return 0

#multithreading pour accélérer l'envoie de l'email
class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run (self):
        self.email.send()

#proteger les fichiers pdf
@login_required(login_url='login')  
def serve_protected_document(request, relative_path):
    
    if re.match(r'^devis/+', relative_path) != None:
        if request.user.is_superuser or request.user.groups.filter(name='Front-office').exists():#frontend
            absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, relative_path)
            response = FileResponse(open(absolute_path, 'rb'), as_attachment=True)
            return response
        else:
            return HttpResponseForbidden()
    else:
        if re.match(r'^doc_pins_my_map/+', relative_path) != None:
            doc = get_object_or_404(Documents, fichier=relative_path)
            print("doc", doc)
            userPere = False
            Doc_owner = User.objects.get(id = doc.username.id)
            if(request.user.userType == 'secondaire'):
                userPere = User.objects.get(id = request.user.lien)
            if request.user == Doc_owner or ( userPere != False and Doc_owner == userPere ) or Doc_owner.lien == request.user.id:
                absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, relative_path)
                response = FileResponse(open(absolute_path, 'rb'), as_attachment=True)
                return response
            else:
                return HttpResponseForbidden()
        else:
            print("image_data","image_data")
            absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, relative_path)
            response = FileResponse(open(absolute_path, 'rb'), as_attachment=True)
            return response

