from django.test import TestCase
import psycopg2
import pandas as pd
'''
# Create your tests here.
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






def merchant_code(value):
    cursor.execute("SELECT rate FROM merchant_code WHERE %s BETWEEN min_value AND max_value"%(value))
    print((cursor.fetchone()[0]))


def InterchangeRate_Calc(Number):
    Barclays_F = 0
    Elavon_F = 0
    AIB_F = 0 
    TransAmount = df.transaction_amount[Number]
    Region = df.interchange_region[Number]
    temp = [Barclays_F,Elavon_F,AIB_F]
    if TransAmount > 120:
            Barclays_F = TransAmount * 0.0002
            Elavon_F = TransAmount * 0.1005
            AIB_F = TransAmount * 0.00015
    if Region == "Inter":
            Barclays_F =+ 0.35
            Elavon_F =+ 0.40
            AIB_F =+ 0.32
    temp = [[Barclays_F,"Barclays"],[Elavon_F,"Elavon"],[AIB_F,"AIB"]]

    return temp
def Msc_calc(InterRate):
    InterRate[0][0] = InterRate[0][0] + (BScheme_fee + Bmargin)
    InterRate[1][0] = InterRate[1][0] + (EScheme_fee + Emargin)
    InterRate[2][0] = InterRate[2][0] + (AEScheme_fee + Amargin)
    sort = sorted(InterRate)
    sort = sort[0]
    return sort












def calc_visatrans(amount):
    fee= 0
    cap = False # cap tells us what bracket the amount is in

    if amount > 500000 and amount <= 1000000:
        cap = True
        fee += (amount-500000) *0.021
        print(fee)
        amount = 400000 

    if amount > 100000 and amount <= 500000:
        if cap == True:
            fee += amount*0.011
        else:
            cap = True
            fee += (amount-100000)*0.011
            print(fee)
        amount = 95000

    if amount > 5000 and amount <= 100000:
        if cap == True:
            fee += amount * 0.0075
        else:
            cap = True
            fee += (amount-5000)*0.0075
            print(fee)
        amount = 4000

    if amount > 1000 and amount <= 5000:
        if cap == True:
            fee += amount * 0.0035
        else:
            cap = True
            fee += (amount-1000)*0.0035
            print(fee)
        amount = 500

    if amount > 500 and amount <= 1000 or (cap == True):
        if cap == True:
            fee += amount * 0.002
            print(fee)
        else:
            cap = True
            fee += (amount-500)*0.002
            print(fee)
        amount = 450

    if amount > 50 and amount <= 500:
        if cap == True:
            fee += amount * 0.001
            print(fee)
        else:
            cap = True
            fee += (amount-50)*0.001
            print(fee)
        amount = 50

    if amount <= 50:
        fee += amount * 0.0001
        print(fee)

    return fee



merchant_code(8398)
'''


'''import matplotlib.pyplot as plt

# Define time points and corresponding prices
time_points = ['12:00 AM', '12:30 AM', '1:00 AM', '1:03 AM', '1:30 AM', '2:00 AM']
prices = [100, 110, 120, 80, 90, 95]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(time_points, prices, marker='o', color='blue', linestyle='-')

# Highlighting the dramatic drop at 1:03 AM
plt.annotate('Dramatic Drop', xy=(time_points[3], prices[3]), xytext=(time_points[3], prices[3]-10),
             arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=12, color='red')

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Curly Tail Stock Price Over Time')

# Displaying the graph
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()'''
'''# Create your tests here.
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



list = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyrpus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom"]

for i in list:
    cursor.execute(f"INSERT INTO countries(country) VALUES ('{i}')")
    conn.commit()
    print(i,"commited")'''


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


csv_file_path = 'existing_file_with_new_column.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Reference a column by its name
column_data = df['card_type']
column_data1 = df['3ds_secure']
column_data2 = df['cardholder_country']
column_data3 = df['issuer_country']
column_data4 = df['merchant_category_code']
column_data5 = df['transaction_method']
column_data6 = df['Acquirer']

for i in range (len(df)):
    cursor.execute(f"""INSERT INTO trans_records(card_type , secure, cardholder_country, issuer_country, merchant_code, transaction_method, best_acquirer)
                   VALUES ( '{column_data[i]},'{column_data1[i]}','{column_data2[i]}','{column_data3[i]}','{column_data4[i]}','{column_data5[i]}','{column_data6[i]}')""")
    conn.commit()