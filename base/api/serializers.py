from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password':{'required':True}}
        
    def validate(self, attrs):
        email = attrs.get('email','').strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','gender')
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username').lower()
        password = attrs.get('password')
        if not username or not password:
            raise serializers.ValidationError("Please give both username and password.")

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('username does not exist.')

        user = authenticate(request=self.context.get('request'), username=username,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs
    