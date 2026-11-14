# Design

## Source of truth
- Status: Active
- Last refreshed: 2026-11-06
- Primary product surfaces: Home/feed, article, archive and category pages, search, sidebar navigation, and table of contents.
- Evidence reviewed: Existing Chirpy/Jekyll layouts and Sass in `_layouts/`, `_includes/`, and `_sass/`; live homepage at `https://ouyangrong.com`; `reports/seetong-user-feedback-daily.html` as the paper-style reference.

## Brand
- Personality: Personal, thoughtful, editorial, and technically grounded.
- Trust signals: Author identity, publication date, reading time, consistent navigation, and readable article structure.
- Avoid: A dashboard-like homepage, decorative gradients, heavy shadows, excessive cards, and low-contrast gray text.

## Product goals
- Goals: Make writing easy to scan, invite reading, and keep article discovery predictable.
- Non-goals: Reorganizing posts, rewriting article content, or changing the existing search and navigation behavior.
- Success signals: Clearer title hierarchy, stronger text contrast, and usable layouts at desktop and phone widths.

## Personas and jobs
- Primary personas: Readers browsing personal essays and engineering notes; the author maintaining and publishing posts.
- User jobs: Find a recent or older article, scan its topic and length, read comfortably, and navigate by category, tag, or table of contents.
- Key contexts of use: Desktop browsing and mobile reading.

## Information architecture
- Primary navigation: Existing Home, Categories, Tags, Archives, and About links in the sidebar.
- Core routes/screens: Home feed, article, category/tag/archive pages, search results, and About.
- Content hierarchy: Site identity, latest writing, article title and excerpt, publication metadata, then supporting navigation and related context.

## Design principles
- Principle 1: Content leads; site chrome stays quiet.
- Principle 2: Use the feedback report's paper palette, fine rules, and restrained rust accent without copying its dense report layout.
- Principle 3: Keep existing routes, controls, and reading tools; improve their presentation rather than replacing them.
- Tradeoffs: Editorial serif typography gives long-form writing character; sans-serif UI text and monospace code remain practical for scanning.

## Visual language
- Color: Warm paper canvas and surface, charcoal ink, fine warm-gray rules, and muted rust accents; a coordinated warm dark mode remains available.
- Typography: System sans-serif for navigation and metadata; system serif for editorial headings and article prose; monospace for code and data tables.
- Spacing/layout rhythm: A consistent 16px gap below the fixed top bar, a restrained editorial column, generous article line-height, and compact list metadata; collapse supporting columns on smaller screens.
- Shape/radius/elevation: Square corners, one-pixel borders, and no decorative shadows.
- Motion: No ornamental page motion; retain existing functional theme/navigation behavior and use brief color changes only for hover/focus feedback. Honor reduced motion by avoiding new animations.
- Imagery/iconography: Preserve the existing author avatar and theme icons; add no decorative imagery.

## Components
- Existing components to reuse: Chirpy sidebar, topbar/search, post list, paginator, article metadata, right-side panels, TOC, and footer.
- New/changed components: Home masthead and feed heading; paper-themed color and typography overrides.
- Variants and states: Light/dark theme, desktop sidebar with optional panels, and mobile slide-out sidebar.
- Token/component ownership: `_sass/addon/paper.scss` owns the blog paper tokens and presentation overrides; upstream theme structure remains in place.

## Accessibility
- Target standard: WCAG 2.1 AA as the practical target for contrast and keyboard access.
- Keyboard/focus behavior: Keep existing links and controls keyboard reachable; retain a visible focus outline.
- Contrast/readability: Use dark ink on warm light surfaces and light ink on warm dark surfaces; keep article body at least 16px.
- Screen-reader semantics: One page-level heading on the home feed, followed by a feed heading and article headings.
- Reduced motion and sensory considerations: No new nonessential motion or flashing states.

## Responsive behavior
- Supported breakpoints/devices: Existing Chirpy breakpoints, with attention to 375px phones, tablet widths, and wide desktop.
- Layout adaptations: Hide desktop-only supporting panels as the theme already does; keep search and navigation operable through the mobile topbar/sidebar.
- Touch/hover differences: Preserve theme touch targets; hover color is supplementary and keyboard focus remains explicit.

## Interaction states
- Loading: Keep existing search and page-view loading indicators.
- Empty: Keep existing theme-provided empty/search states.
- Error: Preserve existing browser and theme error handling.
- Success: Preserve existing navigation and search behavior without new confirmation states.
- Disabled: Keep existing disabled paginator states.
- Offline/slow network, if applicable: Core post content remains statically rendered; existing external analytics and font resources are nonessential.

## Content voice
- Tone: Personal, direct, and reflective; keep the existing English site navigation and author tagline.
- Terminology: Retain existing labels and article titles.
- Microcopy rules: Do not add promotional claims or instructions to the reading interface.

## Implementation constraints
- Framework/styling system: Jekyll with the Chirpy 4.0.1 theme and Sass.
- Design-token constraints: Override theme CSS custom properties after the theme import; preserve theme mode selection.
- Performance constraints: No new dependencies, web fonts, or JavaScript.
- Compatibility constraints: Keep existing permalinks, search, pagination, and light/dark preference behavior.
- Test/screenshot expectations: Inspect desktop and mobile browser renders; use the smallest available Jekyll/Sass validation.

## Open questions
- None for this scoped visual refresh.
