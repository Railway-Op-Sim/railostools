#include <gtest/gtest.h>
#include "railostools/ttb/string.hxx"

TEST(TTBStringTest, SplitStringService) {
    using namespace std::string_literals;
    const std::string test_str = "this;is,a\0test,string;for\0railos"s;
    const std::vector<std::string> expected_comma_{"this;is", "a\0test"s, "string;for\0railos"s};

    ASSERT_EQ(RailOSTools::split(test_str, RailOSTools::ComponentType::Service), expected_comma_);
}

TEST(TTBStringTest, SplitStringEntry) {
    using namespace std::string_literals;
    const std::string test_str = "this;is,a\0test,string;for\0railos"s;
    const std::vector<std::string> expected_semicolon_{"this"s, "is,a\0test,string"s, "for\0railos"s};

    ASSERT_EQ(RailOSTools::split(test_str, RailOSTools::ComponentType::Entry), expected_semicolon_);
}

TEST(TTBStringTest, SplitStringElement) {
    using namespace std::string_literals;
    const std::string test_str = "this;is,a\0test,string;for\0railos"s;
    const std::vector<std::string> expected_null_{"this;is,a", "test,string;for", "railos"};

    ASSERT_EQ(RailOSTools::split(test_str, RailOSTools::ComponentType::Element), expected_null_);
}

TEST(TTBStringTest, JoinStringService) {
    using namespace std::string_literals;
    const std::vector<std::string> test_components_{"this;is", "a\0test"s, "string;for\0railos"s};
    const std::string expected_str_ = "this;is,a\0test,string;for\0railos"s;

    ASSERT_EQ(RailOSTools::concat(test_components_, RailOSTools::ComponentType::Service), expected_str_);
}

TEST(TTBStringTest, JoinStringEntry) {
    using namespace std::string_literals;
    const std::vector<std::string> test_components_{"this"s, "is,a\0test,string"s, "for\0railos"s};
    const std::string expected_str_ = "this;is,a\0test,string;for\0railos"s;

    ASSERT_EQ(RailOSTools::concat(test_components_, RailOSTools::ComponentType::Entry), expected_str_);
}

TEST(TTBStringTest, JoinStringElement) {
    using namespace std::string_literals;
    const std::vector<std::string> test_components_{"this;is,a", "test,string;for", "railos"};
    const std::string expected_str_ = "this;is,a\0test,string;for\0railos"s;

    ASSERT_EQ(RailOSTools::concat(test_components_, RailOSTools::ComponentType::Element), expected_str_);
}
