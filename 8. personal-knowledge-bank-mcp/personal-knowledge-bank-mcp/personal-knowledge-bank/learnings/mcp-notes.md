---
type: learning-note
title: MCP Learning Notes
description: Notes about what I learned during the MCP training
tags: [mcp, learning, ai-agents]
---

# MCP Learning Notes

## What I learned
MCP is a standard way to give an AI assistant controlled access to my own
context and actions, instead of pasting things into a chat every time. The
assistant talks to a small server I control, and I decide what it can see and do.

## Key concepts
- Resources: read-only context I hand over — my Markdown notes (a bit like
  static props feeding a component).
- Tools: actions the assistant can call — the functions that list, read and
  search files (the event handlers).
- Prompts: reusable, parameterised instructions — like a saved snippet or
  shared utility.

## What I still find difficult
- Where the line sits between a resource and a tool
- What is safe to expose once this points at real systems

## How I could use this in my work
Put my component docs, design tokens and Storybook notes behind a server, so an
assistant can answer "which button variant do we use for destructive actions?"
straight from our source of truth.
