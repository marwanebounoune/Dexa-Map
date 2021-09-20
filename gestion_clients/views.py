from gestion_clients.serializers import ClientSerializer
from rest_framework.response import Response
from gestion_clients.models import Client
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
@login_required(login_url='login')
def AjouterClient(request):
    if request.method == 'POST':
        erreur = 0
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        cin = request.POST['cin']
        email = request.POST['email']
        if Client.objects.filter(cin=cin).exists():
            erreur=1
            content = {'message': "Ce client existe déjà."}
            return Response(content)
        if erreur == 0:
            cli = Client(nom=nom, prenom=prenom, tel=tel, cin=cin, email=email)
            cli.save()
            serializer = ClientSerializer(cli, many=False)
            return Response(serializer.data)
    else:
        content = {'message': "permission non accordé"}
        return Response(content)


@login_required(login_url='login')
def clients(request):
    mes_client = Client.objects.all()
    context={
        'mes_client': mes_client
    }
    return render(request, 'clients/gestions_clients.html', context)