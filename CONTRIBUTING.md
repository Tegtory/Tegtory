# Contributing Guide

## Stack

- python 3.12+
- aiogram

## Architecture

```text
.
├── docker
├── protos
│   └── tegtory
├── tegtory
│   ├── common # config/exceptions
│   ├── domain # domain logic
│   │   ├── commands
│   │   ├── entities
│   │   ├── events
│   │   ├── interfaces
│   │   ├── queries
│   │   ├── services # domain services
│   │   └── use_cases # domain use cases splited by type
│   │       ├── commands # commands use cases perform an action and not return any data. Only action result
│   │       ├── event # event use cases executes on events
│   │       └── queries # queries use cases only return data
│   ├── infrastructure
│   │   ├── events # event specific infrastructure
│   │   ├── migration # migrations for database
│   │   │   └── versions
│   │   └── repositories # interfaces implementations
│   ├── presenters
│   │   └── aiogram # Tegtory bot implementation
│   │       ├── filters
│   │       ├── handlers
│   │       │   ├── city
│   │       │   └── factory
│   │       ├── kb
│   │       ├── messages
│   │       ├── middlewares
│   │       ├── states
│   │       └── utils
│   └── static # static resources like images, videos, etc.
│       └── tegtory
└── tests # tests for domain, infrastructure, presenters, services, use cases
    ├── entities
    ├── presenters
    ├── services
    └── use_cases
```

---

# Philosophy

Project architecture was built with clean code in mind. So here you can find some layers (domain, infrastructure, presenters), CQRS, Entities, Dependency injection and other

## `domain/` - clean business logic

### `domain/commands domain/queries` - Commands/Queries data declaration

```python
# domain/commands/shop.py
from tegtory.domain.commands.base import BaseCommand


class CreateShopCommand(BaseCommand):  # 1
    title: str
```

1. every command/query must have *Command/*Query naming and must inherit Base(Command/Query)

### `domain/entities` - Data transfer object or just Entities

we want to create a unit that have: title, health, mana

```python
import dataclasses

@dataclasses.dataclass(kw_only=True) # 1
class Unit:
    title: str
    health: int = 100
    mana: int = 100
```

1. entities are built with dataclasses with kw_only

### `domain/interfaces` - repository protocols

we want to get all units, but in domain layer we can't work with real database, what we need to do?

1. define protocol

    ```python
   from typing import Protocol
   
   class CrudRepository(Protocol):
       async def all(self) -> list: ...
    ```

2. use it in command/query handler
    ```python

    ```


- #1 All protocols functions must be async, and typed

---


# Commit/Push rules

## Automated check (Recommended)

1. set-up pre-commit
   ```bash
   pip install pre-commit
   pre-commit install
   ```

now when using `git commit -m ""` tests will check automatically

## Manual Check

before every commit/push ensure that all linters and tests passed

```bash
ruff format # format code to keep it clean
pytest # check that all existing functional working
mypy . # check that all functions typed correctly
ruff check --fix # check some coding format rules
```

this page is under TODO, be patient. It will be updated very soon

You can help to improve this project. Every contribution is welcome!
