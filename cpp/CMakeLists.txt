cmake_minimum_required( VERSION 3.20 )
set( CMAKE_CXX_STANDARD 17 )
set( CMAKE_CXX_STANDARD_REQUIRED True )

option( RAILOSTOOLS_BUILD_TESTS "Build Unit Tests" OFF )
option( RAILOSTOOLS_CODE_COVERAGE "Enable Coverage" OFF )
set( RAILOSTOOLS railostools )

project( ${RAILOSTOOLS} VERSION 0.6.1 LANGUAGES CXX )
set( TOMLPP tomlplusplus )
set( SEMVER semver )

if( NOT DEFINED RAILOSTOOLS_STATIC_LIBRARY )
    set( RAILOSTOOLS_STATIC_LIBRARY OFF )
endif()

message( STATUS "[RailOSTools]" )
message( STATUS "\t- Use Static Library: ${RAILOSTOOLS_STATIC_LIBRARY}" )
message( STATUS "\t- Build Tests: ${RAILOSTOOLS_BUILD_TESTS}" )
message( STATUS "\t- Test Coverage: ${RAILOSTOOLS_CODE_COVERAGE}" )

file( GLOB_RECURSE SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx )

set( EXTERNAL_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/external )

if( RAILOSTOOLS_STATIC_LIBRARY )
    add_library( ${RAILOSTOOLS} STATIC ${SRC_FILES} )
else()
    add_library( ${RAILOSTOOLS} SHARED ${SRC_FILES} )
endif()

target_include_directories( ${RAILOSTOOLS} PRIVATE ${EXTERNAL_SOURCES} )
target_include_directories( ${RAILOSTOOLS} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include )

# ------------------------- Installation on System --------------------------------- #

install(
    TARGETS ${RAILOSTOOLS}
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/${RAILOSTOOLS}
)
install(
    DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/${RAILOSTOOLS}
    DESTINATION include
    PATTERN "*.hxx"
)
install(
    DIRECTORY ${EXTERNAL_SOURCES}/tomlplusplus
    DESTINATION include
    PATTERN "*.hpp"
)
install(
    DIRECTORY ${EXTERNAL_SOURCES}/semver
    DESTINATION include
    PATTERN "*.hpp"
)
install( FILES ${CMAKE_CURRENT_SOURCE_DIR}/cmake/${RAILOSTOOLS}-config.cmake DESTINATION lib/${RAILOSTOOLS} )

install( TARGETS ${RAILOSTOOLS} EXPORT ${RAILOSTOOLS} DESTINATION "${RAILOSTOOLS_LIBRARY_DEST}" )

target_include_directories( ${RAILOSTOOLS} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${EXTERNAL_SOURCES}>
    $<INSTALL_INTERFACE:include>
    $<INSTALL_INTERFACE:include>
)
include(CMakePackageConfigHelpers)
write_basic_package_version_file( ${CMAKE_CURRENT_BINARY_DIR}/${RAILOSTOOLS}-config-version.cmake
  COMPATIBILITY AnyNewerVersion
)

install( FILES ${CMAKE_CURRENT_BINARY_DIR}/${RAILOSTOOLS}-config-version.cmake DESTINATION lib/${RAILOSTOOLS} )

install( EXPORT ${RAILOSTOOLS} DESTINATION "lib/${RAILOSTOOLS}" )

if( RAILOSTOOLS_BUILD_TESTS )
    add_subdirectory( tests )
endif()
