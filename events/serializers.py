from django.contrib.auth.models import User
from rest_framework import serializers

from events.models import Event
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Event model.

    This serializer is used to convert Event model instances into JSON
    representation and vice versa. It also provides validation for the
    fields of the Event model.

    Methods:
        validate: Validates the start_date and end_date fields of the event checking
        if the end_date is before the start_date.
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    attendees = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'end_date',
                  'description', 'attendees', 'owner', 'capacity')

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError(
                "End date must be after start date.")
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer class for user registration.

    This serializer is used to convert User model instances into JSON
    representation and vice versa. It provides validation for the fields
    required for user registration.

    Methods:
        validate: Validates the password and password2 fields by checking if they match.
        create: Creates a new user instance.
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrides the get_token method to include the username in the token payload.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token
