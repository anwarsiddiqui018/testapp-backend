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
import sqlite3
import json

@csrf_exempt
def handleDBUpload(request):
    # print("Reached Upload area")
    if request.method == 'POST' and request.FILES.get('csvFile'):
        uploaded_file = request.FILES['csvFile']
        df = pd.read_csv(uploaded_file)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        # print("Recived Dataframe goes like this \n",df.tail())
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
        # print(request.FILES['csvFile'])
        response = {'error': 'Invalid request'}
        return JsonResponse(response, status=400)
    
@csrf_exempt
def handlegetData(request):
    # print("up")
    if request.method == 'GET':
            # print("here")
            try:
                database_path = r'C:\Users\siddi\Desktop\testApp\myproject\db.sqlite3'
                # Connect to the SQLite database
                conn = sqlite3.connect(database_path)
                # print("Connection Successful")
                # Query data from the database
                df = pd.read_sql_query("SELECT * FROM myapp_stockfuturesmodel", conn)
                # print(df)
                # Convert the DataFrame to a list of dictionaries
                data = json.loads(df.to_json(orient='records'))
                # print(data)
                # Close the database connection
                conn.close()
                # Return the data as a JSON response
                return JsonResponse(data, safe=False)
                
            except IntegrityError as e:
                print("Error occurred while saving row to db", e)
    else:
        print(request.FILES['csvFile'])
        response = {'error': 'Invalid request'}
        return JsonResponse(response, status=400)