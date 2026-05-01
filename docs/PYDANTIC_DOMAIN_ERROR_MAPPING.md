# Pydantic Validation to Domain Error Mapping

## Goal

When a domain model is created from untrusted input, validation should enforce invariants without leaking raw framework validation details into the rest of the application.

In this project, the concrete example is the `Todo` entity:

- input: a title such as `"   "`
- framework-level event: Pydantic accepts the field type, then the domain model rejects the final state
- desired domain behavior: raise `EmptyTodoTitleError` from the model itself
- desired API behavior: the presentation layer responds with the domain error message, not a raw Pydantic error payload

The objective is not only to solve the `Todo.title` case, but to establish a pattern that scales as more entities and more validation rules are added.

## The Problem

Pydantic is good at validation, but its native error output is framework-oriented:

- error types such as `string_too_short`
- locations such as `("title",)`
- payloads shaped for HTTP `422` responses

That is useful at the transport boundary, but not ideal inside the domain layer.

For domain logic, we usually want:

- business-oriented error names
- domain-specific messages
- stable error classes that the application and presentation layers can reason about
- a single place to define how validation issues are translated into domain errors

If validators raise `DomainError` directly, the implementation becomes tightly coupled to one exception style and harder to scale. Each validator starts making transport and orchestration decisions implicitly. That approach works for one or two rules, but it becomes harder to manage once there are many entities and many field-level constraints.

## Design Principles

This solution follows these rules:

1. Pydantic remains responsible for parsing and basic schema validation.
2. Domain models enforce business invariants after Pydantic has built the model.
3. The domain layer raises `DomainError` directly for invariant failures.
4. Shared post-construction hooks live in the base domain model.
5. The invariant check happens at the domain model boundary, not in the API layer.

This keeps concerns separated:

- Pydantic handles framework validation
- domain models normalize and validate domain state
- the presentation layer only deals with `DomainError` or uncaught `ValidationError`

## Current Implementation

The current variant uses `model_post_init` and a shared base-model hook.

### 1. A shared post-construction hook in `DomainModel`

File: `backend/app/core/domain_model.py`

`DomainModel` now defines a common lifecycle for domain objects:

- `model_post_init(...)`
- `normalize_domain_state()`
- `validate_domain_invariants()`

The important method is:

```python
def model_post_init(self, __context: Any) -> None:
    super().model_post_init(__context)
    self.normalize_domain_state()
    self.validate_domain_invariants()
```

This gives every domain model two overridable hooks:

- `normalize_domain_state()` for post-parse normalization
- `validate_domain_invariants()` for domain-only validation that should raise `DomainError`

### 2. Per-model invariant enforcement

File: `backend/app/todos/domain/todo_entity.py`

The `Todo` model uses those hooks directly:

```python
def normalize_domain_state(self) -> None:
    object.__setattr__(self, "title", self.title.strip())

def validate_domain_invariants(self) -> None:
    if not self.title:
        raise EmptyTodoTitleError()
```

This keeps the rule close to the aggregate that owns it.

This is a good fit for DDD because:

- the `Todo` aggregate owns the `title must not be blank` invariant
- the `Todo` aggregate owns both normalization and the final business check

The creation method stays thin:

```python
@classmethod
def create(
    cls, title: str, status: TodoStatus = TodoStatus.PENDING
) -> Result[Todo, DomainError]:
    try:
        return Result.ok(cls(title=title, status=status))
    except DomainError as error:
        return Result.err(error)
```

Pydantic still validates the field types before `model_post_init` runs. The domain hooks only run once the model instance exists.

## End-to-End Flow

For a blank todo title, the runtime flow is now:

1. `CreateTodoUseCase` calls `Todo.create(...)`.
2. `Todo.create(...)` calls `Todo(title=title, status=status)`.
3. Pydantic validates that `title` is a string and that the other fields have valid schema-level values.
4. `DomainModel.model_post_init(...)` runs.
5. `Todo.normalize_domain_state()` trims the title.
6. `Todo.validate_domain_invariants()` checks the final normalized state.
7. If the title is blank, it raises `EmptyTodoTitleError()`.
8. `Todo.create(...)` catches the `DomainError` and returns `Result.err(error)`.
9. The API route raises the domain error if the result is an error.
10. The registered domain exception handler returns the domain message as the HTTP response.

This gives a clean behavioral chain from validation to domain semantics to transport response.

## Why This Is Scalable

This pattern scales well for domain invariants that should run after the model has already been parsed.

### It centralizes invariant hooks

Every domain model gets the same two extension points.

That means future contributors can answer the question “where does this aggregate normalize itself and enforce invariants?” by looking in one predictable place.

### It supports normalization before validation

A field can have multiple distinct errors:

- blank title
- title too long
- forbidden title value
- invalid status transition encoded in a nested payload

You can trim, canonicalize, or derive state first, then validate the normalized object.

### It preserves Pydantic for schema-level failures

This is important operationally.

If the payload is not even schema-valid, Pydantic still raises `ValidationError` before `model_post_init` runs. That keeps framework validation and domain validation clearly separated.

If a validation failure is not part of the domain contract, the system should not silently turn it into a generic domain error. Re-raising the original `ValidationError` makes those gaps visible.

