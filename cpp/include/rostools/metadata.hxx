#ifndef __ROSTOOLS_METADATA_HXX__
#define __ROSTOOLS_METADATA_HXX__

#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <filesystem>

#include "tomlplusplus/toml.hpp"
#include "semver/semver.hpp"
#include "date/date.h"

#include "country_codes.hxx"

namespace ROSTools {

    const std::vector<std::string> MANDATORY_KEYS = {
        "name",
        "rly_file",
        "ttb_files",
        "doc_files",
        "author",
        "country_code",
        "factual",
    };

    class Metadata {
        private:
            std::filesystem::path toml_file_;
            toml::table meta_data_;
            std::vector<std::string> retrieve_list_(const std::string& key) const;
            std::string retrieve_string_(const std::string& key) const;
        public:
            Metadata() {}
            Metadata(const std::filesystem::path& file_name);
            std::string name() const;
            std::filesystem::path rly_file() const;
            semver::version version() const;
            std::string country_code() const;
            std::string display_name() const;
            std::filesystem::path toml_file() const {return toml_file_;}
            std::vector<std::filesystem::path> ssn_files() const;
            std::vector<std::filesystem::path> ttb_files() const;
            std::vector<std::filesystem::path> doc_files() const;
            std::vector<std::filesystem::path> img_files() const;
            std::vector<std::filesystem::path> graphic_files() const;
            std::vector<std::string> contributors() const;
            bool factual() const;
            int year() const;
            std::string description() const;
            std::string author() const;
            date::year_month_day release_date() const;
    };
};

#endif