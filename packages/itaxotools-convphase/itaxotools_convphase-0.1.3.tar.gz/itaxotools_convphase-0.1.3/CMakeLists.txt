cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C CXX)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
include(ExternalProject)

find_package(
    Python
    COMPONENTS Interpreter Development.Module
    REQUIRED)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
    add_compile_options(-pedantic)
endif()

set(IS_ARM64 false)
set(IS_M64 false)
set(IS_M32 false)
set(IS_UNIVERSAL false)

if (DEFINED ENV{ARCHFLAGS} AND NOT "$ENV{ARCHFLAGS}" STREQUAL "")
    # We are cross-compiling, ARCHFLAGS like "-arch arm64"
    if("$ENV{ARCHFLAGS}" MATCHES ".*x86_64.*")
        set(HXCPP_ARCH HXCPP_M64)
        set(IS_M64 true)
    endif()
    if("$ENV{ARCHFLAGS}" MATCHES ".*arm64.*")
        set(HXCPP_ARCH HXCPP_ARM64)
        set(IS_ARM64 true)
    endif()
    if(IS_ARM64 AND IS_M64)
        set(IS_UNIVERSAL true)
    endif()
else()
    # Compile for system processor
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|AMD64")
        set(HXCPP_ARCH HXCPP_M64)
        set(IS_M64 true)
    elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64|aarch64")
        set(HXCPP_ARCH HXCPP_ARM64)
        set(IS_ARM64 true)
    elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "win32|x86|i386|i686")
        set(HXCPP_ARCH HXCPP_M32)
        set(IS_M32 true)
    endif()
endif()

message("CMake environment variables:")
message("CMAKE_SYSTEM_PROCESSOR: " ${CMAKE_SYSTEM_PROCESSOR})
message("ARCHFLAGS: " "$ENV{ARCHFLAGS}")
message("IS_ARM64: " ${IS_ARM64})
message("IS_M64: " ${IS_M64})
message("IS_M32: " ${IS_M32})
message("IS_UNIVERSAL: " ${IS_UNIVERSAL})

if(IS_UNIVERSAL)
    message(FATAL_ERROR "Cannot generate universal2 library directly, use delocate-fuse")
endif()

# SeqPHASE

ExternalProject_Add(
    SeqPhase
    PREFIX ${CMAKE_BINARY_DIR}/seqphase
    SOURCE_DIR ${PROJECT_SOURCE_DIR}/src/SeqPHASE/haxe
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND "")

ExternalProject_Add_Step(
    SeqPhase haxe
    COMMAND haxe --cpp <BINARY_DIR> -D static_link -D ABI=-MD -D ${HXCPP_ARCH}
            -D HAXE_OUTPUT_FILE=${CMAKE_SHARED_LIBRARY_PREFIX}seqphase
            SeqPhase1.hx SeqPhase2.hx
    WORKING_DIRECTORY <SOURCE_DIR>)


# PHASE

file(GLOB PHASE_SOURCES_CPP ${PROJECT_SOURCE_DIR}/src/phase/src/phase*/*.cpp)
file(GLOB PHASE_SOURCES_C ${PROJECT_SOURCE_DIR}/src/phase/src/phase*/*.c)
set(PHASE_SOURCES ${PHASE_SOURCES_CPP} ${PHASE_SOURCES_C})

file(GLOB PHASE_INCLUDE_DIRS
    ${PROJECT_SOURCE_DIR}/src/phase/src/phase*
    ${PROJECT_SOURCE_DIR}/src/itaxotools/_convphase/include)

add_library(phase STATIC ${PHASE_SOURCES})
target_include_directories(phase PUBLIC ${PHASE_INCLUDE_DIRS})
set_property(TARGET phase PROPERTY CXX_STANDARD 14)

target_compile_definitions(
    phase PUBLIC
    -D CP_PHASE_LIB)

target_compile_definitions(
    phase PRIVATE
    -D CP_PHASE_NOFILE
    -D CP_PHASE_DISABLE_COUT
    -D CP_PHASE_DISABLE_CERR)


# ConvPhase

execute_process(
    COMMAND haxelib libpath hxcpp
    OUTPUT_VARIABLE HAXELIB_HXCPP_PATH
    OUTPUT_STRIP_TRAILING_WHITESPACE)

file(GLOB PYMODULE_SOURCES
    ${PROJECT_SOURCE_DIR}/src/itaxotools/_convphase/src/*.cpp)
set(PYMODULE_INCLUDE_DIRS
    ${PROJECT_SOURCE_DIR}/src/itaxotools/_convphase/include
    ${CMAKE_BINARY_DIR}/seqphase/src/SeqPhase-build/include
    ${HAXELIB_HXCPP_PATH}/include)

python_add_library(_convphase MODULE ${PYMODULE_SOURCES} WITH_SOABI)
target_include_directories(_convphase PRIVATE ${PYMODULE_INCLUDE_DIRS})
target_link_directories(_convphase PRIVATE ${CMAKE_BINARY_DIR}/seqphase/src/SeqPhase-build)
target_link_libraries(_convphase PRIVATE seqphase phase)
set_property(TARGET _convphase PROPERTY CXX_STANDARD 17)
add_dependencies(_convphase SeqPhase)

target_compile_definitions(
    _convphase PRIVATE
    -D ${HXCPP_ARCH}
    -D HXCPP_API_LEVEL=400)

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    target_compile_definitions(_convphase PRIVATE -DHX_WINDOWS)
endif()


install(TARGETS _convphase DESTINATION itaxotools)
