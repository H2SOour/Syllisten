# Deployment and intended use

Syllisten is designed for personal study, limited testing with friends, technical demonstration, and portfolio use.

## Recommended public deployment profile

- Keep the service free of charge and do not describe it as a registered nonprofit organization.
- Do not configure or embed a developer OpenAI API key.
- Permit OpenAI mode only when the user supplies their own API key for the current session.
- Do not intentionally persist user text, API keys, generated audio, or dictation answers.
- Do not add public content libraries, shared audio galleries, or user-upload publishing features without a new legal and privacy review.
- Keep `edge-tts` clearly described as an unofficial client for Microsoft Edge online text-to-speech.
- Retain browser speech as a fallback because the external online speech service may change or become unavailable.
- Do not claim affiliation, sponsorship, approval, or partnership with OpenAI, Microsoft, Streamlit, Snowflake, Apple, Google, or any voice provider.

## Suitable current uses

- Personal use on the developer's own computer.
- Small-scale testing with known friends or colleagues.
- A GitHub portfolio project.
- A live demonstration linked from a résumé or LinkedIn profile.

## Uses requiring a new review

Reassess the architecture, terms, and privacy controls before any of the following:

- Charging users, advertising, sponsorship, or other commercial operation.
- Large-scale public access or automated/batch use.
- Institutional or school deployment.
- Processing children's data or regulated personal information.
- Accounts, databases, analytics, or long-term learning histories.
- Public sharing, downloading, or redistribution of generated audio.
- Bundled copyrighted corpora, textbooks, subtitles, examination content, or media transcripts.
- Replacing the current limited prototype with a production service.

## Pre-deployment checklist

1. Run `python -m py_compile app.py`.
2. Run the app locally with `python -m streamlit run app.py`.
3. Confirm that no developer API key exists in the repository or hosting secrets.
4. Search the repository for secrets before every public release.
5. Verify that the notice dialog and all five interface languages are readable and accurate.
6. Confirm that user-key mode fails safely when no key is entered.
7. Confirm that rule-based mode does not call OpenAI.
8. Confirm that the privacy and third-party notices remain linked from the repository.
9. Use a private or limited-access test deployment before broad promotion.
