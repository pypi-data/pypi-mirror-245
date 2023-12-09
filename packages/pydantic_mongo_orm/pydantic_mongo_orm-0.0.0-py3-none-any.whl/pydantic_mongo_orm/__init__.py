"""Pydantic Mongo ORM is a library that allows users to map Pydantic models to MongoDb."""

from __future__ import annotations

import re
import abc
import functools
import uuid

import pymongo
import pydantic

from typing_extensions import TypedDict, ClassVar
from typing import Any, Iterator, Generic, TypeVar, cast


T = TypeVar('T', bound='BaseModel')


class OrmError(Exception):
    """Error raised by Pydantic Mongo ORM."""


class MongoConfigDict(TypedDict, total=False):
    """A TypedDict for configuring MongoDb behaviour."""

    collection: str  # collection name where the configured model is stored
    objects_class: type[ObjectsStorage]


class ObjectsStorageAccessor:
    """Accessor of model storage.

    This model is required by specifics of Pydantic. We want the `objects` attribute of BaseModel to be a class
    property, not a class method. But to do so, we would have to implement new metaclass that would implement it. This
    is prohibited by Pydantic that already uses complex metaclass for `pydantic.BaseClass`.

    When Pydantic initializes new model class, it iterates over all the attributes and if the attribute is typed using
    `ClassVar`, it creates new property in the metaclass and assigns the default value to it. In the process of getting
    the value, it unintentionally calls `ObjectsStorageAccessor.__get__` which provides the final instance of
    `ObjectsStorage`.

    As an accessor, the `ObjectsStorageAccessor` has access to the owner. In this case, since it's assigned within a
    metaclass, it's the instance of the BaseModel class, not the object.
    """

    def __get__(self, instance: T, owner: type[T]) -> ObjectsStorage[T]:
        """Get model storage for the class where this accessor was initialized.

        Class used as a model storage may be configured in `mongo_config.objects_class` on the specific model class.
        Otherwise, `ObjectsStorage` is used.
        """
        storage_class = owner._get_mongo_storage_class()
        return storage_class(owner)


class ObjectsStorage(Generic[T]):
    """Bound object used to manipulate subset of BaseModel instances."""

    _storage: ClassVar[Storage | None] = None

    def __init__(self, model_class: type[T]) -> None:
        self.model_class = model_class

    @property
    def storage(self) -> Storage:
        """Get bound MongoDb storage."""
        if self.__class__._storage:
            return self.__class__._storage
        raise OrmError('ObjectStorage has no bound storage. Bind an Storage using `Storage(...).bind()`.')

    def find_one(self, filter: dict[str, Any],) -> T | None:
        """Find one of bound object."""
        return self.storage.find_one(self.model_class, filter)

    def get(self, id: uuid.UUID) -> T | None:
        """Get bound object by id."""
        return self.storage.get(self.model_class, id)

    def find(self, filter: dict[str, Any], sort: list[tuple[str, str]] | None = None, limit: int = 0) -> Iterator[T]:
        """Find bound objects using filters."""
        return self.storage.find(model_class=self.model_class, filter=filter, sort=sort, limit=limit)

    def all(self, sort: list[tuple[str, str]] | None = None, limit: int = 0) -> Iterator[T]:
        """Get all bound objects."""
        return self.storage.all(model_class=self.model_class, sort=sort, limit=limit)

    def save(self, model: T) -> None:
        """Save object to MongoDb."""
        self.storage.save(model)

    def delete(self, model: T) -> None:
        """Delete object from MongoDb."""
        self.storage.delete(model)

    def count(self, filter: dict[str, Any] | None = None) -> int:
        """Count objects in MongoDb."""
        return self.storage.count(model_class=self.model_class, filter=filter)


