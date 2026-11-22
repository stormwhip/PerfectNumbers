#include "SingleFlightFactCache.hpp"
#include <atomic>
#include <chrono>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>

int main()
{
    opn_v21::SingleFlightCache<int> cache(2);
    std::atomic<int> computes{0};
    std::vector<std::thread> threads;
    for(int i=0;i<16;i++)
    {
        threads.emplace_back([&]()
        {
            auto x=cache.get_or_compute("same-key", [&]()
            {
                ++computes;
                std::this_thread::sleep_for(std::chrono::milliseconds(20));
                return 42;
            });
            if(*x!=42)
                throw std::runtime_error("unexpected cached value");
        });
    }
    for(auto& t:threads)
        t.join();
    if(computes.load()!=1)
        throw std::runtime_error("single-flight work was repeated");
    std::cout<<"SingleFlightFactCacheTests: ALL TESTS PASSED\n";
}
