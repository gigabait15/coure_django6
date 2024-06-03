import logging

class CustomFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        # ���������� ��������� � �������� ������ � ��������
        if 'first seen with mtime' in message or 'GET /logs_scheduler/' in message or 'changed, reloading.' in message:
            return False
        # ���������� ��������� � SQL �������� � ����������� �� ������������
        if 'SELECT' in message or 'Watching dir' in message:
            return False
        return True
