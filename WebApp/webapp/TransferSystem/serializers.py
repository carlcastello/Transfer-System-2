from rest_framework import serializers, permissions
from .models import Article, Transfer
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'description',
            'price'
        )

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = (
            'location',
            'quantity',
        )    

    def create(self):
        article = self.context.get('article')
        user = self.context.get('user')
        location = self.validated_data.get('location')
        quantity = self.validated_data.get('quantity')

        return Transfer.objects.create(article = article, user = user, location = location, quantity = quantity)

