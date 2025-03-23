#include <gtest/gtest.h>
#include "railostools/common.hxx"
#include "railostools/railway.hxx"
#include "semver/semver.hpp"

TEST(RailwayTest, TestStartPosition) {
  const RailOSTools::Coordinate a(10, 11), b(-4, 2);
  const RailOSTools::StartPosition start(a, b);
  ASSERT_EQ(start.start_coordinate, a);
}

TEST(RailwayTest, TestTimetableLocation) {
  const RailOSTools::Coordinate a(10, 11);
  const RailOSTools::TimetableLocation ttb_loc("test_location", {a});
  ASSERT_EQ(ttb_loc.name, "test_location");
}

TEST(RailwayTest, TestRlyElement) {
  const RailOSTools::Coordinate a(10, 11);
  const RailOSTools::Elements elem = RailOSTools::Elements::Horizontal;
  RailOSTools::RlyElement rly_elem({elem}, a, "test_location");
  ASSERT_EQ(rly_elem.location_name, "test_location");
}

TEST(RailwayTest, TestParseMetadata) {
  const std::vector<std::string> metadata_line{" v2.9.2", "-68", "-6", "1274"};
  const RailOSTools::Metadata metadata = RailOSTools::parse_metadata(metadata_line);
  const RailOSTools::Coordinate expected(-68, -6);
  ASSERT_EQ(metadata.program_version, semver::version("2.9.2"));
  ASSERT_EQ(metadata.home_position, expected);
  ASSERT_EQ(metadata.n_active_elements, 1274);
}

TEST(RailwayTest, TestParseText) {
  const std::vector<std::string> text_line{" 10", "***", "-56", "45", "test", "font", "0", "23", "34", "78"};
  const RailOSTools::Text text = RailOSTools::parse_text(text_line);
  ASSERT_EQ(text.text_string, "test");
  ASSERT_EQ(text.font.name, "font");
}
