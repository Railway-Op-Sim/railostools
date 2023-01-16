#pragma once

#include <chrono>
#include <string>
#include <stdexcept>
#include <vector>
#include <optional>

#include "railostools/ttb/string.hxx"
#include "railostools/validation/numeric.hxx"
#include "date/date.h"

namespace RailOSTools {

    typedef std::pair<std::chrono::hours, std::chrono::minutes> Time;

    bool isInt(const std::string& str) {
        return (str.find_first_not_of("01234556789") == std::string::npos);
    }

    class Element {
        protected:
            const std::string name_;
        public:
            Element(const std::string& name="") :
                name_{(name.empty()) ? std::string(__func__) : name} {}
            virtual ~Element() = default;
            friend std::string operator+(const Element& self, const Element& other) {
                return concat({self.name_, other.name_}, ComponentType::Element);
            }
    };

    class FinishType : public Element {
        public:
            FinishType(): Element("FinishType") {}
    };

    class ActionType : public Element {
        protected:
            const Time time_;
            const bool warning_{false};
        public:
            ActionType(const Time& time, bool warning=false) :
                Element(std::string{(warning) ? "W" : ""} + "ActionType") {}
    };

    class StartType : public Element {
        public:
            StartType(): Element("StartType") {}
    };

    class Reference {
        private:
            const std::string prefix_;
            const std::string service_;
            const std::string id_str_;
            int id_int_;
        public:
            Reference(const std::string& service, const std::string& id, const std::string& prefix="") :
                service_{service},
                prefix_{prefix},
                id_str_{id},
                id_int_{(isInt(id)) ? std::stoi(id_str_) : -1} {}
                void operator++() {
                    if(id_int_ == -1) {
                        throw std::runtime_error("Cannot increment reference with ID '" + id_str_ + "'");
                    }

                    id_int_++;
                }
                void operator--() {
                    if(id_int_ == -1) {
                        throw std::runtime_error("Cannot decrement reference with ID '" + id_str_ + "'");
                    }

                    if(id_int_ - 1 < 0) {
                        throw std::runtime_error("ID must be between 0 and 99");
                    }

                    id_int_--;
                }
            std::string to_string() const {
                std::string out_str_{prefix_ + service_};
                if(id_int_ > -1) {
                    out_str_ += std::string{(id_int_ < 10) ? "0" : ""};
                    out_str_ += std::to_string(id_int_);
                }
                else{out_str_ += id_str_;}

                return out_str_;
            }
    };

    class Header : public Element {
        private:
            const Reference reference_;
            const std::string description_;
            const std::optional<int> start_speed_;
            const std::optional<int> max_speed_;
            const std::optional<int> mass_;
            const std::optional<int> brake_force_;
            const std::optional<int> power_;
            const std::optional<int> max_signaller_speed_;
        public:
            Header(
                const Reference& reference,
                const std::string& description,
                std::optional<int> start_speed=std::nullopt,
                std::optional<int> max_speed=std::nullopt,
                std::optional<int> mass=std::nullopt,
                std::optional<int> brake_force=std::nullopt,
                std::optional<int> power=std::nullopt,
                std::optional<int> max_signaller_speed=std::nullopt):
                    Element("Header"),
                    reference_{reference},
                    description_{description},
                    start_speed_{start_speed},
                    max_speed_{max_speed},
                    mass_{mass},
                    brake_force_{brake_force},
                    power_{power},
                    max_signaller_speed_{max_signaller_speed}
                {}

            std::string to_string() const {
                std::vector<std::string> elements_{reference_.to_string()};

                if(!description_.empty()) elements_.push_back(description_);

                if(max_speed_) {
                    std::vector<std::pair<std::string, std::optional<int>>> specs_{
                        {"start_speed", start_speed_},
                        {"max_speed", max_speed_},
                        {"mass", mass_},
                        {"power", power_}
                    };

                    for(auto [name, spec] : specs_) {
                        if(!spec) {
                            throw std::runtime_error("No value given for '" + name + "'");
                        }

                        // Should not reach this point if the specification is unset
                        elements_.push_back(std::to_string(spec.value()));
                    }
                }

                if(max_signaller_speed_) elements_.push_back(std::to_string(max_signaller_speed_.value()));

                return concat(elements_);
            }
    };

    class Repeat : public Element {
        private:
            const int mins_;
            const int digits_;
            const int repeats_;
        public:
            Repeat(const int mins, const int digits, const int repeats) :
                mins_{NumericValidator<int>("mins").gt(1).validate(mins).value()},
                digits_{NumericValidator<int>("digits").ge(0).validate(digits).value()},
                repeats_{NumericValidator<int>("repeats").gt(1).validate(repeats).value()} {}
    };

};
