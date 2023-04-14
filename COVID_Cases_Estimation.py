# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 00:09:32 2020

@author: EZEQUIEL
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spy

def logistica(x, A, B):
    y = A*x/((B+x**2)**(1/2))
    return y

def exponencial(x, k):
    y = k*np.log(x)
    return y    

def polinomica(x, a, b, c, d):
    y = (x**3)*a+(x**2)*b+x*c+d
    return y

pais = (input("Ingrese el país con el que desea trabajar: \n Argentina \n Australia \n Canada \n Chile \n China \n Egypt \n France \n Germany \n Japan \n New Zealand \n South Africa \n USA \n World \n \nSu elección: "))
data=pd.read_excel('Data.xlsx', sheet_name=pais)

logs = np.array([])
for i in range(len(data['date'])):
    logs=np.append(logs,np.log(data['total_cases'][i]))
   
ajuste_logi = spy.curve_fit(logistica, data['days'], logs, p0 = [12,25])
coef_logi = ajuste_logi[0]
aproxlogi = logistica(data['days'], coef_logi[0], coef_logi[1])

ajuste_expo = spy.curve_fit(exponencial, data['days'], logs, p0 = [12])
coef_expo = ajuste_expo[0]
aproxexpo = exponencial(data['days'], coef_expo[0])

ajuste_pol = spy.curve_fit(polinomica, data['days'], logs, p0 = [1,1,1,1])
coef_pol = ajuste_pol[0]
aproxpol = polinomica(data['days'], coef_pol[0], coef_pol[1], coef_pol[2], coef_pol[3])

e2logi = np.sum((aproxlogi-logs)**2)
e2expo = np.sum((aproxexpo-logs)**2)
e2pol = np.sum((aproxpol-logs)**2)

e2 = [e2logi,e2expo,e2pol]
mejor = np.min(e2)

if mejor == e2[0]:
    print('\n El mejor ajuste lo hace la función logística con un Error cuadrático total de:', np.round(mejor,2), '\n \nSus coeficientes son:\n ', coef_logi, '\n \n ')
if mejor == e2[1]:
    print('\n El mejor ajuste lo hace la función exponencial con un Error cuadrático total de:',np.round(mejor,2), '\n \nSus coeficientes son:\n ', coef_expo, '\n \n ')
if mejor == e2[2]:
    print('\nSi bien el mejor ajuste lo hace la función polinómica con un Error cuadrático total de:', np.round(mejor,2), '\n \nY sus coeficientes son:\n ', coef_pol, '\n \n ')

print('Elijo trabajar las aproximaciones con la función logística ya que es la que simula un comportamiento de los casos de una forma bastante similar a la manera en la que se supone que se comporta una pandemia, alcanzando un máximo asintótico y deteniendo su avance ahí. Cabe recordar que se grafican casos totales y no diarios, en este caso la curva debería ser de tipo parabólico.\n \n')
      
      
dias = data['days'].tolist()
casos = data['total_cases'].tolist()
actual_logi = np.round(np.exp(logistica(dias[-1], coef_logi[0], coef_logi[1])),0)
treinta_logi = np.round(np.exp(logistica(dias[-1]+30, coef_logi[0], coef_logi[1])),0)
sesenta_logi = np.round(np.exp(logistica(dias[-1]+60, coef_logi[0], coef_logi[1])),0)
expandida = np.linspace(dias[0], dias[-1]+60, dias[-1]+60)
actual_ajustada = actual_logi+casos[-1]-actual_logi
treinta_ajustada = treinta_logi+casos[-1]-actual_logi
sesenta_ajustada = sesenta_logi+casos[-1]-actual_logi

plt.plot(expandida, logistica(expandida, coef_logi[0], coef_logi[1]), color = 'red', linestyle='dashed')
plt.plot(expandida, exponencial(expandida, coef_expo[0]), color = 'blue', linestyle='dashed')
plt.plot(expandida, polinomica(expandida, coef_pol[0], coef_pol[1], coef_pol[2], coef_pol[3]), color = 'green', linestyle='dashed')

plt.grid()
plt.plot(data['days'], aproxlogi, label = "Aproximación Logística", color = 'red')
plt.plot(data['days'], aproxexpo, label = "Aproximación Exponencial", color = 'blue')
plt.plot(data['days'], aproxpol, label = "Aproximación Polinomica", color = 'green')
plt.plot(data['days'], logs, label = pais, color = 'black')
plt.plot(dias[-1],np.log(actual_logi),'ro', markersize=6)
plt.plot(dias[-1]+30,np.log(treinta_logi), 'ro')
plt.plot(dias[-1]+60,np.log(sesenta_logi), 'ro')
plt.plot(dias[-1],np.log(actual_ajustada),'ko', markersize=6)
plt.plot(dias[-1]+30,np.log(treinta_ajustada), 'ko')
plt.plot(dias[-1]+60,np.log(sesenta_ajustada), 'ko')
plt.legend(loc="best")
plt.title('Evolución de casos de COVID-19', fontsize=11, verticalalignment='bottom')
plt.xlabel('Días')
plt.ylabel('ln (Casos)')

#print ('Se estima por modelos de tipo logístico que dentro para los', actual_logi, 'casos que tenemos a la fecha, dentro de 30 días tendremos', treinta_logi, 'casos y dentro de sesenta,', sesenta_logi, 'casos en total. \n \n')
#print ('Considerar los errores aparejados a la aproximación ya que a la fecha en realidad hay',casos[-1],'casos. \n \n')
print ('Tener en cuenta los errores inherentes a la estimación por estos métodos. \n \n')
print ('Se suponen para los',casos[-1],'casos actuales,',treinta_ajustada,'para los próximos treinta días y', sesenta_ajustada, 'para los próximos sesenta.')

