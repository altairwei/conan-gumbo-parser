from conans import ConanFile, CMake, tools
import sys, os, shutil

class GumboConan(ConanFile):
    name = "Gumbo"
    version = "0.10.1"
    license = "Apache License 2.0"
    url = "https://github.com/altairwei/conan-gumbo-parser"
    description = "An HTML5 parsing library in pure C99."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    exports_sources = ["CMakeLists.txt"]
    default_options = {'shared': False}
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
            self.options.remove("shared")

    def source(self):
        url = 'https://github.com/google/gumbo-parser/archive/v%s.tar.gz' % self.version
        tools.get(url)
        os.rename("gumbo-parser-" + self.version, self._source_subfolder)
        shutil.copy("CMakeLists.txt",
                    os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        if self.settings.os == "Windows":
            #cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
            # I don't know why kGumboDefaultOptions is not exported from dynamic library on MSVC.
            # Therefore you should avoid using Gumbo dynamic library, otherwise Error LNK2019 or
            # Error LNK2019 will generated by MSVC link tool.
            cmake.definitions["BUILD_SHARED_LIBS"] = False
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include/gumbo-parser", 
            src=os.path.join(self._source_subfolder, "src"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.exp", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

