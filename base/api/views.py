from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView

from django.contrib.auth.models import User
from django.contrib.auth import login
import random, os
import pandas as pd
from base.api.voice_recognizer import my_neural_network_new, features_extraction, nhi_config, inference
from base.models import UserToken
from knox.models import AuthToken 

from .serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer
from knox import views as knox_views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = [
        'GET /api/embedding',
        'GET /api/features-extraction',
        'GET /api/models'
    ]
    return Response(routes)

@api_view(['GET'])
def getModels(request):
    models = {
        "models":[
        'jennie',
        'jisoo',
        'lisa',
        'rose',
        'momo',
        'tzuyu',
            ],
    }
    return Response(models)
# @api_view(["POST"])
# # @permission_classes(IsAuthenticated)
# def getSpeakerEmbedding(request):
#     audio_file = request.FILES["file"]
#     features = features_extraction.extract_mfcc(audio_file)
#     encoder = my_neural_network.get_speaker_encoder(nhi_config.SAVED_MODEL_PATH)
#     embedding = inference.my_inference(features, encoder)
#     print(embedding)
#     result = pd.Series(embedding).to_json(orient='values')
#     data = {"embeddings":result}
#     return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getSpeakerEmbedding(request):
    audio_file = request.FILES["file"]
    
    model_name = request.POST["model_name"]
    if model_name not in nhi_config.MODEL_DICT:
        return Response({
            "message":"Invalid model name"
        })
    features = features_extraction.extract_mfcc(audio_file)
    encoder = my_neural_network_new.get_speaker_encoder(model_name)
    embedding = inference.my_inference(features, encoder)
    print(embedding)
    result = pd.Series(embedding).to_json(orient='values')
    data = {"embeddings":result}
    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getSimilarityOfVoices(request):
    file_1 = request.FILES["file_1"]
    file_2 = request.FILES["file_2"]
    
    model_name = request.POST["model_name"]
    if model_name not in nhi_config.MODEL_DICT:
        return Response({
            "message":"Invalid model name"
        })
    encoder = my_neural_network_new.get_speaker_encoder(model_name)
    
    features_1 = features_extraction.extract_mfcc(file_1)
    embedding_1 = inference.my_inference(features_1, encoder)
    
    features_2 = features_extraction.extract_mfcc(file_2)
    embedding_2 = inference.my_inference(features_2, encoder)
    
    cos_similarity = features_extraction.cosine_similarity(embedding_1, embedding_2)
    same_speaker = True if cos_similarity > nhi_config.MODEL_DICT[model_name]['eer_thres'] else False
    print(embedding_1, embedding_2)
    data = {
        "embedding_1": pd.Series(embedding_1).to_json(orient = 'values'),
        "embedding_2": pd.Series(embedding_2).to_json(orient = 'values'),
        "cosine_similarity" : cos_similarity,
        "same_speaker": str(same_speaker)
    }
    return Response(data)
    # return Response({})
class CreateUserAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny)

class UpdateUserAPI(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            # response = super().post(request, format=None)
            instance, token=AuthToken.objects.create(request.user)
            
            abb = token[:4] +"..." + token[-4:]
            expiry = self.format_expiry_datetime(instance.expiry)
            
            UserToken.objects.create(
                token_key = instance.token_key,
                email = user.email,
                abbreviation = abb,
                expiry = expiry
            )
            data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
            }
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data,status=status.HTTP_200_OK) #response.data