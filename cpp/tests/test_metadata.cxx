#include <gtest/gtest.h>
#include "rostools/metadata.hxx"

#include <filesystem>
#include <iostream>

#ifndef TEST_DATA_DIR
    #error Test Data Directory not defined!
#endif

TEST(MetadataTest, Validation) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    EXPECT_NO_THROW(meta_);
}

TEST(MetadataTest, VersionRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.version(), semver::version(1, 0, 0));
}

TEST(MetadataTest, RlyRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.rly_file(), std::filesystem::path("Antwerpen_Centraal.rly"));
}

TEST(MetadataTest, FileRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.ttb_files()[0], std::filesystem::path("Antwerpen_Centraal_2021.ttb"));
    ASSERT_EQ(meta_.ssn_files()[0], std::filesystem::path("Antwerpen_Centraal_2021.ssn"));
}

TEST(MetadataTest, YearRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.year(), 2021);
}

TEST(MetadataTest, RetrievalFactual) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    ROSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_TRUE(meta_.factual());
}
