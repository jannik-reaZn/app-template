# Todo Backend Architecture Improvements

Step 1 from the original proposal is intentionally omitted.

## 2. Deepen the application module instead of exposing thin use-case wrappers

Files:

- `backend/app/todos/application/use_cases/create_todo_use_case.py`
- `backend/app/todos/application/use_cases/get_todo_use_case.py`
- `backend/app/todos/presentation/dependencies/todo_dependencies.py`

Problem:
The current use-case modules are shallow. `CreateTodoUseCase` forwards to `Todo.create(...)` and the repository. `GetTodoUseCase` forwards directly to the repository. The dependency module mostly wires constructors. By the deletion test, these modules do not currently buy much locality or leverage.

Solution:
Replace the per-use-case wrappers with one deeper todo application module that owns the feature's application seam. Presentation code should depend on this single module rather than on several near-empty wrappers.

Benefits:

- Better locality for feature-flow changes.
- More leverage from a smaller interface.
- Fewer files to bounce through when reading the todo slice.
- Tests can target the application seam instead of thin wrappers.

Implementation status:

- Implemented in this branch by introducing `TodoApplicationService` and routing the presentation layer through that seam.

## 3. Add a presentation adapter so route handlers stop knowing domain internals

Files:

- `backend/app/todos/presentation/api/todo_api.py`
- `backend/app/todos/presentation/responses/todo_response.py`

Problem:
Route handlers unwrap `Result`, raise domain errors, and reach into value objects with `title.value`. The presentation module therefore knows too much about the domain implementation.

Solution:
Introduce a presentation adapter inside the todo slice that translates application outcomes into `TodoResponse` and presentation errors.

Benefits:

- Response-shape changes stop rippling into route handlers.
- Domain refactors leak less into HTTP code.
- Presentation tests can assert on HTTP behaviour through a cleaner seam.

## 4. Separate persistence mapping from the ORM record

Files:

- `backend/app/todos/infrastructure/database/todo_model.py`
- `backend/app/todos/infrastructure/repository/sqlite_todo_repository.py`

Problem:
The ORM record currently translates itself to and from the domain model. That couples persistence implementation to domain shape and gives the record multiple responsibilities.

Solution:
Keep `TodoRecord` as the persistence structure and move shape conversion into a dedicated mapper adapter in infrastructure.

Benefits:

- Better seam discipline.
- One place to change persistence translation logic.
- Cleaner path for additional storage adapters.

## 5. Split the current core package into a shared kernel and outer adapters

Files:

- `backend/app/core/`
- `backend/app/presentation/exception_handlers.py`
- `backend/app/core/database/sqlite.py`
- `backend/app/core/schemas.py`

Problem:
`app/core` currently mixes shared primitives, database support, and web-facing schema concerns. The seam is too broad to communicate what kind of dependency callers are taking on.

Solution:
Keep only true shared-kernel concepts in a narrow shared module and move FastAPI, Pydantic, and SQLAlchemy support into explicit outer-adapter modules.

Benefits:

- Clearer dependency direction.
- Better locality for framework-specific changes.
- More navigable architecture for future feature slices.
