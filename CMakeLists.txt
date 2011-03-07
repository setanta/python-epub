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

set(ARCHIVE_NAME python-epub)
add_custom_target(dist
    COMMAND mkdir -p "${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}" &&
            git log > "${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}/ChangeLog" &&
            git archive --prefix=${ARCHIVE_NAME}/ HEAD --format=tar --output="${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}.tar" &&
            tar -C "${CMAKE_BINARY_DIR}" --owner=root --group=root -r "${ARCHIVE_NAME}/ChangeLog" -f "${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}.tar" &&
            bzip2 -f9 "${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}.tar" &&
            echo "Source package created at ${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}.tar.bz2.\n"
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

if (NOT SITE_PACKAGE)
    execute_process(
        COMMAND ${SHIBOKEN_PYTHON_INTERPRETER} -c "from distutils import sysconfig; \\
            print sysconfig.get_python_lib(1,0,prefix='${CMAKE_INSTALL_PREFIX}')"
        OUTPUT_VARIABLE SITE_PACKAGE
        OUTPUT_STRIP_TRAILING_WHITESPACE)
    if (NOT SITE_PACKAGE)
        message(FATAL_ERROR "Could not detect Python module installation directory.")
    elseif (APPLE)
        message(STATUS "!!! The generated bindings will be installed on ${SITE_PACKAGE}, is it right!?")
    endif()
endif()

# uninstall target
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
               IMMEDIATE @ONLY)
add_custom_target(uninstall ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/epub.so DESTINATION ${SITE_PACKAGE})

