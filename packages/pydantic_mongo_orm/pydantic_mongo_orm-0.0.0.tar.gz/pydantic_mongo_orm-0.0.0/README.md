# Pydantic Mongo ORM

Pydantic Mongo ORM is a library that allows users to map Pydantic models to MongoDb.

## Installation
```pip install pydantic_mongo_orm```

## Usage

### Models

PMO uses Pydantic models to represent data in database. To start using it, you need to create new model based on
`pydantic_mongo_orm.BaseModel`. This class implements all the features from Pydantic but also adds some
orm-specific functionality, e.g. adds read-only field `id` that represents document-id (`_id`) from MongoDb:

```python
from pydantic_mongo_orm import BaseModel

class MyModel(BaseModel):
    greeting: str

my_model = MyModel(greeting='Hello World!')

print(my_model.greeting)  # >> 'Hello World!'
print(my_model.id)  # >> uuid.UUID4('2daaa0ac-501b-4018-9101-cc822a37c1a1')
```

You may also specify `mongo_config` for each model class that further modifies ORM behaviour:

```python
from pydantic_mongo_orm import BaseModel, MongoConfigDict

class MyModel(BaseModel):
    greeting: str

    mongo_config = MongoConfigDict(collection='my_model')
```

Available options are:
- `collection`: Name of the collection where the model will be stored. By default, it's detected from the class
    name.
- `objects_class`: Class that will be used as an object storage for given model. By default, `ObjectsStorage` is
    used. Explained later 


### Storage

The base of PMO is `Storage` - class connected to MongoDb able to map models to objects and vice-versa.

Connect to MongoDb and save new instance of MyModel from previous example:

```python
from pydantic_mongo_orm import Storage

storage = Storage(host='mongodb://127.0.0.1:27017', db_name='local')
storage.connect()

my_model = MyModel(greeting='Hello World!')
storage.save(my_model)

my_models = storage.find(MyModel, {'greeting': 'Hello World!'})
print(list(my_models))  # [MyModel greetings: 'Hello World!']
```

### Bound objects
You may use `Storage` object directly but PMO offers a shorthand that simplifies working with the ORM. Each
model class provides attribute `objects` that provides direct access to collection storing that particular model.
To enable this feature, you must first bind the `Storage` to the `BaseModel` using `.bind()`. This example is
equivalent with the previous one:

```python
from pydantic_mongo_orm import Storage

storage = Storage(host='mongodb://127.0.0.1:27017', db_name='local')
storage.connect()
storage.bind()

my_model = MyModel(greeting='Hello World!')
my_model.save()

my_models = MyModel.objects.find({'greeting': 'Hello World!'})
print(list(my_models))  # [MyModel greetings: 'Hello World!']
```

By default, the `objects` attribute contains an instance of `pydantic_mongo_orm.ObjectsStorage`. It provides the
same functionality as `pydantic_mongo_orm.Storage`. If you wish to customize behaviour of certain model - change
how it's stored, add custom filters etc., you may extend the `ObjectsStorage` class, add new functionality and
then configure it to be used for your models:

```python
from pydantic_mongo_orm import BaseModel, ObjectsStorage, Storage, MongoConfigDict


class RectangleStorage(ObjectsStorage):
    def squares(self):
        return self.find({'$where': 'this.x == this.y'})

    
class Rectangle(BaseModel):
    mongo_config = MongoConfigDict(objects_class=RectangleStorage)

    length: int
    width: int

    
storage = Storage(host='mongodb://127.0.0.1:27017', db_name='local')
storage.connect()
storage.bind()

my_square = Rectangle(x=5, y=5)
my_square.save()

my_rectangle = Rectangle(x=5, y=10)
my_rectangle.save()

print(list(Rectangle.objects.squares()))  # >> [Rectangle x=5 y=5]
```