CMAKE_MINIMUM_REQUIRED(VERSION 3.11)

PROJECT(
  {{ project.name|lower }}
{% if project.version %}  VERSION {{ project.version }}{% endif %}
{% if project.description %}  DESCRIPTION "{{ project.description }}"{% endif %}
{% if project.homepage_url %}  HOMEPAGE_URL "{{ project.homepage_url }}"{% endif %}
  LANGUAGES C CXX
)

FILE(GLOB SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

ADD_EXECUTABLE(
  ${PROJECT_NAME}
  ${SOURCE_FILES}
)

TARGET_INCLUDE_DIRECTORIES(
  ${PROJECT_NAME}
  INTERFACE
    $<BUILD_INTERFACE:${${PROJECT_NAME}_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

TARGET_COMPILE_FEATURES(
  ${PROJECT_NAME}
  INTERFACE
    cxx_std_17
)

INSTALL(
  TARGETS
    ${PROJECT_NAME}
  RUNTIME DESTINATION
    bin
)

ENABLE_TESTING()
ADD_SUBDIRECTORY(test)
