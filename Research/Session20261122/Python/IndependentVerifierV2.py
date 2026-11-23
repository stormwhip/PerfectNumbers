"""Independent integer/fixed-point proof verifier (V2) for OPN search trees.

Security and soundness invariants:
1. External pinning: upper_bound_N, root_set, root_order, and initial root state
   are NEVER trusted from untrusted proof bundles; they are reconstructed from RootTaskPin.
2. Zero `assert` statements for verification logic (immune to `python -O`).
3. Strict JSON parsing rejects duplicate keys; strict int checks reject bool.
4. Unknown/unimplemented rules raise UnsupportedRuleError (never silently accepted).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from RoadblockDual import RoadblockDual, SCALE, log_bounds, odd_primes
import TerminalCertificate
import VerifyRootExponentCoverage


ORIGINAL_ROOTS: Tuple[int, ...] = (3, 5, 7, 11, 13, 17, 19, 31)
REPLACEMENT_ROOTS: Tuple[int, ...] = (3, 5, 7, 11, 13, 17, 23, 31)
DEFAULT_CIRC_ORDER: Tuple[int, ...] = (19, 7, 11, 31, 13, 3, 5, 17)
LP_DYADIC: int = 1 << 24


class VerificationError(Exception):
    """Raised on any integrity, arithmetic, or coverage violation."""


class UnsupportedRuleError(VerificationError):
    """Raised when a proof node relies on an unimplemented or unknown rule."""


# ---------------- Strict Parsing & Hashing ----------------

def require_strict_int(value: object, name: str, minimum: Optional[int] = None) -> int:
    if type(value) is not int:
        raise VerificationError(f"{name} must be strict int, got {type(value).__name__}")
    if minimum is not None and value < minimum:
        raise VerificationError(f"{name} must be >= {minimum}, got {value}")
    return value


def require_strict_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise VerificationError(f"{name} must be strict bool, got {type(value).__name__}")
    return value


def _no_duplicate_keys_hook(pairs: List[Tuple[str, object]]) -> dict:
    obj: dict = {}
    for k, v in pairs:
        if k in obj:
            raise VerificationError(f"duplicate JSON key detected: {k!r}")
        obj[k] = v
    return obj


def strict_json_loads(text: str) -> object:
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys_hook)
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON: {exc}") from exc


def canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------- Exact Number-Theoretic Helpers ----------------

def sigma_prime_power(p: int, e: int) -> int:
    require_strict_int(p, "p", 2)
    require_strict_int(e, "e", 1)
    return (pow(p, e + 1) - 1) // (p - 1)


def integer_factor_count_upper(value: int, min_factor: int) -> int:
    """Exact floor(log_{min_factor}(value)) via integer division."""
    require_strict_int(value, "value", 1)
    require_strict_int(min_factor, "min_factor", 2)
    cnt = 0
    rem = value
    while rem >= min_factor:
        rem //= min_factor
        cnt += 1
    return cnt


def verify_primality_certificate(n: int, cert: object, verified_primes: Set[int]) -> None:
    """Verify an explicit deterministic primality certificate (deduplicated globally)."""
    require_strict_int(n, "primality target", 2)
    if n in verified_primes:
        return
    if not isinstance(cert, dict) or "method" not in cert:
        raise VerificationError(f"missing primality certificate for {n}")

    method = cert["method"]
    if method == "TRIAL_DIV":
        limit = require_strict_int(cert.get("max_divisor"), "max_divisor", 1)
        expected = math.isqrt(n)
        if limit < expected:
            raise VerificationError(f"TRIAL_DIV max_divisor={limit} < isqrt({n})={expected}")
        if limit > 100000:
            raise VerificationError(f"TRIAL_DIV limit {limit} > 100000; use PRATT/POCKLINGTON")
        if n == 2:
            verified_primes.add(2)
            return
        if n % 2 == 0:
            raise VerificationError(f"{n} is even and > 2")
        for d in range(3, expected + 1, 2):
            if n % d == 0:
                raise VerificationError(f"{n} is composite (divisible by {d})")
        verified_primes.add(n)
        return

    if method == "PRATT":
        a = require_strict_int(cert.get("witness"), "Pratt witness", 2)
        if a >= n:
            raise VerificationError(f"Pratt witness {a} must be < {n}")
        factors = cert.get("n_minus_1_factors")
        if not isinstance(factors, list) or not factors:
            raise VerificationError(f"missing n_minus_1_factors in Pratt cert for {n}")
        if pow(a, n - 1, n) != 1:
            raise VerificationError(f"Pratt Fermat check failed for {n}, a={a}")
        prod = 1
        seen_q: Set[int] = set()
        for item in factors:
            if not isinstance(item, dict):
                raise VerificationError(f"malformed Pratt factor entry for {n}")
            q = require_strict_int(item.get("q"), "Pratt q", 2)
            e = require_strict_int(item.get("e"), "Pratt e", 1)
            if q >= n or q in seen_q:
                raise VerificationError(f"invalid or duplicate Pratt factor q={q} for {n}")
            seen_q.add(q)
            verify_primality_certificate(q, item.get("cert"), verified_primes)
            if pow(a, (n - 1) // q, n) == 1:
                raise VerificationError(f"Pratt order check failed for {n}, q={q}")
            prod *= pow(q, e)
        if prod != n - 1:
            raise VerificationError(f"Pratt factor product {prod} != {n - 1}")
        verified_primes.add(n)
        return

    if method == "POCKLINGTON":
        factors = cert.get("partial_factors")
        if not isinstance(factors, list) or not factors:
            raise VerificationError(f"missing partial_factors in Pocklington cert for {n}")
        known = 1
        seen_q: Set[int] = set()
        for item in factors:
            if not isinstance(item, dict):
                raise VerificationError(f"malformed Pocklington factor entry for {n}")
            q = require_strict_int(item.get("q"), "Pocklington q", 2)
            e = require_strict_int(item.get("e"), "Pocklington e", 1)
            a = require_strict_int(item.get("a"), "Pocklington a", 2)
            if q >= n or a >= n or q in seen_q:
                raise VerificationError(f"invalid Pocklington entry for {n}: {item}")
            seen_q.add(q)
            verify_primality_certificate(q, item.get("cert"), verified_primes)
            if pow(a, n - 1, n) != 1:
                raise VerificationError(f"Pocklington Fermat check failed for {n}, q={q}, a={a}")
            if math.gcd(pow(a, (n - 1) // q, n) - 1, n) != 1:
                raise VerificationError(f"Pocklington gcd check failed for {n}, q={q}, a={a}")
            known *= pow(q, e)
        if (n - 1) % known != 0 or known * known <= n:
            raise VerificationError(
                f"Pocklington bound failed for {n}: known={known}, known^2 <= n or not dividing n-1"
            )
        verified_primes.add(n)
        return

    raise UnsupportedRuleError(f"unsupported primality certificate method: {method!r}")


@lru_cache(maxsize=8)
def _build_cutoff_prime_product(low_exclusive: int, high_inclusive: int) -> int:
    """Deterministically build the exact product of all odd primes in (low_exclusive, high_inclusive]."""
    block = 1
    levels: List[int] = []
    within = 0
    for q in odd_primes(high_inclusive):
        if q <= low_exclusive:
            continue
        block *= q
        within += 1
        if within == 1024:
            levels.append(block)
            block = 1
            within = 0
    if within:
        levels.append(block)
    if not levels:
        return 1
    while len(levels) > 1:
        nxt: List[int] = []
        for i in range(0, len(levels), 2):
            nxt.append(levels[i] * levels[i + 1] if i + 1 < len(levels) else levels[i])
        levels = nxt
    return levels[0]


def verify_min_prime_bound(value: int, min_prime: int, cert: Optional[dict]) -> None:
    """Verify that odd integer `value` has no prime divisor < min_prime."""
    require_strict_int(value, "composite value", 3)
    require_strict_int(min_prime, "min_prime", 3)
    if value % 2 == 0:
        raise VerificationError(f"composite residue {value} must be odd")
    if min_prime == 3:
        return
    if not isinstance(cert, dict) or "method" not in cert:
        raise VerificationError(f"missing min_prime_cert for residue {value} with alpha={min_prime}")

    method = cert["method"]
    if method == "TRIAL_DIV_RANGE":
        if min_prime > 10000:
            raise UnsupportedRuleError(
                f"TRIAL_DIV_RANGE alpha={min_prime} > 10000; use PRIME_CUTOFF_GCD"
            )
        for r in odd_primes(min_prime - 1):
            if value % r == 0:
                raise VerificationError(f"residue {value} divisible by {r} < alpha={min_prime}")
        return

    if method == "PRIME_CUTOFF_GCD":
        base_lim = require_strict_int(cert.get("base_trial_limit", 1000), "base_trial_limit", 3)
        cutoff = require_strict_int(cert.get("cutoff"), "cutoff", base_lim + 1)
        if cutoff > 100_000_000:
            raise UnsupportedRuleError(f"cutoff={cutoff} exceeds supported deterministic sieve cap 10^8")
        if min_prime > cutoff + 1:
            raise VerificationError(f"claimed min_prime={min_prime} > cutoff+1={cutoff + 1}")
        for r in odd_primes(min(base_lim, min_prime - 1)):
            if value % r == 0:
                raise VerificationError(f"residue {value} divisible by small prime {r}")
        if min_prime - 1 > base_lim:
            primorial = _build_cutoff_prime_product(base_lim, min_prime - 1)
            if math.gcd(value, primorial) != 1:
                raise VerificationError(
                    f"residue {value} shares prime factor in ({base_lim}, {min_prime - 1}]"
                )
        return

    raise UnsupportedRuleError(f"unsupported composite min_prime_cert method: {method!r}")

# ---------------- Authoritative State & External Root Pin ----------------

@dataclass(frozen=True)
class BranchEntry:
    exp: int
    exact: bool


@dataclass(frozen=True)
class CompositeResidue:
    value: int
    min_prime: int


@dataclass(frozen=True)
class VerifierState:
    branched: Dict[int, BranchEntry]
    unbranched: frozenset
    forbidden: frozenset
    has_special: bool
    composites: Tuple[CompositeResidue, ...]  # ORDER-PRESERVED
    source_v_bounds: Dict[int, Dict[int, int]]  # target_q -> {source_p: lb}
    source_v2_bounds: Dict[int, int]            # source_p -> v2(sigma(p^d))

    def canonical_dict(self) -> dict:
        return {
            "branched": [
                {"p": p, "exp": self.branched[p].exp, "exact": self.branched[p].exact}
                for p in sorted(self.branched)
            ],
            "unbranched": sorted(self.unbranched),
            "forbidden": sorted(self.forbidden),
            "has_special": self.has_special,
            "composites": [
                {"value": c.value, "min_prime": c.min_prime}
                for c in self.composites
            ],
            "source_v_bounds": [
                {
                    "q": q,
                    "sources": [
                        {"p": p, "v": self.source_v_bounds[q][p]}
                        for p in sorted(self.source_v_bounds[q])
                    ],
                }
                for q in sorted(self.source_v_bounds)
            ],
            "source_v2_bounds": [
                {"p": p, "v2": self.source_v2_bounds[p]}
                for p in sorted(self.source_v2_bounds)
            ],
        }

    def state_hash(self) -> str:
        return sha256_hex(canonical_json_bytes(self.canonical_dict()))

    def _even_min_exp(self, q: int) -> int:
        sigma_lb = sum(self.source_v_bounds.get(q, {}).values())
        lb = max(2, sigma_lb)
        return lb if lb % 2 == 0 else lb + 1

    def _odd_euler_min_exp(self, q: int) -> int:
        sigma_lb = sum(self.source_v_bounds.get(q, {}).values())
        lb = max(1, sigma_lb)
        rem = (1 - lb) % 4
        return lb + rem

    def min_exponent(self, p: int) -> int:
        if p in self.branched:
            return self.branched[p].exp
        if p in self.unbranched:
            if not self.has_special and p % 4 == 1:
                return min(self._even_min_exp(p), self._odd_euler_min_exp(p))
            return self._even_min_exp(p)
        raise VerificationError(f"prime {p} is neither branched nor unbranched")

    def min_size_lower_bound(self, override_min_exp: Optional[Tuple[int, int]] = None) -> int:
        """Exact integer lower bound on N using lcm over forced primes & composites."""
        branched_prod = 1
        for p, info in self.branched.items():
            e = info.exp
            if override_min_exp is not None and override_min_exp[0] == p:
                e = max(e, override_min_exp[1])
            branched_prod *= pow(p, e)

        unbranched_sorted = sorted(self.unbranched)
        even_exps: Dict[int, int] = {}
        for q in unbranched_sorted:
            e = self._even_min_exp(q)
            if override_min_exp is not None and override_min_exp[0] == q:
                e = max(e, override_min_exp[1])
            even_exps[q] = e

        def lcm_with_composites(base_prod: int) -> int:
            acc = base_prod
            for c in self.composites:
                acc = math.lcm(acc, c.value)
            return acc

        base_even_prod = branched_prod
        for q, e in even_exps.items():
            base_even_prod *= pow(q, e)
        best = lcm_with_composites(base_even_prod)

        if not self.has_special:
            for q in unbranched_sorted:
                if q % 4 != 1:
                    continue
                odd_e = self._odd_euler_min_exp(q)
                if override_min_exp is not None and override_min_exp[0] == q:
                    odd_e = max(odd_e, override_min_exp[1])
                if odd_e < even_exps[q]:
                    alt_prod = (base_even_prod // pow(q, even_exps[q])) * pow(q, odd_e)
                    best = min(best, lcm_with_composites(alt_prod))
        return best

    def min_abundance_exceeds_two(self) -> bool:
        """Exact rational test: returns True iff sigma(N)/N > 2 for every valid completion."""
        def check_assignment(exps: Dict[int, int]) -> bool:
            num = 1
            den = 1
            for p, e in exps.items():
                num *= sigma_prime_power(p, e)
                den *= pow(p, e)
            return num > 2 * den

        base_exps: Dict[int, int] = {p: info.exp for p, info in self.branched.items()}
        for q in self.unbranched:
            base_exps[q] = self._even_min_exp(q)

        if not check_assignment(base_exps):
            return False
        if not self.has_special:
            for q in self.unbranched:
                if q % 4 != 1:
                    continue
                odd_e = self._odd_euler_min_exp(q)
                if odd_e < base_exps[q]:
                    alt = dict(base_exps)
                    alt[q] = odd_e
                    if not check_assignment(alt):
                        return False
        return True


@dataclass(frozen=True)
class RootTaskPin:
    """Externally pinned theorem & task context (never read from proof bundle)."""
    upper_bound_N: int
    root_set: Tuple[int, ...]
    root_order: Tuple[int, ...]
    circ_order: Tuple[int, ...]
    root_prime: int
    root_exp: int
    root_exact: bool

    def build_initial_state(self, verified_primes: Set[int]) -> VerifierState:
        require_strict_int(self.upper_bound_N, "upper_bound_N", 10)
        if sorted(self.root_order) != sorted(self.root_set) or len(self.root_order) != len(set(self.root_order)):
            raise VerificationError("root_order must be a permutation of root_set")
        if self.root_prime not in self.root_order:
            raise VerificationError(f"root_prime {self.root_prime} not in root_order")
        require_strict_int(self.root_exp, "root_exp", 1)
        require_strict_bool(self.root_exact, "root_exact")

        for q in self.root_set:
            require_strict_int(q, "root prime", 3)
            verify_primality_certificate(q, {"method": "TRIAL_DIV", "max_divisor": math.isqrt(q)}, verified_primes)

        if self.root_exact and self.root_exp % 2 == 1:
            if self.root_prime % 4 != 1 or self.root_exp % 4 != 1:
                raise VerificationError("illegal odd exact root exponent")
            has_special = True
        else:
            if self.root_exp % 2 != 0:
                raise VerificationError("standard or non-special exact root exponent must be even")
            has_special = False

        idx = self.root_order.index(self.root_prime)
        prior_forbidden = frozenset(self.root_order[:idx])
        st = VerifierState(
            branched={self.root_prime: BranchEntry(exp=self.root_exp, exact=self.root_exact)},
            unbranched=frozenset(),
            forbidden=prior_forbidden,
            has_special=has_special,
            composites=(),
            source_v_bounds={},
            source_v2_bounds={},
        )
        _validate_state_invariants(st)
        return st


def _validate_state_invariants(st: VerifierState) -> None:
    if st.branched.keys() & st.unbranched:
        raise VerificationError("overlap between branched and unbranched")
    if (st.branched.keys() | st.unbranched) & st.forbidden:
        raise VerificationError("forced prime present in forbidden set")
    special_count = 0
    for p, info in st.branched.items():
        if p <= 2 or p % 2 == 0:
            raise VerificationError(f"branched prime must be odd > 2, got {p}")
        if info.exp < 1:
            raise VerificationError(f"branched exp must be >= 1 for {p}")
        if info.exact and info.exp % 2 == 1:
            if p % 4 != 1 or info.exp % 4 != 1:
                raise VerificationError(f"illegal Euler commitment p={p}, exp={info.exp}")
            special_count += 1
        elif not info.exact and info.exp % 2 != 0:
            raise VerificationError(f"standard branch exp must be even, got p={p}, exp={info.exp}")
    if st.has_special and special_count != 1:
        raise VerificationError("has_special=True requires exactly one odd exact prime")
    if not st.has_special and special_count != 0:
        raise VerificationError("has_special=False conflicts with odd exact prime")
    for q in st.unbranched:
        if q <= 2 or q % 2 == 0:
            raise VerificationError(f"unbranched prime must be odd > 2, got {q}")
    for c in st.composites:
        if c.value <= 1 or c.value % 2 == 0 or c.min_prime < 3:
            raise VerificationError(f"invalid composite residue {c}")
    for q, smap in st.source_v_bounds.items():
        for src_p, v in smap.items():
            if src_p not in st.branched or v < 1:
                raise VerificationError(f"invalid source_v_bounds entry q={q}, p={src_p}, v={v}")
    for src_p, v2 in st.source_v2_bounds.items():
        if src_p not in st.branched or v2 < 0:
            raise VerificationError(f"invalid source_v2_bounds entry p={src_p}, v2={v2}")


def parse_state_dict(obj: object) -> VerifierState:
    if not isinstance(obj, dict):
        raise VerificationError("state must be a JSON object")
    branched: Dict[int, BranchEntry] = {}
    for item in obj.get("branched", []):
        if not isinstance(item, dict):
            raise VerificationError("malformed branched entry")
        p = require_strict_int(item.get("p"), "branched.p", 3)
        exp = require_strict_int(item.get("exp"), "branched.exp", 1)
        exact = require_strict_bool(item.get("exact"), "branched.exact")
        if p in branched:
            raise VerificationError(f"duplicate branched prime {p}")
        branched[p] = BranchEntry(exp=exp, exact=exact)

    raw_ub = obj.get("unbranched", [])
    if not isinstance(raw_ub, list):
        raise VerificationError("unbranched must be a list")
    unbranched = frozenset(require_strict_int(q, "unbranched item", 3) for q in raw_ub)

    raw_fb = obj.get("forbidden", [])
    if not isinstance(raw_fb, list):
        raise VerificationError("forbidden must be a list")
    forbidden = frozenset(require_strict_int(q, "forbidden item", 3) for q in raw_fb)

    has_special = require_strict_bool(obj.get("has_special"), "has_special")

    raw_comp = obj.get("composites", [])
    if not isinstance(raw_comp, list):
        raise VerificationError("composites must be a list")
    composites_list: List[CompositeResidue] = []
    for c in raw_comp:
        if not isinstance(c, dict):
            raise VerificationError("malformed composite entry")
        composites_list.append(
            CompositeResidue(
                value=require_strict_int(c.get("value"), "composite.value", 3),
                min_prime=require_strict_int(c.get("min_prime"), "composite.min_prime", 3),
            )
        )

    source_v_bounds: Dict[int, Dict[int, int]] = {}
    for entry in obj.get("source_v_bounds", []):
        if not isinstance(entry, dict):
            raise VerificationError("malformed source_v_bounds entry")
        q = require_strict_int(entry.get("q"), "source_v_bounds.q", 3)
        smap: Dict[int, int] = {}
        for s in entry.get("sources", []):
            if not isinstance(s, dict):
                raise VerificationError("malformed source_v_bounds source")
            p = require_strict_int(s.get("p"), "source_v_bounds.p", 3)
            v = require_strict_int(s.get("v"), "source_v_bounds.v", 1)
            if p in smap:
                raise VerificationError(f"duplicate source {p} for target {q}")
            smap[p] = v
        source_v_bounds[q] = smap

    source_v2_bounds: Dict[int, int] = {}
    for entry in obj.get("source_v2_bounds", []):
        if not isinstance(entry, dict):
            raise VerificationError("malformed source_v2_bounds entry")
        p = require_strict_int(entry.get("p"), "source_v2_bounds.p", 3)
        v2 = require_strict_int(entry.get("v2"), "source_v2_bounds.v2", 0)
        if p in source_v2_bounds:
            raise VerificationError(f"duplicate source_v2_bounds for {p}")
        source_v2_bounds[p] = v2

    st = VerifierState(
        branched=branched,
        unbranched=unbranched,
        forbidden=forbidden,
        has_special=has_special,
        composites=tuple(composites_list),
        source_v_bounds=source_v_bounds,
        source_v2_bounds=source_v2_bounds,
    )
    _validate_state_invariants(st)
    return st


# ---------------- Sigma Deduction Verification ----------------

def apply_sigma_deduction(
    state: VerifierState,
    lemma: dict,
    verified_primes: Set[int],
) -> VerifierState:
    """Verify (p-1) * 2^v2 * prod(q_i^e_i) * c == p^(d+1) - 1 and update state."""
    if not isinstance(lemma, dict):
        raise VerificationError("deduction lemma must be dict")
    source_p = require_strict_int(lemma.get("source_p"), "deduction.source_p", 3)
    d = require_strict_int(lemma.get("d"), "deduction.d", 1)
    if source_p not in state.branched or state.branched[source_p].exp != d:
        raise VerificationError(f"deduction ({source_p}, {d}) does not match branched state")

    v2 = require_strict_int(lemma.get("v2", 0), "deduction.v2", 0)
    factors = lemma.get("factors")
    if not isinstance(factors, list):
        raise VerificationError("deduction missing factors list")

    comp_rem = require_strict_int(lemma.get("composite_rem", 1), "deduction.composite_rem", 1)
    if comp_rem % 2 == 0:
        raise VerificationError(f"composite_rem {comp_rem} must be odd")
    min_prime = require_strict_int(lemma.get("composite_min_prime", 3), "deduction.composite_min_prime", 3)
    if comp_rem > 1:
        verify_min_prime_bound(comp_rem, min_prime, lemma.get("composite_min_prime_cert"))

    prod = pow(2, v2) * comp_rem
    seen_q: Set[int] = set()
    new_unbranched = set(state.unbranched)
    new_v_bounds = {q: dict(smap) for q, smap in state.source_v_bounds.items()}
    new_v2_bounds = dict(state.source_v2_bounds)
    new_v2_bounds[source_p] = max(new_v2_bounds.get(source_p, 0), v2)

    for item in factors:
        if not isinstance(item, dict):
            raise VerificationError("malformed factor entry in deduction")
        q = require_strict_int(item.get("q"), "factor.q", 2)
        e = require_strict_int(item.get("e"), "factor.e", 1)
        if q == 2:
            raise VerificationError("factor 2 must be recorded in deduction.v2, not factors")
        if q in seen_q:
            raise VerificationError(f"duplicate factor {q} in sigma({source_p}^{d})")
        seen_q.add(q)
        verify_primality_certificate(q, item.get("cert"), verified_primes)
        prod *= pow(q, e)
        if q in state.forbidden:
            raise VerificationError(f"forbidden factor {q} found; close via FORBIDDEN_FACTOR leaf")
        if q not in state.branched:
            new_unbranched.add(q)
        smap = new_v_bounds.setdefault(q, {})
        smap[source_p] = max(smap.get(source_p, 0), e)

    if (source_p - 1) * prod != pow(source_p, d + 1) - 1:
        raise VerificationError(
            f"factor relation failed for sigma({source_p}^{d}): product mismatch"
        )

    new_composites = list(state.composites)
    if comp_rem > 1:
        new_composites.append(CompositeResidue(value=comp_rem, min_prime=min_prime))

    updated = VerifierState(
        branched=dict(state.branched),
        unbranched=frozenset(new_unbranched),
        forbidden=state.forbidden,
        has_special=state.has_special,
        composites=tuple(new_composites),
        source_v_bounds=new_v_bounds,
        source_v2_bounds=new_v2_bounds,
    )
    _validate_state_invariants(updated)
    return updated


# ---------------- Conditional / State LP Verification (Section 6.2) ----------------

def _lp_allowed_mod(p: int, e: int, forbidden: Set[int]) -> bool:
    for r in forbidden:
        if p % r == 0:
            continue
        if p % r == 1:
            if (e + 1) % r == 0:
                return False
        elif pow(p, e + 1, r) == 1:
            return False
    return True


def _find_next_allowed_exp(
    p: int,
    first: int,
    step: int,
    start_after: int,
    forbidden: Set[int],
    min_exp: int = 1,
    divisor_m: Optional[int] = None,
) -> Optional[int]:
    """Find smallest e >= max(min_exp, start_after+1) with e == first (mod step),
    optional divisor_m | (e + 1), and _lp_allowed_mod(p, e, forbidden) == True.
    Returns None if no such exponent can exist (provable modular obstruction).
    """
    # If standard branch d already forces a forbidden factor r | sigma(p^d),
    # then every e with (d+1) | (e+1) is forbidden.
    if divisor_m is not None and not _lp_allowed_mod(p, divisor_m - 1, forbidden):
        return None
    # For Euler odd exponents (first=1, step=4), e+1 is always divisible by 2,
    # so any forbidden prime dividing sigma(p^1) blocks all Euler exponents.
    if first == 1 and step == 4 and not _lp_allowed_mod(p, 1, forbidden):
        return None

    e = first + step * max(0, (max(start_after, min_exp - 1) - first) // step + 1)
    # Bounded by lcm of step, divisor_m, and forbidden prime orders; safe finite cap
    max_steps = 1
    if divisor_m is not None:
        max_steps = math.lcm(max_steps, divisor_m)
    for r in forbidden:
        if p % r != 0:
            max_steps = math.lcm(max_steps, r if p % r == 1 else (r - 1))
    # Cap search iterations conservatively (all legal residues appear within 1 full period)
    for _ in range(max_steps + 2):
        if e >= min_exp and (divisor_m is None or (e + 1) % divisor_m == 0):
            if _lp_allowed_mod(p, e, forbidden):
                return e
        e += step
    return None


def verify_conditional_lp_leaf(
    working: VerifierState,
    upper_bound_N: int,
    lp_witness: object,
    verified_primes: Set[int],
) -> None:
    """Reconstruct state-conditioned LP from scratch and verify rational dual bound > B.

    Fixes F-1 (guaranteed termination under modular obstruction) and F-2 (duplicate edges).
    """
    if not isinstance(lp_witness, dict):
        raise VerificationError("CONDITIONAL_LP missing lp_witness")
    limit = require_strict_int(lp_witness.get("limit"), "lp.limit", 5)
    cutoff = require_strict_int(lp_witness.get("cutoff"), "lp.cutoff", 2)
    raw_edges = lp_witness.get("edges", [])
    raw_weights = lp_witness.get("weights")
    if not isinstance(raw_edges, list) or not isinstance(raw_weights, list):
        raise VerificationError("lp_witness missing edges or weights")

    if lp_witness.get("omitted_primes"):
        raise VerificationError(
            f"conservative conditional LP forbids deleting explicit/induced primes: {lp_witness['omitted_primes']}"
        )

    forbidden = set(working.forbidden)
    forced_primes = set(working.branched.keys()) | set(working.unbranched)
    base_primes = set(odd_primes(limit)) - forbidden

    edges: List[Tuple[int, int, int, int]] = []
    seen_edges: Set[Tuple[int, int, int, int]] = set()
    for edge in raw_edges:
        if not isinstance(edge, dict):
            raise VerificationError("malformed LP edge")
        p = require_strict_int(edge.get("p"), "edge.p", 3)
        e = require_strict_int(edge.get("e"), "edge.e", 1)
        q = require_strict_int(edge.get("q"), "edge.q", 3)
        k = require_strict_int(edge.get("k"), "edge.k", 1)
        key = (p, e, q, k)
        if key in seen_edges:
            raise VerificationError(f"duplicate LP edge: {key}")
        seen_edges.add(key)
        verify_primality_certificate(q, edge.get("q_cert"), verified_primes)
        if q == p or q in forbidden:
            raise VerificationError(f"invalid LP edge target q={q} for p={p}")
        if sigma_prime_power(p, e) % pow(q, k) != 0:
            raise VerificationError(f"LP edge {q}^{k} does not divide sigma({p}^{e})")
        edges.append(key)
    edges.sort()

    explicit_primes = sorted(base_primes | forced_primes | {q for _, _, q, _ in edges})
    options: Dict[int, List[Tuple[int, int, bool, bool]]] = {}
    costs: List[int] = []
    abundances: List[int] = []
    specials: List[int] = []

    def add_opt(p: int, e: int, special: bool, exact: bool) -> None:
        loglo = log_bounds(p)[0]
        abhi = log_bounds(sigma_prime_power(p, e), pow(p, e))[1] if exact else log_bounds(p, p - 1)[1]
        idx = len(costs)
        costs.append(e * loglo)
        abundances.append(abhi)
        if special:
            specials.append(idx)
        options.setdefault(p, []).append((idx, e, special, exact))

    for p in explicit_primes:
        if p in working.branched:
            binfo = working.branched[p]
            if binfo.exact:
                is_sp = (binfo.exp % 2 == 1)
                if _lp_allowed_mod(p, binfo.exp, forbidden):
                    add_opt(p, binfo.exp, is_sp, True)
            else:
                d = binfo.exp
                for first, step, sp in ((2, 2, False), (1, 4, True)):
                    if sp and (working.has_special or p % 4 != 1):
                        continue
                    stop = cutoff if p in base_primes else 0
                    for e in range(first, stop + 1, step):
                        if e >= d and (e + 1) % (d + 1) == 0 and _lp_allowed_mod(p, e, forbidden):
                            add_opt(p, e, sp, True)
                    tail_e = _find_next_allowed_exp(
                        p, first, step, stop, forbidden, min_exp=d, divisor_m=d + 1
                    )
                    if tail_e is not None:
                        add_opt(p, tail_e, sp, False)
        else:
            lb_v = sum(working.source_v_bounds.get(p, {}).values())
            for first, step, sp in ((2, 2, False), (1, 4, True)):
                if sp and (working.has_special or p % 4 != 1):
                    continue
                stop = cutoff if p in base_primes else 0
                for e in range(first, stop + 1, step):
                    if e >= lb_v and _lp_allowed_mod(p, e, forbidden):
                        add_opt(p, e, sp, True)
                tail_e = _find_next_allowed_exp(
                    p, first, step, stop, forbidden, min_exp=max(1, lb_v), divisor_m=None
                )
                if tail_e is not None:
                    add_opt(p, tail_e, sp, False)

        if p in forced_primes and not options.get(p):
            # Forced prime has zero feasible exponents under modular/state constraints -> valid contradiction
            return

    tail = limit + 1
    tail_loglo = log_bounds(tail)[0]
    tail_abhi = log_bounds(tail, tail - 1)[1]
    tail_index = len(costs)
    costs.append(2 * tail_loglo * SCALE // tail_abhi)
    abundances.append(SCALE)
    if not working.has_special:
        tail_spec_index = len(costs)
        costs.append(tail_loglo)
        abundances.append(tail_abhi)
        specials.append(tail_spec_index)

    rows: List[Tuple[List[Tuple[int, int]], int]] = [
        ([(i, -h) for i, h in enumerate(abundances)], -log_bounds(2)[0]),
    ]
    if not working.has_special:
        rows.append(([(i, SCALE) for i in specials], SCALE))
    for p in explicit_primes:
        opts = options.get(p, [])
        rows.append(([(i, SCALE) for i, _, _, _ in opts], SCALE))
        if p in forced_primes:
            rows.append(([(i, -SCALE) for i, _, _, _ in opts], -SCALE))

    exact_lookup = {
        (p, e): (i, sp)
        for p, opts in options.items()
        for i, e, sp, exact in opts
        if exact
    }
    for p, e, q, k in edges:
        if (p, e) not in exact_lookup:
            continue
        if q not in options or not options[q]:
            raise VerificationError(f"LP implication target q={q} has no variables in model")
        i, is_sp = exact_lookup[(p, e)]
        terms = [
            (j, -SCALE)
            for j, f, q_sp, q_exact in options[q]
            if (not is_sp or not q_sp) and (not q_exact or f >= k)
        ]
        rows.append(([(i, SCALE)] + terms, 0))

    if len(raw_weights) != len(rows):
        raise VerificationError(
            f"conditional LP dual weight count {len(raw_weights)} != reconstructed rows {len(rows)}"
        )
    weights = [require_strict_int(w, f"lp.weights[{idx}]", 0) for idx, w in enumerate(raw_weights)]

    reduced = [c * LP_DYADIC for c in costs]
    rhs_term = 0
    for w, (terms, d_rhs) in zip(weights, rows):
        rhs_term -= w * d_rhs
        for idx, a_coeff in terms:
            reduced[idx] += w * a_coeff

    if reduced[tail_index] < 0:
        raise VerificationError("conditional LP unbounded tail has negative reduced cost")

    dual_bound = rhs_term + sum(min(0, rc) for idx, rc in enumerate(reduced) if idx != tail_index)
    target_hi = log_bounds(upper_bound_N)[1] * LP_DYADIC
    if dual_bound <= target_hi:
        raise VerificationError(
            f"conditional LP dual bound {dual_bound} <= target upper {target_hi}"
        )

def _disjoint_size_lower_log(working: VerifierState) -> int:
    """Scaled lower bound on log(known disjoint size) for roadblock budget."""
    total = 0
    for p, info in working.branched.items():
        total += info.exp * log_bounds(p)[0]
    chosen: List[int] = []
    for c in working.composites:
        val = c.value
        if any(val % p == 0 for p in working.branched):
            continue
        if any(math.gcd(val, d) > 1 for d in chosen):
            continue
        total += log_bounds(val)[0]
        chosen.append(val)
    return total


def _abundance_gap_lower(working: VerifierState) -> int:
    """Scaled lower bound on log(2) - log_abund_hi(known + all composites)."""
    abund_hi = 0
    for p, info in working.branched.items():
        if info.exact:
            abund_hi += log_bounds(sigma_prime_power(p, info.exp), pow(p, info.exp))[1]
        else:
            abund_hi += log_bounds(p, p - 1)[1]
    for c in working.composites:
        k = integer_factor_count_upper(c.value, c.min_prime)
        abund_hi += k * log_bounds(c.min_prime, c.min_prime - 1)[1]
    return log_bounds(2)[0] - abund_hi


def verify_roadblock_witness(
    working: VerifierState,
    upper_bound_N: int,
    rb_witness: object,
) -> int:
    """Verify strict roadblock lower bound L_b(mu) > M_hi; returns certified boundary b."""
    if not isinstance(rb_witness, dict):
        raise VerificationError("CIRCULAR_BRANCH_SPLIT missing roadblock_witness")
    boundary = require_strict_int(rb_witness.get("boundary"), "roadblock.boundary", 3)
    table_limit = require_strict_int(rb_witness.get("table_limit"), "roadblock.table_limit", boundary)
    mu_num = require_strict_int(rb_witness.get("mu_num"), "roadblock.mu_num", 0)
    mu_den = require_strict_int(rb_witness.get("mu_den"), "roadblock.mu_den", 1)

    gap_lo = _abundance_gap_lower(working)
    if gap_lo <= 0:
        raise VerificationError(f"roadblock abundance gap <= 0 ({gap_lo}); node unresolved")
    budget_hi = log_bounds(upper_bound_N)[1] - _disjoint_size_lower_log(working)
    if budget_hi < 0:
        raise VerificationError("negative remaining size budget; close via SIZE_EXCEEDS_BOUND")

    oracle = RoadblockDual(
        boundary=boundary,
        table_limit=table_limit,
        forbidden=working.forbidden,
        expanded=working.branched.keys(),
        special_used=working.has_special,
    )
    mu = Fraction(mu_num, mu_den)
    if mu > oracle.tail_cap:
        raise VerificationError(f"roadblock multiplier {mu} exceeds tail_cap {oracle.tail_cap}")
    bound_lo, _ = oracle.evaluate(gap_lo, mu)
    if bound_lo <= budget_hi:
        raise VerificationError(
            f"roadblock dual bound {bound_lo} <= remaining budget {budget_hi}"
        )
    return boundary


# ---------------- Leaf & Split Node Verification ----------------

def verify_leaf_node(
    expected_state: VerifierState,
    node: dict,
    upper_bound_N: int,
    verified_primes: Set[int],
) -> str:
    """Verify a LEAF node against an externally derived expected_state."""
    if not isinstance(node, dict) or node.get("kind") != "LEAF":
        raise VerificationError("expected LEAF node")
    if "witness" not in node or not isinstance(node["witness"], dict):
        raise VerificationError("LEAF node missing witness (bare PROVEN rejected)")
    if "state" in node and parse_state_dict(node["state"]) != expected_state:
        raise VerificationError("LEAF declared state does not match parent-derived state")

    witness = node["witness"]
    reason = witness.get("reason")
    working = expected_state
    for lemma in witness.get("deductions", []):
        working = apply_sigma_deduction(working, lemma, verified_primes)

    if reason == "FINITE_QUOTIENT_CYCLOTOMIC":
        # Root-only exact-integer certificate, re-enumerated by an independent
        # checker. All theorem parameters come from the parent-derived state.
        from FiniteQuotientClosure2400 import finite_quotient_certificate
        src_p = require_strict_int(witness.get("source_p"), "finite_quotient.source_p", 3)
        d = require_strict_int(witness.get("d"), "finite_quotient.d", 2)
        if (witness.get("deductions") or set(working.branched) != {src_p}
                or working.branched[src_p].exp != d
                or working.branched[src_p].exact
                or working.unbranched or working.composites
                or working.has_special or working.source_v_bounds
                or working.source_v2_bounds):
            raise VerificationError("finite quotient certificate requires an unmodified non-exact root")
        try:
            finite_quotient_certificate(src_p, d, tuple(sorted(working.forbidden)),
                                        upper_bound_N)
        except ValueError as exc:
            raise VerificationError(f"FINITE_QUOTIENT_CYCLOTOMIC rejected: {exc}") from exc
        return "LEAF_ACCEPTED"

    if reason == "CYCLOTOMIC_EULER_PRIMORIAL":
        from CyclotomicPrimorialClosure2400 import cyclotomic_primorial_certificate
        src_p = require_strict_int(witness.get("source_p"), "cyclotomic_primorial.source_p", 3)
        d = require_strict_int(witness.get("d"), "cyclotomic_primorial.d", 2)
        if (witness.get("deductions") or set(working.branched) != {src_p}
                or working.branched[src_p].exp != d
                or working.branched[src_p].exact
                or working.unbranched or working.composites
                or working.has_special or working.source_v_bounds
                or working.source_v2_bounds):
            raise VerificationError("cyclotomic primorial certificate requires an unmodified non-exact root")
        result = cyclotomic_primorial_certificate(
            src_p, d, tuple(sorted(working.forbidden)), upper_bound_N
        )
        if result is None:
            raise VerificationError("CYCLOTOMIC_EULER_PRIMORIAL inequality did not exclude root")
        return "LEAF_ACCEPTED"

    if reason == "SIGMA_DIVISOR_SIZE":
        # For any branch d representing the true exponent e, either e=d
        # or d+1 divides e+1. Thus sigma(p^d) | sigma(p^e) | 2N.
        # Its odd part divides N, and gcd(p, sigma(p^d)) = 1.
        # Therefore p^d * odd(sigma(p^d)) divides every possible N.
        src_p = require_strict_int(witness.get("source_p"), "sigma_size.source_p", 3)
        d = require_strict_int(witness.get("d"), "sigma_size.d", 1)
        if src_p not in working.branched or working.branched[src_p].exp != d:
            raise VerificationError("SIGMA_DIVISOR_SIZE source_p/d mismatch")
        # A cheap exact bit-length witness avoids allocating enormous
        # powers for maliciously oversized exponents.
        if (src_p.bit_length() - 1) * d > upper_bound_N.bit_length():
            return "LEAF_ACCEPTED"
        sigma = sigma_prime_power(src_p, d)
        odd_sigma = sigma // (sigma & -sigma)
        forced_divisor = pow(src_p, d) * odd_sigma
        if forced_divisor <= upper_bound_N:
            raise VerificationError(
                f"SIGMA_DIVISOR_SIZE failed for p={src_p}, d={d}"
            )
        return "LEAF_ACCEPTED"

    if reason == "SIZE_EXCEEDS_BOUND":
        min_size = working.min_size_lower_bound()
        if "claimed_min_size" in witness:
            claimed = require_strict_int(witness["claimed_min_size"], "claimed_min_size", 1)
            if claimed != min_size:
                raise VerificationError(f"claimed_min_size={claimed} != recomputed {min_size}")
        if min_size <= upper_bound_N:
            raise VerificationError(f"SIZE_EXCEEDS_BOUND failed: {min_size} <= {upper_bound_N}")
        return "LEAF_ACCEPTED"

    if reason == "FORBIDDEN_FACTOR":
        lemma = witness.get("forbidden_lemma")
        if not isinstance(lemma, dict):
            raise VerificationError("FORBIDDEN_FACTOR missing forbidden_lemma")
        src_p = require_strict_int(lemma.get("source_p"), "forbidden_lemma.source_p", 3)
        d = require_strict_int(lemma.get("d"), "forbidden_lemma.d", 1)
        q = require_strict_int(lemma.get("forbidden_q"), "forbidden_lemma.forbidden_q", 3)
        if src_p not in working.branched or working.branched[src_p].exp != d:
            raise VerificationError("forbidden_lemma source_p/d mismatch")
        if q not in working.forbidden:
            raise VerificationError(f"{q} is not in forbidden set")
        verify_primality_certificate(q, lemma.get("cert"), verified_primes)
        if sigma_prime_power(src_p, d) % q != 0:
            raise VerificationError(f"{q} does not divide sigma({src_p}^{d})")
        return "LEAF_ACCEPTED"

    if reason == "EXACT_QUOTA_EXCEEDED":
        q = require_strict_int(witness.get("target_q"), "target_q", 3)
        if q not in working.branched or not working.branched[q].exact:
            raise VerificationError(f"EXACT_QUOTA_EXCEEDED target {q} is not exact-branched")
        total_v = sum(working.source_v_bounds.get(q, {}).values())
        if total_v <= working.branched[q].exp:
            raise VerificationError(
                f"EXACT_QUOTA_EXCEEDED failed for {q}: sum v_q={total_v} <= exact exp {working.branched[q].exp}"
            )
        return "LEAF_ACCEPTED"

    if reason == "V2_EXCEEDS_ONE":
        total_v2 = sum(working.source_v2_bounds.values())
        if total_v2 <= 1:
            raise VerificationError(f"V2_EXCEEDS_ONE failed: distinct-source v2 sum={total_v2} <= 1")
        return "LEAF_ACCEPTED"

    if reason == "ABUNDANCE_EXCEEDS_TWO":
        if not working.min_abundance_exceeds_two():
            raise VerificationError("ABUNDANCE_EXCEEDS_TWO failed: rational product <= 2")
        return "LEAF_ACCEPTED"

    if reason == "CONDITIONAL_LP":
        verify_conditional_lp_leaf(working, upper_bound_N, witness.get("lp_witness"), verified_primes)
        return "LEAF_ACCEPTED"

    raise UnsupportedRuleError(f"unsupported or unimplemented LEAF reason: {reason!r}")


def verify_split_node(
    expected_state: VerifierState,
    node: dict,
    upper_bound_N: int,
    circ_order: Tuple[int, ...],
    verified_primes: Set[int],
) -> List[VerifierState]:
    """Verify a SPLIT node and return the ordered list of derived child VerifierStates."""
    if not isinstance(node, dict) or node.get("kind") != "SPLIT":
        raise VerificationError("expected SPLIT node")
    if "split_rule" not in node or "children" not in node:
        raise VerificationError("SPLIT node missing split_rule or children")
    if "state" in node and parse_state_dict(node["state"]) != expected_state:
        raise VerificationError("SPLIT declared state does not match parent-derived state")

    working = expected_state
    for lemma in node.get("deductions", []):
        working = apply_sigma_deduction(working, lemma, verified_primes)

    rule = node["split_rule"]
    if not isinstance(rule, dict):
        raise VerificationError("split_rule must be dict")
    rule_type = rule.get("type")
    children_spec = node["children"]
    if not isinstance(children_spec, list) or not children_spec:
        raise VerificationError("SPLIT node must have non-empty children list")

    if rule_type == "UNBRANCHED_EXPONENT_EXHAUSTION":
        p = require_strict_int(rule.get("branch_prime"), "branch_prime", 3)
        if p not in working.unbranched:
            raise VerificationError(f"branch_prime {p} not in working.unbranched")
        verify_primality_certificate(p, rule.get("prime_cert"), verified_primes)

        cutoff_ge = require_strict_int(rule.get("size_cutoff_ge"), "size_cutoff_ge", 2)
        if working.min_size_lower_bound(override_min_exp=(p, cutoff_ge)) <= upper_bound_N:
            raise VerificationError(
                f"size_cutoff_ge={cutoff_ge} for p={p} does not strictly exceed {upper_bound_N}"
            )

        can_be_special = (p % 4 == 1) and (not working.has_special)
        required: Set[int] = set()
        for e in range(working._even_min_exp(p), cutoff_ge, 2):
            required.add(e)
        if can_be_special:
            for e in range(working._odd_euler_min_exp(p), cutoff_ge, 4):
                required.add(e)

        covered: Set[int] = set()
        derived_children: List[VerifierState] = []
        for entry in children_spec:
            if not isinstance(entry, dict) or "edge" not in entry:
                raise VerificationError("SPLIT child missing explicit edge descriptor")
            edge = entry["edge"]
            if not isinstance(edge, dict):
                raise VerificationError("malformed edge descriptor")
            c_exp = require_strict_int(edge.get("exp"), "edge.exp", 1)
            c_exact = require_strict_bool(edge.get("exact"), "edge.exact")
            new_branched = dict(working.branched)
            new_branched[p] = BranchEntry(exp=c_exp, exact=c_exact)
            child_state = VerifierState(
                branched=new_branched,
                unbranched=working.unbranched - {p},
                forbidden=working.forbidden,
                has_special=working.has_special or (c_exact and c_exp % 2 == 1),
                composites=working.composites,
                source_v_bounds=working.source_v_bounds,
                source_v2_bounds=working.source_v2_bounds,
            )
            _validate_state_invariants(child_state)
            if "state" in entry and parse_state_dict(entry["state"]) != child_state:
                raise VerificationError(f"child state mismatch on exponent edge ({p}, {c_exp}, {c_exact})")

            if c_exact:
                covered.add(c_exp)
            else:
                for e in required:
                    if e >= c_exp and (e + 1) % (c_exp + 1) == 0:
                        covered.add(e)
            derived_children.append(child_state)

        missing = sorted(required - covered)
        if missing:
            raise VerificationError(f"incomplete exponent split for p={p}; missing {missing[:10]}")
        return derived_children

    if rule_type == "CIRCULAR_BRANCH_SPLIT":
        if working.unbranched:
            raise VerificationError("CIRCULAR_BRANCH_SPLIT requires empty unbranched set")
        boundary = verify_roadblock_witness(working, upper_bound_N, rule.get("roadblock_witness"))

        expected_candidates: List[int] = []
        seen_c: Set[int] = set()
        for q in (*circ_order, *odd_primes(boundary - 1)):
            if q >= boundary or q in seen_c:
                continue
            seen_c.add(q)
            if q in working.forbidden or q in working.branched:
                continue
            expected_candidates.append(q)

        if len(children_spec) != len(expected_candidates):
            raise VerificationError(
                f"CIRCULAR_BRANCH_SPLIT child count {len(children_spec)} != expected {len(expected_candidates)}"
            )

        derived_children = []
        running_forbidden = set(working.forbidden)
        for idx, (entry, expected_q) in enumerate(zip(children_spec, expected_candidates)):
            if not isinstance(entry, dict) or "edge" not in entry:
                raise VerificationError(f"circular child {idx} missing edge descriptor")
            edge = entry["edge"]
            if not isinstance(edge, dict):
                raise VerificationError(f"malformed circular edge at index {idx}")
            q = require_strict_int(edge.get("circ_prime"), "edge.circ_prime", 3)
            if q != expected_q:
                raise VerificationError(
                    f"circular order mismatch at index {idx}: got {q}, expected {expected_q}"
                )
            verify_primality_certificate(q, {"method": "TRIAL_DIV", "max_divisor": math.isqrt(q)}, verified_primes)
            child_state = VerifierState(
                branched=dict(working.branched),
                unbranched=frozenset({q}),
                forbidden=frozenset(running_forbidden),
                has_special=working.has_special,
                composites=working.composites,
                source_v_bounds=working.source_v_bounds,
                source_v2_bounds=working.source_v2_bounds,
            )
            _validate_state_invariants(child_state)
            if "state" in entry and parse_state_dict(entry["state"]) != child_state:
                raise VerificationError(f"circular child state mismatch for q={q} (check forbidden prefix)")
            derived_children.append(child_state)
            running_forbidden.add(q)
        return derived_children

    raise UnsupportedRuleError(f"unsupported or unimplemented split_rule type: {rule_type!r}")


# ---------------- Full Tree & Global Partition Closure ----------------

def verify_root_task_bundle(pin: RootTaskPin, proof_bundle: object) -> dict:
    """Verify a complete proof DAG from an externally pinned RootTaskPin."""
    if not isinstance(proof_bundle, dict):
        raise VerificationError("proof_bundle must be a JSON object")
    if "nodes" not in proof_bundle or not isinstance(proof_bundle["nodes"], list):
        raise VerificationError("proof_bundle missing nodes list (bare PROVEN rejected)")

    verified_primes: Set[int] = set()
    root_state = pin.build_initial_state(verified_primes)
    root_hash = root_state.state_hash()

    # If the bundle optionally includes metadata, reject any disagreement with external pin
    if "upper_bound_N" in proof_bundle:
        declared_B = require_strict_int(proof_bundle["upper_bound_N"], "bundle.upper_bound_N", 1)
        if declared_B != pin.upper_bound_N:
            raise VerificationError(
                f"bundle upper_bound_N={declared_B} != externally pinned {pin.upper_bound_N}"
            )
    if "root_state" in proof_bundle:
        if parse_state_dict(proof_bundle["root_state"]) != root_state:
            raise VerificationError("bundle root_state does not match externally pinned initial state")

    node_by_hash: Dict[str, dict] = {}
    for node in proof_bundle["nodes"]:
        if not isinstance(node, dict) or "state" not in node:
            raise VerificationError("node missing state")
        h = parse_state_dict(node["state"]).state_hash()
        if h in node_by_hash:
            raise VerificationError(f"duplicate node for state hash {h}")
        node_by_hash[h] = node

    closed: Set[str] = set()
    visiting: Set[str] = set()
    stats = {"splits_verified": 0, "leaves_verified": 0}

    def dfs_verify(expected_state: VerifierState) -> None:
        h = expected_state.state_hash()
        if h in closed:
            return
        if h in visiting:
            raise VerificationError(f"cycle detected at state {h}")
        if h not in node_by_hash:
            raise VerificationError(f"missing proof node for required state {h}")

        visiting.add(h)
        node = node_by_hash[h]
        kind = node.get("kind")
        if kind == "LEAF":
            status = verify_leaf_node(expected_state, node, pin.upper_bound_N, verified_primes)
            if status != "LEAF_ACCEPTED":
                raise VerificationError(f"leaf rejected at {h}")
            stats["leaves_verified"] += 1
        elif kind == "SPLIT":
            children = verify_split_node(
                expected_state, node, pin.upper_bound_N, pin.circ_order, verified_primes
            )
            stats["splits_verified"] += 1
            for child_st in children:
                dfs_verify(child_st)
        else:
            raise UnsupportedRuleError(f"unknown node kind: {kind!r}")

        visiting.remove(h)
        closed.add(h)

    dfs_verify(root_state)
    return {
        "status": "TREE_ACCEPTED",
        "root_hash": root_hash,
        "splits_verified": stats["splits_verified"],
        "leaves_verified": stats["leaves_verified"],
        "verified_primes_count": len(verified_primes),
    }


def verify_terminal_and_manifest(
    terminal_cert_path: Path,
    expected_root_set: Tuple[int, ...],
    manifest_path: Optional[Path] = None,
) -> dict:
    """Independently verify a terminal coprime certificate and optional 8-root manifest."""
    raw = terminal_cert_path.read_bytes()
    text = (gzip.decompress(raw) if terminal_cert_path.suffix == ".gz" else raw).decode("utf-8")
    cert = strict_json_loads(text)
    if not isinstance(cert, dict):
        raise VerificationError("terminal certificate must be JSON object")
    if tuple(sorted(cert.get("roots", ()))) != tuple(sorted(expected_root_set)):
        raise VerificationError(
            f"terminal certificate roots {cert.get('roots')} != expected {expected_root_set}"
        )
    if not TerminalCertificate.verify(cert):
        raise VerificationError("terminal coprime certificate failed 10^2400 bound")

    task_count = None
    if manifest_path is not None:
        manifest = strict_json_loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise VerificationError("manifest must be JSON object")
        if tuple(sorted(manifest.get("root_order", ()))) != tuple(sorted(expected_root_set)):
            raise VerificationError("manifest root_order does not match terminal certificate root set")
        task_count = VerifyRootExponentCoverage.verify_manifest(manifest)

    return {
        "status": "TERMINAL_AND_PARTITION_ACCEPTED",
        "roots": tuple(sorted(expected_root_set)),
        "terminal_sha256": sha256_hex(raw),
        "manifest_tasks": task_count,
    }
