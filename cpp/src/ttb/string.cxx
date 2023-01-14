#include "railostools/ttb/string.hxx"
#include <iostream>

std::string RailOSTools::concat(const std::vector<std::string>& components, const ComponentType& join_type) {
    if(components.empty()) return "";

    std::string out_str_;
    std::string delimiter_;

    switch(join_type) {
        case(ComponentType::Element):
            delimiter_ = "\0"s;
            break;
        case(ComponentType::Service):
            delimiter_ = ",";
            break;
        default:
            delimiter_ = ";";
    }

    for(int i{0}; i < components.size(); ++i) {
        out_str_ += components[i];
        if(i < components.size() - 1)  out_str_ += delimiter_;
    }

    return out_str_;
}

std::vector<std::string> RailOSTools::split(const std::string& component_str, const ComponentType& split_type) {
    
    std::vector<std::string> components_;
    std::string delimiter_;

    switch(split_type) {
        case(ComponentType::Element):
            delimiter_ = "\0"s;
            break;
        case(ComponentType::Service):
            delimiter_ = ",";
            break;
        default:
            delimiter_ = ";";
    }

    std::string::size_type component_start_ = component_str.find_first_not_of(delimiter_, 0);
    std::string::size_type component_end_ = component_str.find_first_of(delimiter_, component_start_);

    while(std::string::npos != component_start_ || std::string::npos != component_end_) {
        components_.push_back(component_str.substr(component_start_, component_end_ - component_start_));
        component_start_ = component_str.find_first_not_of(delimiter_, component_end_);
        component_end_ = component_str.find_first_of(delimiter_, component_start_);
    }

    return components_;
}