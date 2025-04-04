#include "railostools/common.hxx"
#include "railostools/exceptions.hxx"

std::string RailOSTools::strip(const std::string& in_str) {
  std::string s(in_str);
  s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char c){ return !std::isspace(c); }));
  s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char c){ return !std::isspace(c); }).base(), s.end());
  return s;
}

std::vector<std::string> RailOSTools::strip_svector(const std::vector<std::string>& s_vec) {
  std::vector<std::string> processed_(s_vec.size());
  std::transform(
    s_vec.begin(),
    s_vec.end(),
    processed_.begin(),
    [](std::string s){return RailOSTools::strip(s);}
  );
  processed_.erase(std::remove(processed_.begin(), processed_.end(), ""), processed_.end());

  return processed_;
}

std::pair<int, int> RailOSTools::Coordinate::parse_int_pair_(const std::string& coord_str) {
  const std::regex pattern_("^(N*\\d+)\\-(N*\\d+)$");
  std::smatch matches;
  if(!std::regex_match(coord_str, matches, pattern_)) {
    throw RailOSTools::parsing_error(std::format("Invalid coordinate '{}'", coord_str).c_str());
  }
  const std::string x_val_str_{matches[1].str()};
  const std::string y_val_str_{matches[2].str()};

  int x_val_{0};
  int y_val_{0};

  if(x_val_str_[0] == 'N') {
    x_val_ = -1 * std::stoi(x_val_str_.substr(1));
  } else {
    x_val_ = std::stoi(x_val_str_);
  }
  if(y_val_str_[0] == 'N') {
    y_val_ = -1 * std::stoi(y_val_str_.substr(1));
  } else {
    y_val_ = std::stoi(y_val_str_);
  }

  return std::pair<int, int>{x_val_, y_val_};
}

RailOSTools::Coordinate RailOSTools::Coordinate::operator+(const RailOSTools::Coordinate& second) const {
  return RailOSTools::Coordinate(x_ + second.X(), y_ + second.Y());
}

RailOSTools::Coordinate RailOSTools::Coordinate::operator-(const RailOSTools::Coordinate& second) const {
  return RailOSTools::Coordinate(x_ - second.X(), y_ - second.Y());
}

bool RailOSTools::Coordinate::operator==(const RailOSTools::Coordinate& second) const {
  return x_ == second.X() && y_ == second.Y();
}

bool RailOSTools::Coordinate::operator!=(const RailOSTools::Coordinate& second) const {
  return x_ != second.X() || y_ != second.Y();
}
