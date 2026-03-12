"""
Основные функции работы с задачами
"""

from datetime import datetime
import file_io
import utils
import logging

# функция добавления новой задачи
def add_task(tasks):
    """Добавление новой задачи"""
    logging.debug("Начало функции add_task")
    print("\n--- Добавление новой задачи ---") # /n "новая строка" (перевод строки)

    # просим юзера ввести задачу
    title = input ("Введите название задачи: ") 

    # проверка на пустое значение
    if title == "":
        logging.warning("Попытка добавить пустую задачу")
        print("Ошибка: название не может быть пустым")
        return tasks
    
    new_id = len(tasks) + 1
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M") # получаем текущую дату и время
    
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
    logging.info(f"Добавлена задача ID={new_id}: '{title}'")
    print(f"Задача '{title}' успешно добавлена с ID {new_id}")
    file_io.save_tasks(tasks) # сразу сохраняем в файл
    return tasks

# функция  для показа всех задач
def show_tasks(tasks):
    """Показывает все задачи"""
    logging.debug(f"Вызвана функция show_tasks() с {len(tasks)} задачами")
    print("\n--- Список всех задач ---")

    if len(tasks) == 0:
        logging.info("Список задач пуст")
        print("Список задач пуст")
        return
    
    completed_count = 0
    # проходим по всем задач и выводим их
    for task in tasks:
        if task['completed']:
            completed_count += 1
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
    completed = completed_count
    print(f"\nИтого: всего {total}, выполнено {completed}, осталось {total - completed}")

# функция для отметки задачи как выполненной
def complete_task(tasks):
    """Отмечает задачу как выполненную"""
    logging.debug("Вызвана функция complete_task()")
    print("\n--- Отметка задачи как выполненная ---")

    # показываем только невыполненные задачи
    incomplete_tasks = [task for task in tasks if not task['completed']] # списковое включение (list comprehension) - создаем список из task(1), беря значения task(2) в списке tasks, применяя условие task['completed'] является false (невыполенные)
    

    if len(incomplete_tasks) == 0:
        logging.info("Все задачи уже выполнены")
        print("Нет невыполненных задач")
        return tasks

    # выводим список невыполненных задач
    print("Невыполенные задачи:")
    for task in incomplete_tasks:
        date_info = "" # добавляем дату создания, если есть
        if 'created_at' in task:
            date_info = f" (создано: {task['created_at']})"
        print(f" ❌ [{task['id']}] {task['title']}{date_info}")
    
    # просим ввести ID
    try:
        task_id = int(input("Введите ID задачи, которую выполнили: "))
        logging.info(f"Пользователь ввёл ID для выполнения: {task_id}")
    except ValueError:
        logging.warning("Пользователь ввёл не число")
        print("Ошибка: введите ID")
        return tasks
    
    # ищем задачу
    for task in tasks:
        if task['id'] == task_id:
            if  task['completed']: #проверяем, не выполнена ли уже
                logging.info(f"Попытка отметить уже выполненную задачу ID={task_id}")
                print(f"Задача '{task['title']}' уже отмечена как выполненная")
                if 'completed_at' in task:
                    print(f" ✅ Выполнено: {task['completed_at']}")
            else:
                # получаем такущую дату и время
                current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
                task['completed'] = True # отмечаем как выполненную
                task['completed_at'] = current_time
                logging.info(f"✅ Задача ID={task_id} '{task['title']}' выполнена")
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
                file_io.save_tasks(tasks)
            return tasks
    
    logging.warning(f"Пользователь попытался отметить несуществующий ID={task_id}")
    print(f"Задача с ID {task_id} не найдена")
    return tasks

# функция удаления задачи
def delete_task(tasks):
    """Удаляет задачу по ID"""
    logging.debug("Начало функции delete_task")
    print("\n--- Удаление задачи ---")

    # вызов всех задач для уточнения информации по ID
    show_tasks(tasks)

    if len(tasks) == 0:
        return tasks # если задач нет, то выходим

    try: # try - "попробуй выполнить следующий код, в случае ошибки перейдет в except"
        task_id = int(input("Введите ID задачи для удаления: "))
        logging.info(f"Пользователь ввёл ID для удаления: {task_id}")
    except ValueError: # except - "если случилась ошибка, то выполняй это", но ошибка должна быть конкретизированной ValueError (неправильное значение, в нашем случае если строка не число типа int)
        logging.warning("Пользователь ввёл не число при удалении")
        print("Ошибка: введите ID")
        return tasks

    # Ищем задачу с таким ID для удаления
    for i, task in enumerate(tasks): # функция получение списка состоящего из индекса и сообщение title
        if task['id'] == task_id:
            deleted_title = task['title'] # запоминаем название для сообщения
            tasks.pop(i) # 1. удаляем задачу из списка 2. метод списка, который удаляет элемент с индексом i
            tasks = utils.rebuild_ids(tasks)
            logging.info(f"Удалена задача ID={task_id}: '{deleted_title}'")
            print(f"Задача '{deleted_title}' удалена")
            file_io.save_tasks(tasks) # сохраняем изменения
            return tasks
    
    # если не нашли задачу с таким ID
    logging.warning(f"Попытка удалить несуществующий ID={task_id}")
    print(f"Задача с ID {task_id} не найдена")
    return tasks