That helps during development and avoids hiding incomplete mappings.

## How to Add a New Domain Validation Error

Use the following process for future rules.

### Step 1. Create a domain error class

Example:

```python
class TodoTitleTooLongError(DomainError):
    def __init__(self) -> None:
        super().__init__("Todo title must be 120 characters or fewer")
```

### Step 2. Emit a custom validation type from the validator

Example:

```python
@field_validator("title", mode="before")
@classmethod
def validate_title(cls, value: object) -> object:
    if not isinstance(value, str):
        return value

    normalized_title = value.strip()
    if not normalized_title:
        raise_custom_validation_error(
            error_type="empty_todo_title",
            message_template="Todo title cannot be empty",
        )
    if len(normalized_title) > 120:
        raise_custom_validation_error(
            error_type="todo_title_too_long",
            message_template="Todo title must be 120 characters or fewer",
        )
    return normalized_title
```

### Step 3. Register the mapping on the model

Example:

```python
pydantic_error_handlers: ClassVar[tuple[PydanticErrorHandler, ...]] = (
    PydanticErrorHandler.for_domain_error(
        error_type="empty_todo_title",
        domain_error_factory=EmptyTodoTitleError,
        loc=("title",),
    ),
    PydanticErrorHandler.for_domain_error(
        error_type="todo_title_too_long",
        domain_error_factory=TodoTitleTooLongError,
        loc=("title",),
    ),
)
```

### Step 4. Construct the model through `from_payload(...)`

This is necessary. If code bypasses `from_payload(...)` and calls `model_validate(...)` or the model constructor directly, the mapping layer does not get a chance to translate the error.

For domain construction paths, prefer:

```python
Todo.from_payload(title=title, status=status)
```

not:

```python
Todo(title=title, status=status)
```

### Step 5. Add focused tests

At minimum, test:

- the mapping helper returns the correct domain error for a matching validation error
- the model raises the domain error through `from_payload(...)`
- the use case or API returns the expected behavior for the mapped domain error

## Testing Strategy in This Repo

The core pattern is covered in:

- `backend/tests/core/test_pydantic_error_handlers.py`

The application and API flow are covered by:

- `backend/tests/todos/application/test_create_todo_use_case.py`
- `backend/tests/presentation/test_create_todo_api.py`

That split is useful:

- core tests verify the generic mechanism
- use-case tests verify domain construction behavior
- API tests verify the final user-visible response

## Why Not Map in the Presentation Layer?

Mapping in the presentation layer would be the wrong abstraction level for this problem.

Reasons:

- the blank-title rule belongs to the `Todo` domain, not HTTP
- application use cases may create `Todo` outside HTTP
- CLI, background jobs, tests, or future MCP tools may also construct domain objects
- domain semantics should exist even when no API is involved

If mapping only exists in FastAPI exception handlers, then non-HTTP callers still see raw Pydantic validation failures. That would be inconsistent.

Putting the translation in `DomainModel.from_payload(...)` keeps the behavior transport-agnostic.

## Why Not Raise `DomainError` Directly in Validators?

That can work, but it has tradeoffs.

### Problems with directly raising `DomainError`

- validators become responsible for both validation and domain exception policy
- there is no central registry of which validation failures map to which domain errors
- changing behavior later requires editing validator logic rather than updating declarative mappings
- mixed strategies become likely across the codebase

### Benefits of the current approach

- validators emit a validation signal, not the final domain policy decision
- mapping rules are visible and explicit
- the same generic mapper can be reused by many models
- future extensions can improve matching without rewriting validators

## Limitations and Tradeoffs

This design is intentionally conservative.

### Construction must go through `from_payload(...)`

The mapping only happens there. That is deliberate, but it means domain construction code should consistently use the helper.

### Unmapped validation errors remain framework errors

That is useful for correctness, but it also means new validation rules need explicit mapping if they should become domain errors.

### Multiple simultaneous validation errors currently return the first mapped error

`map_pydantic_validation_error(...)` returns the first matching domain error it finds.

That is acceptable for now because current entity construction focuses on single-rule invariant failures. If the project later needs aggregated domain validation results, the mapper can evolve to return a list or a composite error object.

## Recommended Conventions

To keep this pattern maintainable, follow these conventions.

### Use explicit custom error types

Prefer names like:

- `empty_todo_title`
- `todo_title_too_long`
- `todo_status_transition_invalid`

Avoid overloading generic built-in Pydantic types when the failure is domain-specific.

### Keep messages domain-oriented

Messages should describe the business rule, not the framework rule.

Good:

- `Todo title cannot be empty`

Less useful:

- `String should have at least 1 character`

### Keep mapping close to the model

Put a model's `pydantic_error_handlers` on that model unless multiple models truly share the exact same rule set.

### Keep validators focused

Validators should:

- normalize input
- detect invalid conditions
- emit stable validation types

They should not contain routing, HTTP, or repository concerns.

## Summary

The project now uses a two-step validation strategy for domain models:

1. validators raise stable Pydantic custom error types
2. `DomainModel.from_payload(...)` translates selected validation failures into `DomainError`

This is the right balance between framework power and domain clarity.

It keeps the domain model in control of its invariants, keeps the API layer simple, and gives the codebase a clear, repeatable pattern for future validation rules.
