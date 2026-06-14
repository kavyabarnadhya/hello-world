## 2025-05-15 - Fail-Fast Environment Validation and Defensive Typing
**Vulnerability:** Application crashes or insecure behavior due to missing environment variables or malformed data from external sources (RSS/LLM).
**Learning:** External data should never be assumed to be of a specific type (e.g., LLMs might return non-strings). Missing env vars should be caught at startup rather than mid-execution.
**Prevention:** Implement a `validate_env()` function to check all required secrets and basic formats at boot. Use `isinstance(var, str)` and explicit `str()` conversion for all dynamic data before processing for HTML.

## 2026-05-06 - validate_env() Bug: Empty-String Handling in RECEIVER_EMAIL
**Incident:** The `validate_env()` function introduced in the Sentinel PR caused 3 consecutive daily workflow failures. The RECEIVER_EMAIL regex check iterated over all entries from `.split(",")` without filtering empty strings first. A trailing comma in the secret (e.g. `user@example.com,`) produces an empty string that fails the regex, raising a ValueError → exit(1).
**Fix:** Filter empty entries before validation: `[r.strip() for r in val.split(",") if r.strip()]`
**Lesson:** Always mirror the same split/filter logic used in `send_email()` when validating the same field. **Do NOT modify `validate_env()` or email-handling logic without running `python -m unittest test_parallel_logic.py` AND manually testing the validate_env paths.** For security-sensitive functions, add unit tests before and after changes.

## 2026-05-18 - Protocol Enforcement vs. Compatibility
**Vulnerability:** Risk of Local File Disclosure (LFD) or SSRF via `feedparser.parse()` and dangerous URI schemes (e.g., `javascript:`) in article links.
**Fix:** Implement strict protocol validation to allow only `http://` and `https://`.
**Learning:** Overly restrictive security (e.g., HTTPS-only) can break existing functionality in applications that rely on external legacy sources. While HTTPS is preferred, mandating it for all external feeds can cause regressions if the provider only supports HTTP.
**Prevention:** Use an allow-list of safe web protocols (`http`, `https`) rather than a single restrictive one, unless the environment is fully controlled.

## 2026-05-24 - AI-Driven Resource Exhaustion (DoS)
**Vulnerability:** Resource exhaustion via malformed or malicious LLM output containing duplicate article indices or excessively large JSON structures.
**Learning:** AI-generated content should be treated as untrusted input. Trusting indices returned by an LLM without deduplication and bounding can lead to unbounded iteration or payload growth.
**Fix:** Extracted LLM processing into `process_llm_articles()` with strict bounds: capped input iteration at 100, deduplicated indices via a `seen_indices` set, capped final article count at 50, and limited category topics to 20.
**Prevention:** Always implement hard bounds and deduplication when mapping untrusted identifiers (like indices) back to internal data structures.

## 2026-05-30 - LLM Role Separation for Injection Defense
**Vulnerability:** Prompt injection risk where untrusted article data could override system instructions if both are sent in a single 'user' message.
**Learning:** Sending instructions and untrusted data in the same message makes it easier for an attacker (or malformed input) to manipulate the model's behavior.
**Fix:** Separated persona and instructions into a 'system' message, while keeping the external article data in a 'user' message.
**Prevention:** Always use the 'system' role for static instructions and the 'user' role for dynamic/untrusted data to leverage the model's internal role-based priority and boundary enforcement.
