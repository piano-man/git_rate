from sklearn.externals import joblib
import numpy as np
import sys
import datetime
from time import gmtime, strftime

# LOADING SAVED MODELS FOR EACH LANGUAGE 
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

# CREATING A DICTIONARY TO REFER MODELS WITH LANGUAGE NAMES AS INDICES (KEYS)
models = {'Python':python_clf,'Java':java_clf,'JavaScript':js_clf,'HTML':html_clf,'C':c_clf,'C++':cpp_clf,'C#':cs_clf,'Go':go_clf,'CSS':css_clf,'Shell':shell_clf}

# A LIST OF LANGUAGES CONSIDERED
languages = ['Python','Java','JavaScript','HTML','C','C++','C#','Go','CSS','Shell']

# A DICTIONARY WITH LANGUAGES AS KEYS AND A LIST OF REPOS AS VALUES
repositories = {'Python':[],'Java':[],'JavaScript':[],'HTML':[],'C':[],'C++':[],'C#':[],'Go':[],'CSS':[],'Shell':[],'extra':[]}

# A DICTIONARY TO KEEP TRACK OF NUMBER OF REPOS FOR EACH LANGUAGE
count = {'Python':0,'Java':0,'JavaScript':0,'HTML':0,'C':0,'C++':0,'C#':0,'Go':0,'CSS':0,'Shell':0}

# AN EMPTY DICTIONARY TO STORE PREDICTED SCORES OF EACH REPO
predictions = dict()

# "raw_data" IS THE DATA RECEIVED, "temp_data" SEPARATES EACH VALUE AND MAKES A LIST
raw_data = sys.argv[1]

temp_data = list(raw_data.split(','))
data = []

# TAKING 9 VALUES EACH, CREATING A TUPLE OF DATA FOR EACH REPO AND APPENDING TO "data"
for i in range(int(len(temp_data)/9)):
    a = int(i*9)
    temp = (temp_data[a],temp_data[a+1],temp_data[a+3],temp_data[a+4],temp_data[a+5],temp_data[a+6],temp_data[a+7],temp_data[a+8])
    temp2 = list(map(str,temp))
    data.append(temp2)

# "data" IS NOW A 2-D LIST CONTAINING DATA OF EACH REPO AS A LIST OF 9 ELEMENTS EACH

# IF ANY FIELDS ARE BLANK, SET THEM TO 0 AND MULTIPLYING NO. OF STARS BY 1000 AS THEY ARE VALUES IN TERMS OF "k"
for i in range (len(data)):

    for j in range(3,8):
        if data[i][j] == '':
            data[i][j] = '0'

    data[i][2]  = float(data[i][2]) * 1000

# CONVERTING ALL NUMERIC FIELDS FROM STR TO FLOAT AND SEPARATING REPOS ON THE BASIS OF LANGUAGES
# THE LIST "repositories" DOES NOT CONTAIN THE NAME OF THE REPO, ONLY THE DATA
for i in range(len(data)):
    temp = data[i]
    temp2 = list(map(str,temp))

    for j in range(2,8):
        temp2[j] = float(temp2[j])

    lang = temp2[1]

    if (lang in languages):
        repositories[lang].append(temp2[2:])
    else:
        repositories['extra'].append(temp2[2:])

# PREDICTING SCORES FOR EACH REPO IN THE DICTIONARY "repositories"
# FEEDING A LIST OF REPOSITORIES TO EACH MODEL ACCORDING TO LANGUAGES

for key in repositories:
    if len(repositories[key]) != 0 and key != 'extra':
        predictions[key] = models[key].predict(repositories[key]).tolist()

# "predictions" NOW CONTAINS THE SCORE OF EACH REPO LANGUAGE-WISE
# "final_predictions" IS A LIST THAT CONTAINS THE SCORE OF EACH REPO IN THE ORDER IT WAS SENT IN THE INPUT
final_predictions = []

for i in range(len(data)):
    # TAKING THE KEY AS LANGUAGE OF EACH REPO FROM THE ORIGINAL DATA
    key = data[i][1]
    
    # IF LANGUAGE FIELD WAS EMPTY OR NOT CONSIDERED WE ADD THE SCORE OF THAT REPO AS 0
    if key == '':
        final_predictions.append(0)
    elif key not in languages:
        final_predictions.append(0)
    else:
        point = count[key]
        final_predictions.append(predictions[key][point])
        count[key] = count[key] + 1


# SCALING THE FINAL SCORE TO A RANGE OF 0 TO 500
# 4283703.80381 WAS THE SCORE OF THE IDEAL REPOSITORY TAKEN BY US
for i in range(len(final_predictions)):
    if final_predictions[i] != 0:
        final_predictions[i] = float((final_predictions[i]/4283703.80381)*500)
    if final_predictions[i] > 500:
        final_predictions[i] = 500

print(final_predictions)

sys.stdout.flush()
