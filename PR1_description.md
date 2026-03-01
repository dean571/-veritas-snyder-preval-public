# Pull Request: trackB/run-metadata-no-placeholder

**Branch:** `trackB/run-metadata-no-placeholder`  
**Target:** `main` (Interop Lab repo)  
**Reviewer:** @Richard-Lynes  

## Summary

This PR implements the two fixes requested for Phase 1 conformance:

1. **Canonicalization environment** now correctly reports `jcs==1.0.0` (RFC 8785 via `jcs.canonicalize()`) and captures the installed package version at runtime.
2. **Run metadata** is emitted as the first JSONL record (`{"type":"run_metadata", ...}`), including canonicalization lib, hash algorithm, signature verification status (`stubbed`), and UTC timestamp.
3. **Fail‑closed checks** have been added to the harness:
   - Bans any output containing placeholder tokens (`"placeholder"`, `"deadbeef"`).
   - Bans any 32‑hex substring repeated twice consecutively (covers the `f7a2…f7a2…` pattern without over‑fitting).
4. **Computed digests** for key artifacts are also appended to the JSONL output for traceability.

These changes ensure “no drift” in Track B reports and make the conformance run fully machine‑verifiable.

## Files Changed

- `conformance_harness.py` – updated with metadata emission and validation checks.
- `2026-03-01_veritas-conformance-report.md` – corrected environment section.
- `veritas-conformance-20260301.json` – now includes `run_metadata` as first record.
- `MANIFEST.md` – updated with new file SHA256s (to be computed after merge).

## Testing

- Ran the harness against all 6 test vectors; all passed.
- Verified that the output JSONL contains the required metadata record.
- Artificially introduced a placeholder token; harness failed as expected.
- Artificially introduced a repeated‑hex pattern; harness failed as expected.

## Next Steps

- Merge this PR to officially log Phase 1 conformance.
- Phase 2 (crypto verification) will be addressed under ticket **PH2‑TB‑CRYPTO‑0001**.

---

**Dean Chapman**  
Veritas Core
