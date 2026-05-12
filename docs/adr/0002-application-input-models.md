# ADR 0002: Application Inputs Use Commands And Queries

## Status

Accepted

## Context

The todo use cases originally accepted primitive arguments such as `title: str` and `todo_id: str`. That shape was easy to start with, but it left the application seam shallow and made it harder to grow use-case-specific inputs without leaking transport concerns into application logic.

## Decision

Application use cases accept explicit input models instead of primitive argument lists.

Current examples:

- `CreateTodoUseCase` accepts `CreateTodoCommand`.
- `GetTodoUseCase` accepts `GetTodoQuery`.

Presentation models translate HTTP input into these application models before calling the use cases.

## Consequences

Positive:

- Use-case intent is explicit in the type system.
- The application seam can grow fields and policies without widening method signatures.
- Transport models and application models are separated.

Tradeoffs:

- There are more small types to maintain.
- Very simple use cases may feel slightly more verbose.

## Follow-up

Future todo use cases should default to explicit command or query models unless a primitive truly captures the full use-case intent and is unlikely to evolve.
