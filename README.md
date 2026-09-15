# Amadeus-Extensions

Public design direction and discussion for the Amadeus extension system.

> **Status: Exploratory**
>
> This repository describes our current goals and design direction. No stable extension specification, public API, or SDK has been released. Interfaces, compatibility guarantees, and release dates are not yet committed.

## Why this repository exists

We want developers to extend Amadeus without modifying its core code, and users to install, configure, enable, disable, and uninstall extensions easily.

Our current focus is how extensions fit into Amadeus capability discovery, routing, and runtime management. Package formats and interfaces will be developed and validated through real integrations.

## Current design direction

### Capability discovery within a prompt budget

- Limit the prompt overhead introduced by extensions, without loading every extension's full instructions and tool definitions on every conversation turn.
- Use concise capability descriptions for routing, then load relevant contracts, instructions, and context when execution requires them.
- Account for both individual extension budgets and the total candidate budget while keeping installed capabilities discoverable and selectable.

### Integration with existing routing

- Build on existing routing and execution boundaries so extensions can register, deactivate, and unregister consistently.
- Keep routing-visible capabilities aligned with what the current execution entry point can actually run.
- Allow integrations without requiring each extension to modify core routing logic or append its own system prompt instructions.

### A manageable lifecycle

- Define the behavior of installation, configuration, enablement, disablement, upgrades, and removal.
- Stop accepting new calls after deactivation, with explicit handling for existing tasks, connections, and background resources.
- Preserve necessary history and define clear rules for handling user data.

### Controlled runtime impact

- Contain the effects of extension dependencies, state, and failures on the core runtime and other extensions.
- Keep the Host responsible for identity, permissions, execution authority, and durable facts.
- Installing or enabling an extension does not itself authorize a specific action.

These are design goals. The guarantees provided will be documented as runtime mechanisms are implemented and validated.

## Relationship to Amadeus

The [Amadeus project](https://github.com/Code-Amadeus/Amadeus) already includes foundations such as Providers, MCP, Skills, AUIP, and CapabilityCatalog.

These mechanisms cover execution capabilities, external tools, workflows, application collaboration, and capability management and discovery. Future extension work will build on these boundaries, exploring shared distribution and management while preserving the responsibilities of each native protocol.

Existing internal implementations are not stable third-party extension interfaces. This repository does not currently provide a loader, installable extensions, or integration tutorials.

## Open questions

- Extension package formats and manifest fields.
- Public APIs, SDKs, and supported integration types.
- Prompt budget allocation and capability candidate selection.
- Installation, updates, compatibility, and isolation mechanisms.
- Release schedules and stability commitments.

## Join the discussion

Use [Discussions](https://github.com/Code-Amadeus/Amadeus-Extensions/discussions) to share extension needs, real integration scenarios, and design feedback. We are especially interested in:

- Capabilities you want to add to Amadeus and the runtime support they require.
- How capability descriptions and execution context should fit within a limited prompt budget.
- User-visible behavior that registration, deactivation, and unregistration should guarantee.

For now, the priority is understanding goals and real needs. Specifications, examples, and developer tools will follow as the direction is validated.
