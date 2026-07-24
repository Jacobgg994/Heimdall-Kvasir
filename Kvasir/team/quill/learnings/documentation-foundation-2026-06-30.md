# Documentation Foundation Study

**Quill** — 2026-06-30
**Task:** Study 5 documentation tools and deliver: stack recommendation, API doc template, style guide proposal, docs-as-code workflow

---

## Tools Studied

| Tool | Version | Purpose | License |
|------|---------|---------|---------|
| Docusaurus | v3.10.1 | Documentation site framework | MIT |
| OpenAPI Specification | v3.2.0 | REST API contract standard | Apache-2.0 |
| Mermaid | latest | Text-to-diagram engine | MIT |
| Write the Docs | community | Docs best practices & community | CC |
| Swagger UI | v5.32.0 | Interactive API doc renderer | Apache-2.0 |

---

## 1. Documentation Stack Recommendation

### Primary: Docusaurus

Docusaurus is the recommended foundation. Reasons:

- **Three content types** in one framework: Docs (versioned + sidebar), Blog (changelogs/release notes), Pages (landing/about/custom).
- **MDX support** — embed React components, live demos, and custom interactive elements directly in Markdown.
- **Versioning** — cut doc versions that match API or product releases. Keeps historical docs accessible without cluttering the current tree.
- **i18n** — CrowdIn integration for multi-language documentation (relevant if Thai documentation is needed).
- **Plugin ecosystem** — search (Algolia DocSearch or local), Mermaid diagrams, OpenAPI rendering, analytics.
- **CI/CD ready** — builds to static HTML/JS/CSS; deploys to Netlify, Vercel, GitHub Pages, Cloudflare Pages.

### API Layer: OpenAPI Specification + docusaurus-plugin-openapi-docs

- Write API contracts once in OpenAPI 3.x YAML/JSON.
- `docusaurus-plugin-openapi-docs` converts specs to native MDX pages with sidebar integration, "Try It" functionality, and versioning support.
- The plugin is preferred over embedding Swagger UI directly (no SSR issues, full search integration, better performance via external JSON normalization).
- Alternatively, **Redocusaurus** (Redoc-based) provides a Stripe-style three-panel layout if that aesthetic fits better.

### Diagram Layer: Mermaid

- Enable via `@docusaurus/theme-mermaid`.
- All diagram types supported: flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, C4 architecture diagrams, git graphs.
- Diagrams live in Markdown as text — version-controlled, diffable, never out of sync with code.

### Quality Layer: Write the Docs principles

- Community-curated best practices for structure, tone, accessibility, and workflow.
- Style guide direction (covered in Section 3).
- Docs-as-Code methodology (covered in Section 4).

---

## 2. API Documentation Template

### OpenAPI 3.x Spec Template

```yaml
openapi: "3.2.0"
info:
  title: "[Service Name] API"
  version: "1.0.0"
  description: |
    [One-paragraph description of the service and its purpose.]
  contact:
    name: "[Team Name]"
    url: "https://[team-url]/"
    email: "[team-email]"
  license:
    name: "Proprietary / MIT / Apache-2.0"

servers:
  - url: "https://api.example.com/v1"
    description: "Production"
  - url: "https://staging-api.example.com/v1"
    description: "Staging"

tags:
  - name: "[Resource]"
    description: "[What this resource represents]"

paths:
  /[resource]:
    get:
      operationId: list[Resources]
      tags: ["[Resource]"]
      summary: "List all [resources]"
      description: "[More detail about what this endpoint returns]"
      parameters:
        - name: "page"
          in: query
          required: false
          schema:
            type: integer
            default: 1
          description: "Page number for pagination"
        - name: "limit"
          in: query
          required: false
          schema:
            type: integer
            default: 20
            maximum: 100
          description: "Items per page"
      responses:
        "200":
          description: "Successful response"
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/[Resource]"
    post:
      operationId: create[Resource]
      tags: ["[Resource]"]
      summary: "Create a new [resource]"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Create[Resource]Request"
      responses:
        "201":
          description: "Resource created"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/[Resource]"
        "400":
          description: "Invalid input"

components:
  schemas:
    [Resource]:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
          description: "Unique identifier"
        name:
          type: string
          description: "Display name"
        created_at:
          type: string
          format: date-time
          description: "Creation timestamp"
        updated_at:
          type: string
          format: date-time
          description: "Last update timestamp"
      example:
        id: "550e8400-e29b-41d4-a716-446655440000"
        name: "Example resource"
        created_at: "2026-06-30T12:00:00Z"
        updated_at: "2026-06-30T12:00:00Z"

    Create[Resource]Request:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
          description: "Display name"
```

