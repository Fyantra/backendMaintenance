from rest_framework import serializers
from .models import Endroit, Responsable, Atelier, Chaine

class EndroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endroit
        fields = '__all__'


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'


class AtelierSerializer(serializers.ModelSerializer):
    
    endroit_id = serializers.PrimaryKeyRelatedField(queryset=Endroit.objects.all(), source='endroit', write_only=True)
    responsable_id = serializers.PrimaryKeyRelatedField(queryset=Responsable.objects.all(), source='responsable', write_only=True)
    
    class Meta:
        model = Atelier
        fields = '__all__'


class ChaineSerializer(serializers.ModelSerializer):
    
    atelier_id = serializers.PrimaryKeyRelatedField(queryset=Atelier.objects.all(), source='atelier', write_only=True)
    
    class Meta:
        model = Chaine
        fields = '__all__'
