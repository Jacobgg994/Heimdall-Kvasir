# Security Foundation Report — 2026-06-30

**Author:** PHANTOM
**Role:** Security Engineer
**Mission:** Study core security resources, map to JACOB Team stack, produce actionable hardening roadmap

---

## Executive Summary

This report synthesizes five foundational security resources into a coherent knowledge base tailored to the JACOB Team's technology stack (GemLogin, GemphoneFarm, QCCAP/Q AI, Covertia Nexus). The OWASP Top 10 provides the threat taxonomy; PayloadsAllTheThings gives the exploitation playbook; Nuclei Templates enables automated detection; Awesome Security catalogs the defensive toolkit; and the MCP Security ecosystem opens AI-native security workflows.

Key finding: The team operates with **no authentication on local APIs**, **no penetration testing history**, **no dependency scanning**, and **no compliance framework** (PDPA/GDPR). PHANTOM was created to close this gap. This report is the foundation for that effort.

---

## 1. OWASP Top 10:2021 — Full Breakdown

### A01: Broken Access Control (Formerly #5, now #1)

**What it is:** Users act outside their permitted scope. Occurs through URL manipulation, IDOR (insecure direct object references), privilege escalation, CORS misconfiguration, force browsing, JWT tampering, and directory listing.

**Key data:** 94% of apps tested. 318k occurrences. 19,013 CVEs mapped. Avg weighted impact: 5.93.

**Prevention:** Default-deny on all non-public resources. Reusable access control modules. Enforce record ownership in model layer. Disable directory listing. Remove .git/backup files from web roots. Log access failures; alert on repeated attempts. Rate-limit API endpoints. Invalidate session IDs server-side on logout; keep JWT lifetimes short.

**How it applies to our stack:**
- **GemLogin :1010 API** — No authentication at all. Any local process can control all profiles. Need to add at minimum a local auth token or Unix socket permissions.
- **GemphoneFarm :1256 API** — Same issue. Unauthenticated local API.
- **Cloud webhooks** (both GL and GPF) — Use body token field (not Bearer). Rate limit is 300 req/min/device, which is generous. Ensure token rotation.

---

### A02: Cryptographic Failures (Renamed from "Sensitive Data Exposure")

