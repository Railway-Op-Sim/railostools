#include <gtest/gtest.h>
#include <string>
#include "railostools/common.hxx"

typedef std::pair<std::string, std::pair<int, int>> test_coord_pair;

class CoordStrFixture : public ::testing::TestWithParam<test_coord_pair> {};

TEST_P(CoordStrFixture, InitialiseCoordStr) {
  const test_coord_pair test_pair_{GetParam()};
  const RailOSTools::Coordinate test_coord(test_pair_.first);
  ASSERT_EQ(test_coord.X(), test_pair_.second.first);
  ASSERT_EQ(test_coord.Y(), test_pair_.second.second);
}

INSTANTIATE_TEST_SUITE_P(
  CommonTest,
  CoordStrFixture,
  ::testing::Values(
    std::make_pair("N23-56", std::make_pair(-23, 56)),
    std::make_pair("273-185", std::make_pair(273, 185)),
    std::make_pair("27-N5", std::make_pair(27, -5)),
    std::make_pair("N82-N27", std::make_pair(-82, -27))
  )
);

TEST(CommonTest, CoordOper) {
  const RailOSTools::Coordinate a(10, 4), b(11, -6), eq_add(21, -2), eq_sub(-1, 10);
  ASSERT_EQ(a + b, eq_add);
  ASSERT_EQ(a - b, eq_sub);
}

TEST(CommonTest, CoordAbs) {
  const RailOSTools::Coordinate a(3, 4);
  ASSERT_EQ(a.abs(), 5);
}

TEST(CommonTest, TestStripString) {
  const std::string raw{" The rain in Spain "}, expected{"The rain in Spain"};
  ASSERT_EQ(RailOSTools::strip(raw), expected);
}

TEST(CommonTest, TestStripSVector) {
  const std::vector<std::string> raw{
    " The rain ",
    " in Spain",
    "falls",
    " ",
  };
  const std::vector<std::string> expected{
    "The rain",
    "in Spain",
    "falls"
  };

  ASSERT_EQ(RailOSTools::strip_svector(raw), expected);
}
