#include "railostools/railway.hxx"
#include "railostools/common.hxx"

RailOSTools::ActiveElement RailOSTools::parse_active_element(const std::vector<std::string>& active_elem) {
  const std::vector<std::string> processed_(RailOSTools::strip_svector(active_elem));

  return RailOSTools::ActiveElement(
    static_cast<RailOSTools::Elements>(std::stoi(processed_[1])),
    RailOSTools::Coordinate(std::stoi(processed_[2]), std::stoi(processed_[3])),
    {std::stoi(processed_[4]), (processed_[5] != "-1") ? std::optional<int>(std::stoi(processed_[5])) : std::nullopt},
    {std::stoi(processed_[6]), (processed_[7] != "-1") ? std::optional<int>(std::stoi(processed_[7])) : std::nullopt},
    {},
    (std::empty(processed_[8])) ? std::nullopt : std::optional<std::string>(processed_[8]),
    (std::empty(processed_[9])) ? std::nullopt : std::optional<std::string>(processed_[9])
  );
}

RailOSTools::Text RailOSTools::parse_text(const std::vector<std::string>& text_elem) {
  const std::vector<std::string> processed_(RailOSTools::strip_svector(text_elem));

  if(processed_.size() != 10) {
    throw RailOSTools::parsing_error("Expected 10 elements in text element parsing.");
  }

  const unsigned int n_items = std::stoi(processed_[0]);
  const int x_val = std::stoi(processed_[2]);
  const int y_val = std::stoi(processed_[3]);
  const std::string text_str = processed_[4];
  const std::string font_name = processed_[5];
  const int font_size = std::stoi(processed_[6]);
  const int font_color = std::stoi(processed_[7]);
  const int font_charset = std::stoi(processed_[8]);
  const int font_style = std::stoi(processed_[9]);

  return RailOSTools::Text(
    n_items,
    RailOSTools::Coordinate(x_val, y_val),
    text_str,
    RailOSTools::Font(
      font_name,
      font_size,
      font_color,
      font_charset,
      font_style
    )
  );
}

RailOSTools::Metadata RailOSTools::parse_metadata(const std::vector<std::string>& metadata) {
  const std::vector<std::string> processed_ = RailOSTools::strip_svector(metadata);

  if(processed_.empty()) {
    throw RailOSTools::parsing_error("Failed to retrieve railway metadata.");
  }
  
  semver::version version_(
    (processed_[0][0] == 'v') ? processed_[0].substr(1) :  processed_[0]
  );

  return RailOSTools::Metadata(
    version_,
    Coordinate(std::stoi(processed_[1]), std::stoi(processed_[2])),
    std::stoi(processed_[3])
  );
}

