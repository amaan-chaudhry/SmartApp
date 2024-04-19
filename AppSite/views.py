from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django_recaptcha.fields import ReCaptchaField
import json
from django.shortcuts import render
from .forms import RegistrationForm
import pandas as pd
from django.views.generic import View 
from rest_framework.views import APIView 
from rest_framework.response import Response
import psycopg2
import io
host = "smartpathazure.postgres.database.azure.com"
dbname = "smartpath"
user = "Amaan"
password = "Goldenmile*!"
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connection established")


def dashboard(request):
    optionlist = []
    total = 0
    TotalFee = 0
    marginfee = [[0,"None"]]
    labels = ['AIB', 'Evalon', 'Barclays']
    dataset1 = [0, 0, 0]  # Interchange Rate
    dataset2 = [0, 0, 0]  # Scheme Fee
    dataset3 = [0, 0, 0]  # Margin 
    if request.method == "POST":
        global df
        global file
        file = request.FILES['csvfile']
        EveryRecord = []
        if str(file).endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        total = len(df)
        dropdown = request.POST.get("optionsdropdown")
        i  = int(dropdown[-1]) 
        TransAmount = df.transaction_amount[i]
        card_type = df.card_type[i]
        cur1 = df.currency1[i]
        cur2 = df.currency2[i]
        merchant = df.merchant_category_code[i]
        
        region = df.interchange_region[i]
        card_type = df.card_type[i]
        issuer = df.issuer_country[i]
        cardholder = df.cardholder_country[i]
        method = df.transaction_method[i]
        secure = df.iloc[i]['3ds_secure']
        optionlist.append(f"option {i+1}")


        marginfee = margin(TransAmount)
        InterRate = CardType_fee(i,TransAmount)
        cursor.execute(f"""SELECT scheme_fee
                    FROM account_types
                    WHERE product = '{card_type}'""")
        Scheme_fee = cursor.fetchone()[0] * TransAmount
        Scheme_fee = round(Scheme_fee, 2)
        dataset3 = [round(marginfee[0][0], 2), round(marginfee[1][0], 2), round(marginfee[2][0], 2)]
        dataset1 = [InterRate, InterRate, InterRate]  # Interchange Rate
        dataset2 = [Scheme_fee, Scheme_fee, Scheme_fee]  # Scheme Fee  # Margin
        marginfee.sort()
        TotalFee = round(marginfee[0][0], 2) + round(InterRate, 2) + round(Scheme_fee, 2)
        EveryRecord.append([dataset1,dataset2,dataset3]) 

        context = {
            'labels': json.dumps(labels),
            'dataset1': json.dumps(dataset1),
            'dataset2': json.dumps(dataset2),
            'dataset3': json.dumps(dataset3),
            'Total': total,
            'AIB': dataset3[0],
            'Eva': dataset3[1],
            'Barc': dataset3[2],
            'lowest': marginfee[0][1],
            'TotalFee': round(TotalFee,4),
            'Card_type': card_type,
            'secure': secure,
            'ch_country': cardholder,
            'is_country': issuer,
            'merchant_code': merchant,
            'transmethod': method,
            'Amount': TransAmount,
            'options': optionlist,



        }
        return render(request, "AppSite/dashboard.html",context)
    else:
        return render(request, "AppSite/dashboard.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data
            # For example, you can save the user's registration information to the database
            # Redirect to a success page or perform any other necessary action
            return render(request, 'AppSite/register.html')
    else:
        form = RegistrationForm()
    return render(request, 'AppSite/register.html', {'form': form})




def hello(request):
    #hello
    return render(request, "AppSite/hello.html")

def home(request):
    
    return render(request, "AppSite/home.html")
 

def merchant_fee(number,amount):
    merchant = df.merchant_category_code[number]
    cursor.execute("SELECT rate FROM merchant_code WHERE %s BETWEEN min_value AND max_value"%(merchant))
    value = (cursor.fetchone()[0]) * amount

    return value


def currency_fee(number,amount):
    currency1 = df.currency1[number]
    currency2 = df.currency2[number]
    if currency1 == currency2:
        cursor.execute("SELECT rate FROM international_code WHERE code = '%s'"%(currency1))
        value = cursor.fetchone()[0]
        fee = value * amount
    else:
        cursor.execute("SELECT rate FROM international_code WHERE code = '%s' OR code = '%s'"%(currency1,currency2))
        rates = cursor.fetchall()
        rates = [r for r, in rates]
        fee = (rates[0] + rates[1]) * amount
    return fee

def transaction_fee(amount):
    if amount > 500000 and amount <= 1000000:
        fee = amount *0.021
    if amount > 100000 and amount <= 500000:
        fee = amount*0.011
    if amount > 10000 and amount <= 100000:
        fee = amount* 0.0075
    if amount > 5000 and amount <= 10000:
        fee = amount* 0.005
    if amount > 1000 and amount <= 5000:
        fee = amount * 0.0035
    if amount > 1000 and amount <= 5000:
        fee = amount * 0.0035
    if amount > 500 and amount <= 1000:
        fee = amount * 0.002
    if amount > 50 and amount <= 500:
        fee = amount * 0.0010
    if amount <= 50:
        fee = amount * 0.0001

    return fee

def margin(amount):
    if amount > 500000 and amount <= 1000000:
        Barc = (amount*0.0065) +130
        eva = (amount*0.008) +100
        aib = (amount*0.0065) +90
    if amount > 100000 and amount <= 500000:
        Barc = (amount*0.009) +60
        eva = (amount*0.0095) +40
        aib = (amount*0.009) +30
    if amount > 10000 and amount <= 100000:
        Barc = (amount*0.011) +25
        eva = (amount*0.0105) +20
        aib = (amount*0.011) +15
    if amount > 5000 and amount <= 10000:
        Barc = (amount*0.0135) +5.5
        eva = (amount*0.0133) +5
        aib = (amount*0.0135) +3.75
    if amount > 1000 and amount <= 5000:
        Barc = (amount*0.015) +2.75
        eva = (amount*0.0155) +2.75
        aib = (amount*0.015) +2
    if amount > 500 and amount <= 1000:
        Barc = (amount*0.0165) +0.55
        eva = (amount*0.017) +0.45
        aib = (amount*0.0165) +0.5
    if amount > 50 and amount <= 500:
        Barc = (amount*0.0185) +0.45
        eva = (amount*0.019) +0.3
        aib = (amount*0.0185) +0.25
    if amount <= 50:
        Barc = (amount*0.025) +0.3
        eva = (amount*0.0225) +0.2
        aib = (amount*0.02) +0.1
    fee = [[aib,"AIB"],[eva,"Evalon"],[Barc,"Barclays"]]
    return fee


def CardType_fee(Number,TransAmount):
    region = df.interchange_region[Number]
    card_type = df.card_type[Number]
    issuer = df.issuer_country[Number]
    cardholder = df.cardholder_country[Number]
    method = df.transaction_method[Number]
    secure = df.iloc[Number]['3ds_secure']


    cursor.execute(f"""
        SELECT state_3, state_4, rate
        FROM (
            SELECT *, s1.state AS state_3, s2.state AS state_4
            FROM domestic
            LEFT JOIN security s1 ON domestic.method = s1.id 
            LEFT JOIN security s2 ON domestic.secure = s2.id
            LEFT JOIN countries ON countries.cid = domestic.cid
            INNER JOIN account_types ON domestic.pid = account_types.pid 
            WHERE (countries.country = '{cardholder}' or countries.country is NULL) and account_types.product = '{card_type}' and
            (s1.state = '{method}' or s1.state is NULL) and (s2.state = '{secure}' or s2.state is NULL or s2.state = 'Both')and
            (location = '{region}' or location is NULL)
        ) AS subquery;
    """)
    list = cursor.fetchone()
    fee = 0
    if not(list is None):
        fee += list[2]
        if list[0] is None:
            cursor.execute(f"""
                                SELECT fee
                                FROM security
                                WHERE state = '{method}'
                                """)
            fee += cursor.fetchone()[0]   
        if list[1] is None:
            cursor.execute(f"""
                            SELECT fee
                            FROM security
                            WHERE state = '{secure}'
                            """)
            fee += cursor.fetchone()[0]
    else:
        cursor.execute(f"""
                        SELECT fee
                        FROM security
                        WHERE state = '{secure}' or state = '{method}'
                        
                        UNION
                        
                        SELECT scheme_fee
                        FROM account_types
                        WHERE product = '{card_type}'
                        """)
        fee = cursor.fetchall()
        fee =[r for r, in fee]
        fee = fee[0]+fee[1]+fee[2]
    
    fee = fee * TransAmount
    
    return fee
        



















































class HomeView(View): 
    def get(self, request, *args, **kwargs): 
        return render(request, 'AppSite/login.html') 
   
   
class ChartData(APIView): 
    authentication_classes = [] 
    permission_classes = [] 
   
    def get(self, request, format = None): 
        labels = [ 
            'January', 
            'February',  
            'March',  
            'April',  
            'May',  
            'June',  
            'July'
            ] 
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45] 
        data ={ 
                     "labels":labels, 
                     "chartLabel":chartLabel, 
                     "chartdata":chartdata, 
             } 
        return Response(data) 