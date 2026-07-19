## 2025-05-15 - [Accessibility and Contrast in HTML Emails]
**Learning:** WCAG AA compliance (4.5:1) is crucial for readability in emails, especially on mobile. "Specialist" category colors often need manual darkening to remain accessible against white backgrounds. Contextual ARIA labels (like `aria-label="Read full article: {title}"`) solve the "ambiguous link text" problem when multiple "Read more" links exist on one page.
**Action:** Always verify color contrast using a tool (or standard darker hex codes) and use semantic headers (`<h3>`) even when the visual design requires inline styling to mimic spans.

## 2025-05-16 - [Scannability and Assistive Noise Reduction in Digests]
**Learning:** For daily digests, scannability is paramount. Adding article counts to navigation and an estimated reading time significantly reduces the cognitive load for the user. Additionally, while emojis and decorative arrows provide visual delight, they create unnecessary noise for screen readers in an already dense email;  is essential for these elements.
**Action:** Always include "at-a-glance" meta-info (counts, time) in headers and wrap all decorative glyphs in  spans.

## 2025-05-16 - [Scannability and Assistive Noise Reduction in Digests]
**Learning:** For daily digests, scannability is paramount. Adding article counts to navigation and an estimated reading time significantly reduces the cognitive load for the user. Additionally, while emojis and decorative arrows provide visual delight, they create unnecessary noise for screen readers in an already dense email; `aria-hidden="true"` is essential for these elements.
**Action:** Always include "at-a-glance" meta-info (counts, time) in headers and wrap all decorative glyphs in `aria-hidden="true"` spans.

## 2025-05-17 - [Semantic Structure in Email Digests]
**Learning:** Transitioning from generic `<div>` stacks to semantic HTML (`<article>`, `<h3>`, `<ul>`, `<main>`) significantly improves the experience for assistive technology users without impacting visual design. Screen readers can use landmark navigation (`<main>`) and structural navigation (headings and articles) to quickly parse a dense daily digest.
**Action:** Use semantic landmarks and heading levels in email templates, even when visual consistency requires complex inline styling to match previous non-semantic designs.

## 2025-05-18 - [Email-Safe Accessibility Controls]
**Learning:** For email accessibility features like "Skip to Content" links, avoid JavaScript handlers (`onfocus`) as most email clients strip them. A `<style>` block using `:focus` classes is more robust, though still not supported by all clients (e.g., Gmail on mobile). Always provide descriptive `aria-label` attributes for navigational links even if they contain text, as it provides clearer intent for screen reader users (e.g., "Jump to section" vs just "Economy").
**Action:** Prioritize CSS-based focus states over JavaScript for email interactivity and use descriptive ARIA labels to clarify navigational intent.

## 2025-05-19 - [Accessible Contrast for Themed Section Headers]
**Learning:** Themed section headers using background colors with white text must be carefully selected to meet WCAG AA contrast ratios (4.5:1). Darker, more saturated versions of brand colors (e.g., #196f3d for green, #21618c for blue, #a04000 for orange) ensure readability without sacrificing the visual identity of the sections.
**Action:** Always verify contrast ratios for any new color tokens added to the TOPIC_COLORS mapping and prefer darkened shades for backgrounds that host light text.

## 2024-06-07 - [Print-Optimized Styles for Study-Heavy Content]
**Learning:** For study-oriented content like UPSC digests, users often print materials for offline reading and annotation. Standard email templates with sticky headers, navigation bars, and "back to top" links create significant clutter on paper. A @media print stylesheet that hides these elements and uses 'break-inside: avoid' on article cards ensures a professional, readable, and paper-efficient study guide.
**Action:** Always include a print-optimized media query for digests or long-form reports, and use semantic classes to target navigational noise.

## 2026-07-19 - [Robust Programmatic Focus Management and Contrast in HTML Email Jumps]
**Learning:** When using in-page skip-links and anchor links (e.g., jump-to-section) inside HTML emails, screen readers and key-based browsers often fail to redirect focus to non-interactive container targets (such as `<nav>`, `<main>`, and `<section>`). Setting `tabindex="-1"` on these target elements enables robust programmatic focus shifting, while suppressing browser-default visual focus rings with `[tabindex="-1"]:focus { outline: none !important; }` avoids visual clutter. Additionally, focus outlines on interactive components (like `.topic-pill`) must contrast sharply against parent card backgrounds (e.g. using theme colors like `#1a1a2e` in light mode, `#fff` in dark mode) to comply with WCAG 2.4.7.
**Action:** Always use `tabindex="-1"` on target containers of skiplinks/anchor links and customize `:focus-visible` outline colors to contrast explicitly against the actual parent card or background.
