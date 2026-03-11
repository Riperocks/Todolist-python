# Импорт модулей
import json # работа с json файлом
import os # проверка наличие файла
import subprocess # модуль работы с внешними процессами (современнный стандарт)
import time # модуль работы со временем
from datetime import datetime, timedelta # модуль для работы со временем

filename = "tasks.json" # название файла, где хранятся задачи

# Глобальный список для хранения задач
# Задача будет состоять из полей:
# id: номер задачи
# title: название
# completed: выполнена или нет
tasks = [] # список задач

# функция фильтр
def filter_tasks():
    """Фильтрация задач по различным критериям"""
    print("\n--- Фильтрация задач ---")

    if len(tasks) == 0:
        print("Список задач пуст")
        return
    
    print("Фильтровать по:")
    print("1. Только выполенные")
    print("2. Только невыполненные")
    print("3. Созданные сегодня")
    print("4. Созданные за последние 7 дней")
    print("5. По ID (диапозон)")

    choice = input("\nВыберите фильтр (1-5): ")

    filtered_tasks = []

    if choice == "1":
        filtered_tasks = [task for task in tasks if task['completed']]
        filter_name = "Выполнные задачи"

    elif choice == "2":
        filtered_tasks = [task for task in tasks if not task['completed']]
        filter_name = "Невыполнные задачи"

    elif choice == "3":
        today = datetime.now().date()
        filtered_tasks = []
        for task in tasks:
            if 'created_at' in task:
                try:
                    created = datetime.strptime(task['created_at'], "%d.%m.%Y %H:%M").date()
                    if created == today:
                        filtered_tasks.append(task)
                except:
                    pass
        filter_name = "Задачи, созданные сегодня"
    
    elif choice == "4":
        today = datetime.now().date()
        from datetime import timedelta
        week_ago = today - timedelta(days=7)

        filtered_tasks = []
        for task in tasks:
            if 'created_at' in task:
                try:
                    created = datetime.strptime(task['created_at'], "%d.%m.%Y %H:%M").date()
                    if created >= week_ago:
                        filtered_tasks.append(task)
                except:
                    pass
        filter_name = "Задачи, созданные за последние 7 дней"
    
    elif choice == "5":
        while True:
            try:
                start_id = int(input("Введите начальный ID: "))
                end_id = int(input("Введите конечный ID: "))

                # Защита от отрицательных значений
                if start_id <= 0 or end_id <= 0:
                    print("❌ Ошибка: ID должны быть положительными числами!")
                    continue
            
                # Защита от некорректного диапазона
                if start_id > end_id:
                    print("❌ Ошибка: начальный ID не может быть больше конечного!")
                    continue

                break
            except ValueError:
                print("❌ Ошибка: введите числа! Попробуйте снова.\n")

        filtered_tasks = [task for task in tasks if start_id <= task['id'] <= end_id]
        filter_name = f"ID от {start_id} до {end_id}"
    
    # вывод результата
    if len(filtered_tasks) == 0:
        print(f"\nНет задач, соответствующих фильтру: {filter_name}")
        return
    
    print(f"\nНайдено задач по фильтру '{filter_name}'")
    print("=" * 50)

    for task in filtered_tasks:
        status = "✅" if task['completed'] else "❌"
        print(f"{status} [{task['id']}] {task['title']}")
        
        if 'created_at' in task:
            print(f"   📅 Создано: {task['created_at']}")
        if task['completed'] and 'completed_at' in task:
            print(f"   ✅ Выполнено: {task['completed_at']}")
        print()

# функция поиска
def search_tasks():
    """Поиск задач по названию"""
    print("\n--- Поиск задач ---")

    if len(tasks) == 0:
        print("Список задач пуст")
        return
    
    query = input("Введите текст для поиска: ").lower().strip()

    if query == "":
        print("Поисковый запрос не может быть пустым")
        return
    
    # поиск задачи, где название содержит искомый текст
    found_tasks = []
    for task in tasks:
        if query in task['title'].lower():
            found_tasks.append(task)

    if len(found_tasks) == 0:
        print(f"Задачи с текстом '{query}' не найдены")
        return
    
    print(f"\nНайдено задач: {len(found_tasks)}")
    print("-" * 40)

    for task in found_tasks:
        status = "✅" if task['completed'] else "❌"
        print(f"{status} [{task['id']}] {task['title']}")

        if 'created_at' in task:
            print(f" 📆 Создано: {task['created_at']}")
        if task['completed'] and 'completed_at' in task:
            print(f" ✅ Выполнено: {task['completed_at']}")
        print()

