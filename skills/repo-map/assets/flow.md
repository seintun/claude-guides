---
type: flow
entry: path/to/entry/file.py
components: ["[[component-a]]", "[[component-b]]"]
---
# What happens when a user does X

1. `ExactSymbol` in [[component-a]] receives the request.
2. It calls `other_symbol`, which writes to [[component-b]].
3. The response returns to the caller.
