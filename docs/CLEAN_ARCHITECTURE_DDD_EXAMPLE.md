# Clean Architecture and DDD Example

This version uses a backend-only feature and assumes there is no FastMCP server involved.

The goal is to show a simple feature that moves through:

- API routes
- application use cases
- repositories
- domain objects
- the `Result` railway pattern already present in `backend/app/core/results.py`

## The Feature

Feature name: **Todo Management**

User story:

> As a user, I want to create a todo item and mark it as completed.

This is a good beginner example because:

- everyone understands what a todo item is
- the domain is small
- it still needs business rules
- it naturally uses repositories and use cases
- it works well with success and failure flows

## What We Want to Model

The backend will support two actions:

1. create a todo item
2. complete a todo item

Example HTTP API:

- `POST /todos`
- `POST /todos/{todo_id}/complete`
- `GET /todos/{todo_id}`

## The Layers

### 1. Presentation Layer

This is the FastAPI layer.

Responsibilities:

- receive HTTP requests
- parse request data
- call the correct use case
- convert `Result` values into HTTP responses

Example files:

- `backend/main.py`
- `backend/app/presentation/api/todo_routes.py`

This layer should not contain business rules like:

- "title cannot be empty"
- "a completed todo cannot be completed again"

Those belong to the domain or application layer.

### 2. Application Layer

This layer implements the use cases.

Example use cases:

- `CreateTodoUseCase`
- `CompleteTodoUseCase`
- `GetTodoUseCase`

Responsibilities:

- orchestrate the feature flow
- load and save aggregates through repositories
- return `Result` objects instead of throwing business exceptions everywhere

This layer answers:

> "What steps happen when a request tries to create or complete a todo?"

### 3. Domain Layer

This is the business core.

Example domain concepts:

- `Todo`
- `TodoId`
- `TodoTitle`
- `TodoStatus`
- `DomainError`

Responsibilities:

- express business meaning
- enforce invariants
- protect the model from invalid state

This layer answers:

> "What is a valid todo, and what rules does it follow?"

### 4. Infrastructure Layer

This layer implements technical details.

Examples:

- an in-memory repository
- a SQLAlchemy repository later
- UUID generation if treated as an external detail

Responsibilities:

- store and retrieve data
- translate persistence data into domain objects
- implement repository interfaces defined closer to the application/domain

## DDD Concepts in This Example

### Bounded Context

Use a bounded context such as:

- **Task Management**

Inside this context, terms like `todo`, `complete`, `pending`, and `title` have specific meanings.

### Ubiquitous Language

The same words should be used in:

- route names
- DTOs
- use cases
- domain objects
- repository methods

Good vocabulary:

- todo
- title
- pending
- completed
- complete todo
- create todo

Avoid mixing terms like:

- task
- job
- ticket
- item

if they all mean the same thing. That weakens the model.

### Aggregate

`Todo` is a good aggregate root.

It controls its own rules, for example:

- title must not be blank
- a completed todo cannot be completed again

Example:

```python
from dataclasses import dataclass
from typing import Literal

TodoStatus = Literal["pending", "completed"]


@dataclass(frozen=True, slots=True)
class Todo:
    id: str
    title: str
    status: TodoStatus

    @classmethod
    def create(cls, todo_id: str, title: str) -> "Result[Todo, DomainError]":
        normalized_title = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(id=todo_id, title=normalized_title, status="pending"))

    def complete(self) -> "Result[Todo, DomainError]":
        if self.status == "completed":
            return Result.err(TodoAlreadyCompletedError(todo_id=self.id))
        return Result.ok(Todo(id=self.id, title=self.title, status="completed"))
```

### Repository

The repository represents how the application loads and saves aggregates.

Example contract:

```python
from typing import Protocol


class TodoRepository(Protocol):
    async def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]: ...
    async def save(self, todo: Todo) -> Result[Todo, DomainError]: ...
```

The use case depends on this abstraction, not on a concrete database implementation.

### Domain Errors

Domain errors are part of the model language.

Examples:

- `EmptyTodoTitleError`
- `TodoAlreadyCompletedError`
- `TodoNotFoundError`

These errors are useful because they describe business problems, not framework problems.

## Why the Result Railway Pattern Fits Well

This repo already has a reusable `Result` type in `backend/app/core/results.py`.

That is useful for a railway-oriented flow:

- success stays on the success track
- failure stays on the failure track
- each step can stop the flow early without exceptions controlling normal business behavior

Conceptually:

```text
request -> validate -> load/create domain object -> save -> response
           ok           ok                         ok     ok
           err --------> stop and return error response
```

This is especially good for use cases because they often do a sequence of dependent steps.

## End-to-End Flow

### Example 1: Create Todo

#### Request

```http
POST /todos
Content-Type: application/json

{
  "title": "Pay electricity bill"
}
```

#### Route Handler

The API route receives the request and delegates to the use case.

```python
@router.post("/todos")
async def create_todo(request: CreateTodoRequest):
    result = await create_todo_use_case.execute(title=request.title)
    return result.match(
        ok_fn=lambda todo: TodoResponse.model_validate(todo),
        err_fn=map_error_to_http,
    )
```

