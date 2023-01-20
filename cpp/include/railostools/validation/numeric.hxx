#pragma once

#include <optional>
#include <string>
#include <iostream>

namespace RailOSTools {
    template<typename T>
    class NumericValidator {
        private:
            const std::string label_;
            std::optional<T> lt_=std::nullopt;
            std::optional<T> gt_=std::nullopt;
            std::optional<T> ge_=std::nullopt;
            std::optional<T> le_=std::nullopt;
        public:
            NumericValidator(const std::string& label) : label_{label} {}
            NumericValidator lt(const T& value) {lt_ = value; return *this;}
            NumericValidator le(const T& value) {le_ = value; return *this;}
            NumericValidator gt(const T& value) {gt_ = value; return *this;}
            NumericValidator ge(const T& value) {ge_ = value; return *this;}
            T validate(const T& value) {
                if(lt_.has_value() && lt_.value() <= value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value >= " + std::to_string(lt_.value()));
                }
                if(le_.has_value() && le_.value() < value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value > " + std::to_string(le_.value()));
                }
                if(gt_.has_value() && gt_.value() >= value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value <= " + std::to_string(gt_.value()));
                }
                if(ge_.has_value() && ge_.value() > value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value < " + std::to_string(ge_.value()));
                }
                return static_cast<T>(value);
            }
    };
};
