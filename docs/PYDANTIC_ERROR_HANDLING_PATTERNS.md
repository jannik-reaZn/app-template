# Pydantic Error Handling Patterns

## Goal

When a Pydantic model is used inside the domain layer, there are several ways to handle invalid input and business-rule violations.

This guide shows the main options, what each one is good at, and what to choose when.

## Quick Rule

Use the simplest option that matches the kind of rule you are enforcing.

- Use a `create()` classmethod when object creation contains business flow and should return `Result`.
- Use `model_post_init()` when the model should normalize itself and then enforce invariants.
- Use `field_validator(..., mode="before")` when you must clean or reject raw field input before Pydantic parses it.
- Use `field_validator(..., mode="after")` when the field should be checked after parsing.
- Use `model_validator(mode="after")` when the rule depends on multiple fields.
- Use a Pydantic-to-domain mapping layer when you want Pydantic validation errors to become domain errors in a controlled way.

## 1. `create()` Classmethod Returning `Result`

### When to use it

Use this when creation itself is business logic.

Typical cases:

- the aggregate should not be instantiated directly
- creation may fail with a domain error
- creation needs orchestration beyond validation
- your application already uses a `Result` pattern

### Why use it

This keeps business decisions explicit.

It is especially useful when creation needs to:

- normalize data
- apply defaults with business meaning
- call helper methods
- return `Result.ok(...)` or `Result.err(...)`

### Example

```python
class Todo(DomainModel):
    title: str
    status: TodoStatus = TodoStatus.PENDING

    @classmethod
    def create(cls, title: str) -> Result["Todo", DomainError]:
        normalized_title = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(title=normalized_title))
```

### Tradeoffs

- Very explicit.
- Easy to test.
- Good fit for use cases.
- Can duplicate logic if callers bypass `create()` and instantiate the model directly.

### Choose this when

Choose this when the main question is not just “is this data valid?” but “should this aggregate be created at all, and what should creation return?”

## 2. `model_post_init()`

### When to use it

Use this when Pydantic should parse the data first, and the domain model should then validate its final state.

Typical cases:

- trimming or canonicalizing fields after parsing
- enforcing domain invariants on the full model
- using a shared base model hook for all aggregates

### Why use it

`model_post_init()` runs after Pydantic has built the model instance. That makes it a good place for domain-level checks.

### Example

```python
class DomainModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self.normalize_domain_state()
        self.validate_domain_invariants()

    def normalize_domain_state(self) -> None:
        return None

    def validate_domain_invariants(self) -> None:
        return None


class Todo(DomainModel):
    title: str

    def normalize_domain_state(self) -> None:
        object.__setattr__(self, "title", self.title.strip())

    def validate_domain_invariants(self) -> None:
        if not self.title:
            raise EmptyTodoTitleError()
```

### Tradeoffs

- Keeps invariant logic inside the model.
- Good for shared domain-model lifecycle hooks.
- Works well with immutable models.
- Does not run if Pydantic fails before model creation.

### Choose this when

Choose this when the data is schema-valid, but the fully built domain object may still be invalid.

## 3. `field_validator(..., mode="before")`

### When to use it

Use this when you need to handle raw input before Pydantic parses it.

Typical cases:

- trimming strings
- converting empty strings to `None`
- rejecting raw input formats early
- accepting multiple raw shapes and normalizing them

### Example

```python
class Todo(BaseModel):
    title: str

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if not isinstance(value, str):
            return value

        normalized_title = value.strip()
        if not normalized_title:
            raise ValueError("Title cannot be empty")
        return normalized_title
```

### Tradeoffs

- Good for raw input cleanup.
- Runs very early.
- Keeps logic close to the field.
- Can become noisy if too much business logic is pushed into validators.

### Choose this when

Choose this when the rule is fundamentally about one field's raw input shape.

## 4. `field_validator(..., mode="after")`

### When to use it

Use this when the field should first be parsed into its final Python type, and only then be validated.

