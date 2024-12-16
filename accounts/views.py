import csv
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer, CsvFileSerializer, TransferFundsSerializer
from io import TextIOWrapper
from rest_framework.parsers import (MultiPartParser, FormParser)
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal, InvalidOperation

class ImportAccountsView(APIView):

    serializer_class = CsvFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):

        if request.FILES.get('csv_file'):
        
            csv_file = request.FILES['csv_file']
        
            try:
                csv_decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_data = csv.reader(csv_decoded_file)

                next(csv_data, None)
                
                for row in csv_data:
                    if len(row) >= 3: 
                        Account.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            balance=row[2]
                        )

                return Response({"message": "Accounts imported successfully!"}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({"error": f"Failed to process the file. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "No file uploaded or invalid request."}, status=status.HTTP_400_BAD_REQUEST)


class AccountManagementViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'transfer_funds':
            return TransferFundsSerializer
        else :
            return AccountSerializer



    def list(self, request, *args, **kwargs):
        queryset = Account.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    def retrieve(self, request, pk=None):
        try:
            account = get_object_or_404(Account, pk=pk)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Http404:
            return Response(
                {'error': "The requested Space does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )



    @action(detail=False, methods=['post'])
    def transfer_funds(self, request, *args, **kwargs):

        from_account = Account.objects.get(id=request.data['from_account_id'])
        to_account = Account.objects.get(id=request.data['to_account_id'])
        amount = request.data['amount']

        try:
            if Decimal(from_account.balance) < Decimal(amount):
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                from_account.balance -= Decimal(amount)
                to_account.balance += Decimal(amount)
                from_account.save()
                to_account.save()

            return Response({"message": "Transfer successful!"})
        
        except (Account.DoesNotExist, InvalidOperation) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
