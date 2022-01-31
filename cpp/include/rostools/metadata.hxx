#ifndef __ROSTOOLS_METADATA_HXX__
#define __ROSTOOLS_METADATA_HXX__

#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <filesystem>
#include <fstream>

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
        "version",
        "release_date",
    };

    class Metadata {
        private:
            std::filesystem::path toml_file_;
            toml::table meta_data_;
            std::vector<std::string> retrieve_list_(const std::string& key) const;
            std::string retrieve_string_(const std::string& key) const;
            template<typename T>
            void set_key_value_(const std::string& key, const T& value);
            void append_to_list_(const std::string& label, const std::string& key, const std::string& value);
            void set_list_(const std::string& key, const std::vector<std::string>& list_vals);
        public:
            Metadata() {}
            Metadata(const std::filesystem::path& file_name, bool validate_inputs=true);
            void validate();
            void add_missing_keys();
            toml::table data() const {return meta_data_;}
            std::string name() const;
            std::filesystem::path rly_file() const;
            semver::version version() const;
            semver::version minimum_required() const;
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
            int difficulty() const;
            int year() const;
            std::string description() const;
            std::string author() const;
            date::year_month_day release_date() const;
            void setRLYFile(const std::string& rly_filename);
            void addTTBFile(const std::string& ttb_filename);
            void setTTBFiles(const std::vector<std::string>& ttb_filenames);
            void addSSNFile(const std::string& ssn_filename);
            void setSSNFiles(const std::vector<std::string>& ssn_filenames);
            void addImgFile(const std::string& img_filename);
            void setImgFiles(const std::vector<std::string>& img_filenames);
            void addGraphicFile(const std::string& graphic_filename);
            void setGraphicFiles(const std::vector<std::string>& graphic_filenames);
            void addDocFile(const std::string& doc_filename);
            void setDocFiles(const std::vector<std::string>& doc_filenames);
            void setAuthor(const std::string& author);
            void addContributor(const std::string& author);
            void setYear(const int year);
            void setDifficulty(const int difficulty);
            void setContributors(const std::vector<std::string>& contributor_list);
            void setFactual(bool is_factual);
            void setReleaseDate(const date::year_month_day& release_date_val);
            void setReleaseNow();
            void setDescription(const std::string& description_val);
            void setDisplayName(const std::string& display_name_val);
            void setName(const std::string& name_val);
            void setCountryCode(const std::string& country_code_val);
            void write(const std::filesystem::path& output_file);
            void setVersion(const semver::version& version);
            void setVersion(const std::string& version);
            void setMinimumRequired(const semver::version& version);
            void setMinimumRequired(const std::string& version="0.1.0");
    };
};

#endif