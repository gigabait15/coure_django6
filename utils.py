import logging

class CustomFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        # Фильтрация сообщений о загрузке файлов и запросах
        if 'first seen with mtime' in message or 'GET /logs_scheduler/' in message or 'changed, reloading.' in message:
            return False
        # Исключение сообщений о SQL запросах и наблюдениях за директориями
        if 'SELECT' in message or 'Watching dir' in message:
            return False
        return True