### Docusaurus API Doc Page Template

When writing supplementary documentation for an API endpoint (not the generated spec):

```markdown
---
sidebar_label: "[Endpoint Summary]"
---

# [Endpoint Summary]

## Overview

[One paragraph describing what this endpoint does and when to use it.]

## Endpoint

```
[HTTP_METHOD] [base_url]/[path]
```

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `[name]` | `[type]` | Yes/No | `[value]` | [Description] |

## Request Body

```json
[Example JSON request body]
```

## Response

### Success (20x)

```json
[Example JSON response body]
```

### Error (4xx/5xx)

| Status | Description |
|--------|-------------|
| 400 | [When this happens] |
| 401 | [Auth requirement] |
| 404 | [Resource not found] |
| 500 | [Server error] |

## Example Usage

```bash
curl -X [METHOD] "[base_url]/[path]" \
  -H "Authorization: Bearer [token]" \
  -H "Content-Type: application/json" \
  -d '[request body]'
```

## Notes

[Edge cases, rate limits, idempotency guarantees, migration notes if applicable.]
```

---

## 3. Style Guide Proposal

Based on Write the Docs community consensus, Diátaxis framework, and industry best practices.

### Content Architecture (Diátaxis)

Every piece of documentation belongs to exactly one of four quadrants:

| | **Study** (learning) | **Work** (task) |
|---|---|---|
| **Theory** (concept) | Tutorials — step-by-step lessons | Conceptual guides — explanation of "why" |
| **Practice** (execution) | How-to guides — practical problem solving | Reference — precise technical specs |

**Rule:** Never mix quadrants in a single page. Link between them instead.

### Voice and Tone

| Attribute | Guideline |
|-----------|-----------|
| Voice | Active, direct, human. Prefer "you" over "the user". |
| Tense | Present tense. "The endpoint returns a list" not "will return". |
| Mood | Imperative for instructions ("Run the command"), indicative for reference. |
| Jargon | Define on first use. Avoid when a plain word works. |
| Contractions | Allowed. They sound natural and reduce formality barriers. |
| Humor | Use sparingly and only when it aids clarity. Never at the reader's expense. |

### Writing Conventions

1. **Titles** — Sentence case. "How to configure a profile" not "How To Configure A Profile".
2. **Code blocks** — Always specify language. Fenced with backticks.
3. **Bold** — UI labels and button names.
4. **Inline code** — File paths, commands, parameter names, values.
5. **Lists** — Bullet for unordered. Numbered for sequential steps.
6. **Admonitions** — Docusaurus native: `:::note`, `:::tip`, `:::info`, `:::caution`, `:::danger`.
7. **Links** — Describe the destination. Not "click here" but "see the configuration reference".
8. **Accessibility** — Alt text on all images. Sufficient color contrast. Semantic heading hierarchy (no skipping levels).
9. **Bias** — Use gender-neutral language. Use diverse example names.

### Terminology Rules

| Do | Don't |
|----|----|
| API, not "the API" (as a proper noun) | Utilize (use "use") |
| Login (noun), log in (verb) | Leverage |
| Setup (noun), set up (verb) | Basically / Simply |
| Plugin, not plug-in | Just (as in "just run") |
| Backend, frontend (no hyphen as noun) | Whitelist/blacklist (use allowlist/blocklist) |

### Diagram Style (Mermaid)

- Use consistent direction: `TD` (top-down) for flows, `LR` (left-right) for timelines.
- Color minimalism: limit to 3 distinct colors per diagram.
- Labels are noun phrases, not full sentences.
- Every diagram has a preceding sentence explaining what it shows.

---

## 4. Docs-as-Code Workflow

### Workflow: Documentation Maintained Alongside Code

