# from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import numpy as np
import sys
import datetime
from time import gmtime, strftime

python_clf = joblib.load('Python_model.sav')
java_clf = joblib.load('JAVA_model.sav')
js_clf = joblib.load('JS_model.sav')
html_clf = joblib.load('HTML_model.sav')
c_clf = joblib.load('C_model.sav')
cpp_clf = joblib.load('Cpp_model.sav')
cs_clf = joblib.load('Csharp_model.sav')
go_clf = joblib.load('GO_model.sav')
css_clf = joblib.load('CSS_model.sav')
shell_clf = joblib.load('Shell_model.sav')


models = {'Python':python_clf,'Java':java_clf,'JavaScript':js_clf,'HTML':html_clf,'C':c_clf,'C++':cpp_clf,'C#':cs_clf,'Go':go_clf,'CSS':css_clf,'Shell':shell_clf}

languages = ['Python','Java','JavaScript','HTML','C','C++','C#','Go','CSS','Shell']

answer = []
answer_sum = []

raw_data = sys.argv[1]

raw_data2 = raw_data.replace('null','')
temp_data0 = list(raw_data2.split('"####"'))

for i in range(len(temp_data0)-1):
    temp_data = list(temp_data0[i].split(']'))

    temp_data2 = []
    for j in  range(len(temp_data)):
        tempstr = temp_data[j]

        if ( temp_data[j] != ''):
            if ( temp_data[j][0] == ',' ):
                tempstr2 = tempstr.replace(',[','')
            elif ( temp_data[j][0] == '['):
                tempstr2 = tempstr.replace('[[','')
        
            temp_data2.append(tempstr2)

    temp_data3 = []
    for j in range(len(temp_data2)-1):
        tempstr = temp_data2[j]
        tempstr2 = tempstr.replace('"','')
        
        templist_2 = list(map(str,tempstr2.split(',')))

        templist = []
        for index in range(len(templist_2)):
            if index != 2:
                templist.append(templist_2[index])

        temp_data3.append(templist)

    for k in range (len(temp_data3)):

        for j in range(2,8):
            if temp_data3[k][j] == '':
                temp_data3[k][j] = '0'

        temp_data3[k][2]  = float(temp_data3[k][2]) * 1000

    repositories = {'Python':[],'Java':[],'JavaScript':[],'HTML':[],'C':[],'C++':[],'C#':[],'Go':[],'CSS':[],'Shell':[],'extra':[]}
    predictions = dict()
    repo_names = {'Python':[],'Java':[],'JavaScript':[],'HTML':[],'C':[],'C++':[],'C#':[],'Go':[],'CSS':[],'Shell':[],'extra':[]}
    count = {'Python':0,'Java':0,'JavaScript':0,'HTML':0,'C':0,'C++':0,'C#':0,'Go':0,'CSS':0,'Shell':0}

    for j in range(len(temp_data3)):
        temp = temp_data3[j]
        temp2 = list(map(str,temp))

        for k in range(2,8):
            temp2[k] = float(temp2[k])

        lang = temp2[1]

        if (lang in languages):
            repositories[lang].append(temp2[2:])
            repo_names[lang].append(temp2[0])
        else:
            repositories['extra'].append(temp2[2:])
            repo_names['extra'].append(temp2[0])

    for key in repositories:
        if len(repositories[key]) != 0 and key != 'extra':
            predictions[key] = models[key].predict(repositories[key]).tolist()

    final_predictions = []

    for j in range(len(temp_data3)):
        key = temp_data3[j][1]
        
        if key == '':
            final_predictions.append(0)
        elif key not in languages:
            final_predictions.append(0)
        else:
            point = count[key]
            final_predictions.append(predictions[key][point])
            count[key] = count[key] + 1


    for j in range(len(final_predictions)):
        if final_predictions[j] != -1:
            final_predictions[j] = float((final_predictions[j]/4283703.80381)*500)
        if final_predictions[j] > 500:
            final_predictions[j] = 500

    answer.append(final_predictions)

for i in range(len(answer)):
    sum = 0
    for j in range(len(answer[i])):
        sum = sum + answer[i][j]
    answer_sum.append(sum)

print(answer_sum)

sys.stdout.flush()