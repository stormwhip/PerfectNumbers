// Sources/Cpp/SingleFlightFactCache.hpp
// Thread-safe sharded single-flight cache with immutable shared_ptr values.
// Guarantees:
// 1. Exact key equality (no hash-only aliasing).
// 2. Concurrent misses for the same key coalesce into a single computation.
// 3. Eviction never invalidates readers holding shared_ptr<const Value>.
#pragma once

#include <array>
#include <atomic>
#include <condition_variable>
#include <cstddef>
#include <functional>
#include <memory>
#include <mutex>
#include <string>
#include <unordered_map>

namespace opn_v21 {

template <typename Value>
class SingleFlightCache {
public:
    static constexpr size_t kNumShards = 64;

    explicit SingleFlightCache(size_t max_entries_per_shard = 8192)
        : max_per_shard_(max_entries_per_shard) {}

    template <typename ComputeFn>
    std::shared_ptr<const Value> get_or_compute(const std::string& key, ComputeFn&& compute) {
        Shard& shard = shards_[std::hash<std::string>{}(key) & (kNumShards - 1)];
        std::shared_ptr<InFlight> flight;
        bool is_leader = false;

        {
            std::unique_lock<std::mutex> lk(shard.mtx);
            auto it = shard.entries.find(key);
            if (it != shard.entries.end()) {
                hits_.fetch_add(1, std::memory_order_relaxed);
                return it->second;
            }
            auto fit = shard.in_flight.find(key);
            if (fit != shard.in_flight.end()) {
                flight = fit->second;
                coalesced_.fetch_add(1, std::memory_order_relaxed);
            } else {
                flight = std::make_shared<InFlight>();
                shard.in_flight.emplace(key, flight);
                is_leader = true;
                misses_.fetch_add(1, std::memory_order_relaxed);
            }
        }

        if (!is_leader) {
            std::unique_lock<std::mutex> flk(flight->mtx);
            flight->cv.wait(flk, [&] { return flight->done; });
            if (flight->eptr) std::rethrow_exception(flight->eptr);
            return flight->result;
        }

        std::shared_ptr<const Value> computed;
        std::exception_ptr eptr;
        try {
            computed = std::make_shared<const Value>(compute());
        } catch (...) {
            eptr = std::current_exception();
        }

        {
            std::lock_guard<std::mutex> lk(shard.mtx);
            shard.in_flight.erase(key);
            if (!eptr) {
                if (shard.entries.size() >= max_per_shard_) {
                    shard.entries.clear(); // Safe: existing readers hold shared_ptr<const Value>
                }
                shard.entries.emplace(key, computed);
            }
        }
        {
            std::lock_guard<std::mutex> flk(flight->mtx);
            flight->result = computed;
            flight->eptr = eptr;
            flight->done = true;
        }
        flight->cv.notify_all();
        if (eptr) std::rethrow_exception(eptr);
        return computed;
    }

    uint64_t hits() const { return hits_.load(std::memory_order_relaxed); }
    uint64_t misses() const { return misses_.load(std::memory_order_relaxed); }
    uint64_t coalesced() const { return coalesced_.load(std::memory_order_relaxed); }

private:
    struct InFlight {
        std::mutex mtx;
        std::condition_variable cv;
        bool done = false;
        std::shared_ptr<const Value> result;
        std::exception_ptr eptr;
    };

    struct Shard {
        std::mutex mtx;
        std::unordered_map<std::string, std::shared_ptr<const Value>> entries;
        std::unordered_map<std::string, std::shared_ptr<InFlight>> in_flight;
    };

    size_t max_per_shard_;
    std::array<Shard, kNumShards> shards_;
    std::atomic<uint64_t> hits_{0};
    std::atomic<uint64_t> misses_{0};
    std::atomic<uint64_t> coalesced_{0};
};

} // namespace opn_v21
