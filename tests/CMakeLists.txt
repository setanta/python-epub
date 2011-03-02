macro(add_epub_test name)
    add_test(${name} ${SHIBOKEN_PYTHON_INTERPRETER} ${CMAKE_CURRENT_SOURCE_DIR}/${name}_test.py)
    set_tests_properties(${name} PROPERTIES ENVIRONMENT "PYTHONPATH=${pyepub_BINARY_DIR}")
endmacro(add_epub_test)

add_epub_test(basic)
add_epub_test(contents)
add_epub_test(metadata)
add_epub_test(toc)
add_epub_test(version)

