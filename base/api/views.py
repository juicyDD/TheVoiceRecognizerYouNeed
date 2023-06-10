from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random, os
import pandas as pd
from base.api.voice_recognizer import my_neural_network, features_extraction, nhi_config, inference


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/embedding',
        'GET /api/features-extraction',
        'GET /api/models'
    ]
    return Response(routes)

@api_view(["POST"])
def getSpeakerEmbedding(request):
    audio_file = request.FILES["file"]
    features = features_extraction.extract_mfcc(audio_file)
    encoder = my_neural_network.get_speaker_encoder(nhi_config.SAVED_MODEL_PATH)
    embedding = inference.my_inference(features, encoder)
    print(embedding)
    result = pd.Series(embedding).to_json(orient='values')
    data = {"embeddings":result}
    return Response(data)