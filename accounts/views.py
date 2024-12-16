import csv
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer, CsvFileSerializer
from io import TextIOWrapper
from rest_framework.parsers import (MultiPartParser, FormParser)
from rest_framework.decorators import action


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


class AccountManagement(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
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
        
   