# Release checklist

- [ ] `APP_VERSION`, `pyproject.toml`, `CHANGELOG.md`, and `CITATION.cff` agree.
- [ ] `python -m py_compile app.py` passes.
- [ ] Local Streamlit test passes in rule-based mode.
- [ ] User-key mode requires a user-supplied key and never falls back to a developer key.
- [ ] English accent selector works for British and American speech.
- [ ] Chinese and Japanese punctuation segmentation works.
- [ ] No `DeltaGenerator` or other Streamlit internal object is rendered.
- [ ] All five UI languages and notice-dialog translations are reviewed.
- [ ] No secret, local environment, cache, or generated audio is committed.
- [ ] Direct dependency licenses and external-service disclosures are current.
- [ ] README links to legal, privacy, security, and third-party documents.
- [ ] The live demo is tested privately before public promotion.
