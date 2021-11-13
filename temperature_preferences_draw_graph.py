#-*- coding: utf_8 -*-

import sys
sys.path.append('../../common')  # noqa
import common
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

matplotlib.style.use('ggplot')

data_file_name = 'temperature_preferences_completed.data'
temp_from = 5
temp_to = 30
wind_from = 0
wind_to = 10

data = np.loadtxt(open(data_file_name, 'r'),
                  dtype={'names': ('temperature', 'wind', 'perception'),
                         'formats': ('i4', 'i4', 'S10')},
                         encoding='utf-8')



# Przyporządkowanie kolorów wyświetlania do poszczególnych klas
for i in range(0, len(data)):
    if data[i][2] == 'zimno':
        data[i][2] = 'blue'
    elif data[i][2] == 'ciepło': 
        data[i][2] = 'red'
    else:
        data[i][2] = 'gray'
        
# Konwersja tablicy na format wyświetlania
data_processed = common.get_x_y_colors(data)

# rysowaniw wykresu.
plt.title('Subiektywne odczuwanie temperatury')
plt.xlabel(u"Temperatura w °C")
plt.ylabel(u"Prędkość wiatru w km/h")
plt.axis([temp_from, temp_to, wind_from, wind_to])

# Dodanie legendy do wykresu.
blue_patch = mpatches.Patch(color='blue', label='zimno')
red_patch = mpatches.Patch(color='red', label=u'ciepło')      
plt.legend(handles=[blue_patch, red_patch])
plt.scatter(data_processed['x'], data_processed['y'],
            c=data_processed['colors'], s=[1400] * len(data))
            
print 'debug 3'            
            
plt.show()
