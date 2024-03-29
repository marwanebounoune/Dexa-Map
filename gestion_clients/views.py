from rest_framework.response import Response
from gestion_clients.models import ClientPhysique
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view



@api_view(['POST'])
@login_required(login_url='login')
def AjouterClientPhysique(request):
    if request.method == 'POST':
        erreur = 0
        print(request.data)
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        cin = request.POST['cin']
        email = request.POST['email']
        gsm = request.POST['gsm']
        adresse = request.POST['adresse']
        if ClientPhysique.objects.filter(cin=cin).exists():
            erreur=1
            content = {'message': "Ce client existe déjà."}
            return Response(content)
        if erreur == 0:
            cli = ClientPhysique(adresse=adresse, gsm=gsm, nom=nom, prenom=prenom, tel=tel, cin=cin, email=email)
            cli.save()
            return redirect('clients')
    else:
        content = {'message': "permission non accordé"}
        return Response(content)


@login_required(login_url='login')
def clients(request):
    mes_client = ClientPhysique.objects.all()
    context={
        'mes_client': mes_client
    }
    return render(request, 'clients/gestions_clients.html', context)