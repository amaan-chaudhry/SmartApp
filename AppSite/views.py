import json
from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
import pandas as pd
from pandas import DataFrame
from django.views.generic import View 
from rest_framework.views import APIView 
from rest_framework.response import Response
import psycopg2
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import joblib
from django.http import JsonResponse
import io
from .models import UserDetails
from django.contrib.auth import authenticate, login








host = "smartappazure.postgres.database.azure.com"
dbname = "smartappdatabase"
user = "Amaan"
password = "Goldenmile*!"
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connection established")


def dashboard(request):
    return render(request, "AppSite/dashboard.html")

# --------------- Buttons on home page ---------- #
def contact(request):
    return render(request, "AppSite/contactus.html")
def features(request):
    return render(request, "AppSite/features.html")
def security(request):
    return render(request, "AppSite/security.html")
def about(request):
    return render(request, "AppSite/about.html")
def oursolution(request):
    return render(request, "AppSite/oursolution.html")
# ------------------------------------------------- # 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = UserDetails(
                first_name=form.cleaned_data['fname'],
                last_name=form.cleaned_data['lname'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()  # uploads to the database
            return redirect('home') 
    else:
        form = RegistrationForm()
    return render(request, 'Appsite/register.html', {'form': form})



def authenicate_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(type(email)) 
        print((type(password)))
        cursor.execute(f'''SELECT * FROM public."AppSite_userdetails" WHERE email = '{email}' and password = '{password}' ''')
        if cursor.fetchone():
            print("worked")
            return redirect('/dashboard')
        else:
            print("hello")
    return redirect('/')

def hello(request):
    #hello
    return render(request, "AppSite/hello.html")

def process_csv(request):
    if request.method == 'POST':
        selected_row =   request.POST.get('selected_row')
        selected_row = eval(selected_row)
        print(type(selected_row))
        card_type = selected_row[0]
        secure = selected_row[1]
        cardholder = selected_row[2]
        region = selected_row[4]
        cur1 = selected_row[5]
        cur2 = selected_row[6]
        merchant = selected_row[7]
        print(merchant)
        method = selected_row[8]
        TransAmount = float(selected_row[9])
    
        labels = ['AIB', 'Evalon', 'Barclays']

        EveryRecord = []

        marginfee = margin(TransAmount)
        InterRate = CardType_fee(TransAmount,region,card_type,cardholder,method,secure) +  merchant_fee(TransAmount,merchant) + currency_fee(TransAmount,cur1,cur2)
        cursor.execute(f"""SELECT scheme_fee
                    FROM account_types 
                    WHERE product = '{card_type}'""")
        Scheme_fee = cursor.fetchone()[0] * TransAmount
        Scheme_fee = round(Scheme_fee, 2)
        dataset3 = [round(marginfee[0][0], 2), round(marginfee[1][0], 2), round(marginfee[2][0], 2)]# Margin
        dataset1 = [InterRate, InterRate, InterRate]  # Interchange Rate
        dataset2 = [Scheme_fee, Scheme_fee, Scheme_fee]  # Scheme Fee  
        marginfee.sort()
        TotalFee = round(marginfee[0][0], 2) + round(InterRate, 2) + round(Scheme_fee, 2)
        EveryRecord.append([dataset1,dataset2,dataset3]) 

        context = {
            'labels': json.dumps(labels),
            'dataset1': json.dumps(dataset1),
            'dataset2': json.dumps(dataset2),
            'dataset3': json.dumps(dataset3),
            'AIB': dataset3[0],
            'Eva': dataset3[1],
            'Barc': dataset3[2],
            'lowest': marginfee[0][1],
            'TotalFee': round(TotalFee,4),
        }
            # Return the processed data as JSON
        return JsonResponse({'result': context})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def home(request):
    
    return render(request, "AppSite/home.html")
 

def merchant_fee(amount,merchant):
    cursor.execute(f"SELECT rate FROM merchant_code WHERE {merchant} BETWEEN min_value AND max_value")
    value = (cursor.fetchone()[0]) * amount

    return value


def currency_fee(amount,currency1,currency2):
    if currency1 == currency2:
        cursor.execute(f"SELECT rate FROM international_code WHERE code = '{currency1}'")
        value = cursor.fetchone()[0]
        fee = value * amount
    else:
        cursor.execute(f"SELECT rate FROM international_code WHERE code = '{currency1}' OR code = '{currency2}'")
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


def CardType_fee(TransAmount,region,card_type,cardholder,method,secure):
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
        
def Ai_gather(request):
    if request == 'POST':
        file = request.FILES['csvfile']
        cursor.execute(f"""SELECT card_type, 3ds_secure, cardholder_country, issuer_country, transaction_method, Acquirer 
                           FROM trans_records""")
        df = DataFrame(cursor.fetchall())
        df.columns=[ x.name for x in cursor.description ]
        if str(file).endswith('.xlsx'):
            df = pd.read_excel(file) # if file is xlsx
        else:
            df = pd.read_csv(file) # if the file is a csv
        
        label_encoders = {}
        columns = ['card_type', '3ds_secure', 'cardholder_country', 'issuer_country', 'transaction_method'] # setting the readable columns
        for feature in columns: # going through each column
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            label_encoders[feature] = le
            joblib.dump(le, f'{feature}_encoder.pkl')  # encoder might be used later down the code

        le_Acquirer = LabelEncoder()
        df['Acquirer'] = le_Acquirer.fit_transform(df['Acquirer']) # The Acquirer is what we want the AI to predict, so we're encoding it for the test data
        label_encoders['Acquirer'] = le_Acquirer
        joblib.dump(le_Acquirer, 'Acquirer_encoder.pkl')  

        
        X = df.drop('Acquirer', axis=1) # so here im splitting the file into test data and demo data
        y = df['Acquirer']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 20% of the file will be test data
                                                                                                  # 80% will be to predict the rest
        # Define your model
        model = Sequential()
        model.add(Dense(32, input_dim=len(X.columns), activation='relu')) # using the relu, which basically tells the AI how to deal with the outcome of the prediction
        model.add(Dense(16, activation='relu'))
        model.add(Dense(1, activation='sigmoid')) # this allows the AI to interpret its findings. it ranks it between 0-1

        # Compile your model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) # this allows the AI to know how accurate its prediction was with its current approach
                                                                                          # and how much data was lost with its current approach, this was done through an optimizer
                                                                                          # called adam
        # Train your model
        model.fit(X_train, y_train, epochs=15, batch_size=32) # each epoch allows the AI to adapted its approach, Usually after 8 epochs its approach is 100% accuracy but to be
                                                              # safe I used 15

        _, accuracy = model.evaluate(X_test, y_test) #shows the accuracy and loss of each epoch
        print('Accuracy: %.2f' % (accuracy*100))  #prints them

        # Predict on new data
        new_data = pd.read_csv('existing_file_with_new_column.csv') # user inputted file

        # Load the saved encoders
        label_encoders = {}
        for feature in columns + ['Acquirer']:
            label_encoders[feature] = joblib.load(f'{feature}_encoder.pkl')

        # Apply label encoding using the loaded encoders
        for feature in columns:
            new_data[feature] = label_encoders[feature].transform(new_data[feature])

        # Predict on new data
        predictions = model.predict(new_data.drop('Acquirer', axis=1))

        for i in predictions:  # because the list is between 0 and 1s
            if 0 in i:         # im converting them back into the string values
                print("AIB")
            else:
                print("Evalon")

class HomeView(View): 
    def get(self, request, *args, **kwargs): 
        return render(request, 'AppSite/dashboard.html') 


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
    

def Ai_interface(request):
    if request.method == 'POST':

        df = pd.read_csv('existing_file_with_new_column.csv')


        label_encoders = {}
        columns = ['card_type', '3ds_secure', 'cardholder_country', 'issuer_country', 'transaction_method']
        for feature in columns:
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            label_encoders[feature] = le
            joblib.dump(le, f'{feature}_encoder.pkl')


        le_Acquirer = LabelEncoder()
        df['Acquirer'] = le_Acquirer.fit_transform(df['Acquirer'])
        label_encoders['Acquirer'] = le_Acquirer
        joblib.dump(le_Acquirer, 'Acquirer_encoder.pkl')

 
        X = df.drop('Acquirer', axis=1)
        y = df['Acquirer']


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        num_classes = len(df['Acquirer'].unique())  
        y_train_one_hot = to_categorical(y_train, num_classes=num_classes)
        y_test_one_hot = to_categorical(y_test, num_classes=num_classes)


        model = Sequential()
        model.add(Dense(32, input_dim=len(X.columns), activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))  


        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

 
        model.fit(X_train, y_train_one_hot, epochs=15, batch_size=32)


        _, accuracy = model.evaluate(X_test, y_test_one_hot)
        print('Accuracy: %.2f' % (accuracy * 100))

        new_data = pd.read_csv('existing_file_with_new_column.csv')

 
        for feature in columns:
            new_data[feature] = label_encoders[feature].transform(new_data[feature])


        predictions = model.predict(new_data.drop('Acquirer', axis=1))

        predicted_classes = le_Acquirer.inverse_transform(predictions.argmax(axis=1))

        print("Predicted classes:", predicted_classes)
        df = pd.read_csv('existing_file_with_new_column.csv')
        df['Best_Acquirer'] = predicted_classes
        print(df)
        updated = df.to_csv(index=False)
        response = HttpResponse(updated, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="downloaded_file.csv"'
        return response

    return render(request, 'AppSite/AI_Page.html') 






