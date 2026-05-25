# AGENTS.md: User Service

## Architecture

- All business logic lives in service classes under `src/`
- Validation belongs in the service layer, not in controllers or helpers
- Use class-based design for stateful components

## Specs

- All spec scenarios must include an acceptance-criterion ID in the format `[PREFIX-NNN]`
- Use `@pytest.mark.ac("PREFIX-NNN")` to tag every test that proves a scenario
- Keep `openspec/specs/` current when adding capabilities

## Documentation

- Keep `docs/INDEX.md` current whenever a new document is added under `docs/`
