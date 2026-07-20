# Syllisten

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://syllisten.streamlit.app)

A multilingual focused-listening and dictation web app for Chinese, Japanese, English, Spanish, and French.
Syllisten is a multilingual focused-listening and dictation web application developed by **Siyuan Liu**. It supports Chinese, Japanese, English, Spanish, and French.

> **Project status:** independent, non-commercial educational prototype. The official project and public demo are provided without charge for learning, technical demonstration, and portfolio purposes. This does **not** mean that the project is a legally registered nonprofit organization, and it does not waive any applicable law, third-party license, service term, copyright, trademark, privacy, or data-protection obligation.

## Features

- Rule-based text segmentation without OpenAI
- Optional semantic segmentation using the user's own OpenAI API key
- No developer OpenAI API key and no developer-paid OpenAI usage
- Natural speech through `edge-tts`, with browser speech as a fallback
- Chinese, Japanese, English, Spanish, and French text support
- British or American pronunciation for English
- Adjustable playback speed
- Hidden-text dictation practice and similarity scoring
- Five interface languages: English, Simplified Chinese, Japanese, Spanish, and French
- Multiple low-fatigue visual themes, including a color-vision-friendly theme

## Data flow at a glance

| Function | External transmission |
|---|---|
| Rule-based segmentation | Text is processed by the app server; it is not intentionally sent to OpenAI. |
| User-key OpenAI mode | Text is sent to OpenAI using only the API key supplied by the user for that session. |
| Natural speech (`edge-tts`) | Sentences selected for speech synthesis may be transmitted to Microsoft-operated online speech infrastructure through an unofficial third-party client. |
| Browser speech fallback | Processing depends on the user's browser, operating system, and selected voice. |

Do not submit confidential, regulated, unlawful, infringing, or sensitive personal information unless you have a lawful basis and fully understand the applicable third-party terms.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501` if the browser does not open automatically.

## links
- Live app: https://syllisten.streamlit.app
- Source code: https://github.com/H2SOour/Syllisten

## AI mode and API keys

Syllisten does not include or read a developer OpenAI API key. The optional AI mode works only when a user enters their own OpenAI API key. The key is intended to remain in the current Streamlit session state and is not intentionally written to the repository, a local `.env` file, a database, or a URL by this application. Hosting providers, reverse proxies, browser extensions, and other infrastructure remain outside the developer's control.

Never enter an OpenAI account password. An API key is separate from a ChatGPT subscription, and any API usage is charged to the API account associated with the user's key.

## Non-commercial operation and repository license

The official Syllisten deployment is operated on a non-commercial basis. The source code is currently released under the **MIT License**, which is a permissive open-source license and does not itself prohibit third parties from commercial use. The **Syllisten name, logo, and project identity are not licensed as trademarks** by the MIT License. See [COPYRIGHT_AND_TRADEMARK.md](COPYRIGHT_AND_TRADEMARK.md).

If the project's owner later wishes to prohibit commercial reuse of the code itself, the software license must be changed prospectively; a non-profit disclaimer alone does not create that restriction.

## Project scope and third-party components

Syllisten is an independently developed application that integrates third-party frameworks, libraries, APIs, and online services.

The application-specific design and implementation include the user interface, multilingual workflow, sentence-segmentation rules, dictation interaction, transcription comparison, pronunciation selection, accessibility themes, session behavior, and deployment configuration.

Syllisten does not claim ownership or authorship of the underlying third-party technologies, including:

- Streamlit, used as the web application framework;
- the OpenAI Python SDK and OpenAI API, used only when a user selects API-assisted analysis and supplies their own API key;
- `edge-tts`, an independent third-party package used to access Microsoft Edge's online text-to-speech service;
- browser-provided Web Speech API functionality used as a fallback.

All third-party software, services, trademarks, voices, and related technologies remain the property of their respective owners. Their inclusion does not imply affiliation, sponsorship, endorsement, or official partnership.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [DISCLAIMER.md](DISCLAIMER.md) for details.

## Legal and policy documents

- [DATA_FLOW.md](DATA_FLOW.md)
- [LICENSE](LICENSE)
- [NOTICE](NOTICE)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [DISCLAIMER.md](DISCLAIMER.md)
- [TERMS_OF_USE.md](TERMS_OF_USE.md)
- [PRIVACY.md](PRIVACY.md)
- [SECURITY.md](SECURITY.md)
- [COPYRIGHT_AND_TRADEMARK.md](COPYRIGHT_AND_TRADEMARK.md)

## Maintainer documents

- [DEPLOYMENT.md](DEPLOYMENT.md)
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [CITATION.cff](CITATION.cff)

## Third-party foundations

Syllisten directly depends on the following Python packages:

- [Streamlit](https://github.com/streamlit/streamlit), licensed under Apache License 2.0.
- [OpenAI Python SDK](https://github.com/openai/openai-python), licensed under Apache License 2.0.
- [edge-tts](https://github.com/rany2/edge-tts), an unofficial client for Microsoft Edge online text-to-speech. Its repository states that most files are licensed under LGPLv3 and one SRT composer file is MIT-licensed.

`edge-tts` is not an official Microsoft SDK. Microsoft Edge's online text-to-speech voices are part of Microsoft's online speech infrastructure, and availability, behavior, voice selection, and applicable service terms may change independently of Syllisten.

Full attribution and license notes are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), with license texts under [`licenses/`](licenses/).

## Copyright and user-provided text

Users must have the legal right to process every submitted text. Syllisten does not grant permission to reproduce books, articles, subtitles, examination materials, lyrics, personal data, or other protected material. Educational or non-commercial intent does not automatically make copying or processing lawful.

## No affiliation

Syllisten is independent and is not affiliated with, sponsored by, endorsed by, or an official product of OpenAI, Microsoft, Streamlit, Snowflake, Apple, Google, any browser vendor, any voice provider, or any other third party named in this repository.

## Citation

For academic, educational, or portfolio references, use the metadata in [`CITATION.cff`](CITATION.cff). A simple citation is:

> Liu, Siyuan. *Syllisten: Multilingual Focused-Listening and Dictation Web App*. 2026.

## Important legal note

The included legal documents are general project notices, not jurisdiction-specific legal advice. The current package is specifically scoped for personal study, limited friend testing, GitHub portfolio publication, and résumé/LinkedIn demonstration. They cannot guarantee that every deployment, input, output, dependency, or third-party service use is lawful in every country. Deployers should obtain professional advice before commercial operation, institutional deployment, large-scale user data processing, or use involving children, regulated data, or copyrighted corpora.
