cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(FetchContent)


# Put CSPICE libs inside our package, not top-level lib/
set(CMAKE_INSTALL_LIBDIR "test_cyice" CACHE INTERNAL "")

if(MSVC)
  # Force DLLs to install alongside LIBs instead of bin/
  set(CMAKE_INSTALL_BINDIR "test_cyice" CACHE INTERNAL "")
endif()

# Put CSPICE headers somewhere harmless in our package
set(CMAKE_INSTALL_INCLUDEDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")

# Also redirect data root to avoid polluting share/ etc.
set(CMAKE_INSTALL_DATAROOTDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")

# Bring in your CSPICE CMake project 
FetchContent_Declare(
  cspice
  GIT_REPOSITORY https://github.com/AndrewAnnex/cspice-cmake-spiceypy.git
  GIT_TAG        1975069e3a43391a664dadf7034c5f24d0142cf8    # or a release tag/sha
)
FetchContent_MakeAvailable(cspice)

# Convert pyx to c
set(PYX_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/test_cyice/test_cyice.pyx)
set(PXD_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/test_cyice/test_cyice.pxd)
set(C_FILE ${CMAKE_CURRENT_BINARY_DIR}/test_cyice.c)

add_custom_command(
  OUTPUT ${C_FILE}
  COMMAND Python::Interpreter -m cython ${PYX_FILE} --output-file ${C_FILE}
  DEPENDS ${PYX_FILE} ${PXD_FILE}
  COMMENT "Cythonizing ${PYX_FILE} to ${C_FILE}"
  VERBATIM)

# Make Python extension
python_add_library(test_cyice MODULE ${C_FILE} WITH_SOABI)

# Link to the CSPICE target exposed by the subproject
target_include_directories(test_cyice PRIVATE ${Python_NumPy_INCLUDE_DIRS})

# Link CSPICE + math lib (only on UNIX)
if(UNIX AND NOT WIN32 AND NOT MINGW)
    target_link_libraries(test_cyice PRIVATE cspice m)
else()
    target_link_libraries(test_cyice PRIVATE cspice)
endif()

# Fix runtime search paths so extension finds libcspice in same dir
if(APPLE)
  set_target_properties(test_cyice PROPERTIES
    INSTALL_RPATH "@loader_path"
    BUILD_WITH_INSTALL_RPATH ON
  )
elseif(UNIX)
  set_target_properties(test_cyice PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH ON
  )
endif()

# install cspice, or don't and rely on the lib dir added to the wheel
#install(TARGETS cspice DESTINATION test_cyice/)
# install test_cyice
install(TARGETS test_cyice DESTINATION test_cyice/)