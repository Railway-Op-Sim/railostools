#ifndef __RAILOSTOOLS_RAILWAY_HXX__
#define __RAILOSTOOLS_RAILWAY_HXX__

#include <memory>
#include <string>
#include <regex>
#include <vector>
#include <optional>
#include <filesystem>
#include <ctime>
#include <unordered_map>
#include <algorithm>
#include <iterator>
#include <optional>

#include "semver/semver.hpp"
#include "railostools/common.hxx"
#include "railostools/exceptions.hxx"

namespace RailOSTools {
struct StartPosition {
  const Coordinate start_coordinate;
  const Coordinate end_coordinate;
};

struct TimetableLocation {
  const std::string name;
  const std::vector<Coordinate> start_positions;
};

struct RlyElement {
  const Elements element_id;
  const Coordinate position;
  const std::optional<std::string> location_name = std::nullopt;
};

struct InactiveElement : RlyElement {};

struct ActiveElement : RlyElement {
  const std::pair<unsigned int, std::optional<unsigned int>> length;
  const std::pair<unsigned int, std::optional<unsigned int>> speed_limit;
  const std::vector<std::shared_ptr<ActiveElement>> neighbours;
  const std::optional<std::string> signal = std::nullopt;
  ActiveElement(
    const Elements element_id,
    const Coordinate position,
    const std::pair<unsigned int, std::optional<unsigned int>> length,
    const std::pair<unsigned int, std::optional<unsigned int>> speed_limit,
    const std::vector<std::shared_ptr<ActiveElement>> neighbours,
    const std::optional<std::string> location_name = std::nullopt,
    const std::optional<std::string> signal = std::nullopt
  ) : RlyElement(element_id, position, location_name),
      length(length),
      speed_limit(speed_limit),
      neighbours(neighbours),
      signal(signal) {}
};

struct Font {
  const std::string name;
  const int size;
  const int color;
  const int charset;
  const int style;
};

struct Text {
  const unsigned int n_items;
  const Coordinate position;
  const std::string text_string;
  const Font font;
};

struct Metadata {
  const semver::version program_version;
  const Coordinate home_position;
  const unsigned int n_active_elements;
  const std::optional<unsigned int> n_inactive_elements = std::nullopt;
};

struct RlyData {
  const std::vector<std::shared_ptr<ActiveElement>> active_elements;
  const std::vector<std::shared_ptr<InactiveElement>> inactive_elements;
  const Metadata metadata;
  const std::optional<std::string> text = std::nullopt;
};

ActiveElement parse_active_element(const std::vector<std::string>& active_elem);
Metadata parse_metadata(const std::vector<std::string>& metadata);
Text parse_text(const std::vector<std::string>& text_elem);

class RlyParser {
private:
  std::unordered_map<std::string, RlyData> rly_data_;
  std::optional<std::tm> start_time_ = std::nullopt;
  std::optional<std::filesystem::path> current_file_ = std::nullopt;
  //InactiveElement parse_inactive_element_(const std::vector<std::string&>& inactive_elem) const;
  //RlyData get_rly_components_(const std::string& railway_file_data) const;
public:
  RlyParser() {};
  //void parse(const std::filesystem& rly_file);
};

};

#endif
