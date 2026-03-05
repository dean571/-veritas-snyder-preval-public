# Veritas Core Lane 2 Phase 1 Conformance Bundle (Round 1)
**Date:** 2026-03-05  
**Submitter:** Dean Chapman / Veritas Core  
**Recipient:** Richard Lynes / Genesis AiX Interop Lab  
**Phase:** Phase 1 Conformance (Interface-only, signature stubbed)  
**CTP Package:** ctp-diagnose-driver/1.0 (commit ce36d8f86b6faa9ef7f90b9cc315c10354d17341)

## Bundle Contents
- `conformance_harness.py` – Validator script (RFC 8785 via jcs==1.0.0)
- `test_vectors_v0.1.json` – Six vectors (V1–V6) with canonical reason codes
- `requirements.txt` – Dependencies
- `veritas-conformance-20260305.jsonl` – Run output (run_metadata first)
- `SHA256SUMS.txt` – File integrity hashes

## Replay Instructions
```bash
pip install -r requirements.txt
python conformance_harness.py --vectors test_vectors_v0.1.json --output veritas-conformance-20260305.jsonl


Key Compliance

✅ Canonical reason codes (per repo/spec)
✅ RFC 8785 via jcs==1.0.0
✅ Signature verification: explicitly stubbed (signature_verification: "stubbed")
✅ Run metadata: first JSONL record
✅ Fail-closed: rejects placeholders/repeated hex patterns
✅ Offline-replayable: zero external dependencies beyond jcs==1.0.0


#### 📄 `test_vectors_v0.1.json`
```json
{
  "schema_version": "ctp-v0.1-fixtures",
  "package_id": "CTP-MESHHW-ROUND1",
  "generated_utc": "2026-03-05T00:00:00Z",
  "vectors": [
    {
      "vector_id": "V1",
      "description": "Missing required signal (PPS unavailable)",
      "request": {
        "request_id": "req-v1-0001",
        "decision_time": "2026-03-05T00:00:00Z",
        "subject": {
          "subject_type": "device",
          "subject_id": "dean571:rail0",
          "subject_pubkey_id": "pubkey:veritas:rail0"
        },
        "action": {
          "action_type": "verify_before_commit",
          "action_binding_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
        },
        "inputs_jcs": {
          "opaque_request": {}
        }
      },
      "policy": {
        "policy_bundle_version": "bundle:round1",
        "policy_jcs_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
        "requires_signal": true,
        "requires_attestation": true
      },
      "expected": {
        "decision": "REFUSE",
        "reason_code": "REFUSE_SIGNAL_REQUIRED_UNAVAILABLE",
        "retryable": true
      }
    },
    {
      "vector_id": "V2",
      "description": "Invalid attestation signature",
      "expected": {
        "decision": "REFUSE",
        "reason_code": "REFUSE_SIGNATURE_INVALID",
        "retryable": false
      }
    },
    {
      "vector_id": "V3",
      "description": "Invalid policy bundle digest",
      "expected": {
        "decision": "REFUSE",
        "reason_code": "REFUSE_POLICY_BUNDLE_INVALID",
        "retryable": false
      }
    },
    {
      "vector_id": "V4",
      "description": "Missing required evidence fields",
      "expected": {
        "decision": "REFUSE",
        "reason_code": "REFUSE_EVIDENCE_MISSING",
        "retryable": true
      }
    },
    {
      "vector_id": "V5",
      "description": "Consent revoked in policy",
      "expected": {
        "decision": "BLOCK",
        "reason_code": "BLOCK_CONSENT_REVOKED",
        "retryable": false
      }
    },
    {
      "vector_id": "V6",
      "description": "Happy path – all valid",
      "expected": {
        "decision": "ALLOW",
        "reason_code": "ALLOW_OK",
        "retryable": false
      }
    }
  ]
}
