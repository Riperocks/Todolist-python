"""
ГЛАВНЫЙ ФАЙЛ ПРОГРАММЫ "СПИСОК ДЕЛ"
"""

import file_io
import utils
import tasks_crud as tasks
import search_filter
import logging
from datetime import datetime
import os

# Создаём папку logs
os.makedirs("logs", exist_ok=True)  # exist_ok=True не выдаст ошибку, если папка уже есть

# Настройка логирования
logging.basicConfig(
    filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log', # файл на каждый день
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    encoding='utf-8'
)
# Добавим обработчик для вывода в консоль (по желанию)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)  # в консоль только ошибки
logging.getLogger().addHandler(console)

# Глобальный список для хранения задач
# Задача будет состоять из полей:
# id: номер задачи
# title: название
# completed: выполнена или нет
tasks_list = [] # список задач

# функция показа меню
def show_menu():
    """Показывает главное меню"""
    print("\n" + "="*40)
    print("МОЙ СПИСОК ДЕЛ")
    print("="*40)
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Отметить задачу как выполненнную")
    print("4. Удалить задачу")
    print("5. Поиск задач")
    print("6. Фильтрация задач")
    print("7. Выйти")
    print("="*40)

# Главная функция программы
def main():
    """Главная функция программы"""
    logging.info("="*50)
    logging.info("ПРОГРАММА ЗАПУЩЕНА")
    logging.info("="*50)

    utils.clear_screen()
    print("Добро пожаловать в программу 'Список дел'")

    global tasks_list
    tasks_list = file_io.load_tasks() # загрузка задач при старте

    # Бесконечный цикл программы
    while True:
        show_menu() #показ меню
        choice = input("Выберите действие (1-7): ")

        logging.info(f"Пользователь выбрал действие: {choice}")
        
    # проверяем выбор пользователя и вызываем нужную функцию
        if choice == "1":
            utils.clear_screen()
            tasks_list = tasks.add_task(tasks_list)
            utils.pause_and_clear()
        elif choice == "2":
            utils.clear_screen()
            tasks.show_tasks(tasks_list)
            utils.pause_and_clear()
        elif choice == "3":
            utils.clear_screen()
            tasks_list = tasks.complete_task(tasks_list)
            utils.pause_and_clear()
        elif choice == "4":
            utils.clear_screen()
            tasks_list = tasks.delete_task(tasks_list)
            utils.pause_and_clear()
        elif choice == "5":
            utils.clear_screen()
            search_filter.search_tasks(tasks_list)
            utils.pause_and_clear()
        elif choice == "6":
            utils.clear_screen()
            search_filter.filter_tasks(tasks_list)
            utils.pause_and_clear()
        elif choice == "7":
            logging.info("Пользователь завершил программу")
            print("\nБлагодарим что выбрали нас, до свидания!")
            file_io.save_tasks(tasks_list)
            utils.pause_and_clear()
            break #выход из цикла
        else:
            logging.warning(f"Пользователь ввёл неверный пункт меню: {choice}")
            utils.clear_screen()
            print("Ошибка: нет такого действия")

# условие гарантирует, что код выполнится только если файл запущен напрямую
if __name__ == "__main__":
    main()