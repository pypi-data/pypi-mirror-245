class a:
    def b(task=''):
        #1
        sklad = {
            'import':'import pandas as pd\n\
import numpy as np\n\
from sklearn.datasets import fetch_openml # импорт файла \n\
from sklearn.model_selection import train_test_split\n\
from sklearn.linear_model import LogisticRegression\n\
from sklearn.preprocessing import PolynomialFeatures\n\
from sklearn.metrics import accuracy_score, classification_report\n\
from sklearn.linear_model import Perceptron'
            ,
            '1':'№1 Загрузите предложенный вам датасет с помощью функции sklearn.datasets.fetch_openml. Выведите текстовое описание загруженного датасета. Обозначьте целевую переменную за y, а остальные данные за X.\n\
students = fetch_openml(name = "students_scores", version=1, as_frame=True)\n\
print(students["DESCR"])\n\
#----------------\n\
X = students.data\n\
y = students.target\n\
#----------------\n\
print(y)\n\
#----------------\n\
data = pd.DataFrame(students.data, columns = students.feature_names)\n\
data["gender"] = students.target\n\
data'
            ,
            '2':'№2 Выведите основную статистическую информацию о данных. Сделайте количественное описание датасета: число строк (объектов), число столбцов (признаков), статистику по признакам, количество классов (значений целевой переменной).\n\
type(students)\n\
#----------------\n\
data.describe()\n\
#----------------\n\
data.shape\n\
#----------------\n\
len(data["gender"].unique())'
            ,
            '3':'№3 Убедитесь, что данные пригодны для моделирования. В данных не должно быть пропущенных значений, ве признаки должны быть численными. Если эти условия нарушаются, исправьте это.\n\
data.info()\n\
#----------------\n\
columns_to_drop = ["race.ethnicity", "parental.level.of.education", "lunch", "test.preparation.course"]\n\
data = data.drop(columns=columns_to_drop, axis=1)\n\
#----------------\n\
data["gender"] = data["gender"].map({"male": 1, "female": 0})\n\
#----------------\n\
data\n\
#----------------\n\
# y = data["gender"]\n\
X = data.iloc[:, :-1]'
            ,
            '4':'№4 Обучите модель логистической регрессии на рассматриваемых данных из библиотеки sklearn. Рассчитайте метрики accuracy и выведите таблицу классификации.\n\
import time\n\
TIME = []\n\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\
model = LogisticRegression()\n\
start = time.time()\n\
model.fit(X_train, y_train)\n\
TIME.append(time.time() - start)\n\
\n\
y_pred = model.predict(X_test)\n\
\n\
accuracy = accuracy_score(y_test, y_pred)\n\
print(f"Метрика accuracy: {accuracy}")\n\
\n\
classification_report_result1 = classification_report(y_test, y_pred)\n\
print("Таблица классификации:")\n\
print(classification_report_result1)'
            ,
            '5':'№5 Обучите полиномиальную модель классификации. Рассчитайте метрики accuracy и выведите таблицу классификации. Попробуйте разные степени полинома и выберите ту, которая работает лучше.\n\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\
best_degree = None\n\
best_accuracy = 0\n\
for degree in range(1, 10):\n\
    poly = PolynomialFeatures(degree=degree)\n\
    X_poly = poly.fit_transform(X_train)\n\
\n\
    model = LogisticRegression()\n\
    model.fit(X_poly, y_train)\n\
\n\
    X_test_poly = poly.transform(X_test)\n\
    y_pred = model.predict(X_test_poly)\n\
\n\
    accuracy = accuracy_score(y_test, y_pred)\n\
\n\
    print(f"Степень: {degree}, Метрика accuracy: {accuracy}")\n\
\n\
    if accuracy > best_accuracy:\n\
        best_accuracy = accuracy\n\
        best_degree = degree\n\
\n\
print(f"Лучшая степень: {best_degree}, Лучшая Метрика accuracy: {best_accuracy}")\n\
#----------------------------------------------------------------------------------\n\
poly = PolynomialFeatures(degree=best_degree)\n\
X_train_poly = poly.fit_transform(X_train)\n\
X_test_poly = poly.transform(X_test)\n\
\n\
model = LogisticRegression()\n\
start = time.time()\n\
model.fit(X_train_poly, y_train)\n\
TIME.append(time.time() - start)\n\
\n\
\n\
y_pred = model.predict(X_test_poly)\n\
classification_report_result2 = classification_report(y_test, y_pred)\n\
print("\nBest Model (Polynomial Degree {}):".format(best_degree))\n\
print("Accuracy:", accuracy_score(y_test, y_pred))\n\
print("Classification Report:\n", classification_report_result2)'
            ,
            '6':'№6 Обучите модель классификации по методу опорных векторов. Рассчитайте метрики accuracy и выведите таблицу классификации. Попробуйте разные ядерные функции и выберите ту, которая работает лучше.\n\
from sklearn.svm import SVC\n\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\
\n\
kernel_types = ["linear", "poly", "rbf", "sigmoid"]\n\
best_kernel = None\n\
best_accuracy = 0\n\
\n\
for kernel_type in kernel_types:\n\
    model = SVC(kernel=kernel_type)\n\
    \n\
    model.fit(X_train, y_train)\n\
    \n\
    y_pred = model.predict(X_test)\n\
    \n\
    accuracy = accuracy_score(y_test, y_pred)\n\
    \n\
    print(f"Ядерная функция: {kernel_type}, Accuracy: {accuracy}")\n\
    \n\
    if accuracy > best_accuracy:\n\
        best_accuracy = accuracy\n\
        best_kernel = kernel_type\n\
\n\
print(f"Лучшая ядерная функция: {best_kernel}, Лучшая Accuracy: {best_accuracy}")\n\
\n\
best_model = SVC(kernel=best_kernel)\n\
start = time.time()\n\
best_model.fit(X, y)\n\
TIME.append(time.time() - start)\n\
y_pred_all = best_model.predict(X)\n\
\n\
accuracy_all = accuracy_score(y, y_pred_all)\n\
classification_report_result3 = classification_report(y, y_pred_all)\n\
\n\
print(f"Accuracy: {accuracy_all}")\n\
print("Таблица классификации:")\n\
print(classification_report_result3)'
            ,
            '7':'№7 Обучите модель классификации Перцептрон. Рассчитайте метрики accuracy и выведите таблицу классификации.\n\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\
\n\
model = Perceptron()\n\
start = time.time()\n\
model.fit(X_train, y_train)\n\
TIME.append(time.time() - start)\n\
\n\
y_pred = model.predict(X_test)\n\
\n\
accuracy = accuracy_score(y_test, y_pred)\n\
\n\
classification_report_result4 = classification_report(y_test, y_pred)\n\
print(f"Accuracy: {accuracy}")\n\
print("Таблица классификации:")\n\
print(classification_report_result4)'
            ,
            '8':'№8 Выведите итоговую таблицу сравнения всех моделей. В таблице должна быть информация о эффективности и времени обучения каждой модели. Сделайте вывод о применимости и эффективности моделей для классификации объектов в данной задаче.\n\
TIME\n\
#------------------\n\
reg = ["Логистическая регрессия","Полиномиальная модель", "SVC", "Перцептрон"]\n\
clas = [classification_report_result1, classification_report_result2, classification_report_result3, classification_report_result4]\n\
for i in range(4):\n\
    print(reg[i])\n\
    print(f"Время: {TIME[i]}")\n\
    print(clas[i])\n\
    \n\
    \n\
    \n\
    \n\
"Перцептрон победил, самое быстрое время обучения, хорошее значение accuracy, мы работаем с простой задачей классфификации"\n\
Логистическая регрессия является простой и эффективной моделью для бинарной классификации. Если задача бинарной классификации, то она может быть хорошим выбором.\n\
\n\
Полиномиальные модели могут быть применены в тех случаях, когда зависимость между признаками и целевой переменной имеет нелинейный характер.\n\
\n\
SVM хорошо работает в случаях, когда данные линейно неразделимы или имеют сложную структуру.\n\
\n\
Перцептрон подходит для простых задач классификации.'
            }
        print(sklad[task])




