# Data flow and external services

This document describes the intended data flow of Syllisten. Actual network behavior may also be affected by the hosting provider, browser, operating system, extensions, reverse proxies, and third-party services.

## Rule-based mode

- User text is submitted to the running Streamlit application.
- Built-in Python rules perform language detection and sentence segmentation.
- The application does not intentionally send the text to OpenAI.
- The text may still pass through the hosting infrastructure because Streamlit code runs on the app server.

## User-supplied OpenAI API mode

- The user enters their own OpenAI API key in a password field.
- The key is stored only in the current Streamlit session state by the application.
- The submitted text is sent to OpenAI using that user-provided key.
- Charges, quotas, retention, and processing are governed by the user's OpenAI API account and applicable OpenAI terms.
- Syllisten contains no developer OpenAI API key and does not read one from environment variables or Streamlit secrets.

## Natural speech with edge-tts

- Text selected for speech synthesis is passed to the separately installed `edge-tts` package.
- `edge-tts` is an unofficial client for Microsoft Edge's online text-to-speech service.
- The sentence may be transmitted to Microsoft-operated online speech infrastructure.
- Syllisten does not control the service's availability, processing location, retention, or future terms.

## Browser speech fallback

- If online synthesis fails, Syllisten may use the browser Web Speech API.
- Processing may occur locally or through a browser/operating-system vendor service, depending on the selected voice and platform.

## Intended non-persistence

Syllisten does not intentionally write user text, API keys, dictation answers, or generated audio to a database. Temporary process memory, browser state, server logs, platform diagnostics, network intermediaries, or caches may exist outside the application's direct control.