**What it is:** Weak or missing encryption for data in transit or at rest. Includes cleartext protocols (HTTP, FTP, SMTP), weak ciphers (MD5, SHA1, PKCS#1 v1.5), hardcoded keys, improper IV handling, insufficient randomness, expired certificates, and missing HSTS.

**Key data:** 29 CWEs mapped. 233,788 occurrences. 3,075 CVEs. Max incidence rate: 46.44%. Avg weighted impact: 6.81.

**Prevention:** Classify all data by sensitivity. Encrypt all sensitive data at rest (AES-256-GCM or better) and in transit (TLS 1.3 with forward secrecy). Use Argon2/scrypt/bcrypt for passwords. Never use ECB mode. Use authenticated encryption (AEAD). Generate keys with CSPRNG. HSTS enforcement. Disable caching for sensitive responses. Tokenize or truncate over-retained data.

**How it applies to our stack:**
- **Profile cookies stored on disk** — GemLogin stores cookies in Electron's profile data directory. No encryption at rest. Any user with filesystem access can steal session cookies.
- **Local SQLite databases** (`~/.gemlogin/db.db`, `log.db`) — Unencrypted. Contains profile configurations, proxy details, workflows.
- **DEEPSEEK_API_KEY** — Stored in `.env` file. Ensure file permissions are 600 and the file is gitignored. Verify no `.env` file has ever been committed.
- **Cloud webhook token** — Transmitted as a body field over HTTPS. This is acceptable, but verify the TLS version is 1.2+.

---

### A03: Injection (SQL, NoSQL, OS Command, LDAP, etc.)

**What it is:** Untrusted data is sent to an interpreter as part of a command or query. The attacker tricks the interpreter into executing unintended commands. SQL injection is the most well-known; OS command injection allows arbitrary code execution.

**Key data:** 33 CWEs. 274,228 occurrences. 32,078 CVEs. Avg weighted impact: 7.15. Avg weighted exploit: 7.25 (very easy to exploit).

**Prevention:** Parameterized queries / prepared statements (not concatenation). Positive server-side input validation. Escape special characters per interpreter syntax. NEVER allow user input to control SQL structure (table names, column names). Safe API (ORM with parameterized internals).

**How it applies to our stack:**
- **GemLogin Workflow SQLite** (`~/.gemlogin/db.db`) — The `gemlogin-edit` skill directly executes SQL on this database. If workflow names or data from external sources enter SQL without sanitization, injection is possible.
- **GemphoneFarm workflows** — JSON-based automation definitions. If parsing these with eval() or dynamic execution (javascript-code blocks), ensure input is validated. The code block in GL workflows executes server-side JS.
- **Q AI LLM prompts** — Prompt injection is the AI-equivalent of injection. Ensure system prompts are robustly separated from user input. No untrusted data should touch the prompt template unsanitized.

---

### A04: Insecure Design (New in 2021)

**What it is:** Missing or ineffective control design at the architecture level. Not a coding bug — a failure to plan for threats before writing code. Includes lack of threat modeling, missing business logic controls, no security requirements in user stories.

**Key data:** 40 CWEs mapped. 262,407 occurrences. 2,691 CVEs. Avg weighted impact: 6.78. Max coverage: 77.25%.

**Prevention:** Secure Development Lifecycle (SSDL). Threat model critical flows (auth, access control, business logic). Use secure design patterns library. Write misuse-cases alongside use-cases. Plausibility checks at every tier. Tenant segregation by design. Resource consumption limits per user/service.

**How it applies to our stack:**
- **No threat modeling exists** for any component. Should be done for Covertia Nexus (government buyer compliance requires design documentation).
- **QCCAP multi-tenant design** — If Covertia serves multiple government clients, tenant segregation must be designed in, not bolted on.
- **Business logic flaws in GL workflows** — The workflow engine allows arbitrary automation logic. Need misuse-case testing (what happens if a workflow runs twice? What if a step fails mid-way?).

---

### A05: Security Misconfiguration

**What it is:** Missing hardening across the stack. Default accounts unchanged, unnecessary services running, verbose error messages, missing security headers, unpatched software, open cloud storage.

**Key data:** 20 CWEs. 208,000+ occurrences. 789 CVEs. Avg weighted exploit: 8.12 (easiest to exploit). Max incidence: 19.84%.

**Prevention:** Repeatable hardening process. Identical config across dev/QA/prod (different credentials per env). Minimal platform (remove unnecessary features). Regular config review tied to patch management. Segmented architecture (containers, security groups). Automated config verification. Security Headers (HSTS, CSP, X-Frame-Options, etc.).

**How it applies to our stack:**
- **Local API hardening** — Both :1010 and :1256 should bind only to 127.0.0.1 and ideally use a Unix socket with filesystem permissions.
- **MQTT endpoint exposure** — If cloud webhook uses MQTT, ensure MQTT broker requires authentication and TLS.
- **Covertia deployments** — Enterprise deployments in government environments need hardened OS images, restricted network access, and security header application on any HTTP interfaces.

---

### A06: Vulnerable & Outdated Components

**What it is:** Running software with unknown versions, unpatched libraries, unsupported dependencies. Includes the entire software supply chain (direct + transitive dependencies).

**Key data:** 3 CWEs. 30,457 occurrences. Max incidence: 27.96%. Avg weighted exploit: 5.00. Avg weighted impact: 5.00.

**Prevention:** Remove unused dependencies. Continuous inventory via SCA tools (OWASP Dependency Check, retire.js, Trivy). Obtain signed packages from official sources over secure links. Monitor for unmaintained libraries. Virtual patching when immediate fix is impossible. Formal patch management process with risk-based timelines.

**How it applies to our stack:**
- **GemLogin v5.0.3** — Third-party Vietnamese vendor product. No visibility into their dependency hygiene or patch cycle.
- **Electron/chromium version** — Antidetect browsers often run customized Chromium, potentially missing security patches. Need to verify which Chromium version is embedded.
- **Python dependencies** (gemlogin-mcp, gemphonefarm-mcp) — No evidence of `pip-audit`, `safety`, or Dependabot being used. Must add to CI.
- **atx-agent on phones** — 60+ Android devices running atx-agent. This is a third-party component with its own vulnerabilities.

---

### A07: Identification & Authentication Failures

**What it is:** Weak identity proofing, credential management, and session handling. Includes credential stuffing, brute force, default passwords, weak password recovery, plaintext password storage, missing MFA, session ID in URLs, failure to invalidate sessions on logout.

**Key data:** 22 CWEs. 132,195 occurrences. 3,897 CVEs. Avg weighted exploit: 7.40 (very exploitable). Avg weighted impact: 6.50.

**Prevention:** MFA on all user-facing auth. No default credentials. Reject the top 10k worst passwords (haveibeenpwned API). Align password policy with NIST 800-63b. Identical response messages for all auth outcomes (prevent enumeration). Rate-limit/log/alert on failed logins. Server-side session management with high-entropy session IDs. Invalid sessions on logout, idle timeout, and absolute timeout.

**How it applies to our stack:**
- **GemLogin profile authentication** — Profiles authenticate to Facebook/TikTok/etc. The team handles credentials programmatically. Need to ensure passwords are not logged, stored in clear-text in workflows, or visible in error messages.
- **Q AI access** — If QCCAP/Q AI has a web UI, it needs authentication beyond basic auth. The current Q AI UI at :6035/q.html may be unauthenticated.
- **Covertia government access** — Enterprise deployments require SSO/SAML integration, role-based access, mandatory MFA, and audit logging of all admin actions.

---

### A08: Software & Data Integrity Failures (New in 2021)

**What it is:** Code and infrastructure failing to protect against integrity violations. Includes untrusted dependencies, insecure CI/CD pipelines, auto-update without integrity verification, and insecure deserialization.

**Key data:** 10 CWEs. 47,972 occurrences. 1,152 CVEs. Avg weighted impact: 7.94 (highest impact of all 10 categories!).

**Prevention:** Digital signatures for all software/updates. Consume dependencies from trusted repositories only (internal proxy for high-risk profiles). SCA tools for known-vulnerability scanning. Code review for all pipeline changes. CI/CD pipeline segregation, configuration, and access control. Never send unsigned serialized data to untrusted clients.

**How it applies to our stack:**
- **Software supply chain for GL/GPF** — Both are third-party Vietnamese products. Need to verify distribution integrity (signed builds, checksum verification).
- **Auto-update in both products** — If either GemLogin or GemphoneFarm auto-updates, is the update channel authenticated and integrity-checked? SolarWinds-style attacks are exactly this vector.
- **GemLogin cloud webhook** — The cloud `execscript` endpoint accepts arbitrary execution payloads. This is a powerful feature that must be authenticated and validated. If the MQTT channel can be spoofed, arbitrary code can be pushed to all devices.
- **Q AI LLM model files** — If using local models (Ollama, vLLM), verify model file checksums. A compromised model file is a supply chain attack.

---

### A09: Security Logging & Monitoring Failures

**What it is:** Inability to detect, escalate, and respond to active breaches. Includes missing logs for critical events (logins, failures, high-value transactions), logs not monitored, no centralized collection, no alerting thresholds, no incident response plan.

**Key data:** 4 CWEs. 53,615 occurrences. 242 CVEs. Demonstrates through real breaches lasting years (e.g., children's health data 3.5M records undetected for 7 years; airline GDPR fine of 20M pounds).

**Prevention:** Log all login, access control, and server-side validation failures with user context. Logs must be consumable by centralized log management (ELK, Splunk). Log data properly encoded to prevent injection. Audit trail for high-value transactions with integrity controls (append-only). Incident response plan per NIST 800-61r2. Commercial and open-source tools: OWASP ModSecurity CRS, ELK stack.

**How it applies to our stack:**
- **No evidence of centralized logging** for any component. GemLogin has `log.db` but it's not monitored.
- **No incident response plan** — Explicit gap.
- **GemPhoneFarm 60-device fleet** — No monitoring infrastructure for detecting rogue processes or unusual device behavior.
- **Cloud webhook calls** — Need logging of all cloud webhook invocations (who called, when, what script, result). Audit trail for compliance.
- **Q AI LLM calls** — If DeepSeek API is used, log token usage, response patterns, and errors for anomaly detection.

---

### A10: Server-Side Request Forgery (SSRF) (New in 2021)

**What it is:** An attacker causes the server to make requests to unintended locations, often bypassing firewalls or accessing internal services. The server becomes a proxy.

**Prevention:** Validate and sanitize all URLs that the server will fetch. Block private/internal IP ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, ::1/128). Use allowlists of permitted destinations. Disable HTTP redirect following or restrict to safe URLs. Run network-level controls (firewall, egress filtering).

**How it applies to our stack:**
- **GemLogin CDP proxy** — If profiles use SOCKS/HTTP proxies that resolve to internal addresses, SSRF-like attacks through the browser are possible.
- **MQTT broker** — If the MQTT message broker is accessible internally, any SSRF through the web server can reach it.
- **GemphoneFarm phone automation** — The phones connect to various endpoints. If one phone is compromised, it could SSRF into the local network.

---

## 2. Tools Deep Dive

### 2.1 PayloadsAllTheThings (swisskyrepo, 78.8k stars)

**What it is:** The definitive community payload collection for web application security testing. 60+ attack categories, each with README, Burp Intruder files, and examples.

**Key categories relevant to our stack:**

| Category | Relevance |
|----------|-----------|
| **SQL Injection** | SQLite injection testing for `gemlogin-edit` skill. Parameterized vs non-parameterized workflow DB queries |
| **Command Injection** | If workflow JS blocks allow shell command execution |
| **SSRF** | Testing MQTT/webhook endpoints for internal network access |
| **JWT Attacks** | If QCCAP or Covertia use JWTs for auth |
| **CORS Misconfiguration** | Testing local APIs from browser contexts |
| **Insecure Deserialization** | Workflow JSON parsing — Python `pickle` or Java deserialization risks |
| **Prototype Pollution** | If any component uses JavaScript objects unsafely |
| **XSS Injection** | Any web UI component (Q AI UI, Covertia dashboard) |
| **API Key Leaks** | Scanning repos and configs for committed keys |
| **File Inclusion** | Workflow file inclusion paths |
| **Race Condition** | Concurrent webhook execution on same profile |

**How to use in our workflow:**
- Clone to `Kvasir/lab/payloads/` for reference during audits
- Use the Burp Intruder files in `Intruder/` subdirectories when testing web endpoints
- Reference the `Methodology and Resources/` directory for structured pentest approaches

---

### 2.2 Nuclei Templates (ProjectDiscovery, 12.6k stars, 11,997 files)

**What it is:** 8,000+ YAML-based security templates for the Nuclei scanning engine. Covers HTTP, cloud, file, network, DNS, SSL, and headless checks.

**Template scale:**

| Category | Count | Key Use |
|----------|-------|---------|
| HTTP | 9,281 | Web application scanning |
| Cloud | 659 | Cloud infra misconfiguration |
| File | 436 | File-based vulnerability |
| Network | 259 | Protocol-level checks |
| DAST | 240 | Dynamic application testing |
| Workflows | 205 | Multi-step scans |
| SSL | 38 | TLS configuration |

**Severity distribution:** Info: 4,353 | Low: 330 | Medium: 2,457 | High: 2,552 | Critical: 1,555

**Key tag categories:** vuln (6,468), cve (3,587), discovery (3,265), panel (1,365), xss (1,269), wordpress (1,261), exposure (1,141), osint (848).

**CISA KEV coverage:** 1,496 templates scanning actively exploited vulnerabilities.

**How to use in our workflow:**
- Install Nuclei + clone templates to CI pipeline
- Run `nuclei -t nuclei-templates/ -u http://localhost:1010` — scans GemLogin API
- Run `nuclei -tags kev,vkev -u <target>` — scans for actively exploited vulnerabilities
- Create custom YAML templates for QCCAP-specific endpoints
- Integrate into CI/CD for pre-deployment scanning

---

### 2.3 Awesome Security (sbilly, 14.6k stars)

**What it is:** The most comprehensive curated index of open-source security tools across 20+ domains.

**Most relevant to our stack:**

| Domain | Tool | Use |
|--------|------|-----|
| **Network Scanning** | Nmap, RustScan, Masscan | Infrastructure discovery |
| **Vulnerability Scanning** | OpenVAS, Nuclei, OWASP ZAP | Automated vuln detection |
| **WAF** | ModSecurity, NAXSI, BunkerWeb | Protect any HTTP-facing service |
| **Secrets Management** | HashiCorp Vault, SOPS, passbolt | Replace plaintext `.env` files |
| **Container Security** | Trivy, Falco, Checkov | Scan Docker images |
| **Intrusion Detection** | Snort, Suricata, Wazuh | Host/network monitoring |
| **Threat Intelligence** | MISP, AlienVault OTX, VirusTotal | IoC enrichment |
| **Forensics** | Volatility, GRR, Maigret | Incident response |
| **Mobile Security** | Frida, Apktool, jadx | Mobile app testing |
| **Fraud Prevention** | FingerprintJS | Bot/detection evasion (relevant to antidetect work) |

**Priority tools to adopt first:**
1. **Trivy** — Scan all Docker images for known CVEs
2. **Falco** — Runtime security monitoring on Covertia deployment servers
3. **SOPS** — Encrypt secrets at rest (replace plaintext `.env`)
4. **MISP** — If Covertia handles threat intelligence data
5. **OWASP ZAP** — Automated DAST scanning of web interfaces

---

### 2.4 Awesome Cyber Security MCP (MorDavid)

**What it is:** The emerging ecosystem of security tools exposed through the Model Context Protocol — AI agents that drive security tools conversationally.

**Relevant MCP tools:**

| MCP Server | Purpose | How to Use |
|-----------|---------|------------|
| **Burp Suite MCP** | AI-driven web security testing | Let Claude drive Burp for automated scanning |
| **Nuclei MCP** | AI-triggered Nuclei scans | Run vuln scans via natural language |
| **ZAP MCP Server** | AI-driven OWASP ZAP | DAST scanning via LLM |
| **Shodan MCP** | External attack surface discovery | Find exposed services |
| **VirusTotal MCP** | Threat intel enrichment | Check hashes/IPs |
| **Ghidra MCP** | AI-driven binary analysis | Analyze GL Electron binaries |
| **ExternalAttacker MCP** | External attack surface mapping | Chain subfinder -> httpx -> nuclei via AI |
| **BloodHound MCP** | AD attack path analysis | For Covertia enterprise deployments |
| **Hashcat MCP** | Natural language hash cracking | Password audit workflows |
| **Elastic Security MCP** | AI-driven SIEM querying | Log analysis and threat hunting |

**Architecture pattern:**
```
LLM (Claude) -> Tool Call -> MCP Server -> Security Tool API/CLI -> Results -> LLM reasons -> Next action
```

**How to use in our workflow:**
- Install Nuclei MCP first — gives Claude ability to scan endpoints on request
- Install ZAP MCP for automated web UI testing
- Chain external reconnaissance: `ExternalAttacker MCP` discovers subdomains -> `Nuclei MCP` scans them -> report back
- Use `BloodHound MCP` if Covertia AD integration becomes real

---

## 3. How to Apply to GemLogin / GPF / QCCAP

### 3.1 GemLogin Hardening Roadmap

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | Audit local `:1010` API for unauthenticated endpoints | Any local process controls all profiles today |
| **P0** | Verify no API keys/tokens committed to any repo | A02, A08 — credential leakage |
| **P1** | Add local auth token or Unix socket to `:1010` | A01 — broken access control |
| **P1** | Encrypt SQLite databases (`db.db`, `log.db`) | A02 — cryptographic failures |
| **P1** | Scan GL Electron binary with Trivy/Grype | A06 — vulnerable components |
| **P2** | Create custom Nuclei template for GL API | Enable automated scanning |
| **P2** | Log all cloud webhook executions | A09 — logging failures |
| **P2** | Verify MQTT channel authentication | A08 — integrity failures |
| **P3** | Establish dependency scanning for MCP servers | A06 — outdated components |

### 3.2 GemphoneFarm (GPF) Hardening Roadmap

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | Audit `:1256` local API — confirm broken IPC is the only unauthenticated path | A01 — access control |
| **P0** | Verify no phone credentials in workflow JSONs | A02 — crypto failures |
| **P1** | Add per-device auth token for cloud webhook | A07 — auth failures |
| **P1** | Scan atx-agent version across 60+ devices | A06 — outdated components |
| **P2** | Add device monitoring (which phones are online, what processes run) | A09 — monitoring failures |
| **P2** | Create incident response plan for device compromise | A09 — response failures |
| **P3** | Centrally log all workflow executions with results | A09 — logging failures |

### 3.3 QCCAP / Q AI Hardening Roadmap

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | Confirm `DEEPSEEK_API_KEY` is in `.env` (not code), chmod 600, gitignored | A02, A08 |
| **P0** | Audit Q AI web UI (`:6035/q.html`) for auth | A01, A07 |
| **P1** | Add prompt injection defenses to LLM chain | A03 — injection (AI variant) |
| **P1** | Add rate limiting and auth to Q AI API endpoints | A01, A07 |
| **P2** | Implement token usage anomaly detection | A09 — monitoring |
| **P2** | Add dependency scanning to Q AI Python project | A06 |
| **P3** | Implement audit logging for all API calls | A09 |
| **P3** | Threat model multi-tenant Covertia deployment | A04 — insecure design |

### 3.4 Covertia Nexus (Enterprise) Security Requirements

| Requirement | OWASP Ref | Detail |
|-------------|-----------|--------|
| SSO/SAML authentication | A07 | Enterprise AD/Google Workspace login |
| Role-based access control | A01 | Admin vs operator vs read-only roles |
| Encryption at rest | A02 | All customer data encrypted |
| Audit logging | A09 | All admin actions logged, immutable |
| Supply chain integrity | A08 | Signed builds, verified dependencies |
| Incident response plan | A09 | Per NIST 800-61 |
| Tenant segregation | A04, A01 | Separate data per client |
| Penetration testing | All | Required before government deployment |
| PDPA compliance | All | Data retention, right to deletion, consent |

---

## 4. Security Checklist for JACOB Team

### 4.1 Immediate Actions (this week)

- [ ] **Inventory all secrets** — API keys, tokens, passwords across all projects. Document where each lives.
- [ ] **Verify .gitignore** — Ensure no `.env`, `.pem`, `.key`, or credential files can be committed. Run `git log --all --diff-filter=A -- '*.env'` to check history.
- [ ] **Add Trivy to CI** — Run `trivy fs .` on all code repositories. Add to pre-commit or GitHub Actions.
- [ ] **Test local APIs** — Confirm `:1010` and `:1256` bind only to 127.0.0.1.
- [ ] **Check cloud webhook tokens** — Ensure they're long, random, and rotatable.

### 4.2 Short-term (this month)

- [ ] **Install Nuclei + clone templates** — Run `nuclei -t nuclei-templates/ -u http://localhost:1010` as baseline scan.
- [ ] **Add OWASP Dependency Check** — or `pip-audit` for Python dependencies in gemlogin-mcp and gemphonefarm-mcp.
- [ ] **Deploy SOPS** — Encrypt `.env` files at rest. Store master key in a secure location (not in repo).
- [ ] **Create incident response plan** — Document who to call, what to do, how to isolate compromised profiles or devices.
- [ ] **Set up centralized logging** — ELK stack or Grafana Loki on the HQ Mac1 or Covertia server.

### 4.3 Medium-term (next quarter)

- [ ] **Establish PDPA/GDPR compliance framework** — Data mapping, retention policies, consent mechanisms.
- [ ] **Deploy Wazuh or Falco** — Host intrusion detection on production servers.
- [ ] **Develop custom Nuclei templates** — For QCCAP-specific endpoints and workflows.
- [ ] **Deploy MISP** — If Covertia handles threat intelligence data.
- [ ] **Integrate Nuclei MCP** — Enable AI-driven scanning from within Claude.
- [ ] **Penetration test** — Full OWASP Top 10 assessment of the QCCAP stack.

### 4.4 Long-term (2026-2027)

- [ ] **Bug bounty program** — For Covertia Nexus enterprise platform.
- [ ] **SOC 2 / ISO 27001 certification** — Required for enterprise/ government sales.
- [ ] **Dedicated SIEM** — Elastic Security or Splunk for centralized threat detection.
- [ ] **Security training** — For all team members (secure coding, OWASP awareness).
- [ ] **Red team exercises** — Periodic full-scope adversarial simulation.

---

## 5. Key Resources Reference

| Resource | URL | Use |
|----------|-----|-----|
| OWASP Top 10 2021 | https://owasp.org/Top10/ | Threat taxonomy |
| PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings | Exploitation reference |
| Nuclei Templates | https://github.com/projectdiscovery/nuclei-templates | Automated scanning |
| Awesome Security | https://github.com/sbilly/awesome-security | Tool discovery |
| Awesome Cyber Security MCP | https://github.com/MorDavid/awesome-cyber-security-mcp | AI-native security tools |
| OWASP SAMM | https://owasp.org/www-project-samm/ | Secure development maturity |
| OWASP Dependency Check | https://owasp.org/www-project-dependency-check/ | SCA tool |
| NIST 800-61r2 | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final | Incident response standard |
| NIST 800-63b | https://pages.nist.gov/800-63-3/sp800-63b.html | Authentication guidelines |

---

## 6. Conclusion

The JACOB Team's stack has significant security gaps — primarily unauthenticated local APIs, no penetration testing history, no dependency scanning, and no compliance framework. These are common early-stage problems but become critical as Covertia Nexus targets enterprise and government buyers.

The immediate focus should be:

1. **Inventory and secure all credentials** (stop the bleeding)
2. **Install scanning toolchain** (Nuclei + Trivy + Dependency Check) — make security measurable
3. **Document and test local API security** (close the biggest OWASP A01 gap)
4. **Start the compliance journey** (PDPA awareness at minimum, SOC 2 aspirationally)

PHANTOM will maintain this report as a living document and track progress against the checklists.

---

*Report generated: 2026-06-30*
*Next review: 2026-07-30*
