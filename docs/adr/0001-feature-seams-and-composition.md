# ADR 0001: Feature Seams And Composition

## Status

Accepted

## Context

The backend originally exposed framework concerns and infrastructure choices through broad shared modules and thin route handlers. The todo slice now has explicit seams for presentation, application, and infrastructure, but those choices need to be recorded so future changes do not collapse the dependency direction again.

## Decision

We keep the backend organized around explicit seams:

- `app.core` is the shared kernel for domain-oriented primitives such as `Result`, `DomainError`, and `DomainModel`.
- `app.presentation` owns HTTP-facing schema and exception handling policy.
- `app.infrastructure` owns database and other framework-backed adapters.
- Feature slices depend on ports in the inward direction and wire adapters only at composition time.

For the todo slice specifically:

- HTTP handlers delegate response translation to `TodoPresenter`.
- Repository selection happens in composition through `todo_dependencies.py` and `create_todo_repository(...)`.
- Repository adapters implement `TodoRepositoryPort` and remain replaceable without changing application callers.

## Consequences

Positive:

- Dependency direction is clearer.
- Framework-specific changes stay local to presentation or infrastructure.
- Adapter selection is a composition concern instead of an application concern.

Tradeoffs:

- The codebase has more small modules.
- Some flows now go through extra translation layers, which increases indirection.

## Follow-up

New features should follow the same seam pattern rather than adding framework helpers back into `app.core` or instantiating adapters directly in handlers and use cases.
