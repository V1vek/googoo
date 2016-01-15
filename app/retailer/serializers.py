import logging

from rest_framework import serializers

from app.retailer.models import Retailer
from app.accounts.models import User

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class RetailerSerializer(serializers.ModelSerializer):
    # profile_id = serializers.IntegerField(source='profile.id ')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='profile.username')
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    company_name = serializers.CharField(allow_null=False, required=True, allow_blank=True)
    address1 = serializers.CharField(allow_null=True, required=False, allow_blank=True)

    class Meta:
        model = Retailer
        fields = ('id', 'username', 'first_name', 'last_name', 'company_name',
                  'contact_number', 'email', 'address', 'address1', 'state', 'city', 'zip_code')

    def update(self, instance, validated_data):
        # user = User.objects.get(pk = instance.user.pk);

        user = instance.profile
        user.first_name = validated_data.get('user.first_name', user.first_name)
        user.last_name = validated_data.get('user.last_name', user.last_name)
        user.save()

        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)

        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)

        instance.save()

        return instance

    def create(self, validated_data):
        log.info(validated_data)

        user_data = validated_data.pop('profile')
        user = User.objects.update_user_details(**user_data)

        if user is not None:
            log.info(user)
            profile = Retailer.objects.create(profile=user, **validated_data)
            return profile


