import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import Group
from rest_framework import (
    status,
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from datetime import datetime


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    phone_number = PhoneNumberField(region="IN")
    user_type = serializers.CharField(write_only=True, required=True)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, default="")
    last_name = serializers.CharField(write_only=True, default="")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password',
                  'email', 'phone_number', 'latitude', 'longitude', 'user_type')

    def validate(self, attrs):
        regex_for_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        regex_for_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        compiled_password = re.compile(regex_for_password)
        pass_regex = re.search(compiled_password, attrs['password'])
        # get_group_list = Group.objects.exclude(name = "Client").values_list("name",flat=True)
        # if attrs['user_type'] in get_group_list:
        if not re.fullmatch(regex_for_email, attrs['email']):
            raise serializers.ValidationError("email address is not valid!")
        if not pass_regex:
            raise serializers.ValidationError(
                {"password": "Password should include a capital letter, a special Integeracter and numbers!"})
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password & Confirm Password do not match!"})
        # else:
        #     raise serializers.ValidationError(
        #             {"user_type": "you have no access to register with other user type!"})
        return attrs

    def create(self, validated_data):
        data = dict()
        # get_uuid = uuid.uuid4()
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        get_user_type = Group.objects.get(name=validated_data['user_type'])
        user.groups.add(get_user_type)
        user.set_password(validated_data['password'])

        user.save()

        return user

    def to_representation(self, instance):
        try:
            data = super(UserRegistrationSerializer,
                         self).to_representation(instance)
            data['status'] = status.HTTP_201_CREATED
            data['success'] = True
            data['username'] = instance.username
            return data

        except Exception as exception:
            print(exception)
            return str(exception)


class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, instance):
        token = super().get_token(instance)
        token['name'] = instance.username
        token['email'] = instance.email
        return token


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(
        # label=_("Password"),
        # style={'input_type': 'password'},
        # trim_whitespace=False,
        max_length=128,
        write_only=False,
        required=True
    )
    user_type = serializers.CharField(max_length=64, required=True)

    class Meta:
        extra_kwargs = {
            "email": {'error_messages': {'blank': 'email field may not be blank'}, "required": True},
            "password": {'error_messages': {'blank': 'password field may not be blank'}, "required": True},
            "user_type": {'error_messages': {'blank': 'user_type field may not be blank'}, "required": True},
        }

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        regex_for_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        regex_for_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        compiled_password = re.compile(regex_for_password)
        pass_regex = re.search(compiled_password, password)
        if email and password:
            if not re.fullmatch(regex_for_email, attrs['email']):
                raise serializers.ValidationError("email address is not valid!")
            if not pass_regex:
                raise serializers.ValidationError(
                    {"password": "Password should include a capital letter, a special Integeracter and numbers!"})
        else:
            raise serializers.ValidationError(
                    {"error": 'Must include "email" and "password".'},code='authorization')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid','username','phone_number','email','city','is_active','date_joined']
    
    def to_representation(self, instance):
        data = super(UserSerializer,self).to_representation(instance)
        data['date_joined'] = datetime.strptime(
            data['date_joined'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%d %B, %Y %I:%M %p")
        return data


class UserStatusUpdateSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['is_active']
        extra_kwargs = {
            "is_active": {"required": True}
        }

        extra_kwargs = {
            "is_active": {'error_messages': {'blank': 'is_active field may not be blank'},"required": True},
        }



    def update(self, instance, validated_data):
        try:
            instance = User.objects.get(
                uid=instance.uid
            )
            instance.is_active = validated_data['is_active']
            instance.save()

        except Exception as exception:
            raise serializers.ValidationError({"error": (str(exception))})
        return instance