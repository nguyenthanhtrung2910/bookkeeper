"""
Описан класс, представляющий расходную операцию
"""

import dataclasses
import datetime


@dataclasses.dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime.datetime = dataclasses.field(
        default_factory=datetime.datetime.now)
    date: str = dataclasses.field(
        default=datetime.datetime.now().strftime('%Y-%m-%d'))
    comment: str = ''
    pk: int = 0
