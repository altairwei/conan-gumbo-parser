from conans import ConanFile, CMake, tools
import sys, os, shutil

class GumboparserConan(ConanFile):
    name = "GumboParser"
    version = "0.10.1"
    license = "Apache License 2.0"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "An HTML5 parsing library in pure C99."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    exports_sources = ["CMakeLists.txt"]
    default_options = {'shared': False, 'fPIC': True}
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        url = 'https://github.com/google/gumbo-parser/archive/v%s.tar.gz' % self.version
        tools.get(url)
        os.rename("gumbo-parser-" + self.version, self._source_subfolder)
        shutil.copy("CMakeLists.txt",
                    os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include/gumbo-parser", 
            src=os.path.join(self._source_subfolder, "src"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

