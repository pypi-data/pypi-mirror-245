#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "drjit-core" for configuration "Release"
set_property(TARGET drjit-core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(drjit-core PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/drjit/drjit-core.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "nanothread"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/drjit/drjit-core.dll"
  )

list(APPEND _cmake_import_check_targets drjit-core )
list(APPEND _cmake_import_check_files_for_drjit-core "${_IMPORT_PREFIX}/drjit/drjit-core.lib" "${_IMPORT_PREFIX}/drjit/drjit-core.dll" )

# Import target "nanothread" for configuration "Release"
set_property(TARGET nanothread APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nanothread PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/drjit/nanothread.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/drjit/nanothread.dll"
  )

list(APPEND _cmake_import_check_targets nanothread )
list(APPEND _cmake_import_check_files_for_nanothread "${_IMPORT_PREFIX}/drjit/nanothread.lib" "${_IMPORT_PREFIX}/drjit/nanothread.dll" )

# Import target "drjit-autodiff" for configuration "Release"
set_property(TARGET drjit-autodiff APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(drjit-autodiff PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/drjit/drjit-autodiff.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "drjit-core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/drjit/drjit-autodiff.dll"
  )

list(APPEND _cmake_import_check_targets drjit-autodiff )
list(APPEND _cmake_import_check_files_for_drjit-autodiff "${_IMPORT_PREFIX}/drjit/drjit-autodiff.lib" "${_IMPORT_PREFIX}/drjit/drjit-autodiff.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
