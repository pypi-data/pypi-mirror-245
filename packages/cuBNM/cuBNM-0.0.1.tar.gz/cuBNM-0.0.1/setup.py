from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.spawn import find_executable
import subprocess
import os
import fnmatch
import sys
from pathlib import Path
import numpy as np
import GPUtil

PROJECT = os.path.abspath(os.path.dirname(__file__))

# specify installation options
many_nodes = os.environ.get("CUBNM_MANY_NODES") is not None


def find_file(file_name, search_path):
    result = []
    for root, dirs, files in os.walk(search_path):
        for name in fnmatch.filter(files, file_name):
            result.append(os.path.join(root, name))
    return result

# detect if there are GPUs
def has_gpus(method='nvcc'):
    if method == 'gputil':
        return len(GPUtil.getAvailable()) > 0
    elif method == 'nvcc':
        # can be useful for compiling code on a
        # non-GPU system for running it later
        # on GPUs
        if find_executable("nvcc"):
                return True
        else:
            return False

gpu_enabled = has_gpus()
omp_enabled = not (('CIBUILDWHEEL' in os.environ) or ('CUBNM_NO_OMP' in os.environ))

# Write the flags to a temporary _flags.py file
with open(os.path.join(PROJECT, "src", "cuBNM", "_setup_flags.py"), "w") as flag_file:
    flag_file.write(
        "\n".join(
            [f"many_nodes_flag = {many_nodes}", 
             f"gpu_enabled_flag = {gpu_enabled}",
             f"omp_enabled_flag = {omp_enabled}", # not currently used
            ]
        )
    )

# determine libraries shared between GPU and CPU versions
libraries = ["m"]
if omp_enabled:
    libraries.append("gomp")

_CC = os.environ.get("CC", "gcc") # this will be used for compiling GSL + restoring os $CC and $CXX at the end
_CXX = os.environ.get("CXX", "g++")
os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

# create lists of include directories
shared_includes = [
    os.path.join(PROJECT,"include"),
    os.path.join(PROJECT, "src", "cpp"),
    np.get_include(),
    os.path.join(os.environ.get('HOME', '/root'), 'miniconda', 'include') # added for conda-based cibuildwheel
]
gpu_includes = [
    # with cibuildwheel these do not exist
    # and cuda includes are in ~/miniconda/include
    "/usr/lib/cuda/include",
    "/usr/include/cuda",
]
all_includes = shared_includes + gpu_includes

# extra compile args shared between CPU and GPU
extra_compile_args = [
    "-std=c++11",
    "-O3",
    "-m64",
    "-D NOISE_SEGMENT",
]
if omp_enabled:
    extra_compile_args += [
        "-fopenmp",
        "-D OMP_ENABLED"
    ]

if gpu_enabled:
    print("Compiling for GPU+CPU")
    libraries += ["bnm", "cudart_static"]
    bnm_ext = Extension(
        "cuBNM.core",
        [os.path.join("src","cpp", "run_simulations.cpp")],
        language="c++",
        extra_compile_args=extra_compile_args+["-D GPU_ENABLED"],
        libraries=libraries,
        include_dirs=all_includes,
        library_dirs=[
            "/usr/lib/cuda", 
            os.path.join(PROJECT, "src", "cuda"),
            os.path.join(os.environ.get('HOME', '/root'), 'miniconda', 'lib') # added for conda-based cibuildwheel
        ],
    )
else:
    print("Compiling for CPU")
    bnm_ext = Extension(
        "cuBNM.core",
        [os.path.join("src","cpp", "run_simulations.cpp")],
        language="c++",
        extra_compile_args=extra_compile_args,
        libraries=libraries,
        include_dirs=shared_includes,
        library_dirs=[
            os.path.join(os.environ.get('HOME', '/root'), 'miniconda', 'lib') # added for conda-based cibuildwheel
        ],
    )

