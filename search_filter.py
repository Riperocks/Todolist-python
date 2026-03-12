"""
Функции поиска и фильтрации (ТВОЙ КОД)
"""

import logging
from datetime import datetime, timedelta

# функция поиска
def search_tasks(tasks):
    """Поиск задач по названию"""
    logging.debug("Вызвана функция search_tasks()")
    print("\n--- Поиск задач ---")

    if len(tasks) == 0:
        logging.info("Поиск в пустом списке задач")
        print("Список задач пуст")
        return
    
    query = input("Введите текст для поиска: ").lower().strip()
    logging.info(f"Поисковый запрос: '{query}'")

    if query == "":
        logging.warning("Пустой поисковый запрос")
        print("Поисковый запрос не может быть пустым")
        return
    
    # поиск задачи, где название содержит искомый текст
    found_tasks = []
    for task in tasks:
        if query in task['title'].lower():
            found_tasks.append(task)

    if len(found_tasks) == 0:
        logging.info(f"По запросу '{query}' ничего не найдено")
        print(f"Задачи с текстом '{query}' не найдены")
        return
    
    logging.info(f"По запросу '{query}' найдено {len(found_tasks)} задач")
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

# функция фильтр
def filter_tasks(tasks):
    """Фильтрация задач по различным критериям"""
    logging.debug("Вызвана функция filter_tasks()")
    print("\n--- Фильтрация задач ---")

    if len(tasks) == 0:
        logging.info("Фильтрация в пустом списке задач")
        print("Список задач пуст")
        return
    
    print("Фильтровать по:")
    print("1. Только выполенные")
    print("2. Только невыполненные")
    print("3. Созданные сегодня")
    print("4. Созданные за последние 7 дней")
    print("5. По ID (диапозон)")

    choice = input("\nВыберите фильтр (1-5): ")
    logging.info(f"Выбран фильтр: {choice}")

    filtered_tasks = []
    filter_name = ""

    if choice == "1":
        filtered_tasks = [task for task in tasks if task['completed']]
        filter_name = "Выполнные задачи"
        logging.info(f"Фильтр: выполненные задачи")

    elif choice == "2":
        filtered_tasks = [task for task in tasks if not task['completed']]
        filter_name = "Невыполнные задачи"
        logging.info(f"Фильтр: невыполненные задачи")

    elif choice == "3":
        today = datetime.now().date()
        filtered_tasks = []
        for task in tasks:
            if 'created_at' in task:
                try:
                    created = datetime.strptime(task['created_at'], "%d.%m.%Y %H:%M").date()
                    if created == today:
                        filtered_tasks.append(task)
                except Exception as e:
                    logging.error(f"Ошибка при обработке даты: {e}")
        filter_name = "Задачи, созданные сегодня"
        logging.info(f"Фильтр: задачи за сегодня")
    
    elif choice == "4":
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        filtered_tasks = []
        
        for task in tasks:
            if 'created_at' in task:
                try:
                    created = datetime.strptime(task['created_at'], "%d.%m.%Y %H:%M").date()
                    if created >= week_ago:
                        filtered_tasks.append(task)
                except Exception as e:
                    logging.error(f"Ошибка при обработке даты: {e}")
        filter_name = "Задачи, созданные за последние 7 дней"
        logging.info(f"Фильтр: задачи за 7 дней")
    
    elif choice == "5":
        while True:
            try:
                start_id = int(input("Введите начальный ID: "))
                end_id = int(input("Введите конечный ID: "))
                logging.info(f"Фильтр по ID: от {start_id} до {end_id}")

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
                logging.warning("Пользователь ввёл не число при фильтре по ID")
                print("❌ Ошибка: введите числа! Попробуйте снова.\n")

        filtered_tasks = [task for task in tasks if start_id <= task['id'] <= end_id]
        filter_name = f"ID от {start_id} до {end_id}"
    
    # вывод результата
    if len(filtered_tasks) == 0:
        logging.info(f"По фильтру '{filter_name}' ничего не найдено")
        print(f"\nНет задач, соответствующих фильтру: {filter_name}")
        return
    
    logging.info(f"По фильтру '{filter_name}' найдено {len(filtered_tasks)} задач")
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

if __name__ == "__main__":
    # Здесь можно сразу проверить работу функции
    test_data = [
        {'id': 1, 'title': 'тест1', 'completed': False},
        {'id': 2, 'title': 'тест2', 'completed': True},
        {'id': 3, 'title': 'тест3', 'completed': True}
    ]
    
    print("Тест фильтрации:")
    result = [t for t in test_data if t['completed']]
    print(f"Найдено выполненных: {len(result)}")