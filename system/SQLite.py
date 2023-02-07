# -*- coding: utf-8 -*-
# Сервис по работе с БД
from datetime import datetime, date
from typing import Optional
import sqlite3
import os

from system.logging import log, err_log


DateTimeFormat = "%Y-%m-%d %H:%M:%S"
DateFormat = "%Y-%m-%d"


# ---------------------------------------------------------
# вн.сервис преобразование в строку для SQL
def value_str(value: any) -> str:
    if value is None: return 'NULL'
    elif type(value) == int or type(value) == float: return str(value)
    elif type(value) == datetime: return f'"{value.strftime(DateTimeFormat)}"'
    elif type(value) == date: return f'"{value.strftime(DateFormat)}"'
    elif type(value) == bool:
        if value: return 'TRUE'
        else: return 'FALSE'
    else:
        if '"' in value: value = value.replace('"', "'")
        return f'"{value}"'


# ---------------------------------------
# Класс работы с базой данных
class DataBase:
    connect = None  # Коннект к БД
    cursor = None   # Текущий курсор

    # Инициализация базы данных
    def __init__(self, db: str):
        self.connect = sqlite3.connect(os.path.abspath(db), check_same_thread=False)  # Подключение к базе данных
        self.cursor = self.connect.cursor()
        # self.cursor.execute("PRAGMA foreign_keys = ON")
        log('Успешное подключение к базе данных:', db)

    def __del__(self):
        self.connect.close()  # Отключение от базы данных

    # Создание пустой таблицы
    def create_table(self, table_name: str, columns: dict, info: bool = True) -> bool:
        sql = f'CREATE TABLE {table_name} ('
        for key in columns:
            sql += f'{key} {columns[key]}, '
        sql = sql[:-2] + ')'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log(f"Таблица '{table_name}' успешно создана!")
            return True
        except Exception as e:  # возможно таблица создана ранее
            err_log(e)
            return False

    # Создание новой таблицы и добавление данных в таблицу
    def table_data(self, table_name: str, columns: dict, data: list, info: bool = True) -> bool:
        create = self.create_table(table_name, columns, info=info)
        set_data = self.write_block(table_name, data, info=info)
        return create and set_data

    # Получение информации о колонках таблицы в БД
    def table_info(self, table_name: str, info: bool = True) -> Optional[list]:
        sql = f"pragma table_info('{table_name}')"
        if info: log(sql, log_type='SQL')
        result = []
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():  # получить тип list
                result.append(row)
            if info: log(f"По таблице '{table_name}' получено сведений:", len(result))
            return result
        except Exception as e:  # возможно таблица неверно задана
            err_log(e)
            return None

    # Запись строки данных в таблицу [list]
    def write_row(self, table_name: str, row: list, info: bool = True) -> bool:
        sql = f'INSERT INTO {table_name} VALUES ('
        for item in row:
            sql += value_str(item) + ', '
        sql = sql[:-2] + ')'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log(f"Запись в таблицу '{table_name}' успешно добавлена!")
            return True
        except Exception as e:  # проблема с записью
            err_log(e)
            return False

    # Запись данных из словаря [dict]
    def write_dict(self, table_name: str, row: dict, info: bool = True) -> bool:
        columns = ', '.join(row.keys())
        placeholders = ':'+', :'.join(row.keys())
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql, row)
            self.connect.commit()
            if info: log(f"Запись в таблицу '{table_name}' успешно добавлена!")
            return True
        except Exception as e:  # проблема с записью
            err_log(e)
            return False

    # Запись данных [dict]
    def write_dicts(self, table_name: str, rows: list, info: bool = True) -> bool:
        columns = ', '.join(rows[0].keys())
        placeholders = ':'+', :'.join(rows[0].keys())
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        if info: log(sql, log_type='SQL')
        mRows = []
        for row in rows:
            m = []
            for key in row:
                m.append(row[key])
            mRows.append(m)
        try:
            self.cursor.executemany(sql, mRows)
            self.connect.commit()
            if info: log('Добавлено строк:', self.cursor.rowcount)
            return True
        except Exception as e:  # проблема с записью
            err_log(e)
            return False

    # Запись данных блоками
    def write_block(self, table_name: str, block: list, info: bool = True) -> bool:
        sql = f'INSERT INTO %s VALUES (' % table_name
        for item in block[0]:
            sql += '?,'
        sql = sql[:-1] + ')'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.executemany(sql, block)
            self.connect.commit()
            if info: log('Добавлено строк:', self.cursor.rowcount)
            return True
        except Exception as e:  # ошибка при записи
            err_log(e)
            return False

    # Запись словаря целиком
    def write_dictionary(self, table_name: str, dictionary: dict, info: bool = True) -> bool:
        mDict = []
        for key in dictionary:
            mDict.append([key, dictionary[key]])
        return self.write_block(table_name, mDict, info=info)

    # Получение числа строк (rows)
    def count(self, table_name: str, info: bool = True) -> int:
        sql = f'SELECT count(*) FROM {table_name}'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if info: log(f"Число записей в таблице '{table_name}':", row[0])
            return int(row[0])
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return -1

    # Загрузка всей таблицы
    def read_all(self, table_name: str, info: bool = True) -> list:
        sql = f'SELECT * FROM {table_name}'
        result = []  # создаём пустой массив
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():  # проверить тип list
                result.append(row)
            if info: log(f"Из таблицы '{table_name}' получено записей:", len(result))
            return result
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return result

    # Чтение по одному критерию (равенство или like)
    def find_read(self, table_name: str, column: str, value: any, like: bool = False, only_one: bool = False,
                  info: bool = True) -> list:
        if type(value) == str and like:
            value = f'%{value.upper()}%'
        value = value_str(value)
        if like:
            sql = f'SELECT * FROM {table_name} WHERE UPPER({column}) LIKE {value}'
        else:
            sql = f'SELECT * FROM {table_name} WHERE {column} = {value}'
        result = []  # создаём пустой массив
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            if only_one:
                result = self.cursor.fetchone()  # загрузка данных по одной строке
                if info:
                    if result: log(f"В таблице '{table_name}' найдена одна запись")
                    else: log(f"В таблице '{table_name}' не найдено записей")
            else:
                for row in self.cursor.fetchall():  # Загрузка всех данных
                    result.append(row)
                if info: log(f"В таблице '{table_name}' найдено записей:", len(result))
            return result
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return result

    # Чтение по одному критерию (условие больше или меньше)
    def find_condition(self, table_name: str, column: str,
                       value_min: any = None, value_max: any = None, info: bool = True) -> list:
        if value_min: value_min = value_str(value_min)
        if value_max: value_max = value_str(value_max)
        if value_min and value_max:
            sql = f'SELECT * FROM {table_name} WHERE {column} BETWEEN {value_min} AND {value_max}'
        else:
            if value_min:
                sql = f'SELECT * FROM {table_name} WHERE {column} >= {value_min}'
            elif value_max:
                sql = f'SELECT * FROM {table_name} WHERE {column} <= {value_max}'
            else:
                sql = f'SELECT * FROM {table_name}'
        result = []  # создаём пустой масив
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():  # Загрузка всех данных
                result.append(row)
            if info: log(f"В таблице '{table_name}' найдено записей:", len(result))
            return result
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return result

    # Чтение по нескольким критериям
    def find_conditions(self, table_name: str, info: bool = True, **kwargs) -> list:
        sql = f'SELECT * FROM {table_name}'
        if kwargs:
            sql += ' WHERE '
            for key in kwargs:  # включаем все условия
                sql += f'{key} = {value_str(kwargs[key])} AND '
            sql = sql[:-5]
        result = []  # создаём пустой массив
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():  # Загрузка всех данных
                result.append(row)
            if info: log(f"В таблице '{table_name}' найдено записей:", len(result))
            return result
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return result

    # Чтение одной записи по id
    def read_row(self, table_name: str, value: any, column: str = 'ID', info: bool = True) -> list:
        return self.find_read(table_name=table_name, column=column, value=value, like=False, only_one=True,
                              info=info)

    # Чтение всех записей
    def read_rows(self, table_name: str, value: any, column: str = 'ID', info: bool = True) -> list:
        return self.find_read(table_name=table_name, column=column, value=value, like=False, only_one=False,
                              info=info)

    # Загрузка всей таблицы в виде словаря
    def read_dict(self, table_name: str, all_columns: bool = True, info: bool = True) -> dict:
        rows = self.read_all(table_name)
        dict_result = {}
        try:
            if all_columns and len(rows[0]) > 2:  # если всё загружать
                # end = len(rows[0])
                for row in rows:
                    row_result = []
                    for i, item in enumerate(row):
                        if i > 0: row_result.append(item)
                    dict_result[row[0]] = row_result  # формируем словарь со всеми вложениями
                return dict_result
            # если не нужно всё или всего 2 колонки
            for row in rows:
                dict_result[row[0]] = row[1]  # формируем словарь по первым двум колонкам
            return dict_result
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return dict_result

    # Поиск строк по точным критериям и получение списка словарей
    def read_dicts(self, table_name: str, info: bool = True, **kwargs) -> list:
        rows = self.find_conditions(table_name, info=info, **kwargs)
        table_info = self.sql(f"PRAGMA TABLE_INFO('{table_name}')", info=info)
        results: list = []
        for row in rows:
            items: dict = {}
            for i, item in enumerate(row, start=0):
                text = table_info[i][1]
                items[table_info[i][1]] = row[i]
            results.append(items)
        return results

        # Обновление данных по одному критерию (равенство или like)
    def find_update(self, table_name: str, column: str, value: any,
                    column_update: str, value_update: any, like: bool = False, info: bool = True) -> bool:
        if type(value) == str and like:
            value = f'%{value.upper()}%'
        value = value_str(value)
        value_update = value_str(value_update)
        if like:
            sql = f'UPDATE {table_name} SET {column_update} = {value_update} WHERE UPPER({column}) LIKE {value}'
        else:
            sql = f'UPDATE {table_name} SET {column_update} = {value_update} WHERE {column} = {value}'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log('Обновлено записей:', self.cursor.rowcount)
            return True
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return False

    # Обновление нескольких данных по одному критерию (равенство или like)
    def find_updates(self, table_name: str, column: str, value: any,
                     like: bool = False, info: bool = True, **kwargs) -> bool:
        if type(value) == str and like:
            value = f'%{value.upper()}%'
        value = value_str(value)
        sql = f'UPDATE {table_name} SET '
        for attr in kwargs:
            kwargs[attr] = value_str(kwargs[attr])
            sql += f'{attr} = {kwargs[attr]}, '
        sql = sql[:-2]
        if like:
            sql += f' WHERE UPPER({column}) LIKE {value}'
        else:
            sql += f' WHERE {column} = {value}'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log('Обновлено записей:', self.cursor.rowcount)
            return True
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return False

    # Удаление данных по одному критерию (равенство)
    def find_delete(self, table_name: str, column: str, value: any, like: bool = False, info: bool = True) -> int:
        if type(value) == str and like:
            value = f'%{value.upper()}%'
        value = value_str(value)
        if like:
            sql = f'DELETE FROM {table_name} WHERE UPPER({column}) LIKE {value}'
        else:
            sql = f'DELETE FROM {table_name} WHERE {column} = {value}'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log('Удалено записей:', self.cursor.rowcount)
            return self.cursor.rowcount
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return self.cursor.rowcount

    # Удаление всех записей таблицы
    def data_delete(self, table_name: str, info: bool = True) -> bool:
        sql = 'DELETE FROM ' + table_name
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log(f"Таблица '{table_name}' успешно удалена!")
            return True
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return False

    # Удаление всей таблицы!
    def delete(self, table_name: str, info: bool = True) -> bool:
        sql = 'DROP TABLE ' + table_name
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            if info: log(f"Таблица '{table_name}' успешно удалена!")
            return True
        except Exception as e:  # ошибка при чтении
            err_log(e)
            return False

    # Универсальный запрос
    def sql(self, query: str, info: bool = True) -> any:
        result = []  # создаём пустой масив
        if info: log(query, log_type='SQL')
        try:
            self.cursor.execute(query)
            self.connect.commit()
            if 'SELECT ' in query.upper() or 'TABLE_INFO' in query.upper():
                for row in self.cursor.fetchall():  # Загрузка всех данных
                    result.append(row)
                return result
            else:
                log('Изменено строк: ', self.cursor.rowcount)
                return self.cursor.rowcount
        except Exception as e:  # ошибка при обработке запроса
            err_log(e)
            return None

    # Универсальный запрос из нескольких команд
    def sql_script(self, queries: str, info: bool = True) -> bool:
        if info: log(queries, log_type='SQL')
        try:
            self.cursor.executescript(queries)
            self.connect.commit()
            return True
        except Exception as e:  # ошибка при обработке запроса
            err_log(e)
            return False

    # Поиск всех данных по нескольким столбцам (like %text%)
    def find_all(self, table_name: str, columns: list, value: any, like: bool = True) -> list:
        result = []
        for col in columns:
            result += self.find_read(table_name=table_name, column=col, value=value, like=like, info=False)
        return result

    # Получение максимального идентификатора/значения таблицы
    def max_value(self, table_name: str, column_id: str = 'ID', info: bool = True) -> int:
        sql = f'SELECT MAX({column_id}) FROM {table_name}'
        if info: log(sql, log_type='SQL')
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:  # ошибка при обработке запроса
            err_log(e)
            return -1

    # Индексация таблицы (по завершению загрузки данных в таблицу)
    def indexation(self, table_name: str, columns: list):
        sql = 'CREATE INDEX %s ON %s (' % (table_name + '_idx', table_name)
        for col in columns:
            sql += col + ', '
        sql = sql[:-2] + ')'
        return self.sql(sql)

    # Создание триггеров удаления зависимых
    def trigger_deleting(self, table_name: str, table_delete_from: str, name_id, trigger_name: str):
        sql = f"CREATE TRIGGER {trigger_name} BEFORE DELETE ON {table_name} " \
              f"BEGIN DELETE FROM {table_delete_from} WHERE {name_id} = OLD.id"
        return self.sql(sql)
