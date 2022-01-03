#include "rostools/metadata.hxx"

std::string ROSTools::Metadata::retrieve_string_(const std::string& key) const {
    return meta_data_[key].value<std::string>().value_or("");
}

std::string ROSTools::Metadata::name() const {
    return retrieve_string_("name");
}

std::string ROSTools::Metadata::author() const {
    return retrieve_string_("author");
}

std::string ROSTools::Metadata::description() const {
    return retrieve_string_("description");
}

std::string ROSTools::Metadata::display_name() const {
    return retrieve_string_("display_name");
}

int ROSTools::Metadata::year() const {
    return meta_data_["year"].value<int>().value_or(-1);
}

bool ROSTools::Metadata::factual() const {
    return meta_data_["factual"].value<bool>().value_or(false);
}

std::string ROSTools::Metadata::country_code() const {
    return retrieve_string_("country_code");
}

std::vector<std::string> ROSTools::Metadata::contributors() const {
    return retrieve_list_("contributors");
}

semver::version ROSTools::Metadata::version() const {
    const std::string ver_str_ = meta_data_["version"].value<std::string>().value_or("");
    if(ver_str_.empty()) return semver::version();
    return semver::version(ver_str_);
}

std::filesystem::path ROSTools::Metadata::rly_file() const {
    return std::filesystem::path(meta_data_["rly_file"].value<std::string>().value_or(""));
}

std::vector<std::string> ROSTools::Metadata::retrieve_list_(const std::string& key) const {
    std::vector<std::string> items_;
    if(!meta_data_.contains(key)) {
        return items_;
    }
    toml::array file_arr_ = *meta_data_.get_as<toml::array>(key);

    for (auto&& elem : file_arr_)
    {
        items_.push_back(elem.value<std::string>().value_or(""));
    }

    return items_;
}

ROSTools::Metadata::Metadata(const std::filesystem::path& file_name) {
    toml_file_ = file_name;
    meta_data_ = toml::parse_file(file_name.string());

    for(const std::string& required : MANDATORY_KEYS) {
        if(!meta_data_.contains(required)) {
            throw std::runtime_error("Expected missing key '"+required+"'");
        }
    }

    if(COUNTRY_CODES.count(country_code()) == 0) {
        throw std::runtime_error("Invalid country code '"+country_code()+"'");
    }

}

std::vector<std::filesystem::path> ROSTools::Metadata::ssn_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("ssn_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> ROSTools::Metadata::ttb_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("ttb_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> ROSTools::Metadata::doc_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("doc_files")) {
        files_.push_back(file);
    }
    return files_;
}
