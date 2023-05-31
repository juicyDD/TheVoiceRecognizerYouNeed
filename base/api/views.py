from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/embedding',
        'GET /api/features-extraction',
        'GET /api/models'
    ]
    return Response(routes)