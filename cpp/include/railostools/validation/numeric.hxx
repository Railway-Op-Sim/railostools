#pragma once

#include <optional>
#include <string>

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
            std::optional<T> validate(const T& value) {
                if(lt_ && lt_.value() <= value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value >= " + std::to_string(lt_.value()));
                }
                if(le_ && le_.value() < value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value > " + std::to_string(lt_.value()));
                }
                if(gt_ && gt_.value() >= value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value <= " + std::to_string(lt_.value()));
                }
                if(ge_ && ge_.value() > value) {
                    throw std::runtime_error("Validation of '" + label_ + "' failed, value < " + std::to_string(lt_.value()));
                }
                return value_;
            }
    };
};
