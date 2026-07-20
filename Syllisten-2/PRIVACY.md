# Privacy Notice

**Effective date:** 20 July 2026

This notice describes the intended behavior of the official Syllisten application code. A third-party fork or hosting provider may behave differently.

## Data entered by users

Syllisten may process pasted text, dictation answers, interface and speech settings, a voluntarily entered OpenAI API key, and ordinary technical information handled by the hosting provider, web server, browser, and network.

## Processing by mode

### Rule-based segmentation

Text is processed by the application server using built-in rules and is not intentionally sent to OpenAI. A hosted Streamlit deployment is not entirely local because the hosting server receives the text.

### OpenAI user-key mode

The user-provided API key and submitted text are used to make an OpenAI API request. Processing is subject to the user's OpenAI account and applicable OpenAI agreements. Syllisten contains no developer OpenAI API key.

### Speech generation

Natural speech uses `edge-tts`, an unofficial client for Microsoft Edge online speech synthesis. Sentence text may be sent to Microsoft-operated online speech infrastructure. Browser speech is a fallback and may be local or remote depending on the environment.

## Storage

The application is designed to keep exercise state and a user-entered API key in the current Streamlit session rather than intentionally writing them to the repository, a `.env` file, a database, or a URL. Session termination and memory cleanup depend on Streamlit and the hosting environment.

Generated audio may be cached temporarily by the runtime, host, browser, or network layers. Deployers should configure retention and cache controls appropriate to their environment.

## Logs and infrastructure

Syllisten code is not intended to print complete API keys. Hosting platforms, reverse proxies, security tools, browser extensions, operating systems, or modified deployments may collect logs or technical metadata independently.

## User choices

Use rule mode to avoid OpenAI transmission; do not enter a key unless you trust the deployment; use limited project-scoped keys; revoke suspected exposed keys; do not submit sensitive information; and clear the key when finished.

## Children and regulated data

The official deployment is not specifically designed for children or regulated personal information. Deployers in schools, healthcare, employment, or similar settings must implement their own lawful consent, notice, security, retention, and governance.
