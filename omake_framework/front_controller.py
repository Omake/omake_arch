import time


def add_time(request):
    """Добавляем время в реквест"""
    request['time'] = time.time()


fronts_list = [add_time]
