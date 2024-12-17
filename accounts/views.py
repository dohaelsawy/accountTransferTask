import csv
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer, CsvFileSerializer, TransferFundsSerializer
from io import TextIOWrapper
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal, InvalidOperation
from drf_spectacular.utils import extend_schema




class AccountManagementViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'transfer_funds':
            return TransferFundsSerializer
        if self.action == 'import_accounts':
            return CsvFileSerializer
        else :
            return AccountSerializer
        

    @action(detail=False, methods=['post'],)
    def import_accounts(self, request, *args, **kwargs):
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
                            defaults={
                                'name': row[1],
                                'balance': row[2],
                            }
                        )

                return Response({"message": "Accounts imported successfully!"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": f"Failed to process the file. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "No file uploaded or invalid request."}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = Account.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def retrieve(self, request, pk=None):
        try:
            account = get_object_or_404(Account, pk=pk)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

            return Response({"message": "Transfer successful!"}, status=status.HTTP_200_OK)
        
        except (Account.DoesNotExist, InvalidOperation) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response(
            {'error': 'create is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Update is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'update is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'delete is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    