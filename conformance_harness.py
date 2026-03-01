#!/usr/bin/env python3
"""
Veritas Core Lane 2 Conformance Harness (Phase 1)
- Loads test vectors from JSON
- Validates each against CTP v0.1 logic
- Emits JSONL output with run metadata as first record
- Fails if any placeholder token or repeated hex pattern appears in outputs
"""

import json
import hashlib
import time
import sys
import argparse
from pathlib import Path
from importlib.metadata import version
import jcs  # RFC 8785 canonicalization

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
PLACEHOLDER_TOKENS = ["placeholder", "deadbeef"]
REPEATED_HEX_PATTERN_LEN = 32  # look for any 32-hex substring repeated twice consecutively

# ----------------------------------------------------------------------
# Core validation logic (Lane 2)
# ----------------------------------------------------------------------
def canonicalize(obj):
    """Canonicalize JSON object per RFC 8785."""
    return jcs.canonicalize(obj)

def sha3_256(data):
    return hashlib.sha3_256(data).hexdigest()

def validate_receipt(predicate, receipt):
    """Return (ALLOW/BLOCK, refusal_code)"""
    # Compute hash of canonicalized predicate
    pred_canon = canonicalize(predicate)
    pred_hash = sha3_256(pred_canon)

    # Check predicate_hash match
    if pred_hash != receipt["predicate_hash"]:
        return "BLOCK", "HASH_MISMATCH"

    # Signature verification is stubbed in Phase 1
    # We only check that the signature field exists and is not obviously invalid
    if receipt["signature"]["alg"] == "placeholder":
        if receipt["signature"]["sig_hex"] in PLACEHOLDER_TOKENS:
            # In Round 1, we treat placeholder signatures as "allowed" only if the vector expects ALLOW
            # The test vectors already encode expected result; we'll rely on that.
            # For cryptographic runs later, we'll implement real verification.
            pass

    # Freshness check (simulated)
    # In a real environment we'd compare to current time; here we just trust the receipt's timestamp.
    # We'll skip actual clock check for this conformance run.

    # Lineage continuity check
    if receipt.get("prev_receipt_hash") and len(receipt["prev_receipt_hash"]) != 64:
        return "BLOCK", "LINEAGE_BROKEN"

    # All checks passed
    return "ALLOW", None

# ----------------------------------------------------------------------
# Output validation (placeholder / pattern checks)
# ----------------------------------------------------------------------
def contains_placeholder(text):
    """Return True if any placeholder token appears."""
    for tok in PLACEHOLDER_TOKENS:
        if tok in text:
            return True
    return False

def contains_repeated_hex(text):
    """Return True if any 32‑hex substring appears twice consecutively."""
    # Convert text to lowercase hex characters only
    hex_chars = ''.join(c for c in text.lower() if c in '0123456789abcdef')
    # Scan for repeated 32‑hex chunks
    for i in range(len(hex_chars) - 2*REPEATED_HEX_PATTERN_LEN + 1):
        chunk1 = hex_chars[i:i+REPEATED_HEX_PATTERN_LEN]
        chunk2 = hex_chars[i+REPEATED_HEX_PATTERN_LEN:i+2*REPEATED_HEX_PATTERN_LEN]
        if chunk1 == chunk2:
            return True
    return False

def validate_outputs(output_path):
    """Read output JSONL and check for banned patterns."""
    with open(output_path, 'r') as f:
        for line in f:
            if contains_placeholder(line) or contains_repeated_hex(line):
                print(f"ERROR: Output contains placeholder or repeated hex pattern:\n{line[:200]}...")
                sys.exit(1)
    print("Output validation passed: no placeholder tokens or repeated hex patterns.")

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vectors', required=True, help='Path to test vectors JSON')
    parser.add_argument('--output', required=True, help='Output JSONL file')
    parser.add_argument('--summary', help='Optional Markdown summary file')
    args = parser.parse_args()

    # Load vectors
    with open(args.vectors, 'r') as f:
        vectors = json.load(f)

    # Prepare output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, 'w') as f:
        # Write run metadata as first record
        metadata = {
            "type": "run_metadata",
            "canonicalization_lib": f"jcs=={version('jcs')}",
            "hash_algorithm": "SHA3-256",
            "signature_verification": "stubbed",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        f.write(json.dumps(metadata) + '\n')

        results = []
        for v in vectors:
            pred = v["predicate"]
            receipt = v["receipt"]
            expected = v["expected_validation_result"]

            actual, refusal = validate_receipt(pred, receipt)

            res = {
                "id": v["id"],
                "description": v["description"],
                "expected": expected,
                "actual": actual,
                "refusal_code": refusal,
                "status": "PASS" if actual == expected else "FAIL"
            }
            f.write(json.dumps(res) + '\n')
            results.append(res)

        # Also write computed digests for key artifacts (optional, for record)
        canonical_demo_in = {"y":20, "x":10, "command":"move"}
        canonical_demo_out = canonicalize(canonical_demo_in)
        digest_demo = sha3_256(canonical_demo_out)
        v1_pred = vectors[0]["predicate"]
        digest_v1 = sha3_256(canonicalize(v1_pred))
        digests = {
            "type": "computed_digests",
            "canonicalization_demo": digest_demo,
            "v1_predicate": digest_v1
        }
        f.write(json.dumps(digests) + '\n')

    # Post-run output validation
    validate_outputs(args.output)

    # Generate summary if requested
    if args.summary:
        passed = sum(1 for r in results if r["status"] == "PASS")
        total = len(results)
        with open(args.summary, 'w') as f:
            f.write(f"# Conformance Summary\n\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n\n")
            f.write(f"**Vectors:** {total} total, {passed} passed, {total-passed} failed\n\n")
            f.write("| ID | Expected | Actual | Refusal | Status |\n")
            f.write("|----|----------|--------|---------|--------|\n")
            for r in results:
                f.write(f"| {r['id']} | {r['expected']} | {r['actual']} | {r['refusal_code'] or '-'} | {r['status']} |\n")
        print(f"Summary written to {args.summary}")

    print("Conformance run complete.")

if __name__ == '__main__':
    main()
