import json
from django.shortcuts import render
from .forms import RegistrationForm
import pandas as pd
from django.views.generic import View 
from rest_framework.views import APIView 
from rest_framework.response import Response
import psycopg2
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import joblib
from django.http import JsonResponse
import io
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

def process_csv(request):
    if request.method == 'POST':
        selected_row =  request.POST.get('selected_row')
        print(selected_row)
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
    cursor.execute("SELECT rate FROM merchant_code WHERE %s BETWEEN min_value AND max_value"%(merchant))
    value = (cursor.fetchone()[0]) * amount

    return value


def currency_fee(amount,currency1,currency2):
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

        le_aquirier = LabelEncoder()
        df['Aquirier'] = le_aquirier.fit_transform(df['Aquirier']) # The aquirier is what we want the AI to predict, so we're encoding it for the test data
        label_encoders['Aquirier'] = le_aquirier
        joblib.dump(le_aquirier, 'aquirier_encoder.pkl')  

        
        X = df.drop('Aquirier', axis=1) # so here im splitting the file into test data and demo data
        y = df['Aquirier']
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
        for feature in columns + ['Aquirier']:
            label_encoders[feature] = joblib.load(f'{feature}_encoder.pkl')

        # Apply label encoding using the loaded encoders
        for feature in columns:
            new_data[feature] = label_encoders[feature].transform(new_data[feature])

        # Predict on new data
        predictions = model.predict(new_data.drop('Aquirier', axis=1))

        for i in predictions:  # because the list is between 0 and 1s
            if 0 in i:         # im converting them back into the string values
                print("AIB")
            else:
                print("Evalon")

