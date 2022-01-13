cmake_minimum_required( VERSION 3.20 )
set( CMAKE_CXX_STANDARD 17 )
set( CMAKE_CXX_STANDARD_REQUIRED True )

option( BUILD_TESTS "Build Unit Tests" OFF )
option( CODE_COVERAGE "Enable Coverage" OFF )

project( rostools VERSION 0.4.0 LANGUAGES CXX )

set( ROSTOOLS rostools )
set( TOMLPP tomlplusplus )
set( SEMVER semver )
set( ROSTOOLS_STATIC_LIBRARY FALSE )

file( GLOB SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx )

set( EXTERNAL_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/external )

if( ROSTOOLS_STATIC_LIBRARY )
    add_library( ${ROSTOOLS} STATIC ${SRC_FILES} )
else()
    add_library( ${ROSTOOLS} SHARED ${SRC_FILES} )
endif()

target_include_directories( ${ROSTOOLS} PRIVATE ${EXTERNAL_SOURCES} )
target_include_directories( ${ROSTOOLS} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include )

# ------------------------- Installation on System --------------------------------- #

install(
    TARGETS ${ROSTOOLS}
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/rostools
)
install(
    DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/rostools
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
install( FILES ${CMAKE_CURRENT_SOURCE_DIR}/cmake/${ROSTOOLS}-config.cmake DESTINATION lib/rostools )

install( TARGETS ${ROSTOOLS} EXPORT ${ROSTOOLS} DESTINATION "${ROSTOOLS_LIBRARY_DEST}" )

target_include_directories( ${ROSTOOLS} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${EXTERNAL_SOURCES}>
    $<INSTALL_INTERFACE:include>
    $<INSTALL_INTERFACE:include>
)
include(CMakePackageConfigHelpers)
write_basic_package_version_file( ${CMAKE_CURRENT_BINARY_DIR}/${ROSTOOLS}-config-version.cmake
  COMPATIBILITY AnyNewerVersion
)

install( FILES ${CMAKE_CURRENT_BINARY_DIR}/${ROSTOOLS}-config-version.cmake DESTINATION lib/rostools )

install( EXPORT ${ROSTOOLS} DESTINATION "lib/rostools" )

add_subdirectory( tests EXCLUDE_FROM_ALL )
