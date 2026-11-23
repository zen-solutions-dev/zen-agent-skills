# The architecture report

One self-contained HTML file, written to the operating system's temporary directory, readable with
no network at all. Everything it needs is inside it: an inline `<style>` block and inline SVG or
plain HTML for every diagram. No CDN, no external script, font, stylesheet or image. A report that
needs the network shows a blank page on a train, behind a proxy, or a year from now.

## Scaffold

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Architecture review: {{repository}}</title>
  <style>
    :root { --ink:#1f2933; --paper:#fafaf7; --line:#cbd2d9; --accent:#0f766e;
            --leak:#b91c1c; --warn:#b45309; --muted:#64748b; }
    @media (prefers-color-scheme: dark) {
      :root { --ink:#e5e7eb; --paper:#111827; --line:#374151; --muted:#94a3b8; } }
    body { margin:0; background:var(--paper); color:var(--ink);
           font:16px/1.5 system-ui, sans-serif; }
    main { max-width:60rem; margin:0 auto; padding:2rem 1rem; }
    article { border:1px solid var(--line); border-radius:8px; padding:1.25rem; margin:2rem 0; }
    .pair { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
    @media (max-width:40rem) { .pair { grid-template-columns:1fr; } }
    .badge { font-size:.75rem; text-transform:uppercase; letter-spacing:.05em;
             border:1px solid currentColor; border-radius:4px; padding:0 .4rem; }
    .strong { color:var(--accent); } .explore { color:var(--warn); } .speculative { color:var(--muted); }
    .seam { stroke-dasharray:4 4; } .leak { stroke:var(--leak); }
    code, .files { font-family:ui-monospace, monospace; font-size:.875rem; }
  </style>
</head>
<body><main>
  <header>repository, date, scope and the command that chose it, and a legend</header>
  <section id="candidates">one article per candidate</section>
  <section id="top">the top recommendation</section>
</main></body>
</html>
```

## Header

Repository name, date, the scope and the hot-spot command that produced it, and a legend: a solid
box is a module, a dashed line is a seam, a red arrow is a leak, a thick dark box is a deep module.
No introduction paragraph.

## Candidate card

One `<article>` each, in this order:

- **Title** naming the deepening ("Collapse the order-intake pipeline").
- **Badges**: strength (`Strong`, `Worth exploring`, `Speculative`) and dependency category.
- **Files**, monospaced.
- **Before and after**, side by side in `.pair`. This carries the weight; if it needs a paragraph to
  be understood, redraw it.
- **Problem**: one sentence. **Solution**: one sentence.
- **Wins**: short bullets in vocabulary terms.
- **Decision-record callout**, only when the candidate reopens one, and why.

## Diagram patterns

Draw with inline SVG (`<svg viewBox=...>` with `<rect>`, `<line>`, `<path>`, `<text>`) or with
bordered `<div>` boxes. Vary the pattern to fit the candidate:

- **Boxes and arrows** for call flow and dependencies. Colour leaking edges with `.leak`, draw seams
  with `.seam`.
- **Cross-section**: stacked horizontal bands for the layers a call passes through. Before: six thin
  bands doing little. After: one thick band named for its responsibility.
- **Mass diagram**: two rectangles per module, interface above implementation. Shallow: the two are
  nearly the same height. Deep: a short interface over a tall implementation.
- **Call-graph collapse**: a tree of nested boxes, then the same tree folded into one box with the
  now-internal calls faded inside it.

Keep each diagram about 320 pixels tall so the pair sits side by side without scrolling. A Mermaid
source block may be included as `<pre>` text for a reader who wants to paste it elsewhere, but the
rendered diagram must be the inline drawing, since Mermaid needs a script the report cannot load.

## Top recommendation

One larger card: the candidate's name, one sentence on why it comes first, and a link to its card.

## Tone

Plain and short. The architectural nouns come from [`vocabulary.md`](vocabulary.md) and from
nowhere else. If a sentence could be a bullet, make it one; if a bullet could go, cut it.
