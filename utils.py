"""
Вспомогательные функции
"""
import time # модуль работы со временем
import os
import subprocess # модуль работы с внешними процессами (современнный стандарт)
import logging

# пересборка ID
def rebuild_ids(tasks):
    # Пересборка используется для простоты в данном проекте, однако лучше хранить счетчик отдельно, чтобы не ломать ссылки на задачи или использовать UUID (универсальные идентификаторы, но ID будут выглядеть как случайные числа)
    """Переназначает ID всем задачам по порядку"""
    logging.debug(f"Пересборка ID для {len(tasks)} задач")
    old_ids = [task['id'] for task in tasks]
    for i, task in enumerate(tasks, start=1):
        task['id'] = i
    logging.info(f"ID пересобраны: было {old_ids}, стало {[task['id'] for task in tasks]}")
    return tasks

# пауза и очистка экрана
def pause_and_clear():
    """Пауза и очистка экрана"""
    logging.debug("Пауза перед очисткой")
    input("\nНажмите Enter для продолжения...")
    time.sleep(0.3) # задержка
    clear_screen()

# очистка экрана
def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear') # 'nt' - для Windows (NT - технология Wimdows)
    logging.debug("Экран очищен")
    
    # альтернатива, современный способ с subprocess (безопасный метод для современных проектов, позволяющий вернуть все: код возврата, вывод команды, ошибки и др. без возвожности подсунуть чужую команду)
    # if os.name == 'nt':
    #   subprocess.run('cls', shell=True)
    # else:
    #   subprocess.run('clear', shell=True)

if __name__ == "__main__":
    print("Тестируем очистку экрана...")
    clear_screen()
    print("Если экран очистился - всё работает!")
    
    # Тест пересборки ID
    test_tasks = [{'id': 5, 'title': 'тест'}]
    result = rebuild_ids(test_tasks)
    print(f"ID после пересборки: {result[0]['id']} (должен быть 1)")