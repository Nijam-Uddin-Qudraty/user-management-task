from rest_framework import serializers
from django.contrib.auth.models import User



from django.contrib.auth.models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Include all fields
        fields = "__all__"
        # Make sensitive fields read-only for normal users
        read_only_fields = [
            "id",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
            "password"  # password should never be updated here
        ]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserRegSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs={
            'password':{'write_only':True},
            'first_name':{'required':False},
            'last_name':{'required':False},
        }

    def create(self,validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
                raise serializers.ValidationError({"password":"Password fields didn't match."})
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email":"Email already exists."})
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],  
            password=validated_data["password"],
            is_active=False
        )
        return user