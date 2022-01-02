#ifndef __ROSTOOLS_METADATA_HXX__
#define __ROSTOOLS_METADATA_HXX__

#include <map>
#include <string>
#include <filesystem>

#include "toml.hpp"
#include "semver.hpp"

#include "country_codes.hxx"

namespace ROSTools {
    class Metadata {
        private:
            const std::vector<std::string> mandatory_keys_ = {
                "name",
                "rly_file",
                "ttb_files",
                "doc_files",
                "author",
                "country_code",
                "factual",
            };
            toml::table meta_data_;
            std::vector<std::string> retrieve_list_(const std::string& key) const;
            std::string retrieve_string_(const std::string& key) const;
        public:
            Metadata(const std::filesystem::path& file_name);
            std::string name() const;
            std::filesystem::path rly_file() const;
            semver::version version() const;
            std::string country_code() const;
            std::string display_name() const;
            std::vector<std::filesystem::path> ssn_files() const;
            std::vector<std::filesystem::path> ttb_files() const;
            std::vector<std::filesystem::path> doc_files() const;
            std::vector<std::string> contributors() const;
            bool factual() const;
            int year() const;
            std::string description() const;
            std::string author() const;
    };
};

#endif