project(pyepub)

cmake_minimum_required(VERSION 2.6)

find_package(GeneratorRunner REQUIRED)
find_package(Shiboken REQUIRED)
find_library(EPUB_LIBRARY epub)
find_path(EPUB_INCLUDE_DIR epub.h)

set(epub_SRC
    ${CMAKE_CURRENT_BINARY_DIR}/epub/epub_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/epub/epub_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/epub/eiterator_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/epub/titerator_wrapper.cpp
)

add_library(epub MODULE ${epub_SRC})
set_property(TARGET epub PROPERTY PREFIX "")
include_directories(epub
                    ${CMAKE_CURRENT_SOURCE_DIR}
                    ${SHIBOKEN_PYTHON_INCLUDE_DIR}
                    ${SHIBOKEN_INCLUDE_DIR}
                    ${EPUB_INCLUDE_DIR}
)
target_link_libraries(epub
                      ${SHIBOKEN_PYTHON_LIBRARIES}
                      ${SHIBOKEN_LIBRARY}
                      ${EPUB_LIBRARY}
)

add_custom_command(OUTPUT ${epub_SRC}
                   COMMAND ${GENERATORRUNNER_BINARY} --generator-set=shiboken
                   --include-paths=${EPUB_INCLUDE_DIR}:${CMAKE_CURRENT_SOURCE_DIR} # take this out!
                   --output-directory=${CMAKE_CURRENT_BINARY_DIR}
                   ${CMAKE_SOURCE_DIR}/epub_global.h
                   ${CMAKE_SOURCE_DIR}/typesystem_epub.xml
                   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                   COMMENT "Running generator for libepub..."
)

enable_testing()
add_subdirectory(tests)

