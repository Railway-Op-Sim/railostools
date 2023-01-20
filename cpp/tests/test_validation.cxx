#include <gtest/gtest.h>
#include <stdexcept>
#include "railostools/validation/numeric.hxx"

TEST(ValidationTest, TestNumericValidationInt) {
    RailOSTools::NumericValidator<int> validator("test");
    ASSERT_EQ(validator.gt(2).lt(12).validate(10), 10);
    ASSERT_THROW(validator.ge(0).le(5).validate(2), std::runtime_error);
}

TEST(ValidationTest, TestNumericValidationFloat) {
    RailOSTools::NumericValidator<float> validator("test");
    ASSERT_EQ(validator.gt(2.4).lt(12.1).validate(10.7), 10.7);
    ASSERT_THROW(validator.ge(0.2).le(5.8).validate(10.7), std::runtime_error);
}
