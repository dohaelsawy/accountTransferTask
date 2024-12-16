from django.forms import FileField
from rest_framework import serializers
from .models import Account
from rest_framework.serializers import Serializer, FileField, IntegerField, UUIDField



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance']



class CsvFileSerializer(Serializer):
    csv_file = FileField()
    class Meta:
        csv_file = ['csv_file']


class TransferFundsSerializer(Serializer):
    from_account_id = UUIDField()
    to_account_id = UUIDField()
    amount = IntegerField()
    class Meta:
        csv_file = ['from_account_id', 'to_account_id', 'amount']