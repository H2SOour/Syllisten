# Security Policy

## Supported version

Security fixes are applied to the latest version on the default branch. Older releases may not receive updates.

## Reporting a vulnerability

Do not post a live API key, exploit, private user text, or sensitive detail in a public issue. Use GitHub private vulnerability reporting when enabled, or contact the repository owner privately through the profile contact method.

Include the affected version, reproduction steps, impact, sanitized logs, and suggested mitigation if available.

## API-key safety

- Syllisten must never contain a developer OpenAI API key.
- User keys must not be committed, placed in URLs, intentionally logged, or stored in repository files.
- Users should apply project limits and revoke keys after suspected exposure.
- Maintainers should run secret scanning before releases.

## Deployment checklist

Enable HTTPS; review host logging and retention; disable debug logging; update and scan dependencies; rate-limit public endpoints; restrict environment access; clean temporary audio; and confirm errors do not expose keys or submitted text.
