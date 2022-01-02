include(FetchContent)

FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

set( TESTS Test${PROJECT_NAME} )

file( GLOB TEST_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx )

enable_testing()

add_executable( ${TESTS} ${TEST_SRCS} )
target_link_libraries( ${TESTS} PUBLIC gtest_main )
target_link_libraries( ${TESTS} PUBLIC ${PROJECT_NAME} )
target_include_directories( ${TESTS} PUBLIC ${CMAKE_SOURCE_DIR}/include )
target_compile_definitions( ${TESTS} PRIVATE TEST_DATA_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/data\" )
target_include_directories( ${TESTS} PUBLIC ${tomlplusplus_SOURCE_DIR} ${semver_SOURCE_DIR}/include )
target_include_directories( ${TESTS} PRIVATE ${CMAKE_SOURCE_DIR}/include )

include( GoogleTest )
gtest_discover_tests( ${TESTS} )
