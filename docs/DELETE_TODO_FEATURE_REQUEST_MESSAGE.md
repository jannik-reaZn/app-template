# Artificial Feature Request: Delete TODO

## Message From Domain Expert

Hey dev,

quick heads-up from the task management side of the house: the app is kinda missing a basic move right now. Folks can create tasks, update them, all that good stuff, but if a task is dead weight, wrong, duplicated, or just straight-up not needed anymore, it still hangs around like bad leftovers.

We need a proper way to delete a task.

Right now the flow feels janky. Users clean up their list mentally, but the system keeps the old junk sitting there, and that makes the board look messy real fast. If somebody fat-fingers a task or drops in a duplicate, they should be able to bin it without doing weird workaround stuff.

What we need is pretty simple:

- A user can delete an existing task by its id.
- If the task is not there, the API should respond cleanly and not act shady about it.
- After deletion, that task should be gone from the active workflow.

If there are edge cases you want to lock down, cool, but the core ask is: let users remove tasks when those tasks are no longer relevant. That is standard hygiene for any TODO flow, and right now we are missing it.

Can you slot this in as the next feature slice?

Thanks,
The overly caffeinated TODO domain expert
