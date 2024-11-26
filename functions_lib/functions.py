import numpy as np
import pandas as pd

def get_education_level(arg):
    """
    Функция выделяет из строки уровень образования соискателя по ключевому слову
    Args:
        arg (str): строка таблицы
        
    Returns:
        str: строка таблицы с уровнем образования соискателя
    """
    arg_splitted = arg.split(' ') #сплитуем строку
    target_word='образование' #выделяем ключевое слово, на которое мы будем равняться
    if target_word == arg_splitted[1]:
        education_level = arg_splitted[0]
    if target_word == arg_splitted[2]:
        education_level = arg_splitted[:2]
        education_level = ' '.join(education_level) #объединяем получившуюся разделенную запятыми строку
    education_level = education_level.lower() #перевод символов строки в нижний регистр
    return education_level
    
def get_experience(arg):
    """
    Функция выделяет из строки опыт работы соискателя в месяцах
    Args:
        arg (str): строка таблицы
        
    Returns:
        int: количество месяцев
    """
    if arg is np.nan or arg == 'Не указано': #улословие для явных и скрытых пропусков 
        return None
    arg_splitted = arg.split(' ')[:7] #сплитуем первые 8 слов
    month_key_word = ['месяц', 'месяца', 'месяцев',]
    year_key_word = ['год', 'лет', 'года']
    month = 0
    year = 0
    for i in range(len(arg_splitted)):
        if arg_splitted[i] in month_key_word:
            month = arg_splitted[i-1]
        if arg_splitted[i] in year_key_word:
            year = arg_splitted[i-1]  
    return int(year)*12 + int(month)

million_cities = ['Новосибирск', 'Екатеринбург','Нижний Новгород','Казань', 'Челябинск','Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж','Волгоград']
def get_city(arg):
    """
    Функция причисляет город России к одной из 4 категорий (Москва, Санкт-Петербург, город-миллионник, другие)
    Args:
        arg (str): строка таблицы
        
    Returns:
        str: категория города
    """
    arg_splitted = arg.split(' ') #сплитуем строку по пробелу
    city = arg_splitted[0]
    if city in million_cities: 
        return 'город-миллионник'
    elif (city=='Москва') or (city=='Санкт-Петербург'):
        return city
    else:
        return 'другие'

def get_readiness_to_move(arg):
    """
    Функция позволяет определить готовность соискателя к переезду
    Args:
        arg (str): строка таблицы
        
    Returns:
        bool: True (готов) или False (не готов)
    """
    if ('не готов к переезду' in arg) or ('не готова к переезду' in arg):
        return False
    elif 'хочу' in arg:
        return True
    else:
        return True

def get_readiness_for_bisiness_trips(arg):
    """
    Функция позволяет определить готовность соискателя к командировкам
    Args:
        arg (str): строка таблицы
        
    Returns:
        bool: True (готов) или False (не готов)
    """
    if ('командировка' in arg):
        if ('не готов к командировкам' in arg) or('не готова к командировкам' in arg):
            return False
        else: 
            return True
    else:
        return False

def outliers_z_score(data, feature, left=3, right=3, log_scale=True):
    """
    Находит выбросы в данных, используя метод z-отклонений. 
    Классический метод модифицирован путем добавления:
    * возможности логарифмирования распредления
    * ручного управления количеством стандартных отклонений в обе стороны распределения
    Args:
        data (pandas.DataFrame): набор данных
        feature (str): имя признака, на основе которого происходит поиск выбросов
        left (float, optional): количество стандартных отклонений в левую сторону распределения. По умолчанию 1.5.
        right (float, optional): количество стандартных в правую сторону распределения. По умолчанию 1.5.
        log_scale (bool, optional): режим логарифмирования. По умолчанию False - логарифмирование не применяется.

    Returns:
        pandas.DataFrame: наблюдения, попавшие в разряд выбросов
        pandas.DataFrame: очищенные данные, из которых исключены выбросы
    """
    if log_scale:
        x = np.log(data[feature]+1)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return outliers, cleaned