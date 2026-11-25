# The UI branch

A UI prototype answers a question about **how something looks**: layout, hierarchy, the primary
action. It renders several structurally different variants of one screen, switchable in the browser,
so the judge compares them in place instead of in their head.

## 1. Choose the host

**Prefer an existing page.** A variant judged inside the real app, with its real header, data and
density, shows problems an empty page hides. Mount the variants on the existing route, or inside the
page the new thing would live in, and keep its data loading and access checks as they are; only the
rendered part changes. Make a new, throwaway route (named with `prototype`, under the project's own
routing convention) only when nothing existing could host it, and say why.

## 2. Decide how many, and write the plan down

Three variants by default, five at most: past that they stop differing and become noise. Write one
line at the top of the switcher: which screen, how many variants, which route, and the parameter
that selects them (`?variant=`).

## 3. Make the variants differ in structure

Each variant serves the screen's purpose with the data it already has, in the project's own
component library and styling, as its own named component. They must disagree about **structure**:
layout, information hierarchy, primary affordance. Colour or copy changes are a tweak, not a
variant; redo a draft that comes out too close to another. Share small pieces (a header) if needed,
never the layout.

## 4. Wire one switcher

The route reads the variant from the URL parameter and renders that variant, falling back to the
first. A small floating bar, visibly not part of the design, shows the current variant's key and
name and steps to the previous and next, wrapping around; the arrow keys do the same except while
a text field has focus. Changing variant updates the URL, so a variant is shareable and survives a
reload. **Gate the bar and the variants out of production builds** with the project's own
environment check, so a stray merge cannot ship them.

## 5. Hand it over

Give the judge the URL and the variant keys. The usual answer is a combination ("the header from B,
the sidebar from C"), which is the design they want; record it as the verdict.

## 6. Clean up

Fold the chosen design into the real page, written properly (tests, error handling), not promoted
from the variant code. All the variants and the switcher go to the prototype branch as evidence,
and none stay on the working branch.

## What does not belong

- Variants wired to real writes; point a variant that must write at a stub.
- A variant promoted straight to production.
- A new route when an existing page could host the variants.
