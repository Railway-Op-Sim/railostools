#include <gtest/gtest.h>
#include <stdexcept>
#include "railostools/validation/numeric.hxx"

TEST(ValidationTest, TestNumericValidationInt) {
    RailOSTools::NumericValidator<int> validator(10, "test");
    ASSERT_NO_THROW(validator.gt(2).lt(12));
    ASSERT_THROWS(validator.ge(0).le(5), std::runtime_error);
}

TEST(ValidationTest, TestNumericValidationFloat) {
    RailOSTools::NumericValidator<float> validator(10.7, "test");
    ASSERT_NO_THROW(validator.gt(2.4).lt(12.1));
    ASSERT_THROWS(validator.ge(0.2).le(5.8), std::runtime_error);
}
