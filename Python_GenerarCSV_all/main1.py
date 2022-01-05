
from datetime import datetime
from datetime import date
import dateutil.parser
from punto import Punto
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import requests as req
import json
import statistics



print("SOLICITANDO INFORMACION DE INTERNET")
print("espere....") 
URL = 'https://apptaxis2.azurewebsites.net/Carrera' #configuramos la url
#solicitamos la información y guardamos la respuesta en data.
data = req.get(URL) 
data = data.json() #convertimos la respuesta en dict
id=0
d=date;
day=0
cont=1;
lat=[]
lng=[]
ides=[]
dates=[]
day=[]
kilometros=[]
velocidad=[]
tiempo=[]
costo=[]
#f----------------------------------------------------------------------------------------


  
def transHoras(tiempo):
    arrtiemp=tiempo.split(sep=':')
    return float(arrtiemp[0])+(float(arrtiemp[1])/60)+(float(arrtiemp[2])/3600)    
       
	
#---------------------------------------------------------------
for element in data:
    id=id+1
    if element['kilometro']!=0:
      
       velocidades=[]

       for velo in element['carrera']:
               velocidades.append(velo['speed']) 
       if statistics.mean(velocidades)!=0:   
         ides.append(id)          
         velocidad.append(round(statistics.mean(velocidades),3))
         lat.append(element['carrera'][0]['latitud'])
         lng.append(element['carrera'][0]['longitud'])   
         dates.append(element['createAt'])       
         yourdate = dateutil.parser.parse(element['createAt'])
         day.append(yourdate.isoweekday())       
         kilometros.append(round(element['kilometro'],3)) 
         tiempo.append(round(transHoras(element['tiempo']),3))
         costo.append(element['costo'])
         #tiempo.append(element['kilometro']/statistics.mean(velocidades));

 
	
dict = {'id': ides, 'latitud': lat, 'longitud': lng, 'dia':day, 'date':dates, 'kilometro': kilometros, 'velocidad':velocidad,'tiempo':tiempo,'costo':costo} 
df = pd.DataFrame(dict) 
df.to_csv('testGeneral.csv')
