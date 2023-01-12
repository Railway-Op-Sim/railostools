include(FetchContent)

FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

set( RAILOSTOOLS_TESTS tests )

file( GLOB TEST_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx )

enable_testing()

add_executable( ${RAILOSTOOLS_TESTS} ${TEST_SRCS} )
set_target_properties( ${RAILOSTOOLS_TESTS} PROPERTIES OUTPUT_NAME run-tests )
target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC gtest_main )
target_link_libraries( ${RAILOSTOOLS_TESTS} PUBLIC ${RAILOSTOOLS} )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_compile_definitions( ${RAILOSTOOLS_TESTS} PRIVATE TEST_DATA_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/data\" )
target_include_directories( ${RAILOSTOOLS_TESTS} PUBLIC ${tomlplusplus_SOURCE_DIR} ${semver_SOURCE_DIR}/include )

include( GoogleTest )
gtest_discover_tests( ${RAILOSTOOLS_TESTS} )
