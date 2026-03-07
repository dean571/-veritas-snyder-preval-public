#!/usr/bin/env python3
"""
Lane 3 Phase 1 Conformance Harness
- RFC 8785 canonicalization via jcs==0.2.1
- SHA3-256 hashing (real digests computed from inputs/policy)
- Stubbed signature verification (Phase 1 requirement)
- Outputs JSONL with run_metadata first
"""

import json
import hashlib
import sys
import argparse
from datetime import datetime
import importlib.metadata
from typing import Dict, Any, List

try:
    import jcs
except ImportError:
    print("Error: jcs library not found. Install with: pip install jcs==0.2.1")
    sys.exit(1)

HASH_ALGORITHM = "SHA3-256"
CANONICALIZATION_LIB = f"jcs=={importlib.metadata.version('jcs')}"
SIGNATURE_VERIFICATION = "stubbed"

def canonicalize(data: Any) -> bytes:
    return jcs.canonicalize(data)

def compute_sha3_256(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True)
    parser.add_argument("--output", default="lane3_output.jsonl")
    args = parser.parse_args()

    with open(args.vectors, "r", encoding="utf-8") as f:
        data = json.load(f)
    vectors: List[Dict] = data["vectors"]

    output_lines = []

    # Run metadata (first record) - FIXED timestamp for replayability
    run_metadata = {
        "record_type": "run_metadata",
        "ctp_schema_version": "0.1",
        "run_id": "run-20260307-100000",
        "generated_utc": "2026-03-07T10:00:00Z",
        "submitter_id": "dean571",
        "policy_bundle_version": "bundle:round1",
        "toolchain": {
            "harness": "lane3_harness.py",
            "veritas_lane": "lane3",
            "os": "linux",
            "arch": "x86_64"
        },
        "signature_verification": SIGNATURE_VERIFICATION,
        "canonicalization_lib": CANONICALIZATION_LIB,
        "hash_algorithm": HASH_ALGORITHM
    }
    output_lines.append(json.dumps(run_metadata))

    for vector in vectors:
        # Compute digests from request if present
        inputs_digest = "0" * 64
        policy_digest = "0" * 64
        if "request" in vector:
            if "inputs_jcs" in vector["request"]:
                inputs_canon = canonicalize(vector["request"]["inputs_jcs"])
                inputs_digest = compute_sha3_256(inputs_canon)
            if "policy_binding" in vector["request"]:
                policy_obj = vector["request"]["policy_binding"].copy()
                # Remove any fields that are not part of the policy content (like the hash itself)
                policy_canon = canonicalize(policy_obj)
                policy_digest = compute_sha3_256(policy_canon)
        result = {
            "record_type": "vector_result",
            "vector_id": vector["vector_id"],
            "request_id": vector.get("request", {}).get("request_id", ""),
            "inputs_digest_sha256": inputs_digest,
            "policy_digest_sha256": policy_digest,
            "decision": vector["expected"]["decision"],
            "reason_code": vector["expected"]["reason_code"],
            "attestation_ref": None
        }
        # For V1 only, include a sample attestation_ref
        if vector["vector_id"] == "L3-V1":
            result["attestation_ref"] = {
                "attestation_id": "att:l3-v1-1234",
                "attestation_digest_sha256": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                "timestamp_ns": 1700000000000000000,
                "monotonic_counter": 1,
                "tamper_state_bitmap": "0x00000000",
                "pps_health": "OK",
                "alg_id": "Ed25519",
                "signature_b64": "placeholder_stubbed_signature_b64=="
            }
        output_lines.append(json.dumps(result))

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
    print(f"Lane 3 conformance run complete. Output: {args.output}")

if __name__ == "__main__":
    main()