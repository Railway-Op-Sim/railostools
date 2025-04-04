include(FetchContent)

FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.16.0
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

set( RAILOSTOOLS_TESTS tests )

file( GLOB TEST_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx )


add_executable( ${RAILOSTOOLS_TESTS} ${TEST_SRCS} )
set_target_properties( ${RAILOSTOOLS_TESTS} PROPERTIES OUTPUT_NAME run-tests )
target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC gtest_main )
target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC ${RAILOSTOOLS} )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_compile_definitions( ${RAILOSTOOLS_TESTS} PRIVATE TEST_DATA_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/data\" )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${tomlplusplus_SOURCE_DIR} ${semver_SOURCE_DIR}/include )

add_test( NAME RailOSTests COMMAND $<TARGET_FILE:${RAILOSTOOLS_TESTS}> )

include( GoogleTest )
gtest_discover_tests( ${RAILOSTOOLS_TESTS} )
