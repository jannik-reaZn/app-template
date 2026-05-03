# Delete TODO Grill Session

Use this as an interview checklist before implementing the delete TODO feature.

## Questions

1. What exact HTTP contract do we want for deletion?
   Common options are `DELETE /api/todos/{todo_id}` returning either `204 No Content` with an empty body or `200 OK` with a confirmation payload.

2. Should delete be idempotent from the client perspective?
   If the TODO is already gone, should the API still return success, or should it return a clean `404 Not Found`?

3. What does "gone from the active workflow" mean in this codebase?
   Should this be a hard delete from storage, or a soft delete that keeps the record but removes it from normal reads?

4. What should a follow-up `GET /api/todos/{todo_id}` return after deletion?
   Expected default: `404 Not Found`.

5. Are there domain rules that should block deletion for some TODO states?
   Example: completed items may still be deletable, or some states may be protected.

6. Should the API return any deletion metadata?
   Options include no body, a confirmation message, the deleted id, or audit fields such as `deleted_at`.

7. What test coverage is required for this feature slice?
   Minimum useful set:
   - deleting an existing TODO succeeds
   - reading the deleted TODO returns `404`
   - deleting a missing TODO returns `404`

8. Should missing TODOs continue to be modeled as a domain error?
   This would keep delete aligned with the existing get-by-id flow, which already uses `TodoNotFoundError`.

9. Are there any audit, retention, logging, or integration side effects required when a TODO is deleted?

10. What matters most for this implementation?
    Pick the primary constraint:
    - clean REST contract
    - consistent domain modeling
    - strong tests
    - minimal code surface
    - future-friendly path to soft delete

## Proposal

This is the proposal I would implement unless the interview answers change the requirements.

### API contract

- Add `DELETE /api/todos/{todo_id}`.
- Return `204 No Content` when deletion succeeds.
- Return `404 Not Found` with `{ "detail": "Todo not found" }` when the TODO does not exist.

Reasoning: the existing API already maps `TodoNotFoundError` to `404`, and `204` is the cleanest success response when no resource representation needs to be returned.

### Domain and application shape

- Add a `DeleteTodoUseCase` in the application layer.
- Extend `TodoRepository` with a `delete(todo_id: str)` method.
- Keep absence modeled as `TodoNotFoundError` for consistency with the current get flow.

Reasoning: this preserves the current architecture. The API stays thin, the use case expresses intent, and the repository owns persistence behavior.

### Persistence behavior

- Implement deletion as a hard delete in the repository.
- After deletion, `get_by_id(todo_id)` should return `TodoNotFoundError`.

Reasoning: the feature request asks for removal, not archival. A hard delete is the smallest implementation that satisfies the current need. If soft delete becomes necessary later, it can be introduced explicitly with different storage and query rules.

### Tests

- Add a presentation test for deleting an existing TODO.
- Add a presentation test proving `GET` returns `404` after deletion.
- Add a presentation test for deleting a missing TODO.
- Add an application-layer test for `DeleteTodoUseCase`.
- Add repository tests if the repository test suite already covers behavioral CRUD slices in the same style.

Reasoning: this gives one end-to-end slice of confidence plus one focused use-case check without overbuilding the test surface.

### Acceptance criteria

- A user can delete an existing TODO by id.
- Deleting a missing TODO returns a clean `404`.
- A deleted TODO is no longer retrievable through the active API flow.
- The implementation follows the existing domain-error mapping conventions.