The route should stay thin. It should not manually enforce the todo rules.

#### Use Case

The use case coordinates the workflow.

```python
class CreateTodoUseCase:
    def __init__(self, todo_repository: TodoRepository, id_generator: IdGenerator):
        self.todo_repository = todo_repository
        self.id_generator = id_generator

    async def execute(self, title: str) -> Result[Todo, DomainError]:
        todo_result = Todo.create(todo_id=self.id_generator.new(), title=title)
        if todo_result.is_err:
            return todo_result

        return await self.todo_repository.save(todo_result.value)
```

This is already railway-oriented:

- create the domain object
- if invalid, stop immediately
- otherwise save it

#### Repository

An in-memory repository might look like this:

```python
class InMemoryTodoRepository:
    def __init__(self) -> None:
        self.items: dict[str, Todo] = {}

    async def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        todo = self.items.get(todo_id)
        if todo is None:
            return Result.err(TodoNotFoundError(todo_id=todo_id))
        return Result.ok(todo)

    async def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.items[todo.id] = todo
        return Result.ok(todo)
```

#### Response

Success response:

```json
{
  "id": "todo-123",
  "title": "Pay electricity bill",
  "status": "pending"
}
```

Failure response when title is blank:

```json
{
  "error": "Todo title cannot be empty"
}
```

### Example 2: Complete Todo

#### Request

```http
POST /todos/todo-123/complete
```

#### Use Case with Result Chaining

This is the most useful place to demonstrate the railway pattern.

```python
class CompleteTodoUseCase:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    async def execute(self, todo_id: str) -> Result[Todo, DomainError]:
        todo_result = await self.todo_repository.get_by_id(todo_id)
        if todo_result.is_err:
            return todo_result

        completed_result = todo_result.value.complete()
        if completed_result.is_err:
            return completed_result

        return await self.todo_repository.save(completed_result.value)
```

The flow is:

1. load todo from repository
2. if not found, stop
3. ask the aggregate to complete itself
4. if already completed, stop
5. save updated aggregate
6. return success

That is a clean railway flow: every step returns either `Ok` or `Err`.

## Suggested Backend Structure

If you want this example to be visible in a clean architecture style, a structure like this is easy to understand:

```text
backend/
  app/
    core/
      results.py
    domain/
      todos/
        entities.py
        errors.py
        value_objects.py
        repositories.py
    application/
      todos/
        create_todo.py
        complete_todo.py
        get_todo.py
    infrastructure/
      todos/
        in_memory_repository.py
    presentation/
      api/
        todo_routes.py
        schemas.py
  main.py
```

## Example Responsibilities by File Type

### API Route

The API route should:

- accept HTTP input
- call a use case
- translate domain/application errors into HTTP status codes

It should not:

- build domain rules itself
- directly talk to the database

### Use Case

The use case should:

- coordinate one business action
- depend on repository interfaces
- return `Result`

It should not:

- know about FastAPI request objects
- know about SQLAlchemy session details

### Repository

The repository should:

- persist and retrieve aggregates
- hide storage details

It should not:

- contain business rules like "cannot complete twice"

### Domain Model

The domain model should:

- enforce invariants
- express the language of the business
- remain framework-independent

## Error Mapping at the API Boundary

This is where the presentation layer adds HTTP semantics.

Example:

```python
def map_error_to_http(error: DomainError):
    if isinstance(error, EmptyTodoTitleError):
        raise HTTPException(status_code=400, detail="Todo title cannot be empty")
    if isinstance(error, TodoNotFoundError):
        raise HTTPException(status_code=404, detail="Todo not found")
    if isinstance(error, TodoAlreadyCompletedError):
        raise HTTPException(status_code=409, detail="Todo is already completed")
    raise HTTPException(status_code=500, detail="Unexpected error")
```

This keeps the domain free from HTTP concerns while still producing proper API responses.

## How It Would Connect to FastAPI

If the current `backend/main.py` grows beyond the root endpoint, it can register a router:

```python
from fastapi import FastAPI
from app.presentation.api.todo_routes import router as todo_router

app = FastAPI()
app.include_router(todo_router, prefix="/api")
```

Then the route module can expose:

- `POST /api/todos`
- `GET /api/todos/{todo_id}`
- `POST /api/todos/{todo_id}/complete`

## Why This Example Works Better for Backend-Only Learning

Compared with a more infrastructure-heavy example, todo management is easier to reason about because:

- there is no external API dependency
- the repository pattern is obvious
- the aggregate rules are easy to explain
- the `Result` pattern has visible success and failure paths
- FastAPI routes can stay very thin

This makes the architecture easier to see.

## Short Summary

If you want a backend-only clean architecture and DDD example in this project, a good feature is:

- **Todo Management**

It demonstrates:

- FastAPI routes as the presentation layer
- use cases as the application layer
- repositories as persistence abstractions
- a `Todo` aggregate in the domain layer
- DDD concepts like bounded context and ubiquitous language
- the `Result` railway pattern for explicit success and failure flow

It is simple, concrete, and fits naturally with the existing `Result` type in the backend.
