#include <gtest/gtest.h>
#include "railostools/ttb/components.hxx"

TEST(TTBComponentTest, AddElements) {
    using namespace std::string_literals;
    ASSERT_EQ(RailOSTools::Element() + RailOSTools::Element(), "Element\0Element"s);
}

TEST(TTBComponentTest, AddServices) {
    using namespace std::string_literals;
    ASSERT_EQ(RailOSTools::FinishType() + RailOSTools::FinishType(), "FinishType\0FinishType"s);
}
