cmake_minimum_required( VERSION 3.20 )
set( CMAKE_CXX_STANDARD 17 )
set( CMAKE_CXX_STANDARD_REQUIRED True )

option( BUILD_TESTS "Build Unit Tests" OFF )
option( CODE_COVERAGE "Enable Coverage" OFF )

project( rostools VERSION 0.4.0 LANGUAGES CXX )

set( TOMLPP tomlplusplus )
set( SEMVER semver )

file( GLOB SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.cxx )

set( EXTERNAL_SOURCES ${CMAKE_SOURCE_DIR}/external )

add_library( ${PROJECT_NAME} ${SRC_FILES} )
target_include_directories( ${PROJECT_NAME} PUBLIC ${EXTERNAL_SOURCES} )
target_include_directories( ${PROJECT_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/include )

install(
    TARGETS ${PROJECT_NAME}
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/rostools
)
install(
    DIRECTORY ${CMAKE_SOURCE_DIR}/include/rostools
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

if( BUILD_TESTS )
    add_subdirectory( tests EXCLUDE_FROM_ALL )
endif()
