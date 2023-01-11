#include "railostools/metadata.hxx"

std::string RailOSTools::Metadata::retrieve_string_(const std::string& key) const {
    return meta_data_[key].value<std::string>().value_or("");
}

template<typename T>
void RailOSTools::Metadata::set_key_value_(const std::string& key, const T& value) {
    meta_data_.insert_or_assign(key, toml::value{value});
}

std::string RailOSTools::Metadata::name() const {
    return retrieve_string_("name");
}

std::string RailOSTools::Metadata::signal_position() const {
    return retrieve_string_("signal_position");
}

std::string RailOSTools::Metadata::author() const {
    return retrieve_string_("author");
}

std::string RailOSTools::Metadata::description() const {
    return retrieve_string_("description");
}

std::string RailOSTools::Metadata::display_name() const {
    return retrieve_string_("display_name");
}

int RailOSTools::Metadata::year() const {
    return meta_data_["year"].value<int>().value_or(-1);
}

int RailOSTools::Metadata::difficulty() const {
    return meta_data_["difficulty"].value<int>().value_or(-1);
}

bool RailOSTools::Metadata::factual() const {
    return meta_data_["factual"].value<bool>().value_or(false);
}

std::string RailOSTools::Metadata::country_code() const {
    return retrieve_string_("country_code");
}

std::vector<std::string> RailOSTools::Metadata::contributors() const {
    return retrieve_list_("contributors");
}

semver::version RailOSTools::Metadata::version() const {
    const std::string ver_str_ = meta_data_["version"].value<std::string>().value_or("");
    if(ver_str_.empty()) return semver::version();
    return semver::version(ver_str_);
}

semver::version RailOSTools::Metadata::minimum_required() const {
    const std::string key_ = "minimum_required";
    if(!meta_data_.contains(key_)) return semver::version{"0.1.0"};
    const std::string ver_str_ = meta_data_[key_].value<std::string>().value_or("");
    if(ver_str_.empty()) return semver::version();
    return semver::version(ver_str_);
}

std::filesystem::path RailOSTools::Metadata::rly_file() const {
    return std::filesystem::path(meta_data_["rly_file"].value<std::string>().value_or(""));
}

std::vector<std::string> RailOSTools::Metadata::retrieve_list_(const std::string& key) const {
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

RailOSTools::Metadata::Metadata(const std::filesystem::path& file_name, bool validate_inputs) {
    toml_file_ = file_name;
    meta_data_ = toml::parse_file(file_name.string());

    if(validate_inputs) validate();
}

void RailOSTools::Metadata::validate() {
    const std::vector<std::string> check_excludes_ = {
        "factual",
        "country_code",
        "year",
        "version"
    };

    for(const std::string& required : MANDATORY_KEYS) {
        if(!meta_data_.contains(required)) {
            throw std::runtime_error("Expected missing key '"+required+"'");
        }
        if(std::find(check_excludes_.begin(), check_excludes_.end(), required) != check_excludes_.end()) {
            continue;
        }
        if(required.find("files") != std::string::npos) {
            if(retrieve_list_(required).empty()) {
                throw std::runtime_error("Required key '"+required+"' cannot have empty list");
            }
        }
        else {
            if(retrieve_string_(required).empty()) {
                throw std::runtime_error("Required key '"+required+"' cannot be empty list");
            }
        }
    }

    if(meta_data_.contains("graphic_files") && !retrieve_list_("graphic_files").empty()) {
        if(!meta_data_.contains("minimum_required")) {
            setMinimumRequired("2.4.0"); // Graphics introduced in v2.4.0
        }
        else {
            if(minimum_required() < semver::version{"2.4.0"}) {
                setMinimumRequired("2.4.0");
            }
        }
    }

    if(COUNTRY_CODES.count(country_code()) == 0) {
        throw std::runtime_error("Invalid country code '"+country_code()+"'");
    }
}

void RailOSTools::Metadata::add_missing_keys() {
    const std::vector<std::string> list_vals_ = {
        "ttb_files",
        "doc_files",
    };

    const std::vector<std::string> str_vals_ = {
        "rly_file",
        "author",
        "release_date",
        "name",
        "version",
        "country_code"
    };

    for(const std::string& key : list_vals_) {
        if(meta_data_.contains(key)) continue;
        set_list_(key, {});
    }

    for(const std::string& key : str_vals_) {
        if(meta_data_.contains(key)) continue;
        set_key_value_(key, "");
    }

    if(!meta_data_.contains("factual")) set_key_value_("factual", false);
}

std::vector<std::filesystem::path> RailOSTools::Metadata::ssn_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("ssn_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> RailOSTools::Metadata::ttb_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("ttb_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> RailOSTools::Metadata::doc_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("doc_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> RailOSTools::Metadata::img_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("img_files")) {
        files_.push_back(file);
    }
    return files_;
}

std::vector<std::filesystem::path> RailOSTools::Metadata::graphic_files() const {
    std::vector<std::filesystem::path> files_;
    for(const std::string& file : retrieve_list_("graphic_files")) {
        files_.push_back(file);
    }
    return files_;
}

date::year_month_day RailOSTools::Metadata::release_date() const {
    const std::string date_ = retrieve_string_("release_date");
    std::stringstream stream_(date_);
    std::string part_;

    std::vector<int> date_elements_;

    while(std::getline(stream_, part_, '-'))
    {
        date_elements_.push_back(std::stoi(part_));
    }

    if(date_elements_.size() != 3) {
        throw std::runtime_error("Expected release_date to be in form YYYY-MM-DD");
    }

    return date::year{date_elements_[0]}/date::month{date_elements_[1]}/date::day{date_elements_[2]};
}

void RailOSTools::Metadata::setAuthor(const std::string& author) {
    if(author.empty()) {
        throw std::runtime_error("Key 'author' cannot be empty");
    }
    set_key_value_("author", author);
}

void RailOSTools::Metadata::setFactual(bool is_factual) {
    set_key_value_("factual", is_factual);
}

void RailOSTools::Metadata::setReleaseDate(const date::year_month_day& release_date_val) {
    std::stringstream ss;
    ss << release_date_val;
    set_key_value_("release_date", ss.str());
}

void RailOSTools::Metadata::setReleaseNow() {
    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);
    std::stringstream ss;

    ss << std::put_time(&tm, "%Y-%m-%d");
    set_key_value_("release_date", ss.str());
}

