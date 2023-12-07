CMAKE_MINIMUM_REQUIRED(VERSION 3.11)

PROJECT(
  {{ project.name|lower }}
{% if project.version %}  VERSION {{ project.version }}{% endif %}
{% if project.description %}  DESCRIPTION "{{ project.description }}"{% endif %}
{% if project.homepage_url %}  HOMEPAGE_URL "{{ project.homepage_url }}"{% endif %}
  LANGUAGES C CXX
)

FILE(GLOB SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

ADD_LIBRARY(
  ${PROJECT_NAME}
  SHARED
  ${SOURCE_FILES}
)

TARGET_INCLUDE_DIRECTORIES(
  ${PROJECT_NAME}
  PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)

TARGET_COMPILE_FEATURES(
  ${PROJECT_NAME}
  INTERFACE
    cxx_std_17
)

INSTALL(
  TARGETS
    ${PROJECT_NAME}
  LIBRARY DESTINATION
    lib
)

INSTALL(
  DIRECTORY
    ${CMAKE_CURRENT_SOURCE_DIR}/include
  DESTINATION
    include
  FILES_MATCHING PATTERN
    "*.hpp"
)

ENABLE_TESTING()
ADD_SUBDIRECTORY(test)
