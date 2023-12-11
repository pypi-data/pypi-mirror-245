#ifndef RANDOM_BUFFER_H
#define RANDOM_BUFFER_H

#include "utility.hpp"

#include <vector>
#include <cstddef>


class RandomBuffer {
public:
    explicit RandomBuffer(size_t size)
        : buffer(size), current(0), tempprob{0.4, 0.3, 0.3} {
        for (int i; i<size; i++) buffer.push_back(rint2(tempprob, 1.0));
    }

    double get() {
        if (current > buffer.size() - 1)
            buffer.push_back(rint2(tempprob, 1.0));
        return buffer[current++];
    }

    void reset() {
        current = 0;
    }

private:
    const std::vector<double> tempprob;
    std::vector<double> buffer;
    size_t current;
};

#endif