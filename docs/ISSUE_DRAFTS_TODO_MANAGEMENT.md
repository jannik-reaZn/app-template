# Todo Management Issue Drafts

These issue drafts break the backend-only Todo Management example into thin vertical slices.

All slices are backend-only and assume no FastMCP layer.

## Proposed Breakdown

1. **Title**: Add create-todo vertical slice
   **Type**: AFK
   **Blocked by**: None
   **User stories covered**: As a user, I want to create a todo item.

2. **Title**: Add get-todo vertical slice
   **Type**: AFK
   **Blocked by**: Issue 1
   **User stories covered**: Support reading a todo by id so created state is observable through the API.

3. **Title**: Add complete-todo vertical slice
   **Type**: AFK
   **Blocked by**: Issue 2
   **User stories covered**: As a user, I want to mark a todo item as completed.

4. **Title**: Add delete-todo vertical slice
   **Type**: AFK
   **Blocked by**: Issue 2
   **User stories covered**: As a user, I want to delete a todo item that is no longer relevant.

5. **Title**: Finalize delete-todo product contract
   **Type**: AFK
   **Blocked by**: Issue 4
   **User stories covered**: Ensure delete behavior is clearly defined and consistent for API consumers.

## Issue Draft 1

Title: Add create-todo vertical slice

Labels: `needs-triage`

## What to build

Implement the first end-to-end backend slice for Todo Management so the API can create a todo item. The slice should include the Task Management domain model, a create-todo use case that returns `Result`, an in-memory repository implementation, FastAPI request and response schemas, route wiring, and focused tests.

## Acceptance criteria

- [ ] `POST /api/todos` accepts a title and returns a created todo with `id`, `title`, and `pending` status.
- [ ] Blank or whitespace-only titles are rejected by domain rules and returned as `400 Bad Request` through API error mapping.
- [ ] The slice introduces a `Todo` aggregate, domain errors for invalid creation, a repository contract, a create use case, and tests that cover the route and use case.

## Blocked by

None - can start immediately.

## Issue Draft 2

Title: Add get-todo vertical slice

Labels: `needs-triage`

## What to build

Implement the read path for Todo Management so the API can retrieve a todo by id. The slice should include repository lookup support, a get-todo use case that returns `Result`, API response mapping for found and missing todos, and tests that verify the end-to-end behavior.

## Acceptance criteria

- [ ] `GET /api/todos/{todo_id}` returns the todo with its current status when the id exists.
- [ ] Missing todo ids are returned as `404 Not Found` through `Result`-based error mapping from a domain or application error.
- [ ] The slice adds the get-todo use case, repository lookup behavior, route wiring, and tests for both success and not-found cases.

## Blocked by

- Issue 1: Add create-todo vertical slice

## Issue Draft 3

Title: Add complete-todo vertical slice

Labels: `needs-triage`

## What to build

Implement completion of an existing todo through the API. The slice should load the aggregate through the repository, apply the domain rule that a completed todo cannot be completed again, persist the updated aggregate, return the updated representation, and cover success and failure paths with tests.

## Acceptance criteria

- [ ] `POST /api/todos/{todo_id}/complete` returns the todo with `completed` status when the todo exists and is still pending.
- [ ] Completing a missing todo returns `404 Not Found`, and completing an already completed todo returns `409 Conflict`.
- [ ] The slice adds the complete-todo use case, domain error for repeated completion, API error mapping, and tests for success, not-found, and already-completed cases.

## Blocked by

- Issue 2: Add get-todo vertical slice

## Issue Draft 4

Title: Add delete-todo vertical slice

Labels: `needs-triage`

## What to build

Implement deletion of an existing todo through the API as a thin end-to-end backend slice. The slice should let clients remove a todo by id, return a clean response when the id does not exist, and ensure the deleted todo is no longer available through the standard read flow.

## Acceptance criteria

- [ ] `DELETE /api/todos/{todo_id}` deletes an existing todo successfully.
- [ ] Deleting a missing todo returns `404 Not Found` through the existing error-handling approach.
- [ ] A todo that has been deleted is no longer returned by `GET /api/todos/{todo_id}`.

## Blocked by

- Issue 2: Add get-todo vertical slice

## Issue Draft 5

Title: Finalize delete-todo product contract

Labels: `needs-triage`

## What to build

Finalize the product-facing contract for the delete-todo capability so API consumers and future contributors have a clear, stable definition of how deletion behaves. This issue should align the feature request, PRD, and delivery expectations around success behavior, missing-resource handling, and the expected post-delete user experience.

## Acceptance criteria

- [ ] The delete-todo behavior is documented clearly enough that API consumers can understand the expected success and not-found outcomes.
- [ ] The defined delete behavior matches the product requirements and accepted feature scope.
- [ ] The delete capability is described as part of the supported todo lifecycle.

## Blocked by

- Issue 4: Add delete-todo vertical slice
