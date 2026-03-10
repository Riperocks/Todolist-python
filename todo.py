# Импорт модулей
import json # работа с json файлом
import os # проверка наличие файла
import subprocess # модуль работы с внешними процессами (современнный стандарт)
import time # модуль работы со временем

filename = "tasks.json" # название файла, где хранятся задачи

# Глобальный список для хранения задач
# Задача будет состоять из полей:
# id: номер задачи
# title: название
# completed: выполнена или нет
tasks = [] # список задач

# пересборка ID
def rebuild_ids():
    """Переназначает ID всем задачам по порядку"""
    for i, task in enumerate(tasks, start=1):
        task['id'] = i

# пауза и очистка экрана
def pause_and_clear():
    """Пауза и очистка экрана"""
    input("\nНажмите Enter для продолжения...")
    time.sleep(0.3) # задержка
    clear_screen()

# очистка экрана
def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear') # 'nt' - для Windows (NT - технология Wimdows)
    
    # альтернатива, современный способ с subprocess (безопасный метод для современных проектов, позволяющий вернуть все: код возврата, вывод команды, ошибки и др. без возвожности подсунуть чужую команду)
    # if os.name == 'nt':
    #   subprocess.run('cls', shell=True)
    # else:
    #   subprocess.run('clear', shell=True)

# функция загрузки задач из файла
def load_tasks():
    """Загрузка задачи из json файла"""
    global tasks # глобальная переменная tasks, для изменения внешней переменной

    # условие проверки файла
    if os.path.exists(filename):
        # открытие файла для чтения (из-за 'r')
        with open(filename, 'r', encoding='utf-8') as file: # конструкция with open закрывает файл после работы
            tasks = json.load(file) # загрузка данных из json
        print(f"Загружено {len(tasks)} задач из файла") # f-строка, стандарт при вставление переменных в текст
    else:
        print("Файл с задачами не найден, начинаем с пустого списка")
        tasks = [] # создает пустой файл при else

# функция сохранения задач в файл
def save_tasks():
    """Сохранение задачи в json файл"""
    with open(filename, 'w', encoding='utf-8') as file: # 'w' - запись, будет создан или перезаписан
        json.dump(tasks, file, ensure_ascii=False, indent=2) # json.dump функция из модуля json для записи в файл, сохраняем tasks в открытый файл file. Ensure_ascii=False не позволит заменить буквы на коды
    print("Задачи сохранены")

# функция добавления новой задачи
def add_task():
    """Добавление новой задачи"""
    print("\n--- Добавление новой задачи ---") # /n "новая строка" (перевод строки)

    # просим юзера ввести задачу
    title = input ("Введите название задачи: ") 

    # проверка на пустое значение
    if title == "":
        print("Ошибка: название не может быть пустым")
        return
    
    # создание новой задачи
    new_task = {
        'id': len(tasks) + 1, # простой способ сделать уникальный id (id могут повторяться при удалении (неидеально, но как учебный проект ок, можно хранить счетчик отдельно))
        'title': title,
        'completed': False
    }

    # добавление задачи в список
    tasks.append(new_task) #append метод списка, добавляет элемент в конец
    print(f"Задача '{title}' успешно добавлена с ID {new_task['id']}")
    save_tasks() # сразу сохраняем в файл

# функция удаления задачи
def delete_task():
    """Удаляет задачу по ID"""
    print("\n--- Удаление задачи ---")

    # вызов всех задач для уточнения информации по ID
    show_tasks()

    if len(tasks) == 0:
        return # если задач нет, то выходим

    try: # try - "попробуй выполнить следующий код, в случае ошибки перейдет в except"
        task_id = int(input("Введите ID задачи для удаления: "))
    except ValueError: # except - "если случилась ошибка, то выполняй это", но ошибка должна быть конкретизированной ValueError (неправильное значение, в нашем случае если строка не число типа int)
        print("Ошибка: ввидите число")
        return

    # Ищем задачу с таким ID для удаления
    for i, task in enumerate(tasks): # функция получение списка состоящего из индекса и сообщение title
        if task['id'] == task_id:
            # запоминаем название для сообщения
            deleted_title = task['title']
            # удаляем задачу из списка
            tasks.pop(i) # метод списка, который удаляет элемент с индексом i
            print(f"Задача '{deleted_title}' удалена")
            save_tasks() # сохраняем изменения
            return
    
    # если не нашли задачу с таким ID
    print(f"Задача с ID {task_id} не найдена")

# функция для отметки задачи как выполненной
def complete_task():
    """Отмечает задачу как выполненную"""
    print("\n--- Отметка задачи как выполненная ---")

    # показываем только невыполненные задачи
    incomplete_tasks = [task for task in tasks if not task['completed']] # списковое включение (list comprehension) - создаем список из task(1), беря значения task(2) в списке tasks, применяя условие task['completed'] является false (невыполенные)
    

    if len(incomplete_tasks) == 0:
        print("Нет невыполненных задач")
        return

    # выводим список невыполненных задач
    print("Невыполенные задачи:")
    for task in incomplete_tasks:
        status = "❌" if not task['completed'] else "✅"
        print(f" {status} [{task['id']}] {task['title']}")
    
    # просим ввести ID
    try:
        task_id = int(input("Введите ID задачи, которую выполнили: "))
    except ValueError:
        print("ошибка: введите число")
        return
    
    # ищем задачу
    for task in tasks:
        if task['id'] == task_id:
            if  task['completed']: #проверяем, не выполнена ли уже
                print(f"Задача '{task['title']}' уже отмечена как выполненная")
            else:
                task['completed'] = True # отмечаем как выполненную
                print(f"Задача '{task['title']}' отмечена как выполеннная")
                save_tasks()
            return
    
    print(f"Задача с ID {task_id} не найдена")

# функция  для показа всех задач
def show_tasks():
    """Показывает все задачи"""
    print("\n--- Список всех задач ---")

    if len(tasks) == 0:
        print("Список задач пуст")
        return
    
    # проходим по всем задач и выводим их
    for task in tasks:
        status = "✅" if task['completed'] else "❌"
        print(f"{status} [{task['id']}] {task['title']}")

    # считаем статистику
    total = len(tasks)
    completed = sum(1 for task in tasks if task['completed'])
    print(f"\nИтого: всего {total}, выполнено {completed}, осталось {total - completed}")

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
    print("5. Выйти")
    print("="*40)

# Главная функция программы
def main():
    """Главная функция программы"""

    clear_screen()

    print("Добро пожаловать в программу 'Список дел'")

    # загрузка задач при старте
    load_tasks()

    # Бесконечный цикл программы
    while True:
        show_menu() #показ меню

        choice = input("Выберите действие (1-5): ")
        
    # проверяем выбор пользователя и вызываем нужную функцию
        if choice == "1":
            add_task()
            pause_and_clear()
        elif choice == "2":
            show_tasks()
            pause_and_clear()
        elif choice == "3":
            complete_task()
            pause_and_clear()
        elif choice == "4":
            delete_task()
            pause_and_clear()
        elif choice == "5":
            print("\nБлагодарим что выбрали нас, до свидания!")
            save_tasks()
            pause_and_clear()
            break #выход из цикла
        else:
            print("Ошибка: нет такого действия")

# условие гарантирует, что код выполнится только если файл запущен напрямую
if __name__ == "__main__":
    main()