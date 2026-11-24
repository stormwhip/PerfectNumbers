"""Exact bounded search for odd perfect numbers in a root/exponent case."""

import argparse
from bisect import bisect_right
from collections import Counter
from contextlib import nullcontext
from functools import lru_cache
from math import gcd, isqrt
from pathlib import Path
from time import perf_counter
import json


ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
PILOT = [(19, 742), (7, 1128), (11, 772), (31, 642), (13, 858), (3, 1302), (5, 676)]
THRESHOLDS = (25, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000)
ROUGH = 5001


@lru_cache(maxsize=4)
def primes_up_to(limit):
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00' * ((limit - p*p) // p + 1)
    return tuple(p for p in range(3, limit + 1, 2) if sieve[p])


def floor_log(n, base):
    low, high = 0, n.bit_length() // (base.bit_length() - 1) + 1
    while high - low > 1:
        mid = (low + high) // 2
        if base ** mid <= n:
            low = mid
        else:
            high = mid
    return low


@lru_cache(maxsize=8192)
def remove_prime(n, p):
    exponent = 0
    while n % p == 0:
        exponent += 1
        n //= p
    return exponent, n


def sigma(p, f):
    return (p ** (f + 1) - 1) // (p - 1)


class Search:
    def __init__(self, p, e, digits, max_depth, max_nodes, seconds, strategy, on_uncovered=None):
        self.p, self.e = p, e
        self.digits = digits
        self.bound = 10 ** digits
        self.max_depth, self.max_nodes = max_depth, max_nodes
        self.seconds, self.strategy = seconds, strategy
        self.fixed_forbidden = frozenset(ROOTS[:ROOTS.index(p)])
        self.primes = primes_up_to(20000)
        self.trial = self.primes[:bisect_right(self.primes, ROUGH - 1)]
        self.tail = {}
        self.stats = Counter()
        self.depth_stats = Counter()
        self.sample_open = []
        self.first_split = None
        self.on_uncovered = on_uncovered

    def tail_table(self, threshold, euler_used):
        key = threshold, euler_used
        if key in self.tail:
            return self.tail[key]
        costs, nums, dens = [1], [1], [1]
        product = 1
        for r in self.primes[bisect_right(self.primes, threshold):]:
            if r in self.fixed_forbidden or r == self.p:
                continue
            product *= r
            cost = product * product if euler_used else product * product // r
            if cost > self.bound:
                break
            costs.append(cost)
            nums.append(nums[-1] * r)
            dens.append(dens[-1] * (r - 1))
        else:
            raise ValueError('Prime table too short for the target bound')
        self.tail[key] = costs, nums, dens
        return self.tail[key]

    def uncovered(self, reason, exact, depth, forbidden, threshold=None):
        self.stats[reason] += 1
        state = {'reason': reason, 'root': self.p, 'exponent': self.e,
                 'digits': self.digits,
                 'exact': list(exact.items()), 'depth': depth,
                 'absent': sorted(forbidden), 'threshold': threshold}
        if len(self.sample_open) < 5:
            self.sample_open.append(state)
        if self.on_uncovered is not None:
            self.on_uncovered(state)

    def visit(self, exact, value, divisor_sum, euler_used, forbidden, depth):
        if self.stats['nodes'] >= self.max_nodes or perf_counter() >= self.deadline:
            self.uncovered('budget', exact, depth, forbidden)
            return False
        self.stats['nodes'] += 1
        self.depth_stats[depth] += 1
        if value > self.bound:
            self.stats['size'] += 1
            return True
        if divisor_sum > 2 * value:
            self.stats['abundancy_lower'] += 1
            return True

        # For R=N/value, I(R)=2*value/divisor_sum in lowest terms demands
        # divisor_sum/gcd(divisor_sum, 2*value) | R and gcd(value, R)=1.
        forced = divisor_sum // gcd(divisor_sum, 2 * value)
        if gcd(forced, value) > 1 or any(forced % r == 0 for r in forbidden):
            self.stats['divisibility'] += 1
            return True
        if value * forced > self.bound:
            self.stats['size'] += 1
            return True

        euler_one_only = False
        if self.p in (3, 5):
            assigned_valuation, _ = remove_prime(divisor_sum, self.p)
            need = self.e - assigned_valuation
            if need:
                source = next(r for r in self.primes if r % self.p == 1
                              and r not in exact and r not in forbidden)
                price = source ** (self.p - 1)
                available = self.bound // value
                if euler_used and price ** need > available:
                    self.stats['valuation_size'] += 1
                    return True
                # If the Euler exponent is at least five, its size is at
                # least p^(5s-5) for s units of root valuation (see README).
                if not euler_used and price >= self.p ** 5:
                    euler_one_only = self.p ** (5 * (need - 1)) > available

        rough = forced
        lower_num, lower_den = divisor_sum, value
        upper_num, upper_den = divisor_sum, value
        forced_primes = []
        # Pay for parity rounding of known factors, saving at most one premium.
        rounded, max_saving = 1, 1
        for r in self.trial:
            if rough == 1:
                break
            if rough % r:
                continue
            c, rough = remove_prime(rough, r)
            can_be_euler = not euler_used and r % 4 == 1
            f_even = c + c % 2
            f_min = (c + ((1 - c) % 4)) if can_be_euler else f_even
            f_min = min(f_min, f_even)
            if c % 2:
                rounded *= r
                if f_min == c:
                    max_saving = max(max_saving, r)
            lower_num *= sigma(r, f_min)
            lower_den *= r ** f_min
            upper_num *= r
            upper_den *= r - 1
            forced_primes.append((r, c))
        paid = value * forced * (rounded // max_saving)
        if paid > self.bound:
            self.stats['size_parity'] += 1
            return True
        if lower_num > 2 * lower_den:
            self.stats['abundancy_lower'] += 1
            return True
        # When the forced cofactor is rough, its distinct primes are at least
        # ROUGH and their count is at most floor(log_ROUGH(rough)).
        count = floor_log(rough, ROUGH)
        upper_num *= ROUGH ** count
        upper_den *= (ROUGH - 1) ** count
        threshold = None
        budget = self.bound // paid
        if upper_num < 2 * upper_den:
            for t in THRESHOLDS:
                costs, nums, dens = self.tail_table(t, euler_used)
                k = bisect_right(costs, budget) - 1
                if upper_num * nums[k] < 2 * upper_den * dens[k]:
                    threshold = t
                    break

        if threshold == THRESHOLDS[0]:
            first_threshold = 0
        else:
            first_threshold = THRESHOLDS[THRESHOLDS.index(threshold) - 1] if threshold else 0
        # Any proof that another prime <= threshold is needed allows an
        # ordered split on the least new prime. Smaller thresholds tested
        # above may have failed and do not exclude any candidate.
        new_primes = ([] if threshold is None else
                      [r for r in self.trial[:bisect_right(self.trial, threshold)]
                       if r not in forbidden and r not in exact and forced % r])
        if threshold is not None and not new_primes:
            self.stats['abundancy_upper'] += 1
            return True
        if forced_primes and (self.strategy == 'forced-first' or not new_primes):
            pivots = [forced_primes[-1]]
            acquire = False
        else:
            pivots = [(r, 1) for r in new_primes]
            acquire = True
        if depth == 0:
            self.first_split = {'threshold': threshold, 'previous_threshold': first_threshold,
                                'candidates': len(new_primes), 'pivot_primes': len(pivots),
                                'mode': 'new-prime' if acquire else 'forced-prime',
                                'euler_one_only': euler_one_only}
        if not pivots:
            self.uncovered('no_pivot', exact, depth, forbidden, threshold)
            return False
        if depth == self.max_depth:
            self.uncovered('depth', exact, depth, forbidden, threshold)
            return False

        absent = forbidden
        complete = True
        for r, c in pivots:
            known_exponent, other_forced = remove_prime(forced, r)
            assert known_exponent == (0 if acquire else c)
            limit = floor_log(self.bound // (value * other_forced), r)
            power = r ** (c - 1)
            may_be_euler = not euler_used and r % 4 == 1
            for f in range(c, limit + 1):
                power *= r
                is_euler = bool(f % 2)
                if is_euler and not (may_be_euler and f % 4 == 1):
                    continue
                if is_euler and euler_one_only and f != 1:
                    self.stats['skipped_euler_exponents'] += 1
                    continue
                if self.stats['nodes'] >= self.max_nodes or perf_counter() >= self.deadline:
                    self.uncovered('budget', exact, depth, absent, threshold)
                    return False
                ok = self.visit(exact | {r: f}, value * power,
                                divisor_sum * ((power * r - 1) // (r - 1)),
                                euler_used or is_euler, absent, depth + 1)
                complete = complete and ok
            if acquire:
                absent = absent | {r}
        return complete

    def run(self, state=None):
        start = perf_counter()
        self.deadline = start + self.seconds
        assert 0 < self.e and (self.e % 2 == 0 or self.p % 4 == self.e % 4 == 1)
        exact = dict(state['exact']) if state else {self.p: self.e}
        if state and state['digits'] != self.digits:
            raise ValueError('Saved state uses a different size bound')
        forbidden = self.fixed_forbidden | (frozenset(state['absent']) if state else frozenset())
        if exact.get(self.p) != self.e or forbidden.intersection(exact):
            raise ValueError('Inconsistent saved state')
        value = divisor_sum = 1
        euler_count = 0
        for r, f in exact.items():
            if r not in self.primes or f <= 0 or (f % 2 and not (r % 4 == f % 4 == 1)):
                raise ValueError('Invalid exact component in saved state')
            euler_count += f % 2
            value *= r ** f
            divisor_sum *= sigma(r, f)
        if euler_count > 1:
            raise ValueError('Multiple Euler components in saved state')
        complete = self.visit(exact, value, divisor_sum, bool(euler_count), forbidden, 0)
        return {'root': self.p, 'exponent': self.e, 'complete': complete,
                'wall_seconds': round(perf_counter() - start, 4), 'counts': dict(self.stats),
                'by_depth': dict(self.depth_stats), 'first_split': self.first_split,
                'sample_open': self.sample_open}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', nargs=2, type=int, action='append', metavar=('P', 'E'))
    parser.add_argument('--digits', type=int, default=2400)
    parser.add_argument('--depth', type=int, default=2)
    parser.add_argument('--nodes', type=int, default=100000)
    parser.add_argument('--seconds', type=float, default=10, help='wall time per case')
    parser.add_argument('--strategy', choices=('reverse-first', 'forced-first'), default='reverse-first')
    parser.add_argument('--frontier', type=Path, help='write unresolved branches as JSON lines')
    parser.add_argument('--states', type=Path, help='read JSON lines from a previous --frontier output')
    parser.add_argument('--partition', nargs=2, type=int, metavar=('INDEX', 'COUNT'), default=(0, 1))
    args = parser.parse_args()
    if min(args.digits, args.nodes, args.seconds) <= 0 or args.depth < 0:
        parser.error('invalid search limit')
    if args.case and args.states:
        parser.error('--case and --states are mutually exclusive')
    index, count = args.partition
    if not 0 <= index < count:
        parser.error('--partition requires 0 <= INDEX < COUNT')
    if args.states and args.frontier and args.states.resolve() == args.frontier.resolve():
        parser.error('input and output frontier files must differ')
    state_input = args.states.open(encoding='utf-8-sig') if args.states else nullcontext()
    state_output = args.frontier.open('x', encoding='utf-8') if args.frontier else nullcontext()
    with state_input as rows, state_output as frontier:
        jobs = ((state['root'], state['exponent'], state) for state in map(json.loads, rows)) if rows else (
            (p, e, None) for p, e in args.case or PILOT)

        def save(state):
            print(json.dumps(state), file=frontier, flush=True)

        for job, (p, e, state) in enumerate(jobs):
            if job % count != index:
                continue
            search = Search(p, e, args.digits, args.depth, args.nodes, args.seconds,
                            args.strategy, save if frontier else None)
            print(json.dumps(search.run(state)), flush=True)


if __name__ == '__main__':
    main()