class BaseModel(pydantic.BaseModel, abc.ABC):
    """Extension of `pydantic.BaseModel` that adds handling of MongoDb."""

    mongo_config: ClassVar[MongoConfigDict] = MongoConfigDict()
    objects: ClassVar[ObjectsStorage] = cast(ObjectsStorage, ObjectsStorageAccessor())

    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True, description='Unique identifier of a Model')

    @classmethod
    @functools.cache
    def _get_mongo_collection_name(cls) -> str:
        """Get name of mongo collection used with this model."""
        collection = cls.mongo_config.get('collection', cls.__name__)
        collection = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', collection)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', collection).lower()

    @classmethod
    @functools.cache
    def _get_mongo_storage_class(cls) -> type[ObjectsStorage]:
        """Get name of mongo collection used with this model."""
        return cls.mongo_config.get('objects_class', ObjectsStorage)

    def save(self) -> None:
        """Save object to MongoDb."""
        self.objects.save(self)

    def delete(self) -> None:
        """Delete object from MongoDb."""
        self.objects.delete(self)


class Storage:
    """ORM storage connected to MongoDb that can manipulate BaseModels."""

    def __init__(self, host: str, db_name: str) -> None:
        self.host = host
        self.db_name = db_name

        self._client: pymongo.MongoClient | None = None
        self._db: pymongo.database.Database | None = None

    @property
    def db(self) -> pymongo.database.Database:
        """Get connected MongoDb database."""
        if self._db:
            return self._db
        raise OrmError('Storage is not connected. Connect to MongoDb using `Storage(...).connect()`.')

    def connect(self) -> None:
        """Connect to MongoDb."""
        self._client = pymongo.MongoClient(self.host, uuidRepresentation='standard')
        self._db = self._client.get_database(self.db_name)

    def disconnect(self) -> None:
        """Disconnect from MongoDb."""
        if self._client:
            self._client.close()
        self._client = None
        self._db = None

    def bind(self) -> None:
        """Bind this storage to BaseModel object storages.

        Ensures that `BaseModel.objects` uses this connection to manipulate with objects.
        """
        ObjectsStorage._storage = self

    def save(self, model: T) -> None:
        """Save object to MongoDb."""
        collection = self._get_model_collection(model)
        data = self._serialize_model(model)
        collection.update_one({'_id': model.id}, {'$set': data}, upsert=True)

    def delete(self, model: T) -> None:
        """Delete object from MongoDb."""
        collection = self._get_model_collection(model)
        collection.delete_one({'_id': model.id})

    def find_one(self, model_class: type[T], filter: dict[str, Any]) -> T | None:
        """Find one object."""
        collection = self._get_model_collection(model_class)
        if data := collection.find_one(filter):
            return self._deserialize_model(model_class, data)
        return None

    def get(self, model_class: type[T], id: uuid.UUID) -> T | None:
        """Get object by its id."""
        return self.find_one(model_class, {'_id': id})

    def find(
        self, model_class: type[T], filter: dict[str, Any], sort: list[tuple[str, str]] | None = None, limit: int = 0
    ) -> Iterator[T]:
        """Find all objects that match given filter."""
        collection = self._get_model_collection(model_class)
        for document in collection.find(filter=filter or {}, sort=sort, limit=limit):
            yield self._deserialize_model(model_class, document)

    def all(self, model_class: type[T], sort: list[tuple[str, str]] | None = None, limit: int = 0) -> Iterator[T]:
        """Find all objects."""
        collection = self._get_model_collection(model_class)
        for document in collection.find(filter={}, sort=sort, limit=limit):
            yield self._deserialize_model(model_class, document)

    def count(self, model_class: type[T], filter: dict[str, Any] | None = None) -> int:
        """Count objects that match filters."""
        collection = self._get_model_collection(model_class)
        return collection.count_documents(filter or {})

    def _serialize_model(self, model: T) -> dict[str, Any]:
        """Serialize model to dict that can be stored in MongoDb."""
        return model.model_dump(exclude={'id'})

    def _deserialize_model(self, model_class: type[T], data: dict[str, Any]) -> T:
        """Deserialize model from MongoDb data."""
        data['id'] = data.pop('_id')
        return model_class.model_validate(data)

    def _get_model_collection(self, model: T | type[T]) -> pymongo.collection.Collection:
        """Get collection where given model is stored."""
        model_class = model if isinstance(model, type) else model.__class__
        collection_name = model_class._get_mongo_collection_name()
        return self.db.get_collection(collection_name)
