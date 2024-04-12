# yamtt (yet another menu template tag)

--- 

### Описание
Тестовый проект Django 5, для работы с древовидным меню через tamplate tag 
Меню, редактируется в админке Django.
Меню формируется одним запросом к БД.
Используется одна модель с ограничениями(constraints).
Можно отрисовать на любой странице с использованием:
```
{% load draw_menu %}
{% draw_menu 'main_menu' %}
```

### Технологии
* Python
* Django

### Запуск проекта
Для Windows:

```shell
git clone git@github.com:kyzman/yamtt.git
cd yamtt
python -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```
Для Linux:

```shell
git clone git@github.com:kyzman/yamtt.git
cd yamtt
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```

Для корректной работы приложения необходимо:
 * создать суперпользователя
```shell
python manage.py createsuperuser
```
 * При первом запуске(отсутствии записей в БД) будет предложено создать меню и его элементы.

Запустить сервер разработки
```shell
python manage.py runserver
```
