import pyperclip as pc
def imports():
    s = '''from sklearn.datasets import fetch_openml
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import time
    '''
    return pc.copy(s)
    
def n1():
    s = '''data = fetch_openml(name='vertebra-column')
print(data.DESCR)
X = data.data
y = data.target
    '''
    return pc.copy(s)
    
def n2():
    s = '''
df = pd.DataFrame(X, columns=data.feature_names)
df['target'] = y

print(f'Число строк: {len(df)}')
print(f'Число столбцов: {len(df.columns)}')
print(f'Статистика по признакам:\n{df.describe()}')
print(f'Количество классов: {len(set(df.target))}') #unique
    '''
    return pc.copy(s)

def n3():
    s = '''print(df.isnull().sum())  # нет пропущенных значений
#df.fillna(mean)

# все признаки численные
#for col in df:
# print(df[col].dtype)

#если есть текстовые значения перевести в числа:
#label_encoder = LabelEncoder()
#X['col'] = label_encoder.fit_transform(X['col'])
    '''
    return pc.copy(s)
    
def n4():
    s = '''
info_dict = dict()
start_time = time.time()
lr_model = LogisticRegression(max_iter = 10000)
lr_model.fit(X, y)
lr_time = time.time() - start_time
y_pred = lr_model.predict(X)
acc_lr = accuracy_score(y, y_pred)
classification_matrix = confusion_matrix(y, y_pred)

print(f'Accuracy: {acc_lr}')
print(f'Матрица классификации:\n{classification_matrix}')
#print(classification_report(y,y_pred))
info_dict['LogisticRegression'] = [lr_time, acc_lr]
    '''
    return pc.copy(s)
    
def n5():
    s = '''
degrees = [2, 3, 4, 5, 6]
for degree in degrees:
    start_time = time.time()
    poly_model = make_pipeline(PolynomialFeatures(degree), LogisticRegression())
    poly_model.fit(X, y)
    poly_time = time.time() - start_time
    s = f'Polynomial (Degree = {degree})'

    y_pred = poly_model.predict(X)
    acc_poly = accuracy_score(y, y_pred)
    cm_poly = confusion_matrix(y, y_pred)
    info_dict[s] = [poly_time, acc_poly]

    print(f'Степень полинома: {degree}')
    print(f'Accuracy: {acc_poly}')
    #print(f'Матрица классификации:\n{cm_poly}')
    print()
    '''
    return pc.copy(s)

def n6():
    s = '''
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for kernel in kernels:
    start_time = time.time()
    svm_model = SVC(kernel=kernel)
    svm_model.fit(X, y)
    s = f'SVM (kernel = {kernel})'
    svm_time = time.time() - start_time
    y_pred = svm_model.predict(X)
    acc_svm = accuracy_score(y, y_pred)
    cm_svm = confusion_matrix(y, y_pred)
    info_dict[s] = [svm_time, acc_svm]

    print(f'Ядро: {kernel}')
    print(f'Accuracy: {acc_svm}')
    #print(f'Матрица классификации:\n{cm_svm}')
    '''
    return pc.copy(s)
    
def n7():
    s = '''
# Обучение модели Перцептрона
start_time = time.time()
perceptron_model = MLPClassifier(hidden_layer_sizes=(100,100,100),max_iter=1000)#можно менять кол-во слоев и нейронов
perceptron_model.fit(X, y)
perceptron_time = time.time() - start_time

# Расчет метрик и вывод таблицы классификации
y_pred_perceptron = perceptron_model.predict(X)
accuracy_perceptron = accuracy_score(y, y_pred_perceptron)
cm_perceptron = confusion_matrix(y, y_pred)
info_dict['Perceptron'] = [perceptron_time, accuracy_perceptron]
print("Perceptron:")
print("Accuracy: ", accuracy_perceptron)
#print("Таблица классификации:\n", cm_perceptron)
    '''
    return pc.copy(s)
    
def n8():
    s = '''
print(info_dict)
info = pd.DataFrame.from_dict(info_dict, orient='index', columns=['Время обучения', 'Эффективность'])
info = info.sort_values(by='Эффективность', ascending=True)
print(info)
    '''
    return pc.copy(s)