Typical cases:

- checking parsed enums
- validating parsed dates
- validating a parsed value object

### Example

```python
class Todo(BaseModel):
    due_date: date

    @field_validator("due_date", mode="after")
    @classmethod
    def validate_due_date(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Due date cannot be in the past")
        return value
```

### Tradeoffs

- Cleaner than `before` when you want typed values.
- Easier to read for type-based rules.
- Still field-local, so not ideal for cross-field business rules.

### Choose this when

Choose this when the rule is about the final typed field value, not the raw input.

## 5. `model_validator(mode="after")`

### When to use it

Use this when the rule depends on multiple fields.

Typical cases:

- start date must be before end date
- completed todos must have a completion timestamp
- either `email` or `phone` must be present

### Example

```python
class Todo(BaseModel):
    status: TodoStatus
    completed_at: datetime | None = None

    @model_validator(mode="after")
    def validate_completion_state(self) -> "Todo":
        if self.status == TodoStatus.COMPLETED and self.completed_at is None:
            raise ValueError("Completed todos need a completion timestamp")
        return self
```

### Tradeoffs

- Best built-in choice for cross-field checks.
- Keeps object-level rules in one place.
- Can become too broad if many unrelated rules are packed into one validator.

### Choose this when

Choose this when the rule depends on the relationship between fields.

## 6. Mapping `ValidationError` to `DomainError`

### When to use it

Use this when you want Pydantic to do validation, but the rest of the domain or application layer should see domain errors instead of raw Pydantic errors.

Typical cases:

- API payload validation should surface domain wording
- multiple models should share a consistent translation strategy
- you want typed domain errors, not generic validation payloads

### Example

```python
handlers = (
    PydanticErrorHandler.for_domain_error(
        error_type="empty_todo_title",
        domain_error_factory=EmptyTodoTitleError,
        loc=("title",),
    ),
)


try:
    TodoModel.model_validate(payload)
except ValidationError as error:
    mapped_error = map_pydantic_validation_error(error, handlers)
    if mapped_error is not None:
        raise mapped_error from error
    raise
```

### Tradeoffs

- Strong separation between framework errors and domain errors.
- Scales well when many mappings are needed.
- More moving parts than direct validation.
- Best used when you really need translation, not just validation.

### Choose this when

Choose this when the error must remain domain-specific even though the underlying validation is performed by Pydantic.

## 7. Raise `DomainError` Directly in a Validator

### When to use it

Use this sparingly.

This can be acceptable for very small codebases or for one very domain-specific rule where indirection would add more noise than value.

### Example

```python
class Todo(BaseModel):
    title: str

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            raise EmptyTodoTitleError()
        return value
```

### Tradeoffs

- Very direct.
- Minimal code.
- Couples validator behavior to domain exception policy.
- Harder to scale consistently across many models.

### Choose this when

Choose this only when the rule is small, stable, and you are confident you do not need a reusable translation strategy.

## What to Choose When

### If creation should return `Result`

Use a `create()` classmethod.

### If the model should normalize itself and then enforce invariants

Use `model_post_init()`.

### If you need to inspect raw field input

Use `field_validator(..., mode="before")`.

### If you need typed field validation

Use `field_validator(..., mode="after")`.

### If the rule depends on multiple fields

Use `model_validator(mode="after")`.

### If Pydantic errors must become domain errors

Use a validation-error mapping layer.

### If the code is tiny and the rule is very local

Directly raising `DomainError` in a validator can be acceptable, but it should not be the default.

## Recommended Default for This Repo

For this codebase, a good default is:

1. Use `create()` when aggregate creation is part of business flow and should return `Result`.
2. Use `model_post_init()` for domain invariants that apply after parsing.
3. Use field or model validators for schema-local validation and normalization.
4. Add a validation-error mapping layer only when raw Pydantic errors need to be translated into domain errors consistently.

That keeps the domain explicit without pushing every rule into one mechanism.
