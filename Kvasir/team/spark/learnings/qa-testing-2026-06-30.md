# SPARK ⚡ Learning Report — QA Testing & Automation Framework

> **วันที่:** 2026-06-30
> **แหล่งเรียนรู้:** Selenium-Python-Example, Playwright Framework, Playwright Docs, Social Analyzer, JavaScript Testing Best Practices
> **วัตถุประสงค์:** สร้าง QA testing strategy สำหรับ GemLogin workflows, template QA checklist, regression testing approach

---

## สารบัญ

1. [Enterprise Test Architecture](#1-enterprise-test-architecture)
2. [Playwright Framework Analysis](#2-playwright-framework-analysis)
3. [Social Profile Validation](#3-social-profile-validation)
4. [Testing Best Practices Compendium](#4-testing-best-practices-compendium)
5. [GemLogin QA Strategy](#5-gemlogin-qa-strategy)
6. [Template QA Checklist](#6-template-qa-checklist)
7. [Regression Testing Approach](#7-regression-testing-approach)
8. [Common Workflow Bugs & Fixes](#8-common-workflow-bugs--fixes)
9. [Recommendations](#9-recommendations)

---

## 1. Enterprise Test Architecture

### ที่มา: [nirtal85/Selenium-Python-Example](https://github.com/nirtal85/Selenium-Python-Example)

### โครงสร้างโปรเจกต์มาตรฐาน

```
project/
├── src/                    # Core framework (Page Objects, utilities)
├── tests/                  # Test cases organized by feature/suite
├── resources/              # Test data, configuration assets
├── .github/                # CI/CD workflow definitions
├── pyproject.toml          # Project metadata & tool config
├── uv.lock                 # Deterministic dependency locking
└── .pre-commit-config.yaml # Pre-commit hooks
```

**Key Takeaway:** แยก source code ออกจาก tests, config ไว้ข้างนอก, CI pipeline อยู่กับ code

### Design Patterns ที่ค้นพบ

| Pattern | รายละเอียด | นำไปใช้กับ GL Workflows |
|---------|-----------|----------------------|
| **Page Object Model** | สร้าง class แทนแต่ละหน้า UI | สร้าง block abstraction — each GL block = 1 class with business-level methods |
| **Pytest Fixtures** | conftest.py จัดการ browser/driver lifecycle | สร้าง workflow fixture template — setup profile, load cookies, run, teardown |
| **Tag-Based Selection** | pytest -m sanity — เลือก tests ตาม tag | Tag workflows: #smoke, #regression, #edge-case, #performance |
| **Browser Version Pinning** | กำหนดเวอร์ชัน browser ตายตัว | กำหนด GemLogin/CDP browser version — ป้องกัน surprise breakage |
| **Environment Config** | .env สำหรับ secrets | ใช้ .env สำหรับ proxy, cookies paths, API keys — ไม่ hardcode |

### CI/CD Integration Patterns

- **Continuous Integration:** run บนทุก push (fast checks)
- **Scheduled Validation:** monthly/weekly full regression
- **Report Deployment:** Allure Reports → GitHub Pages (screenshots, logs, video)

### Retry & Resilience

- Tenacity library สำหรับ retry flaky operations
- Visual Regression Tracker สำหรับ pixel-level UI drift detection
- Pre-commit hooks (Ruff) สำหรับ lint ก่อน CI

### สิ่งที่ควรนำมาใช้กับ GemLogin

1. **Allure-style reporting** — จับ screenshot, log, video ทุก step ใน workflow
2. **Tag-based workflow selection** — รันเฉพาะ sanity/regression suite
3. **Deterministic dependency lock** — freeze dependency versions
4. **Pre-flight checks** — validate proxy, cookies, profile state ก่อน run

---

## 2. Playwright Framework Analysis

### ที่มา: [microsoft/playwright](https://github.com/microsoft/playwright), [playwright.dev](https://playwright.dev)

### Core Value Propositions

| Feature | รายละเอียด | ประโยชน์สำหรับ GL QA |
|---------|-----------|---------------------|
| **Single API, 3 engines** | Chromium, Firefox, WebKit — 1 API | Test GL workflows ข้าม browser engine |
| **Auto-waiting** | รอ element actionable โดยอัตโนมัติ | ลด flaky tests — ไม่ต้อง guess timeout |
| **Web-first assertions** | Assertions retry จนกว่าจะผ่าน | ตรวจสอบ state จริง ไม่ใช่แค่ DOM exist |
| **Browser contexts** | Isolated session per test — zero overhead | เปิดหลาย profile แยกกันได้ clean |
| **Trace Viewer** | DOM snapshot ทุก action + network + console | Debug workflow failure โดยไม่ต้อง re-run |
| **Codegen** | Record actions → generate code | สร้าง GL workflow template จาก manual run |
| **Network interception** | route() — mock/stub/modify network | ทดสอบ proxy fail, timeout scenarios |
| **Storage state** | Save/reuse auth state | Reuse FB-VIA cookie state ข้าม tests |

### Locator Strategy Hierarchy

Playwright แนะนำ locators แบบนี้ (จากดีไปหาน้อย):

1. `getByRole()` — ตาม semantic role (button, textbox, dialog)
2. `getByLabel()` — ตาม label text
3. `getByPlaceholder()` — ตาม placeholder
4. `getByTestId()` — data-testid attribute (recommended สำหรับ automation)
5. **CSS/XPath** — ใช้เป็นทางเลือกสุดท้าย

**GemLogin Application:** GL ใช้ CDP protocol — เราควรใช้ `page.locator()` ด้วย data-testid หรือ unique selectors เหมือนกัน

### Playwright vs Selenium — ข้อแตกต่างที่สำคัญ

| มิติ | Selenium | Playwright |
|------|----------|------------|
| Auto-wait | ต้อง manual — WebDriverWait | Built-in auto-wait |
| Cross-browser | ต้อง WebDriver แยกแต่ละตัว | 1 API สำหรับ 3 engines |
| Network control | จำกัด (ผ่าน proxy middleware) | Native route() API |
| Test isolation | ต้อง setup เอง | Browser context = instant isolation |
| Tracing | ต้อง third-party | Built-in trace viewer |
| Parallelism | Thread-based | Worker-based (ประสิทธิภาพสูงกว่า) |
| Modern web support | ตามหลัง | First-class — Shadow DOM, SPAs, iframes |
| Debugging | Screenshot | Trace with DOM snapshots |

### Playwright MCP & CLI สำหรับ AI Agent

Playwright มีเครื่องมือสำหรับ AI agent โดยเฉพาะ:

- **`@playwright/cli`** — Token-efficient browser automation สำหรับ Claude Code, Copilot — ใช้ skill-based workflows
- **Playwright MCP Server** — ให้ LLM ควบคุม browser ผ่าน accessibility snapshots (ไม่ต้องใช้ vision model)
- **Accessibility snapshots** — ใช้ structured accessibility tree (role, name, ref) — deterministic interaction

**สำหรับ GL Workflow Automation:** เขียน GL workflow validation scripts โดยใช้ Playwright CLI — ถูกกว่า MCP ในแง่ token usage

---

## 3. Social Profile Validation

### ที่มา: [qeeqbox/social-analyzer](https://github.com/qeeqbox/social-analyzer)

### Architecture

```
social-analyzer/
├── modules/       # Detection engines (normal, advanced, special, OCR)
├── public/        # Web frontend
├── data/          # Website definitions, rules, profiling data
└── test/          # Test suites
```

3 interfaces: Web app, Node.js CLI, Python CLI (importable as object)

### Detection Mode Tiers

| Mode | Mechanism | Speed | Use Case |
|------|-----------|-------|----------|
| **Fast** | HTTPS library (~1000+ sites) | วินาที | Quick health check |
| **Slow** | WebDriver (Selenium) | นาที | Full page rendering |
| **Special** | Facebook/Google-specific | กลาง | FB-VIA profile validation |

### Rating System

- 0–100 rating ใน 3 categories: **No-Maybe-Yes**
- Multi-technique: string permutation, HTTP probing, WebDriver, OCR, metadata extraction
- ออกแบบมาให้ "fewer false positives"

### ประโยชน์สำหรับ QA ของ FB-VIA / Social Media Profiles

**ใช้ได้:**
- ตรวจสอบว่า FB-VIA profile ถูก detect บน platforms ต่างๆ
- JSON output mode — integratable เข้ากับ test harness
- Multi profile search — ทดสอบ correlation ระหว่าง profiles
- Re-check failed profiles — retry strategy สำหรับ flaky detection

**ข้อจำกัด:**
- No access control — ใช้ได้เฉพาะ local
- ไม่เหมาะกับ production-facing test data
- Detection rules อาจ stale ถ้า platform เปลี่ยน
- Dependencies หนัก (Chrome, Firefox, Tesseract)
- ไม่มี versioned REST API — ไม่มี contract testing

### ข้อเสนอแนะสำหรับ QA Pipeline

1. **ใช้ Fast mode** สำหรับ daily health check — ตรวจว่า profile ยังถูก detect อยู่ไหม
2. **ใช้ Slow mode** สำหรับ weekly full validation — ตรวจ layout, content, metadata
3. **ใช้ Special mode** สำหรับ FB-VIA profiles โดยเฉพาะ — FB detection มี heuristics พิเศษ
4. **Integrate JSON output** กับ Allure test report

---

## 4. Testing Best Practices Compendium

### ที่มา: [goldbergyoni/javascript-testing-best-practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

### The Golden Rule

> "Design for lean testing — short, dead-simple, flat, and delightful to work with."

Test code ไม่ควรใช้ mental bandwidth เท่ากับ production code Cherry-pick cost-effective techniques with high ROI.

### 4.1 หลักการตั้งชื่อ Test — Three-Part Name

```
[สิ่งที่ทดสอบ] - [ภายใต้สถานการณ์] - [ผลลัพท์ที่คาดหวัง]
```

ตัวอย่าง:
```
"WorkflowExecutor.runProfile — when proxy fails — should retry 3 times then log error"
```

### 4.2 AAA Pattern (Arrange, Act, Assert)

```
// Arrange — เตรียมทุกอย่าง
const profile = createTestProfile({ proxy: { host: '...', port: ... }});
const workflow = loadWorkflow('fb-warm.json');

// Act — กระทำการ (1 บรรทัด)
const result = await workflow.execute(profile);

// Assert — ตรวจสอบผลลัพท์ (1-2 บรรทัด)
expect(result.status).toBe('completed');
expect(result.errors).toHaveLength(0);
```

### 4.3 Black-Box Testing — ทดสอบเฉพาะ Public Behavior

- ทดสอบ output ไม่ใช่ internal implementation
- "Test the behavior, not the implementation"
- ถ้า API ให้ผลลัพท์ถูกต้อง — ไม่สนว่า internally มันทำงานยังไง
- ไม่งั้น test จะ fragile — พอ refactor ก็พัง

### 4.4 Test Doubles — เลือกให้ถูกประเภท

| Type | เมื่อไหร่ควรใช้ |
|------|----------------|
| **Stub** | ทดสอบ behavior ภายใต้ conditions ต่างๆ (เช่น proxy fail, timeout) |
| **Spy** | ตรวจสอบ side effects (เช่น verify ว่า email/SMS ถูกส่ง) |
| **Mock** | ระวัง — ถ้าใช้ตรวจ internal calls จะ fragile |

หลักการ: "Do I use it to test functionality that appears, or could appear, in the requirements document?" ถ้าไม่ใช่ — เป็น white-box testing smell

### 4.5 Realistic Input Data — ใช้ Faker/Chance

- อย่าใช้ "Foo", "bar", "test123"
- สร้าง realistic data — phone numbers, usernames, emails
- พิจารณา randomize หรือ import production data
- GL QA: ใช้ realistic FB-VIA profile data, real proxy endpoints

### 4.6 Property-Based Testing

- แทนที่จะเลือก input 2-3 ตัว — สุ่ม hundreds/thousands permutations
- Library: fast-check, jsverify
- GL QA: Property test GL workflow JSON schema — สุ่มค่าต่างๆ ดูว่า schema validation จับได้ทุกเคส

### 4.7 การวัด Test Effectiveness

| Method | Tools | วัดอะไร |
|--------|-------|---------|
| **Code Coverage** | Istanbul | ว่า code ถูก execute กี่ % |
| **Mutation Testing** | Stryker | mutate code → ดูว่า test จับได้ไหม |
| **Requirements Coverage** | Manual mapping | test ครอบคลุม requirement หรือไม่ |
| **Flakiness Tracking** | CI history | ติดตาม % flaky tests เหนือเวลา |

**Key Insight:** High code coverage ≠ good tests. Mutation testing คือมาตรวัดที่แท้จริง — ถ้าเปลี่ยน logic แล้ว test ยังผ่าน แสดงว่า test ไม่ได้ assert อะไรจริง

### 4.8 Testing Pyramid — Enhanced

```
        /\
       /E2E\          ← ช้า, ใช้กับ release candidates
      /------\
     /Contract\       ← API boundaries, ทุก build
    /------------\
   / Component  \     ← API + DB (real), ทุก commit
  /----------------\
 /     Unit         \ ← Function/class, ทุก save
/--------------------\
```

สำหรับ GL Workflow:
- **Unit:** ทดสอบ block logic แต่ละ block แยกกัน
- **Component:** ทดสอบ workflow ทั้งเส้นด้วย fake profile
- **Integration:** ทดสอบ GL API endpoint interactions
- **Contract:** ทดสอบ workflow JSON schema
- **E2E:** Full profile run with real proxy, browser, cookies
- **Mutation:** Mutate workflow JSON → ดูว่า validation จับได้ไหม

---

## 5. GemLogin QA Strategy

### 5.1 Test Pyramid สำหรับ GL Workflows

```
         /\
        / E2E  \         ← Full profile run จริง (real proxy, real cookies)
       /----------\
      / Integration \    ← GL API endpoint interactions
     /----------------\
    /  Component      \  ← Workflow เต็มเส้น แต่ fake proxy (mock/stub)
   /--------------------\
  /    Block Unit        \ ← แต่ละ block ทดสอบแยก — delay, condition, scroll
 /------------------------\
```

### 5.2 Test Categories & Priority

| Priority | Category | เมื่อไหร่ run | Duration | ตัวอย่าง |
|----------|----------|--------------|----------|---------|
| P0 | **Smoke** | ทุก publish | < 5 min | Workflow เริ่มต้นได้, login สำเร็จ |
| P1 | **Sanity** | ทุก PR | < 15 min | Block หลักทำงาน, cookies ถูก save |
| P2 | **Regression** | ก่อน release | < 60 min | ทุก block, edge cases, error paths |
| P3 | **Performance** | Weekly | < 30 min | Concurrent profiles, memory, speed |
| P4 | **Chaos** | Monthly | < 30 min | Proxy fail, timeout, rate limit |

### 5.3 Block Unit Testing — แต่ละ Block

| Block | Test Cases |
|-------|-----------|
| **Delay** | random(N,M), fixed N, edge (0, 0.1, 99999), negative handling |
| **Condition** | match/no-match, fallback path, nested conditions, empty items |
| **Loop** | 0 iterations, 1 iteration, N iterations, breakpoint edge, infinite loop guard |
| **Scroll** | element-scroll all fields, partial fields, empty fields, timeout |
| **Javascript** | async/sync, early return, IIFE wrapper, external data, error handling |
| **Cookie I/O** | export format, import validation, expired cookies, missing domain |
| **Element Click** | element not found, multiple matches, disabled element, hidden element |
| **Profile Data** | missing fields, partial data, empty arrays, null values |

### 5.4 Test Data Strategy

- **Per-test data** — แต่ละ test สร้าง profile/target ของตัวเอง — ไม่ share
- **Realistic data** — ใช้ Faker ช่วยสร้าง: phone numbers, usernames, emails, proxy endpoints
- **Property-based** — สุ่มค่าต่างๆ ใน workflow JSON เพื่อ validate schema coverage
- **Production-sampled** — import real production workflow data สำหรับ regression (nothing deleted — anonymize)

### 5.5 CI Pipeline

```
pre-commit (lint workflow JSON schema validity)
    ↓
P0: Smoke (profile load + login)
    ↓
P1: Sanity (block หลัก + export)
    ↓
P2: Regression (full suite — parallel)
    ↓
P3: Performance (ถ้า relevant)
    ↓
Report → Allure dashboard
```

---

## 6. Template QA Checklist

### 6.1 Pre-Publish Checklist

#### Schema Validation
- [ ] Workflow JSON เป็นไปตาม spec — fields, types, nesting ครบ
- [ ] Edge connections — sourceHandle/targetHandle ถูกต้อง
- [ ] ไม่มี "Cannot read properties of undefined" triggers (missing fields)
- [ ] Version ถูก increment (`version` field)
- [ ] `name` และ `description` สมเหตุสมผล

#### Block Integrity
- [ ] Delay block — `time` format ถูก (ไม่ใช่ random(N,M) wrapper)
- [ ] Condition block — nested schema 3-level พร้อม items triplet
- [ ] Scroll block — element-scroll มีทุก fields ที่ต้องการ (18 fields)
- [ ] Loop block — breakpoint edge ไป POST-loop step
- [ ] Javascript block — ไม่มี IIFE wrapper, ไม่มี early return
- [ ] Javascript block — async calls ใช้ await อย่างถูกต้อง

#### Environmental Validation
- [ ] Proxy format ถูก (host:port:user:pass หรือ host:port)
- [ ] Cookies — domain/path/expiry ถูกต้อง
- [ ] Target URLs reachable
- [ ] User agent valid
- [ ] Viewport size สมเหตุสมผล

#### Behavior Tests
- [ ] Workflow เริ่มต้น — profile load → blocks execute → complete
- [ ] Error path — proxy fail, timeout, CAPTCHA → handled gracefully
- [ ] Idempotency — run 2 ครั้งติด → state สอดคล้อง
- [ ] Cleanup — profile return to initial state หลัง complete
- [ ] Logging — แต่ละ step log ข้อมูลพอให้ debug

### 6.2 Template Documentation Checklist

- [ ] Use case — workflow นี้ใช้ทำอะไร เมื่อไหร่
- [ ] Prerequisites — ต้องมีอะไรก่อนใช้ (proxy? cookies? profile?)
- [ ] Expected behavior — workflow ทำอะไรบ้าง แต่ละ step
- [ ] Known limitations — อะไรที่ workflow นี้ทำไม่ได้
- [ ] Error recovery — workflow fail แล้ว怎麼辦
- [ ] Version history — changelog
- [ ] Estimated runtime — นานแค่ไหน

### 6.3 Template Library Management

```
templates/
├── stable/       # ผ่าน QA ครบ — พร้อม publish
├── beta/         # กำลังทดสอบ — ยังไม่ผ่าน QA
├── deprecated/   # ไม่แนะนำให้ใช้แล้ว — แต่เก็บไว้ (Nothing is Deleted)
└── archived/     # เลิกใช้ — เก็บประวัติ
```

---

## 7. Regression Testing Approach

### 7.1 Scope Definition

**Full Regression** (ก่อน release):
- ทุก block types (delay, condition, loop, scroll, javascript, element, cookie, profile data)
- ทุก execution paths (success, error, edge)
- Cross-browser (Chromium, Firefox, WebKit ถ้า relevant)
- Performance metrics (execution time, memory)

**Selective Regression** (ทุก PR — based on what changed):
- Changed blocks + all dependent paths
- Block integration boundaries
- Error paths
- 20% full random sampling

### 7.2 Automation Strategy

```python
# Concept — regression runner structure
class GemLoginRegressionRunner:
    def __init__(self):
        self.test_suites = {
            'smoke': [...],
            'full': [...],
            'changed': self._detect_changed_blocks()
        }

    def run_smoke(self):
        """P0: Profile load → login → complete"""
        ...

    def run_block_tests(self, block_type):
        """ทดสอบ block type เดียว — ทุก variant"""
        ...

    def run_workflow_tests(self, workflow_path):
        """ทดสอบ workflow ทั้งเส้น"""
        ...

    def run_edge_cases(self):
        """proxy fail, timeout, CAPTCHA, rate limit"""
        ...
```

### 7.3 Regression Test Selection — Impact Analysis

เมื่อมีการเปลี่ยนแปลง workflow:

1. **ระบุ blocks ที่เปลี่ยน** — diff workflow JSON กับ stable version
2. **ระบุ downstream blocks** — blocks ที่รับ output จาก changed block
3. **รัน tests เฉพาะ** — changed block unit tests + downstream integration
4. **รัน full suite** — ก่อน publish

### 7.4 Flakiness Management

- **Track flakiness rate** — % tests ที่ผ่าน/ไม่ผ่านในแต่ละ run
- **Retry policy** — flaky test retry 3 ครั้งก่อน mark as failed
- **Flaky tag** — mark tests ที่ flaky แต่ไม่ critical — review รายสัปดาห์
- **Root cause analysis** — flaky test → เขียน bug report → fix → remove flaky tag

### 7.5 Performance Regression

| Metric | Baseline | Alert Threshold |
|--------|----------|-----------------|
| Workflow execution time | 120s | > 180s (+50%) |
| Profile memory | 800 MB | > 1.2 GB |
| Block failure rate | < 1% | > 5% |
| API response time (GL :1010) | 200ms | > 1s |

---

## 8. Common Workflow Bugs & Fixes

### สรุปจาก Production Feedback

| Bug | Pattern | Root Cause | Fix | Source |
|-----|---------|------------|-----|--------|
| **IIFE crash** | Javascript block wraps code in `(() => {...})()` | GL handler ไม่ support IIFE สำหรับ non-trivial code | เขียน top-level code โดยตรง | feedback-gemlogin-no-iife-wrapper |
| **Early return crash** | `return;` ใน IIFE top-level | GL handler crash เพราะ undefined 'insert' | ใช้ if-else nesting แทน early return | feedback-gemlogin-no-iife-early-return |
| **Async lost** | await ใน IIFE — ตัวแปรหาย | JS handler ไม่ await async IIFE | อย่าใช้ async IIFE; ใช้ top-level await หรือ callback | feedback-gemlogin-js-sync |
| **Delay format wrong** | ใช้ `random(N,M)` wrapper | GL time field ไม่ support wrapper | ใช้ `N,M` format โดยตรง | feedback-gemlogin-delay-and-loop |
| **Loop breakpoint edge wrong** | Breakpoint edge ไปยัง loop block | ต้องไป POST-loop step ไม่ใช่ loop | แก้ targetHandle | feedback-gemlogin-delay-and-loop |
| **Condition edge wrong** | numeric `output-1`, `output-2` | sourceHandle ต้องใช้ `<node>-output-<group_id>` และ `<node>-output-fallback` | ใช้命名ที่ถูกต้อง | feedback-gemlogin-conditions-edges |
| **Condition schema flat** | Schema flat (ไม่ nesting) | GL ต้องการ 3-level nested schema with items triplet | สร้าง schema ให้ถูกต้อง | feedback-gemlogin-conditions-schema |
| **Scroll fields missing** | element-scroll มีแค่ fields ที่ใช้ | GL ต้องการ ทุก fields (18 fields) | populate ทั้ง 18 fields | feedback-gemlogin-block-full-schema |
| **Cookie not persisting** | profile_data.cookie[] ไม่ refresh | GL import cookies เฉพาะ launch ครั้งแรก | ใช้ CDP Network.setCookie ก่อน navigate | reference-gemlogin-cookie-persistence |
| **Wrong edge target** | Click block → second block ผิด order | Visual editor อาจลากผิด | ตรวจสอบ edges ทุกครั้งก่อน publish | production experience |

### 8.1 Workflow JSON Structure — Golden Rules

```
{
  "nodes": [
    {
      "id": "unique-node-id",
      "type": "delayBlock" | "conditionBlock" | "loopBlock" | "scrollBlock" | "javascriptCode" | "elementClick" | ...,
      "position": { "x": number, "y": number },
      "data": {
        "blockData": {
          // block-type-specific fields — ทุก field ต้องมี
        }
      }
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "source": "source-node-id",
      "target": "target-node-id",
      "sourceHandle": "<source-node>-output-<group_id>" | "<source-node>-output-fallback",
      "targetHandle": "<target-node>-input"
    }
  ]
}
```

### 8.2 Validation Script Concept

```python
# concept — workflow validator
def validate_workflow(workflow_json):
    errors = []

    # Schema check
    if missing_required_fields(workflow_json):
        errors.append("Missing required fields")

    # Edge check
    for edge in workflow_json.get('edges', []):
        if not edge.get('sourceHandle'):
            errors.append(f"Edge {edge['id']} missing sourceHandle")
        if not edge.get('targetHandle'):
            errors.append(f"Edge {edge['id']} missing targetHandle")

    # Block-specific checks
    for node in workflow_json.get('nodes', []):
        block_type = node['type']
        data = node['data'].get('blockData', {})

        if block_type == 'delayBlock':
            if '(' in str(data.get('time', '')):
                errors.append(f"Node {node['id']}: delay time should not use wrapper")

        if block_type == 'javascriptCode':
            if re.search(r'\(\(\)\s*=>\s*\{', data.get('code', '')):
                errors.append(f"Node {node['id']}: contains IIFE wrapper")

        if block_type == 'conditionBlock':
            if 'items' not in data:
                errors.append(f"Node {node['id']}: condition missing items")

        if block_type == 'scrollBlock':
            required_keys = [...]
            missing = [k for k in required_keys if k not in data]
            if missing:
                errors.append(f"Node {node['id']}: scroll missing {missing}")

    return errors
```

---

## 9. Recommendations

### 9.1 Immediate Actions

1. **สร้าง Workflow Schema Validator** — script ตรวจสอบ workflow JSON structure ก่อน publish (ป้องกัน bugs ที่รู้แล้ว 10+ รายการ)
2. **กำหนด Test Categories ด้วย Tags** — #smoke, #regression, #edge-case, #performance — ใน workflow metadata
3. **สร้าง Pre-publish Checklist** — template สำหรับ QA ทุกครั้งก่อน publish (Section 6.1)
4. **ตั้ง CI Pipeline แบบ Staged** — pre-commit → smoke → sanity → regression → report

### 9.2 Medium-Term

1. **Block-Level Unit Tests** — แต่ละ GL block type มี unit test suite ของตัวเอง
2. **Workflow Impact Analysis** — script วิเคราะห์ว่า block ไหนเปลี่ยน → เลือก regression tests
3. **Flakiness Dashboard** — ติดตาม flaky rate, execution time trends
4. **Mutation Testing** — mutate workflow JSON → validate schema ครอบคลุม

### 9.3 Long-Term

1. **Playwright Integration** — ใช้ Playwright CLI หรือ MCP สำหรับ browser-level validation
2. **Social Analyzer Integration** — ใช้สำหรับ validate FB-VIA profile state
3. **Allure Reporting** — สร้าง test report ที่ดูง่าย มี screenshot, log, trace
4. **Performance Benchmarking** — baseline + alert thresholds สำหรับ execution time, memory

### 9.4 Tools Stack ที่แนะนำ

| Layer | Tool | Reason |
|-------|------|--------|
| **Schema Validation** | JSON Schema + custom validator | จับ structural bugs |
| **Block Testing** | Python + pytest | Test unit tests |
| **Workflow E2E** | Playwright (CLI/MCP) | Browser-level validation |
| **Profile Validation** | Social Analyzer (Fast mode) | ตรวจสอบ profile state |
| **Reporting** | Allure + Trace Viewer | Debug-friendly |
| **CI** | GitHub Actions staged pipeline | เร็ว → ช้า |
| **Performance** | Custom benchmark script | ติดตาม regression |
| **Mutation** | Stryker หรือ custom | วัด test quality จริง |

---

## สรุป

Enterprise test architecture (Selenium-Python-Example) สอนให้เรา **systematize reliability** — ไม่ใช่ scale แต่เป็น systematic approach ที่จัดการ failure modes ที่ plague test suites: flakiness (retries, browser pinning), poor debugging (reports with videos/screenshots/logs), environment drift (dependency locks)

Playwright นำ **auto-waiting และ trace viewer** ที่เปลี่ยนวิธี debug failure — จาก guess-and-retry เป็น inspect-and-fix

Social Analyzer ให้ **multi-tier detection approach** ที่สามารถใช้ validate social profile state โดยเฉพาะ FB-VIA profiles

JavaScript Testing Best Practices ให้ **comprehensive framework** สำหรับจัด structure testing program — ตั้งแต่ naming conventions, AAA pattern, ไปจนถึง mutation testing

**สำหรับ GemLogin โดยเฉพาะ:** ความรู้ 10+ production bugs ที่ค้นพบแล้วบอกเราชัดเจนว่า — schema validation, edge naming convention, IIFE handling, delay format, และ cookie persistence คือ pain points หลัก การมี pre-publish validator script จะป้องกัน bugs ซ้ำได้ถึง 80%+ ของ bugs ที่เคยเจอ

---

*SPARK ⚡ — ประกายไฟที่จุดชนวน ทดสอบทุกอย่างก่อนส่งมอบ*
