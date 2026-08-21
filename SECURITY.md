# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| latest  | ✅ Yes             |
| older   | ❌ No              |

Only the latest version on the `main` branch receives security updates.

## Reporting a Vulnerability

If you discover a security vulnerability in PIXELTOWN, **please do not open a public issue.** Instead, report it privately:

1. **Email**: Send a detailed description to **salassahuquilloraul@gmail.com** with the subject line `[SECURITY] PIXELTOWN`.
2. Include:
   - A clear description of the vulnerability.
   - Steps to reproduce it.
   - The potential impact.
   - A suggested fix, if you have one.

## Response Timeline

- **Acknowledgement**: Within **48 hours** of receiving your report.
- **Assessment**: Within **7 days**, we will confirm the vulnerability and its severity.
- **Fix & Disclosure**: A patch will be developed and released as soon as possible. Public disclosure will follow once a fix is available.

## Scope

The following areas are in scope for security reports:

- **Local save file handling** (`saves/`, `accounts.json`, `*_save.json`): injection, path traversal, or data corruption.
- **Password storage** (`hashlib` SHA-256 hashing in `terminal.py`): weaknesses in the hashing mechanism.
- **Deserialization of user data** (`json.load` of save files): malicious payloads.
- **Dependency vulnerabilities**: issues in `pygame`, `pyvidplayer2`, or other dependencies.

The following are **out of scope**:

- Bugs that do not have a security impact (use regular GitHub Issues for those).
- Social engineering attacks.
- Physical access attacks.

## Best Practices for Contributors

- Never store passwords in plaintext.
- Validate and sanitize all user input, especially file paths and loaded JSON data.
- Keep dependencies up to date.
- Do not introduce network features without explicit review and approval.

---

*Thank you for helping keep PIXELTOWN safe for everyone.*
