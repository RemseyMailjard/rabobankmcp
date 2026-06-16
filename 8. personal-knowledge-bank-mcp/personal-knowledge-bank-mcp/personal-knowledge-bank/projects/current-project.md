---
type: project
title: Current Project
description: Notes about my current front-end project
tags: [project, frontend, accessibility]
---

# Current Project

## Project summary
We are redesigning the "new payment" screen in the online-banking web app. The
legacy screen uses old, inconsistent components that are hard to maintain and
fall short on accessibility. We are rebuilding it with design-system-aligned
React components that are fully keyboard- and screen-reader-friendly. The work
is front-end only; amounts and account data come from existing back-end services.

## Goal
Replace the legacy payment components with reusable, WCAG 2.2 AA compliant
components from our design system, without changing the underlying payment logic.

## Stakeholders
- Product owner (payments squad)
- UX designer
- Accessibility specialist
- Back-end squad (payment services)

## Current status
The component breakdown and design tokens are agreed. The amount-input and
recipient-select components are in review. The confirmation step still needs
accessibility testing.

## Open questions
- How do we announce inline validation errors to screen readers without being noisy?
- Can the recipient-select reuse the existing autocomplete component, or do we fork it?

## Next actions
- Finish keyboard-navigation pass on the confirmation step
- Add Playwright tests for the happy path and one error path
- Book an accessibility review slot
