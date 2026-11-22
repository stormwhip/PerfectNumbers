"""Deterministic residual prime-cutoff GCD acceptance and tamper regression."""
from IndependentVerifierV2 import VerificationError, verify_min_prime_bound

def main():
    residue = 1009 * 1013
    cert = {"method": "PRIME_CUTOFF_GCD", "base_trial_limit": 1000, "cutoff": 2000}
    verify_min_prime_bound(residue, 1009, cert)
    verify_min_prime_bound(residue, 3, cert)
    for alpha in (1013, 1017):
        try:
            verify_min_prime_bound(residue, alpha, cert)
        except VerificationError:
            continue
        raise RuntimeError(f"false minimum prime bound was accepted: alpha={alpha}")
    print("PrimeCutoffGCDTests: ALL TESTS PASSED")

if __name__ == "__main__":
    main()
