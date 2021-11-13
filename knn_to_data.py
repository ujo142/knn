#-*- coding: utf_8 -*-

# Implementacja algorytmu knn
# Plik wejściowy jest plikiem tekstowym, zawierającym w każdej linii
# jedną pozycję zawierającą:
#   temperaturę (w st. Celsjusza), 
#   prędkość wiatru w km/h
#   klasyfikator zimno/ciepło

import sys
sys.path.append('..')
sys.path.append('../../common')
import knn  # noqa
import common  # noqa

# Początek programu
       
if len(sys.argv) < 8:
    sys.exit(
        'Proszę podać parametry:\n' +
        '1.   Nazwę pliku danych ze współrzędnymi punktów dla algorytmu knn.\n' +
        '2.   Nazwę pliku wyjściowego, w którym zapisane zostaną wyniki klasyfikacji.\n' +
        '3.   Liczbę k-sąsiadów uwzględnianych w klasyfikacji.\n' +
        '4-7. Współrzędne prostokąta, w którym określane będą klasy sąsiadów:\n' +
        '4.      współrzędna x lewego dolnego punktu,\n' +
        '5.      współrzędna x prawego górnego punktu,\n' +
        '6.      współrzędna y lewego dolnego punktu,\n' +
        '7.      współrzędna y prawego górnego punktu,\n\n' +
        'Na przykład:\n' +
        'python knn_to_data.py temperature_preferences.data' +
        ' temperature_preferences_completed.data' +
        ' 1 5 30 0 10')
        
        

# Np. "temperature_preferences.data"
input_file = sys.argv[1]
# Np. "temperature_preferences_completed.data"
output_file = sys.argv[2]

k = int(sys.argv[3])
x_from = int(sys.argv[4])
x_to = int(sys.argv[5])
y_from = int(sys.argv[6])
y_to = int(sys.argv[7])

data = common.load_3row_data_to_dic(input_file)
new_data = knn.knn_to_2d_data(data, x_from, x_to, y_from, y_to, k)
common.save_3row_data_from_dic(output_file, new_data)
