#include <gtest/gtest.h>
#include "railostools/metadata.hxx"

#include <filesystem>
#include <iostream>

#ifndef TEST_DATA_DIR
    #error Test Data Directory not defined!
#endif

using namespace date;

TEST(MetadataTest, Validation) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    EXPECT_NO_THROW(meta_);
}

TEST(MetadataTest, VersionRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.version(), semver::version(1, 0, 0));
}

TEST(MetadataTest, RlyRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.rly_file(), std::filesystem::path("Antwerpen_Centraal.rly"));
}

TEST(MetadataTest, FileRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.ttb_files()[0], std::filesystem::path("Antwerpen_Centraal_2021.ttb"));
    ASSERT_EQ(meta_.ssn_files()[0], std::filesystem::path("Antwerpen_Centraal_2021.ssn"));
    ASSERT_EQ(meta_.img_files()[0], std::filesystem::path("Antwerp_Centraal_2021.bmp"));
    ASSERT_EQ(meta_.graphic_files()[0], std::filesystem::path("Antwerp.jpg"));
}

TEST(MetadataTest, YearRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(meta_.year(), 2021);
}

TEST(MetadataTest, FactualRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_TRUE(meta_.factual());
}

TEST(MetadataTest, ReleaseRetrieval) {
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata meta_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    const year_month_day expected_ = 2021_y/October/9;
    ASSERT_EQ(meta_.release_date(), expected_);
}

TEST(MetadataTest, AssignValues) {
    RailOSTools::Metadata meta_;
    const std::string cont_name_ = "Albert Ball";
    const std::string author_name_ = "Krizar";
    const std::string image_file_ = "Antwerp_Centraal_2021.bmp";
    const std::string rly_file_ = "Antwerpen_Centraal.rly";
    const std::string ttb_file_ = "Antwerpen_Centraal_2021.ttb";
    const std::string ssn_file_ = "Antwerpen_Centraal_2021.ssn";
    const std::string doc_file_ = "README.md";
    const std::string graphic_file_ = "Antwerp.jpg";
    const std::string desc_ = "Simulation covering the lines from Antwerpen Centraal to St. Katelijne-Waver/Lier";
    const std::string display_name_ = "Antwerpen Centraal";
    const std::string country_code_fail_ = "LL";
    const std::string country_code_pass_ = "BE";
    const std::string signal_position_ = "left";
    const std::string name_ = "Simulation of Antwerp south";
    const date::year_month_day release_date_ = 2021_y/October/9;
    const std::string version_ = "1.0.0";
    const int year_ = 2021;
    const std::string out_file_name_ = "test_meta.toml";
    meta_.addContributor(cont_name_);
    meta_.setAuthor(author_name_);
    meta_.addImgFile(image_file_);
    meta_.addSSNFile(ssn_file_);
    meta_.addDocFile(doc_file_);
    meta_.addTTBFile(ttb_file_);
    meta_.setDescription(desc_);
    meta_.addGraphicFile(graphic_file_);
    meta_.setRLYFile(rly_file_);
    meta_.setDisplayName(display_name_);
    meta_.setYear(year_);
    meta_.setFactual(true);
    meta_.setReleaseDate(2021_y/October/9);
    meta_.setName(name_);
    meta_.setVersion(version_);
    meta_.setSignalPosition(signal_position_);
    ASSERT_EQ(meta_.contributors()[0], cont_name_);
    ASSERT_EQ(meta_.author(), author_name_);
    ASSERT_EQ(meta_.img_files()[0], image_file_);
    ASSERT_EQ(meta_.ttb_files()[0], ttb_file_);
    ASSERT_EQ(meta_.ssn_files()[0], ssn_file_);
    ASSERT_EQ(meta_.doc_files()[0], doc_file_);
    ASSERT_EQ(meta_.description(), desc_);
    ASSERT_EQ(meta_.display_name(), display_name_);
    ASSERT_EQ(meta_.name(), name_);
    ASSERT_EQ(meta_.graphic_files()[0], graphic_file_);
    ASSERT_EQ(meta_.year(), year_);
    ASSERT_EQ(meta_.rly_file(), rly_file_);
    ASSERT_TRUE(meta_.factual());
    EXPECT_THROW(meta_.setCountryCode(country_code_fail_), std::runtime_error);
    EXPECT_THROW(meta_.setDifficulty(6), std::runtime_error);
    EXPECT_NO_THROW(meta_.setCountryCode(country_code_pass_));
    EXPECT_NO_THROW(meta_.setDifficulty(3));
    ASSERT_EQ(meta_.country_code(), country_code_pass_);
    ASSERT_EQ(meta_.difficulty(), 3);
    ASSERT_EQ(meta_.release_date(), release_date_);
    ASSERT_EQ(meta_.version(), semver::version{version_});
    ASSERT_EQ(meta_.signal_position(), signal_position_);
    meta_.write(out_file_name_);
    ASSERT_TRUE(std::filesystem::exists(out_file_name_));
    const std::filesystem::path data_dir_(TEST_DATA_DIR);
    RailOSTools::Metadata new_file_(out_file_name_);
    RailOSTools::Metadata expected_(data_dir_ / std::filesystem::path("Antwerpen_Centraal.toml"));
    ASSERT_EQ(new_file_.data(), expected_.data());
    std::filesystem::remove(out_file_name_);
}
