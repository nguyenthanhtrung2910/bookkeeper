"""
Модуль содержит описание абстрактного репозитория

Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
идентификатор в атрибуте pk (primary key). Объекты, которые могут быть сохранены
в репозитории, должны поддерживать добавление атрибута pk и не должны
использовать его для иных целей.
"""

import abc
import typing


class Model(typing.Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут pk
    """
    pk : int


T = typing.TypeVar('T', bound=Model)


class AbstractRepository(abc.ABC, typing.Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    @abc.abstractmethod
    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """

    @abc.abstractmethod
    def get(self, pk: int) -> T | None:
        """ Получить объект по id """

    @abc.abstractmethod
    def get_all(self, where: dict[str, typing.Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    @abc.abstractmethod
    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

    @abc.abstractmethod
    def delete(self, pk: int) -> None:
        """ Удалить запись """
