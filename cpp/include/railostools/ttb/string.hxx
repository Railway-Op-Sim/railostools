#pragma once

#include <string>
#include <vector>
#include <cstddef>

using namespace std::string_literals;

namespace RailOSTools {
    enum class ComponentType {
        Element,
        Entry,
        Service
    };

    std::string concat(
        const std::vector<std::string>& components,
        const ComponentType& join_type=ComponentType::Entry
    );
    std::vector<std::string> split(
        const std::string& component_str,
        const ComponentType& split_type=ComponentType::Element
    );
};