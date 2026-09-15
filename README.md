# Amadeus-Extensions

Exploring how developers can extend [Amadeus](https://github.com/Code-Amadeus/Amadeus) with new tools, workflows, applications, agents, and assets.

> **Exploratory:** The opening order and shared extension management below express our intentions. A public extension specification, API, and SDK have not yet been released.

## Extension paths

| Developer goal | Suggested integration | Opening direction |
| --- | --- | --- |
| Connect services, query data, or provide tools | MCP | First wave |
| Provide specialist methods, workflows, or templates | Skill | First wave |
| Build interactive apps that collaborate with the character | AUIP | Improve application distribution in a later phase |
| Connect a new agent or execution engine | Provider adapter | Limited developer preview |
| Customize character appearance, scenes, or assets | Existing character-pack system | Maintain a separate asset specification |

## Integration direction

```mermaid
block-beta
    columns 5
    MCP["MCP<br/>Tools and services"] SKILL["Skill<br/>Methods and workflows"] AUIP["AUIP<br/>Interactive apps"] PROVIDER["Provider<br/>Agents and engines"] ASSETS["Character packs<br/>Appearance and assets"]
    SHARED["Shared extension management · Design direction<br/>Bounded prompt context · Routing · Registration and removal"]:5
    CORE["Amadeus core<br/>Conversation and interaction · Permissions and state · Execution and presentation"]:5

    classDef integration fill:#e9f5ef,stroke:#3d8060,color:#193c2a
    classDef direction fill:#fff5df,stroke:#a47a29,color:#4b3510
    classDef core fill:#eaf2ff,stroke:#416da6,color:#192d49
    class MCP,SKILL,AUIP,PROVIDER,ASSETS integration
    class SHARED direction
    class CORE core
```

The integration families already exist; a unified extension layer remains a design goal. Each family keeps its own role, and an extension may combine several of them.

Share ideas and use cases in [Discussions](https://github.com/Code-Amadeus/Amadeus-Extensions/discussions).
