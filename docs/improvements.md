# Backend Architecture Improvements

This document captures the highest-value clean architecture and domain-driven design improvements identified in the current backend.

## 1. Deepen the todo presentation seam

Files:

- `backend/app/todos/presentation/api/todo_api.py`
- `backend/app/todos/presentation/responses/todo_response.py`
- `backend/app/presentation/exception_handlers.py`

Problem:

The route handlers still unwrap `Result`, raise domain errors, and reach into value objects with `title.value`. The HTTP module therefore knows too much about domain internals and behaves like a shallow pass-through.

Suggestion:

Introduce a presentation adapter inside the todo slice that translates application outcomes into HTTP responses and presentation errors.

Benefits:

- Better locality for HTTP behavior.
- More leverage from a smaller interface.
- Cleaner API tests that do not depend on domain object structure.

## 2. Separate persistence mapping from the ORM record

Files:

- `backend/app/todos/infrastructure/database/todo_model.py`
- `backend/app/todos/infrastructure/repository/sqlite_todo_repository.py`

Problem:

`TodoRecord` currently acts as both the persistence structure and the mapping adapter through `from_domain(...)` and `to_domain()`. That couples storage shape to domain translation logic.

Suggestion:

Keep `TodoRecord` as the persistence structure and move conversion logic into a dedicated infrastructure mapper used by the SQLite repository.

Benefits:

- Better seam discipline between infrastructure and domain.
- Stronger locality for storage-related changes.
- Cleaner path for introducing additional repository adapters.

## 3. Narrow the shared kernel

Files:

- `backend/app/core/__init__.py`
- `backend/app/core/domain_model.py`
- `backend/app/core/schemas.py`
- `backend/app/core/database/sqlite.py`

Problem:

`app/core` currently mixes shared domain primitives, schema concerns, and database support. That makes the seam too broad and obscures the dependency direction when a module imports from `app.core`.

Suggestion:

Keep only true shared-kernel concepts together, such as `Result` and `DomainError`, and move Pydantic schema policy and SQLAlchemy support into explicit outer-adapter modules.

Benefits:

- Clearer dependency direction.
- Better locality for framework-specific changes.
- A more navigable codebase as the number of feature slices grows.

## 4. Make the repository seam real in composition

Files:

- `backend/app/todos/presentation/dependencies/todo_dependencies.py`
- `backend/app/todos/infrastructure/repository/sqlite_todo_repository.py`
- `backend/app/todos/infrastructure/repository/in_memory_todo_repository.py`

Problem:

The repository seam exists in the type system, but runtime composition always wires SQLite directly. That keeps the seam partly hypothetical rather than fully exercised.

Suggestion:

Introduce a small composition module that selects the repository adapter by environment or configuration, and run the same application-facing checks against both adapters where that adds value.

Benefits:

- Higher leverage from the existing repository interface.
- Stronger confidence that the seam is load-bearing.
- Easier adapter swaps without editing callers.

## 5. Replace primitive application inputs with explicit commands

Files:

- `backend/app/todos/application/todo_application_service.py`
- `backend/app/todos/presentation/requests/create_todo_request.py`

Problem:

`TodoApplicationService.create_todo(...)` currently accepts primitive values such as `title: str`. That is manageable now, but it will become a shallow interface as the use case grows.

Suggestion:

Define explicit application inputs such as `CreateTodoCommand` and let the application seam own normalization and orchestration around that command.

Benefits:

- Clearer use-case intent.
- A deeper application interface with room to grow.
- Simpler evolution when new fields or policies are added.

## 6. Add a domain glossary and ADRs

Files:

- `docs/`

Problem:

The workspace currently has no `CONTEXT.md` or ADR directory. That makes it harder to preserve naming discipline and architectural decisions as the codebase grows.

Suggestion:

Add a small domain glossary for the core concepts in this backend and record non-obvious architecture decisions as ADRs.

Benefits:

- Shared language across the codebase.
- Better AI navigability.
- Less architectural drift over time.

## Suggested Order

If implemented incrementally, the recommended order is:

1. Deepen the todo presentation seam.
2. Separate persistence mapping from the ORM record.
3. Narrow the shared kernel.
4. Add a domain glossary and ADRs.

The first two changes provide the best locality gains with the least churn.
