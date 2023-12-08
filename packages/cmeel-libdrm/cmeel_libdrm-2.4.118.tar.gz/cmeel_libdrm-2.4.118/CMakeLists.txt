cmake_minimum_required(VERSION 3.20)

set(NAME libdrm)
set(VERSION 2.4.118)
set(EXT tar.xz)
set(HASH d65000b9afd5780961a3f65db973eaa39556d434)

project(cmeel-${NAME} VERSION ${VERSION})

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://dri.freedesktop.org/${NAME}/${NAME}-${VERSION}.${EXT}"
  URL_HASH "SHA1=${HASH}"
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  BUILD_IN_SOURCE OFF
  CONFIGURE_COMMAND "meson" "setup" "--prefix=${CMAKE_INSTALL_PREFIX}"
                    "../${NAME}"
  BUILD_COMMAND "ninja"
  TEST_COMMAND "ninja" "test"
  INSTALL_COMMAND "ninja" "install")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-${NAME}/)
