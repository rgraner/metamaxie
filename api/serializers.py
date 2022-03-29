from rest_framework import serializers
from scholarships.models import Scholarship
from users.models import Scholar


class ScholarshipModelSerializer(serializers.ModelSerializer):
    ronin = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    last_claim = serializers.SerializerMethodField()
    # scholar = serializers.SerializerMethodField()
    class Meta:
        model = Scholarship
        fields = '__all__'

    def get_ronin(self, obj):
        return obj.ronin.ronin
    
    def get_owner(self, obj):
        return obj.owner.username

    def get_created(self, obj):
        return obj.created.strftime("%d-%m-%Y, %H:%M:%S")
    
    def get_last_claim(self, obj):
        return obj.last_claim.strftime("%d-%m-%Y, %H:%M:%S")

    # def get_scholar(self, obj):
    #     return obj.scholar.username

