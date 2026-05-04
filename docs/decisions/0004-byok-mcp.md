# ADR-0004: BYOK via MCP — Not Direct API Calls, Not Shell-Out

* Status: accepted
* Deciders: ASE Book Contributors
* Date: 2026-05-04

## Context and Problem Statement

The AI-assisted layer of ase-cli requires an AI model to evaluate semantic qualities. The tool must decide how to interact with AI: direct API calls to a specific provider, shell-out to CLI tools, or a protocol-based bridge that lets the user's own AI agent handle the evaluation.

## Considered Options

* Direct API calls (e.g., OpenAI, Anthropic SDKs)
* Shell-out to CLI tools (e.g., `claude`, `opencode`)
* MCP (Model Context Protocol) — tool starts server, user's AI connects

## Decision Outcome

Chosen option: "MCP", because it is the only option that achieves BYOK (Bring Your Own Key/Agent). The tool does not hardcode a provider, does not manage API keys, and does not assume which AI the user has. MCP is the emerging standard for AI-tool integration and aligns with ASE's vendor-agnostic principle.

### Consequences

* Good, because BYOK — user brings any MCP-compatible AI agent
* Good, because no API key management — the tool never touches credentials
* Good, because vendor-agnostic — works with any AI that speaks MCP
* Good, because MCP is an open standard, not a single-vendor protocol
* Bad, because MCP requires the user's AI to support the protocol — not all agents do yet
* Bad, because the tool must start a server (lightweight, but adds process management)

## Pros and Cons of the Options

### Direct API calls

* Good, because simple — one network call, no process management
* Bad, because vendor lock-in — hardcodes a provider (or requires a provider abstraction layer)
* Bad, because API key management — the tool must handle or configure secrets
* Bad, because violates BYOK — the tool chooses the AI, not the user

### Shell-out to CLI tools

* Good, because leverages existing AI CLI tools
* Bad, because each AI tool has a different CLI interface — maintenance burden
* Bad, because fragile — parsing stdout, error handling varies per tool
* Bad, because the tool must know which AI CLI the user has installed

### MCP

* Good, because BYOK — user's AI connects via standard protocol
* Good, because no API keys in the tool
* Good, because vendor-agnostic — any MCP-compatible agent works
* Good, because structured — tool sends prompt, gets structured response, not raw text
* Neutral, because requires MCP support — growing standard, but not universal yet

## Validation

Verified by: `mcp` Python SDK selected as implementation. MCP server architecture defined: tool starts server on demand, constructs structured prompts from version-controlled templates, sends to user's AI via MCP, parses structured response.