```
┌─────────────────────────────────────────────────────────────────┐
│                        Feature Branch                           │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐   │
│  │ Code changes  │   │ Doc changes  │   │ Diagram changes  │   │
│  │ (src/)        │   │ (docs/)      │   │ (Mermaid in .md) │   │
│  └──────┬───────┘   └──────┬───────┘   └────────┬─────────┘   │
│         │                  │                     │              │
│         └──────────────────┼─────────────────────┘              │
│                            │                                    │
│                     ┌──────▼──────┐                             │
│                     │  PR Review  │                             │
│                     │  + Vale     │                             │
│                     │  lint check │                             │
│                     └──────┬──────┘                             │
└────────────────────────────┼───────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   CI Preview    │
                    │  (Vercel/Netlify│
                    │   deploy)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Merge → main  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Production     │
                    │  publish        │
                    │  (Docusaurus    │
                    │   build)        │
                    └─────────────────┘
```

### Step-by-step Process

**Before writing:**
1. Determine which Diátaxis quadrant the content belongs to (tutorial / how-to / conceptual / reference).
2. Choose the file location: `docs/` (versioned), `blog/` (release notes), `src/pages/` (custom).
3. Write the OpenAPI spec first for any API-related content (design-first approach).

**During writing:**
1. Write in Markdown with MDX for interactive components.
2. Use Mermaid for diagrams inline — never embed static images of diagrams.
3. Follow the style guide from Section 3.
4. Reference existing docs with relative file paths: `[link](../concepts/architecture.md)` — Docusaurus resolves these to correct versioned URLs.

**Before commit:**
1. Run `vale` linting for terminology, tone, and style compliance.
2. Verify all internal links resolve (Docusaurus `build` step catches broken links).
3. Verify OpenAPI spec validity (`swagger-cli validate` or `redocly lint`).

**In PR:**
1. Docs changes are reviewed alongside code changes (same PR, same reviewer).
2. Docusaurus preview deployment is auto-generated from the PR branch.
3. Vale check results block merge if failing.

**On merge to main:**
1. CI builds Docusaurus site.
2. If a new API version is cut, run `docusaurus gen-api-docs:version` to snapshot the spec.
3. Deploy to production hosting (Vercel/Netlify/GitHub Pages).

### Tooling Pipeline

| Stage | Tool | Purpose |
|-------|------|---------|
| Authoring | VS Code + Markdown | Write content |
| Diagrams | Mermaid (inline) | Version-controlled diagrams |
| Linting | Vale | Terminology, tone, style |
| Validation | redocly-cli | OpenAPI spec correctness |
| Build | Docusaurus CLI | Generate static site |
| Preview | Vercel / Netlify | Per-PR preview deploys |
| Search | Algolia DocSearch | Full-text search |
| Deploy | CI (GitHub Actions) | Production publish |

### Versioning Strategy

| Scenario | Approach |
|----------|----------|
| API version changes | Cut new OpenAPI spec file, run `gen-api-docs:version` |
| Product feature release | Cut new Docusaurus docs version via `docusaurus docs:version` |
| Patch documentation fix | Edit current version only (no new version cut) |
| Deprecated documentation | Keep in `versions/` archive, add deprecation banner via MDX component |

### Content Review Cadence

| Frequency | Activity |
|-----------|----------|
| Per PR | Technical accuracy review + Vale lint check |
| Per release | Version cut + API spec update |
| Quarterly | Full content audit: remove stale content, update screenshots, verify all links |
| Annually | Style guide review, accessibility check, SEO performance review |

---

## Summary: Why This Stack for the JACOB Team

| Need | Solution | Why |
|------|----------|-----|
| Public docs site | Docusaurus | Versioned, searchable, MDX-powered, deploy anywhere |
| API documentation | OpenAPI + docusaurus-plugin-openapi-docs | Single source of truth, interactive "Try It", versioned |
| Diagrams | Mermaid | Text-defined, version-controlled, never out of date |
| Quality standards | Write the Docs / Vale | Community-vetted best practices enforced by CI |
| Interactive API UI | Swagger UI (via plugin) | The de facto API exploration interface, integrated natively |

The stack follows the "Nothing is Deleted" principle: specs, diagrams, and docs all live in git history. It follows "Patterns Over Intentions": the OpenAPI spec is the single source of truth — the generated docs are derived, not duplicated. And it follows "External Brain, Not Command": the docs surface what exists without deciding what to build.
