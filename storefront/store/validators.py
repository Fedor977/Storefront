from rest_framework import serializers
import re
from datetime import date


def customer_phone_validate(value):
    sample = r'\+998[93][0134579]\d{7}$'
    if not re.search(sample, value):
        raise serializers.ValidationError('Неверный формат номера')


def customer_validate_birth_date(value: date):
    from datetime import datetime
    current_year = datetime.now().year
    valid_year = current_year - value.year
    if valid_year < 18:
        raise serializers.ValidationError('Ты еще маленький')
