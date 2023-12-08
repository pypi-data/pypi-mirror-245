def help_():
    print('''
Чтобы получить доступ к заданиям используйте метод task(принимает числа от 1 до 8
Чтобы выввести список библиотек используйте метод libs()
''')
    
def libs():
    print('''
# Импорт необходимых библиотек
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
import time
import plotly.express as px
import seaborn as sns
''')
    
def task(num):
    dc = {
        1:'''
from sklearn.datasets import fetch_openml
# Загрузка датасета
dataset = fetch_openml(name='students_scores', version=1, as_frame=True)
# Вывод описания датасета
# print(dataset.DESCR)
# Определение целевой переменной и признаков
y = dataset.target
X = dataset.data
df = pd.concat([X, y], axis=1)
''',
2:'''
# основная статистическая информация о данных
df.describe(include='all')
_________________________________________
# число строк (объектов)
print(f'Число строк: {df.shape[0]}')
# число столбцов (признаков)
print(f'Число столбцов: {df.shape[1]}')
# статистику по признакам
_________________________________________
# количество классов (значений целевой переменной)
y.value_counts()
_________________________________________
df.dtypes
_________________________________________
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

numerical_columns = df.select_dtypes(include='number').columns
# Создать subplot
fig = make_subplots(rows=len(numerical_columns), cols=2, subplot_titles=[f'Histogram and Box Plot of {column}' for column in numerical_columns])

for i, column in enumerate(numerical_columns, start=1):
    # Гистограмма
    hist_fig = px.histogram(df, x=column)
    # Box-plot
    box_fig = px.box(df, y=column, points='all')
    box_fig.update_layout(showlegend=False)  # Не показывать легенду для box plot

    # Добавить гистограмму и box plot в subplot
    fig.add_trace(go.Histogram(hist_fig['data'][0]), row=i, col=1)
    fig.add_trace(go.Box(box_fig['data'][0]), row=i, col=2)

fig.update_layout(height=300 * len(numerical_columns), showlegend=False, title_text="Histograms and Box Plots")
fig.show()
_________________________________________
# Получить информацию о числовых столбцах
numerical_columns = df.select_dtypes(include='number').columns

# Цикл для построения гистограмм и box-plot'ов
for column in numerical_columns:
    # Гистограмма
    fig = px.histogram(df, x=column, title=f'Histogram of {column}')
    fig.show()
    # Box-plot
    fig = px.box(df, y=column, points='all', title=f'Box Plot of {column}')
    fig.update_layout(showlegend=True, legend=dict(x=0.1, y=1.15), yaxis=dict(title=f'{column}'))
    fig.show()
''',
3:'''
df.isnull().sum()
_________________________________________
# заполнение нанов средними значениями и удаление строк, если столбец категориальный
for column in df.columns:
    if df[column].isnull().any():
        try:
            mean_value = df[column].mean()
            df[column].fillna(mean_value, inplace=True)
        except:
            df.dropna(subset=[column], inplace=True)
_________________________________________
all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns)
_________________________________________
category_mapping = {}

for column in df.columns:
    if pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
        labels, uniques = pd.factorize(df[column])
        category_mapping[column] = dict(zip(uniques, labels))
        df[column] = labels
_________________________________________
category_mapping
_________________________________________
all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns)
''', 
4:'''
# Импорт необходимых библиотек
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y = df['gender']
X = df.drop('gender', axis=1)
# Разделение на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Стандартизация признаков
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Создание и обучение модели логистической регрессии
logreg_model = LogisticRegression(random_state=42)
logreg_model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_logreg_pred = logreg_model.predict(X_test)

# Оценка модели
logreg_accuracy = accuracy_score(y_test, y_logreg_pred)
logreg_conf_matrix = confusion_matrix(y_test, y_logreg_pred)
logreg_classification_rep = classification_report(y_test, y_logreg_pred)

# Вывод результатов
print("Logistic Regression:")
print(f'Accuracy: {logreg_accuracy:.2f}\n')
print(f'Confusion Matrix:\n{logreg_conf_matrix}\n')
print(f'Classification Report:\n{logreg_classification_rep}\n')
''',
5:'''
# Импорт необходимых библиотек
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Задание параметров
degree_poly = 2  # степень полинома

# Создание и обучение полиномиальной модели
poly_model = make_pipeline(PolynomialFeatures(degree_poly), LogisticRegression(random_state=42))
poly_model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_poly_pred = poly_model.predict(X_test)

# Оценка модели
poly_accuracy = accuracy_score(y_test, y_poly_pred)
poly_conf_matrix = confusion_matrix(y_test, y_poly_pred)
poly_classification_rep = classification_report(y_test, y_poly_pred)

# Вывод результатов
print("Polynomial Regression:")
print(f'Accuracy: {poly_accuracy:.2f}\n')
print(f'Confusion Matrix:\n{poly_conf_matrix}\n')
print(f'Classification Report:\n{poly_classification_rep}\n')
''',
6:'''
# Импорт необходимых библиотек
from sklearn.svm import SVC

# Задание параметров
kernel_svm = 'linear'  # тип ядра для SVM

# Создание и обучение модели метода опорных векторов
svm_model = SVC(kernel=kernel_svm, random_state=42)
svm_model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_svm_pred = svm_model.predict(X_test)

# Оценка модели
svm_accuracy = accuracy_score(y_test, y_svm_pred)
svm_conf_matrix = confusion_matrix(y_test, y_svm_pred)
svm_classification_rep = classification_report(y_test, y_svm_pred)

# Вывод результатов
print("Support Vector Machine (SVM):")
print(f'Accuracy: {svm_accuracy:.2f}\n')
print(f'Confusion Matrix:\n{svm_conf_matrix}\n')
print(f'Classification Report:\n{svm_classification_rep}\n')
''',
7:'''
# Импорт необходимых библиотек
from sklearn.linear_model import Perceptron

# Создание и обучение модели перцептрона
perceptron_model = Perceptron(random_state=42)
perceptron_model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_perceptron_pred = perceptron_model.predict(X_test)

# Оценка модели
perceptron_accuracy = accuracy_score(y_test, y_perceptron_pred)
perceptron_conf_matrix = confusion_matrix(y_test, y_perceptron_pred)
perceptron_classification_rep = classification_report(y_test, y_perceptron_pred)

# Вывод результатов
print("Perceptron:")
print(f'Accuracy: {perceptron_accuracy:.2f}\n')
print(f'Confusion Matrix:\n{perceptron_conf_matrix}\n')
print(f'Classification Report:\n{perceptron_classification_rep}\n')
''',
8:'''
# Обучение и измерение времени для каждой модели
start_time = time.time()
logreg_model.fit(X_train, y_train)
logreg_time = time.time() - start_time

start_time = time.time()
poly_model.fit(X_train, y_train)
poly_time = time.time() - start_time

start_time = time.time()
svm_model.fit(X_train, y_train)
svm_time = time.time() - start_time

start_time = time.time()
perceptron_model.fit(X_train, y_train)
perceptron_time = time.time() - start_time

# ... (весь последующий код)

# Создание итоговой таблицы сравнения
results_data = {
    'Модель': ['Logistic Regression', 'Polynomial Regression', 'Support Vector Machine', 'Perceptron'],
    'Accuracy': [logreg_accuracy, poly_accuracy, svm_accuracy, perceptron_accuracy],
    'Время обучения (сек)': [logreg_time, poly_time, svm_time, perceptron_time]
}

results_df = pd.DataFrame(results_data)

# Вывод итоговой таблицы
results_df
'''}
    print(dc[num])

help_()