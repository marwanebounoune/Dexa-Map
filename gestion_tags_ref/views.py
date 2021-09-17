from api_map.serializers import TagsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from api_map.models import  Tags
import logging

#recupération des tags
@api_view(['GET'])
@login_required(login_url='login')
def getTags(request):
    try:
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
