"""
Функции для загрузки и сохранения задач
"""

import json # работа с json файлом
import os # проверка наличие файла
import logging

filename = "tasks.json"

# функция загрузки задач из файла
def load_tasks():
    """Загрузка задачи из json файла"""
    global tasks # глобальная переменная tasks, для изменения внешней переменной
    logging.debug("Вызвана функция load_tasks()")

    # условие проверки файла
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file: # открытие файла для чтения (из-за 'r'), конструкция with open закрывает файл после работы
                tasks = json.load(file) # загрузка данных из json
            if not isinstance(tasks, list):
                logging.info(f"Успешно загружено {len(tasks)} задач")
                tasks = []
            else:
                logging.info(f"✅ Успешно загружено {len(tasks)} задач")
                print(f"Загружено {len(tasks)} задач из файла") # f-строка, стандарт при вставление переменных в текст

        except json.JSONDecodeError as e:
            logging.error(f"❌ Файл повреждён (невалидный JSON): {e}")
            print("Ошибка: файл с задачами повреждён")
            tasks = []
        except PermissionError as e:
            logging.error(f"❌ Нет прав на чтение файла: {e}")
            print("Ошибка: нет доступа к файлу задач")
            tasks = []
        except Exception as e:
            logging.error(f"❌ Неожиданная ошибка при загрузке: {type(e).__name__}: {e}")
            print(f"Ошибка при загрузке: {e}")
            tasks = []

    else:
        logging.warning("Файл с задачами не найден")
        tasks = []
    
    logging.debug(f"load_tasks() возвращает {len(tasks)} задач")
    return tasks

# функция сохранения задач в файл
def save_tasks(tasks):
    """Сохранение задачи в json файл"""
    logging.debug(f"Вызвана функция save_tasks() с {len(tasks)} задачами")
    
    try:
        with open(filename, 'w', encoding='utf-8') as file: # 'w' - запись, будет создан или перезаписан
            json.dump(tasks, file, ensure_ascii=False, indent=2) # json.dump функция из модуля json для записи в файл, сохраняем tasks в открытый файл file. Ensure_ascii=False не позволит заменить буквы на коды
        logging.info(f"Сохранено {len(tasks)} задач")
        print("Задачи сохранены")
        return True
    except PermissionError as e:
        logging.error(f"❌ Нет прав на запись файла: {e}")
        print("Ошибка: нет прав на сохранение файла")
        return False
    except Exception as e:
        logging.error(f"❌ Ошибка сохранения: {type(e).__name__}: {e}")
        print(f"Ошибка при сохранении: {e}")
        return False