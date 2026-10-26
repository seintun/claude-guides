# Grader map (from the prompts alone)

| Hidden test | Prompt | DONE WHEN item | Note |
|---|---|---|---|
| H1 header row naming the page's columns | feature | 2 (also 4) | Item 2 claims "the header line plus one line per row"; item 4 claims the header line alone. Neither names the columns explicitly; the ASSUMED line sets header = row-object keys. |
| H2 exactly the rows the page shows, several filters | feature | 2 | Item 2 claims data lines match `renderReportsPage(rows, filter)` for one dataset and filter. |
| H3 no-match filter gives header only | feature | 4 | |
| H4 commas, quotes, newlines survive round trip | feature | 3 | |
| H5 session resetPassword returns stays signed in | bugfix | 1 | |
| H6 old password fails, new works, older sessions end | bugfix | none | Item 3 covers refused tokens only; no item claims old/new password or ending older sessions. |
