# Third-Party Notices

This document records the principal third-party software and external services used by Syllisten. It is informational and does not replace the full upstream licenses or service terms.

## 1. Streamlit

- Purpose: web interface, widgets, session state, and application runtime
- Upstream: https://github.com/streamlit/streamlit
- License: Apache License 2.0
- Upstream license: https://github.com/streamlit/streamlit/blob/develop/LICENSE
- Local license copy: [`licenses/APACHE-2.0.txt`](licenses/APACHE-2.0.txt)

Streamlit is a trademark/product name of its respective owner. Syllisten is not affiliated with or endorsed by Streamlit or Snowflake.

## 2. OpenAI Python SDK

- Purpose: optional text-language detection and semantic segmentation when the user selects API mode
- Upstream: https://github.com/openai/openai-python
- License: Apache License 2.0
- Upstream license: https://github.com/openai/openai-python/blob/main/LICENSE
- Local license copy: [`licenses/APACHE-2.0.txt`](licenses/APACHE-2.0.txt)

The application contains no developer OpenAI API key. API mode requires the user's own key. OpenAI services, accounts, data processing, and charges are governed by the agreements applicable to the user's OpenAI API account. Syllisten is not an OpenAI product and is not endorsed by OpenAI.

## 3. edge-tts

- Purpose: primary online text-to-speech synthesis
- Upstream: https://github.com/rany2/edge-tts
- Package description: an unofficial Python client for Microsoft Edge's online text-to-speech service
- Upstream license: https://github.com/rany2/edge-tts/blob/master/LICENSE
- License summary stated by upstream: most files are licensed under GNU LGPL version 3; `src/edge_tts/srt_composer.py` is MIT-licensed
- Local LGPL copy: [`licenses/LGPL-3.0.txt`](licenses/LGPL-3.0.txt)
- Local MIT copy: [`licenses/MIT.txt`](licenses/MIT.txt)

Syllisten imports `edge-tts` as an external Python dependency and does not modify or vendor its source code. Deployers who redistribute packaged copies should preserve the upstream license notices and ensure that recipients can replace or update the separately installed library as required by applicable license terms.

`edge-tts` is not an official Microsoft SDK. It accesses Microsoft Edge online speech synthesis, and sentence text submitted for speech may be transmitted to Microsoft-operated infrastructure. Microsoft documents online text-to-speech voices as online, higher-quality voice fonts connected with its speech services. Service availability, voices, privacy behavior, acceptable use, and terms may change independently of this project.

Syllisten does not claim ownership of Microsoft voices, voice names, generated speech technology, or Microsoft trademarks.

## 4. Browser Web Speech API

- Purpose: fallback speech synthesis when online natural speech generation is unavailable
- Nature: browser API, not bundled software
- Reference: https://developer.mozilla.org/docs/Web/API/Web_Speech_API

Actual implementations and voices are supplied by the user's browser, operating system, or third-party voice provider. Processing may occur locally or remotely. Users and deployers are responsible for reviewing their browser and operating-system privacy settings and terms.

## 5. Python and transitive dependencies

Syllisten uses the Python standard library and packages installed transitively by the direct dependencies above. Those packages remain subject to their own licenses. A deployment or binary redistribution should generate and review a complete software bill of materials for the exact locked dependency set, for example with `pip-licenses`, `pipdeptree`, or an equivalent tool.

## 6. No bundled third-party content

The repository is not intended to bundle third-party books, articles, subtitles, examination texts, lyrics, voice recordings, proprietary fonts, logos, datasets, or speech models. Users supply their own text and are responsible for ensuring lawful use.

## 7. Reporting an attribution or rights concern

Open a GitHub issue marked **legal/attribution**, or contact the repository owner through the contact method published on the repository profile. Include the material concerned, the relevant right or license, its exact location, evidence of authority, and the requested correction or removal.

Good-faith, sufficiently documented notices will be reviewed and, where appropriate, corrected, attributed, disabled, or removed.
