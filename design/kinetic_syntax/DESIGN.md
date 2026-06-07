---
name: Kinetic Syntax
colors:
  surface: '#131315'
  surface-dim: '#131315'
  surface-bright: '#39393b'
  surface-container-lowest: '#0e0e10'
  surface-container-low: '#1c1b1d'
  surface-container: '#201f22'
  surface-container-high: '#2a2a2c'
  surface-container-highest: '#353437'
  on-surface: '#e5e1e4'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e5e1e4'
  inverse-on-surface: '#313032'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#131315'
  on-background: '#e5e1e4'
  surface-variant: '#353437'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.7'
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  container-max: 1440px
  sidebar-width: 280px
---

## Brand & Style

The design system is engineered for the high-density information requirements of backend engineering. It prioritizes rapid knowledge acquisition through a minimalist, "Linear-like" aesthetic that balances technical rigor with sophisticated visual polish.

The brand personality is **precise, authoritative, and focused**. It targets senior engineers who value speed and clarity. The UI evokes a sense of being inside a high-performance terminal—efficient and distraction-free—while leveraging **Glassmorphism** and **Modern Minimalism** to prevent visual fatigue. 

Key stylistic pillars include:
- **High-Density Utility**: Maximizing screen real estate without sacrificing legibility.
- **Glassmorphism**: Using depth and translucency to maintain context during navigation.
- **Technical Contrast**: Using stark dark backgrounds to make code and status indicators pop.

## Colors

The palette is optimized for long-duration deep work in low-light environments. 

- **Primary Canvas**: A deep charcoal (`#09090b`) serves as the foundation to minimize eye strain.
- **Accents**: Indigo (`#6366f1`) is used for primary actions and focus states, providing a high-energy contrast against the dark background.
- **Borders**: Subdued grays (`#27272a`) define structure without creating visual noise.
- **Semantic Logic**: Status colors are saturated and vibrant to ensure critical technical information (e.g., performance bottlenecks or error codes) is immediately identifiable.

## Typography

The typography system employs a dual-font strategy to separate UI intent from technical content.

- **UI & Content**: **Inter** provides a neutral, highly legible foundation for prose and navigation. Tight letter-spacing is used on larger headings to achieve the "Linear" look.
- **Technical Data**: **JetBrains Mono** is reserved for code, metadata, difficulty badges, and system-level labels. The increased x-height and distinct characters ensure no ambiguity in syntax.
- **Hierarchy**: Use `label-caps` for section headers in sidebars and `code-block` for all non-prose technical descriptions.

## Layout & Spacing

The design system utilizes a **Fixed-Fluid Hybrid** layout. 

- **Navigation**: A fixed `sidebar-width` on the left for category browsing.
- **Main Content**: A fluid central column with a maximum width of `1440px` to prevent line lengths from becoming unreadable on ultra-wide monitors.
- **Grid**: A 12-column grid system is used for internal page layouts.
- **Rhythm**: All spacing is derived from a 4px base unit. Use `lg` (24px) for primary guttering between panels and `md` (16px) for internal padding within cards and code blocks.
- **Mobile**: On devices < 768px, sidebars collapse into a bottom-anchored command palette or "drawer" menu.

## Elevation & Depth

Depth is achieved through **Tonal Layering** and **Glassmorphism** rather than traditional heavy shadows.

1.  **Level 0 (Base)**: `#09090b` (Deepest layer).
2.  **Level 1 (Panels/Cards)**: Surface at `#121214` with a 1px solid border of `#27272a`.
3.  **Level 2 (Overlays/Popovers)**: Background of `rgba(24, 24, 27, 0.8)` with a `backdrop-filter: blur(12px)`. This is used for the Command Palette and Hover Tooltips.
4.  **Interaction**: Focus states use a subtle outer glow (0px 0px 8px) using the primary indigo color at 30% opacity.

## Shapes

This design system utilizes a **Soft (0.25rem)** rounding strategy. This ensures the UI feels modern and engineered without the "playfulness" of fully rounded corners.

- **Standard Elements**: Buttons, input fields, and small badges use `0.25rem`.
- **Large Elements**: Cards and code blocks use `0.5rem` (rounded-lg).
- **Interactive States**: Buttons remain rectangular in spirit but soften slightly to `0.25rem` to indicate touch/click targets.

## Components

- **Command Palette**: The primary navigation tool. Centered, glassmorphic overlay. Search results use `jetbrainsMono` for shortcuts (e.g., `⌘K`).
- **Code Blocks**: Background of `#18181b`. Includes a header row with the language label (Top-right, `label-caps`) and a "Copy" utility. Syntax highlighting follows a customized "Nord-Dark" or "Sublime" high-contrast scheme.
- **Difficulty Badges**: Small, `jetbrainsMono` labels. Colors: Green (Easy), Amber (Intermediate), Red (Advanced/Critical). High saturation text on a 10% opacity background of the same color.
- **Interactive Cards**: Horizontal layout for "Relationship Tags." Hovering a card triggers a subtle border color shift from `#27272a` to `#6366f1`.
- **Input Fields**: Minimalist style. No background; only a bottom border of `#27272a` that transitions to a full 1px primary border on focus.
- **Sticky Sidebars**: Used for Table of Contents. Subtle typography (`body-sm`) with a vertical "active" line indicator on the left of the current section.