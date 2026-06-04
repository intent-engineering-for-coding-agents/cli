---
status: accepted
date: 2026-05-04
decision-makers: Intent Engineering for Coding Agents Contributors
---

# ADR-0004: BYOK via MCP — Not Direct API Calls, Not Shell-Out

## Context and Problem Statement

The agent-assisted layer of iec-cli requires a model to evaluate semantic qualities. The tool must decide how to interact with a coding agent: direct API calls to a specific provider, shell-out to CLI tools, or a protocol-based bridge that lets the user's own coding agent handle the evaluation.

## Considered Options

* Direct API calls (e.g., OpenAI, Anthropic SDKs)
* Shell-out to CLI tools (e.g., `claude`, `opencode`)
* MCP (Model Context Protocol) — tool starts server, user's coding agent connects

## Decision Outcome

Chosen option: "MCP", because it is the only option that achieves BYOK (Bring Your Own Key/Agent). The tool does not hardcode a provider, does not manage API keys, and does not assume which coding agent the user has. MCP is the emerging standard for agent-tool integration and aligns with Intent Engineering's vendor-agnostic principle.

### Consequences

* Good, because BYOK — user brings any MCP-compatible coding agent
* Good, because no API key management — the tool never touches credentials
* Good, because vendor-agnostic — works with any coding agent that speaks MCP
* Good, because MCP is an open standard, not a single-vendor protocol
* Bad, because MCP requires the user's coding agent to support the protocol — not all agents do yet
* Bad, because the tool must start a server (lightweight, but adds process management)

## Pros and Cons of the Options

### Direct API calls

* Good, because simple — one network call, no process management
* Bad, because vendor lock-in — hardcodes a provider (or requires a provider abstraction layer)
* Bad, because API key management — the tool must handle or configure secrets
* Bad, because violates BYOK — the tool chooses the agent, not the user

### Shell-out to CLI tools

* Good, because leverages existing coding agent CLI tools
* Bad, because each coding agent CLI has a different interface — maintenance burden
* Bad, because fragile — parsing stdout, error handling varies per tool
* Bad, because the tool must know which coding agent CLI the user has installed

### MCP

* Good, because BYOK — user's coding agent connects via standard protocol
* Good, because no API keys in the tool
* Good, because vendor-agnostic — any MCP-compatible agent works
* Good, because structured — tool sends prompt, gets structured response, not raw text
* Neutral, because requires MCP support — growing standard, but not universal yet

## Validation

Verified by: `mcp` Python SDK selected as implementation. MCP server architecture defined: tool starts server on demand, constructs structured prompts from version-controlled templates, sends to user's coding agent via MCP, parses structured response.
