from django.shortcuts import render
from rest_framework import generics
from .models import StockFuturesModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# from .models import UploadedFile
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

@csrf_exempt
def handleDBUpload(request):
    # print("Reached Upload area")
    if request.method == 'POST' and request.FILES.get('csvFile'):
        uploaded_file = request.FILES['csvFile']
        df = pd.read_csv(uploaded_file)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        print("Recived Dataframe goes like this \n",df.tail())
        for index, row in df.iterrows():
            if row['SYMBOL'] == '':
                continue
            try:        # hdr = ['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'OPEN_INT', 'CHG_IN_OI', 'TIMESTAMP']
                obj = StockFuturesModel.objects.create(
                SYMBOL= row['SYMBOL'],
                OPEN = row['OPEN'],
                HIGH = row['HIGH'],
                LOW = row['LOW'],
                CLOSE = row['CLOSE'],
                VOLUME = row['CONTRACTS'],
                OPEN_INT = row['OPEN_INT'],
                CHG_IN_OI = row['CHG_IN_OI'],   
                TIMESTAMP = row['TIMESTAMP'],
                )
                obj.save()
            except IntegrityError as e:
                print("Error occurred while saving row to db", row['Issue key'], e)

        response = {"result": "Saved to DB"}
        return JsonResponse(response)
    else:
        response = {'error': 'Invalid request'}
        return JsonResponse(response, status=400)