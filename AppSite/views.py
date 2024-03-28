from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd

region_fee = 0
BScheme_fee = 0.8
Bmargin = 0.14
EScheme_fee = 0.21
Emargin = 0.11
AEScheme_fee = 0.15
Amargin = 0.5



def home(request):
    global df
    #if request.method == 'POST':
    #ButtonPress()
    df = pd.read_csv('Barclays Settlement File Example.csv')
    for i in range (len(df)):
        Rate = InterchangeRate_Calc(i)
        #print(Msc_calc(Rate))
    return render(request, "AppSite/home.html")
 
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