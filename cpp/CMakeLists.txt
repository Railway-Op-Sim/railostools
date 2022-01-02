cmake_minimum_required( VERSION 3.20 )
set( CMAKE_CXX_STANDARD 17 )
set( CMAKE_CXX_STANDARD_REQUIRED True )

option( BUILD_TESTS "Build Unit Tests" OFF )
option( CODE_COVERAGE "Enable Coverage" OFF )

project( rostools VERSION 0.4.0 LANGUAGES CXX )

set( TOMLPP tomlplusplus )
set( SEMVER semver )

file( GLOB SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.cxx )

include( FetchContent )
FetchContent_Declare(
    ${TOMLPP}
    GIT_REPOSITORY https://github.com/marzer/tomlplusplus.git
    GIT_TAG        v2.5.0
)
FetchContent_MakeAvailable( ${TOMLPP} )

include( FetchContent )
FetchContent_Declare(
    ${SEMVER}
    GIT_REPOSITORY https://github.com/Neargye/semver.git
    GIT_TAG         v0.3.0
)
FetchContent_MakeAvailable( ${SEMVER} )

add_library( ${PROJECT_NAME} ${SRC_FILES} )
target_include_directories( ${PROJECT_NAME} PUBLIC ${tomlplusplus_SOURCE_DIR} ${semver_SOURCE_DIR}/include )
target_include_directories( ${PROJECT_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/include )

if( BUILD_TESTS )
    add_subdirectory( tests )
endif()
