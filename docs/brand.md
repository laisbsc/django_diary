> Scope: currently applied to the blog. Intended to extend to the full personal website.

# Brand identity — laís.

A reference file for Claude (or anyone else) working on this blog. Follow these rules exactly when building components, writing copy, or extending the design.

---

## Concept

Warm, editorial, personal. The blog lives at the intersection of AI engineering and human community. It should feel like a smart person's notebook, not a tech publication. The cobalt accent is the signal of intellectual rigour inside the warmth.

---

## Colour palette

| Name | Hex | Role |
|---|---|---|
| Cream | `#F2EBD5` | Page background, base surface |
| Amber | `#E8A62C` | Primary accent, CTA highlights, decorative |
| Sand | `#D9C49C` | Secondary backgrounds, cards, sidebars |
| Sienna | `#D98723` | Hover states, category tags, border accents |
| Cobalt | `#153FB3` | Links, active nav, buttons, pull-focus elements |
| Ink | `#1A1610` | Headings, body text base |
| Ink Muted | `#5C4F35` | Body text, descriptions |
| Ink Light | `#9A8A6A` | Metadata, timestamps, secondary labels |

### Usage rules

- Cream is the only page background. Never use white as a base.
- Cobalt is the single "attention" colour. Use it deliberately: links, CTAs, active states, the logo dot. Do not use it for decoration.
- Amber is decorative and warm. Use for accents, highlights, pullquote borders, and the arrow in ghost buttons. Never use as a primary button fill.
- Sienna is amber's deeper twin. Use for hover states, category label text, and subtle borders.
- Sand is the surface colour for cards, sidebars, and secondary containers.
- Never use pure `#fff` white or pure `#000` black. Use Cream and Ink respectively.

---

## Typography

| Role | Font | Weight | Size |
|---|---|---|---|
| Display / Headline | Lora (serif) | 600 | 30–46px |
| Subheadline / Card title | Lora (serif) | 600 | 15–24px |
| Italic emphasis | Lora (serif) | 400 italic | same as context |
| Body text | DM Sans | 400 | 14–15px |
| UI labels / nav | DM Sans | 400–500 | 12–13px |
| Meta / timestamps | DM Sans | 400 | 11–12px |
| Pullquotes | Lora italic | 400 | 17px |

### Google Fonts import

Always load both fonts together via a single `<link>` tag placed before any stylesheet:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
```

### CSS variables

Always use these variables rather than hardcoding font names:

```css
--font-serif: 'Lora', Georgia, serif;
--font-sans: 'DM Sans', system-ui, sans-serif;
```

### Rules

- Headlines and card titles always use Lora.
- Body copy, navigation, and UI text always use DM Sans.
- Italic text in headlines uses Lora italic and Cobalt colour to signal an idea or phrase worth noticing.
- Sentence case everywhere. Never title case, never all-caps (except micro-labels with `letter-spacing`).
- No font-size below 11px.

---

## Layout

- Max content width: no explicit max — the blog is full-width within its container.
- Base padding: `40px` horizontal on all sections.
- Section dividers: `1px solid var(--sand)` top border. Never box shadows between sections.
- Border radius: `2–4px` on interactive elements. Cards use `3–4px`. Avoid large radii; this design is editorial, not bubbly.

---

## Components

### Logo mark

```
laís.
```

- Lora serif, 18–19px, weight 600.
- The dot (`.`) is Cobalt `#153FB3`.
- Always lowercase. Never "Laís" with a capital L in the logo.

### Navigation

- Background: Cream with a 1px Sand bottom border.
- Height: 56px.
- Links: DM Sans 13px, Ink Muted. Active state: Cobalt, weight 500.
- CTA ("Subscribe"): 1px Cobalt border, Cobalt text, transparent background, 2px border-radius.

### Buttons

**Primary** (e.g. "Read latest"):
```css
background: #153FB3;
color: #fff;
font-size: 13px;
font-weight: 500;
padding: 10px 24px;
border: none;
border-radius: 2px;
letter-spacing: 0.04em;
```

**Ghost** (e.g. "All posts"):
```css
background: none;
border: none;
color: #5C4F35; /* Ink Muted */
font-size: 13px;
/* append → arrow in Amber via ::after */
```

### Cards

Post cards use white `#fff` background with a `1px solid var(--sand)` border and a 3px coloured top bar:
- AI category: Cobalt `#153FB3`
- Community category: Amber `#E8A62C`
- Personal category: Sienna `#D98723`

Featured / hero card uses Sand background.

### Tags and labels

Micro-labels (category tags, topic pills):
```css
font-size: 10–11px;
font-weight: 500;
letter-spacing: 0.1em;
text-transform: uppercase;
```

Active tag: Cobalt background, white text.
Inactive tag: Cream background, Ink Muted text, 1px Sand border.

### Pullquotes

```css
border-left: 3px solid #E8A62C; /* Amber */
padding: 12px 20px;
background: rgba(232,166,44,0.08);
border-radius: 0 2px 2px 0;
font-family: var(--font-serif);
font-style: italic;
font-size: 17px;
color: #1A1610; /* Ink */
```

### Avatar / initials circle

```css
width: 24px;
height: 24px;
background: #153FB3; /* Cobalt */
border-radius: 50%;
color: #fff;
font-size: 10px;
font-weight: 500;
```

---

## Voice

The blog is personal and direct. A few rules:

- First person. "I moderated", "I learned", not "one can observe".
- Short sentences for emphasis. Longer ones to develop an idea.
- No em dashes. Ever. Use a comma, a full stop, or a new sentence.
- No corporate phrasing. Nothing "seamless", "powerful", "robust", or "game-changing".
- Sentence-case headlines only.
- Honest over polished. It's fine to say "I'm not sure" or "this surprised me".

---

## What to avoid

- White backgrounds as page base. Always Cream.
- Large border radii (>6px on content elements).
- Gradients anywhere except the hero card image abstract decoration.
- Pure black text. Use Ink `#1A1610`.
- Cobalt used decoratively. Reserve it for interactive and focus elements.
- Title case headlines.
- Em dashes in any copy.
- Inter, Roboto, or system-ui fonts in user-facing text. Always load Lora + DM Sans.