# пересборка ID
def rebuild_ids():
    # Пересборка используется для простоты в данном проекте, однако лучше хранить счетчик отдельно, чтобы не ломать ссылки на задачи или использовать UUID (универсальные идентификаторы, но ID будут выглядеть как случайные числа)
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
    
    new_id = len(tasks) + 1

    # получаем текущую дату и время
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # создание новой задачи
    new_task = {
        # устарело -> 'id': len(tasks) + 1, # простой способ сделать уникальный id (id могут повторяться при удалении (неидеально, но как учебный проект ок, можно хранить счетчик отдельно))
        'id': new_id,
        'title': title,
        'completed': False,
        'created_at': current_time # добавлние даты создания
    }

    # добавление задачи в список
    tasks.append(new_task) #append метод списка, добавляет элемент в конец
    print(f"Задача '{title}' успешно добавлена с ID {new_id}")
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
        print("Ошибка: введите ID")
        return

    # Ищем задачу с таким ID для удаления
    for i, task in enumerate(tasks): # функция получение списка состоящего из индекса и сообщение title
        if task['id'] == task_id:
            # запоминаем название для сообщения
            deleted_title = task['title']
            # удаляем задачу из списка
            tasks.pop(i) # метод списка, который удаляет элемент с индексом i
            rebuild_ids()
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
        # добавляем дату создания, если есть
        date_info = ""
        if 'created_at' in task:
            date_info = f" (создано: {task['created_at']})"
        print(f" ❌ [{task['id']}] {task['title']}{date_info}")
    
    # просим ввести ID
    try:
        task_id = int(input("Введите ID задачи, которую выполнили: "))
    except ValueError:
        print("Ошибка: введите ID")
        return
    
    # ищем задачу
    for task in tasks:
        if task['id'] == task_id:
            if  task['completed']: #проверяем, не выполнена ли уже
                print(f"Задача '{task['title']}' уже отмечена как выполненная")
                if 'completed_at' in task:
                    print(f" ✅ Выполнено: {task['completed_at']}")
            else:
                # получаем такущую дату и время
                current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
                task['completed'] = True # отмечаем как выполненную
                task['completed_at'] = current_time
                print(f" ✅ Задача '{task['title']}' отмечена как выполеннная")
                print(f" 📆 Создано: {task.get('created_at', 'неизвестно')}")
                print(f" ✅ Выполнено: {current_time}")

                # если есть дата создания, показываем сколько дней заняло
                # if 'created_at' in task:
                #     try:
                #         created = datetime.strptime(task['created_at'], "%d.%m.%Y %H:%M")
                #         now = datetime.now()
                #         days_taken = (now - created).days
                #         print(f" ⏱️ Заняло дней: {days_taken}")
                #     except:
                #         pass #если что-то пошло не так, просто пропускаем

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

        # добавление даты
        if 'created_at' in task: # дата создания
            print(f" 📆 Создано: {task['created_at']}")
        if task['completed'] and 'completed_at' in task: # дата выполнения
            print(f" ✅ Выполнено: {task['completed_at']}")

        print()

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
    print("5. Поиск задач")
    print("6. Фильтрация задач")
    print("7. Выйти")
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

        choice = input("Выберите действие (1-7): ")
        
    # проверяем выбор пользователя и вызываем нужную функцию
        if choice == "1":
            clear_screen()
            add_task()
            pause_and_clear()
        elif choice == "2":
            clear_screen()
            show_tasks()
            pause_and_clear()
        elif choice == "3":
            clear_screen()
            complete_task()
            pause_and_clear()
        elif choice == "4":
            clear_screen()
            delete_task()
            pause_and_clear()
        elif choice == "5":
            clear_screen()
            search_tasks()
            pause_and_clear()
        elif choice == "6":
            clear_screen()
            filter_tasks()
            pause_and_clear()
        elif choice == "7":
            print("\nБлагодарим что выбрали нас, до свидания!")
            save_tasks()
            pause_and_clear()
            break #выход из цикла
        else:
            clear_screen()
            print("Ошибка: нет такого действия")
            #pause_and_clear()

# условие гарантирует, что код выполнится только если файл запущен напрямую
if __name__ == "__main__":
    main()