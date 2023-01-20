find_package(GTest)

if( NOT GTest_FOUND )
  message( STATUS "GTest not found locally, retrieving...")
  include(FetchContent)

  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.12.1
  )

  # For Windows: Prevent overriding the parent project's compiler/linker settings
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

  FetchContent_MakeAvailable(googletest)
endif()

set( RAILOSTOOLS_TESTS tests )

file( GLOB TEST_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx )

enable_testing()

add_executable( ${RAILOSTOOLS_TESTS} ${TEST_SRCS} )

set_target_properties( ${RAILOSTOOLS_TESTS} PROPERTIES OUTPUT_NAME run-tests )

if( NOT GTest_FOUND )
  target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC gtest_main )
else()
  target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC GTest::gtest GTest::gtest_main )
endif()
target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC ${RAILOSTOOLS} )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_compile_definitions( ${RAILOSTOOLS_TESTS} PRIVATE TEST_DATA_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/data\" )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${tomlplusplus_SOURCE_DIR} ${semver_SOURCE_DIR}/include )

include( GoogleTest )
gtest_discover_tests( ${RAILOSTOOLS_TESTS} )
add_test( ${RAILOSTOOLS_TESTS} ${RAILOSTOOLS_TESTS} )
