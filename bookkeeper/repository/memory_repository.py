"""
Модуль описывает репозиторий, работающий в оперативной памяти
"""

import itertools
import typing

from bookkeeper.repository import abstract_repository


class MemoryRepository(abstract_repository.AbstractRepository[abstract_repository.T]):
    """
    Репозиторий, работающий в оперативной памяти. Хранит данные в словаре.
    """

    def __init__(self) -> None:
        self._container: dict[int, abstract_repository.T] = {}
        self._counter = itertools.count(1)

    def add(self, obj: abstract_repository.T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> abstract_repository.T | None:
        return self._container.get(pk)

    def get_all(self, where: dict[str, typing.Any] | None = None) -> list[abstract_repository.T]:
        if where is None:
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: abstract_repository.T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        self._container.pop(pk)