void RailOSTools::Metadata::set_list_(const std::string& key, const std::vector<std::string>& list_vals) {
    toml::array out_vals_;

    for(const std::string& val : list_vals) {
      out_vals_.push_back(val);
    }
    meta_data_.insert_or_assign(key, out_vals_);
}

void RailOSTools::Metadata::append_to_list_(const std::string& label, const std::string& key, const std::string& value) {
    std::vector<std::string> existing_ = retrieve_list_(key);
    if(std::find(existing_.begin(), existing_.end(), value) != existing_.end()) {
        // Already in the list
        return;
    }
    existing_.push_back(value);
    set_list_(key, existing_);
}

void RailOSTools::Metadata::setContributors(const std::vector<std::string>& contributor_list) {
    set_list_("contributors", contributor_list);
}

void RailOSTools::Metadata::setTTBFiles(const std::vector<std::string>& ttb_filenames) {
    set_list_("ttb_files", ttb_filenames);
}

void RailOSTools::Metadata::setSSNFiles(const std::vector<std::string>& ssn_filenames) {
    set_list_("ssn_files", ssn_filenames);
}

void RailOSTools::Metadata::setImgFiles(const std::vector<std::string>& img_filenames) {
    set_list_("img_files", img_filenames);
}

void RailOSTools::Metadata::setGraphicFiles(const std::vector<std::string>& graphic_filenames) {
    set_list_("graphic_files", graphic_filenames);
}

void RailOSTools::Metadata::setDocFiles(const std::vector<std::string>& doc_filenames) {
    set_list_("doc_files", doc_filenames);
}

void RailOSTools::Metadata::setRLYFile(const std::string& rly_filename){
    if(rly_filename.empty()) {
        throw std::runtime_error("Key 'rly_file' cannot be empty");
    }
    set_key_value_("rly_file", rly_filename);
}

void RailOSTools::Metadata::setDisplayName(const std::string& display_name_val){
    set_key_value_("display_name", display_name_val);
}

void RailOSTools::Metadata::setName(const std::string& name_val){
    if(name_val.empty()) {
        throw std::runtime_error("Key 'name' cannot be empty");
    }
    set_key_value_("name", name_val);
}

void RailOSTools::Metadata::setDescription(const std::string& description_val){
    set_key_value_("description", description_val);
}

void RailOSTools::Metadata::setYear(const int year){
    if(year < 1900 || year > 9999) {
        throw std::runtime_error("Year must be in range [1999,9999]");
    }
    set_key_value_("year", year);
}

void RailOSTools::Metadata::setDifficulty(const int difficulty_val){
    if(difficulty_val < 1 || difficulty_val > 5) {
        throw std::runtime_error("Difficulty must be in the range [1, 5]");
    }
    set_key_value_("difficulty", difficulty_val);
}

void RailOSTools::Metadata::addContributor(const std::string& contributor){
    append_to_list_("Contributor", "contributors", contributor);
}

void RailOSTools::Metadata::addTTBFile(const std::string& ttb_filename){
    append_to_list_("Timetable file", "ttb_files", ttb_filename);
}

void RailOSTools::Metadata::addSSNFile(const std::string& ssn_filename){
    append_to_list_("Session file", "ssn_files", ssn_filename);
}

void RailOSTools::Metadata::addImgFile(const std::string& img_filename){
    append_to_list_("Image file", "img_files", img_filename);
}

void RailOSTools::Metadata::addGraphicFile(const std::string& graphic_filename){
    append_to_list_("Graphic file", "graphic_files", graphic_filename);
}

void RailOSTools::Metadata::addDocFile(const std::string& doc_filename){
    append_to_list_("Document file", "doc_files", doc_filename);
}

void RailOSTools::Metadata::setCountryCode(const std::string& country_code_val) {
    if(COUNTRY_CODES.count(country_code_val) == 0) {
        throw std::runtime_error("Invalid country code '"+country_code_val+"'");
    }
    set_key_value_("country_code", country_code_val);
}

void RailOSTools::Metadata::write(const std::filesystem::path& output_file) {
    std::ofstream outs;
    outs.open(output_file);

    outs << meta_data_ << "\n";

    outs.close();
}

void RailOSTools::Metadata::setVersion(const semver::version& version) {
    set_key_value_("version", semver::to_string(version));
}

void RailOSTools::Metadata::setVersion(const std::string& version) {
    try {
        setVersion(semver::version{version});
    } catch(std::exception&) {
        throw std::runtime_error("Failed to parse version "+version);
    }
}

void RailOSTools::Metadata::setMinimumRequired(const semver::version& version) {
    set_key_value_("minimum_required", semver::to_string(version));
}

void RailOSTools::Metadata::setMinimumRequired(const std::string& version) {
    try {
        setMinimumRequired(semver::version{version});
    } catch(std::exception&) {
        throw std::runtime_error("Failed to parse minimum required version "+version);
    }
}