# extend build_ext to also build GSL (if needed) and compile GPU code
class build_ext_gsl_cuda(build_ext):
    def build_extensions(self):
        # Build GSL (if needed)
        # search for libgsl.a and libgslcblas.a in some common paths
        lib_dirs = [
            "/usr/lib", 
            "/lib", 
            "/usr/local/lib",
            os.path.join(os.environ.get('HOME', '/root'), 'miniconda', 'lib'), # cibuildwheel
            # TODO: identify and search current conda env
            os.path.join(os.environ.get('HOME', '/root'), '.cuBNM', 'gsl', 'build', 'lib'), # has been installed before by cuBNM
        ] \
            + os.environ.get("LIBRARY_PATH","").split(":") \
            + os.environ.get("LD_LIBRARY_PATH","").split(":")
        found_gsl = False
        for lib_dir in lib_dirs:
            if ((lib_dir!='') & os.path.exists(lib_dir)):
                r = find_file('libgsl.a', lib_dir)
                if r: # assuming libgsl.a and libgslcblas.a are in the same directory
                    found_gsl = True
                    GSL_LIB_DIR = os.path.dirname(r[0])
                    print(f"Found libgsl.a and libgslcblas.a in {GSL_LIB_DIR}")
                    break
        if not found_gsl:
            print("Downloading and building GSL")
            try:
                gsl_dir = os.path.join(os.path.expanduser('~'), '.cuBNM', 'gsl')
                os.makedirs(gsl_dir, exist_ok=True)
            except OSError:
                gsl_dir = os.path.join(os.path.abspath(self.build_lib), 'gsl')
                os.makedirs(gsl_dir, exist_ok=True)
            gsl_tar = os.path.join(gsl_dir, 'gsl-2.7.tar.gz')
            gsl_src = os.path.join(gsl_dir, 'gsl-2.7')
            gsl_build = os.path.join(gsl_dir, 'build')
            os.makedirs(gsl_build, exist_ok=True)
            # use gcc (or other default C compilers) as with g++ set as CC
            # GSL compilation fails. Note that this will not affect the compiler
            # of bnm extension as it has already been set to g++
            os.environ["CC"] = _CC
            gsl_setup_commands = [
                f"wget https://mirror.ibcp.fr/pub/gnu/gsl/gsl-2.7.tar.gz -O {gsl_tar}",
                f"cd {gsl_dir} && tar -xf {gsl_tar} &&"
                f"cd {gsl_src} && ./configure --prefix={gsl_build} --enable-shared &&"
                f"make && make install",
            ]
            for command in gsl_setup_commands:
                result = subprocess.run(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
                # print(f"Command: {command}")
                # print(f"Return Code: {result.returncode}")
                # print(f"stderr:\n{result.stderr}")
            GSL_LIB_DIR = os.path.join(gsl_build, 'lib')
        # Compile CUDA code into libbnm.a
        if gpu_enabled:
            cuda_dir = os.path.join(PROJECT, 'src', 'cuda')

            if 'CUBNM_MANY_NODES' in os.environ:
                add_flags = "-D NOISE_SEGMENT MANY_NODES"
            else:
                add_flags = "-D NOISE_SEGMENT"
            include_flags = " ".join([f"-I {p}" for p in all_includes])
            compile_commands = [
                f"nvcc -c -rdc=true -std=c++11 --compiler-options '-fPIC' -o {cuda_dir}/bnm_tmp.o {cuda_dir}/bnm.cu "
                    f"{include_flags} {add_flags}",
                f"nvcc -dlink --compiler-options '-fPIC' -o {cuda_dir}/bnm.o {cuda_dir}/bnm_tmp.o "
                    f"-L {GSL_LIB_DIR} -lm -lgsl -lgslcblas -lcudart_static",
                f"rm -f {cuda_dir}/libbnm.a",  # remove the previously created .a
                f"ar cru {cuda_dir}/libbnm.a {cuda_dir}/bnm.o {cuda_dir}/bnm_tmp.o",
                f"ranlib {cuda_dir}/libbnm.a",
            ]

            for command in compile_commands:
                print(command)
                result = subprocess.run(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
                print(f"Return Code: {result.returncode}")
                if result.stderr:
                    print(f"Standard Error:\n{result.stderr}")
        # Continue with Python extension build
        # add libgsl.a and libgslcblas.a to the compiler objects for
        # their explicit linking
        self.compiler.objects.append(os.path.join(GSL_LIB_DIR, 'libgsl.a'))
        self.compiler.objects.append(os.path.join(GSL_LIB_DIR, 'libgslcblas.a'))
        # self.compiler.add_library_dir(GSL_LIB_DIR) # uncomment for dynamic linking of gsl
        super().build_extensions()

setup(
    ext_modules=[bnm_ext],
    cmdclass={
        'build_ext': build_ext_gsl_cuda,
    },
)

# restore OS's original $CC and $CXX
os.environ['CC'] = _CC
os.environ['CXX'] = _CXX