#pragma once

#include <chrono>
#include <string>
#include <stdexcept>
#include <vector>

#include "railostools/ttb/string.hxx"
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
            const int start_speed_;
            const int max_speed_;
            const int mass_;
            const int brake_force_;
            const int power_;
            const int max_signaller_speed_;
        public:
            Header(
                const Reference& reference,
                const std::string& description,
                int start_speed=-1,
                int max_speed=-1,
                int mass=-1,
                int brake_force=-1,
                int power=-1,
                int max_signaller_speed=-1): 
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

                if(max_speed_ > 0) {
                    std::vector<int> specs_{
                        start_speed_,
                        max_speed_,
                        mass_,
                        power_
                    };

                    for(int spec : specs_) {
                        if(spec < 0) {
                            throw std::
                        }
                    }
                }
            }
    };

};
