# Design System

This document outlines the design tokens, typography, colors, and common components used across the Ariel Parra website.

## Colors

The project uses the [Nord theme](https://www.nordtheme.com/) color palette as its base, ensuring a clean and consistent aesthetic.

### Brand Palette (Nord)
- **Yellow**: `#ebcb8b`
- **Orange**: `#d08770`
- **Red**: `#bf616a`
- **Magenta**: `#b48ead`
- **Blue**: `#5e81ac`
- **Cyan**: `#81a1c1`
- **Aqua**: `#8fbcbb`
- **Green**: `#a3be8c`

### Neutral Palette
- **White (Snow Storm)**: `#d8dee9`
- **Black (Polar Night)**: `#242933`
- **Gray 1**: `#323a48`
- **Gray 2**: `#373e4d`
- **Gray 3**: `#3b4252`
- **Gray 4**: `#4c566a`
- **Gray 5**: `#4b5f82`

## Theme Modes

The site supports dynamic theming (`theme-dark` and `theme-light`).

### Dark Mode (Default)
- **Background**: Black (`#242933`)
- **Card Background**: Gray 3 (`#3b4252`)
- **Text**: White (`#d8dee9`)
- **Links**: Aqua (`#8fbcbb`), Hover: Magenta (`#b48ead`)
- **Buttons**: Gray 4 (`#4c566a`), Hover: Card Background (`#3b4252`)

### Light Mode
- **Background**: White (`#d8dee9`)
- **Card Background**: Cyan (`#81a1c1`)
- **Text**: Black (`#242933`)
- **Links**: White (`#d8dee9`), Hover: Blue (`#5e81ac`)
- **Buttons**: Blue (`#5e81ac`), Hover: Gray 4 (`#4c566a`)

## Typography

- **Primary Font**: `sans-serif` (System default)
- **Display/Brand Font**: `Pixelify Sans` (Used for specific stylizations, e.g., the letter "a" in the name)

## Components

### Buttons
- **Shape**: Rounded borders (`border-radius: 35px`)
- **Padding**: `15px`
- **Shadow**: `box-shadow: 4px 4px 2px 1px var(--gray1)`
- **Behavior**: Scale `1.2` on active.

### Cards (`.card`)
- **Shape**: Rounded corners (`border-radius: 5px`)
- **Padding/Margin**: `10px`
- **Shadow**: `box-shadow: 4px 4px 2px 1px var(--gray1)`
- **Width constraints**: Min `20rem`, Max `20rem` (except `.max-width` modifiers)

### Navigation (`nav > a`)
- **Shape**: Rounded corners (`border-radius: 5px`)
- **Padding**: `1rem 2rem`
- **Shadow**: `box-shadow: 4px 4px 2px 1px var(--gray1)`
- **Interactions**: Smooth hover effects and color transition.

## Accessibility
- Links are clearly distinguishable and implement focus rings (`outline: 2px solid var(--nord10)`).
- Icon-only buttons (like Theme and Language toggles) use explicit `aria-label` attributes.
- Meaningful image assets use valid `alt` tags, while decorative elements use empty strings.
