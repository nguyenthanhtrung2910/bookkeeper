from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет
    amount - сумма
    category - id категории расходов
    tern - срок использования
    pk - id записи в базе данных
    """
    amount: int
    category: int
    tern: str = 'month'
    pk: int = 0
