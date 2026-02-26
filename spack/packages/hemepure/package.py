# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Hemepure(CMakePackage):
    """HemeLB is a high performance lattice-Boltzmann solver optimized for
    simulating blood flow through sparse geometries, such as those found in the
    human vasculature. It is routinely deployed on powerful supercomputers,
    scaling to hundreds of thousands of cores even for complex geometries.
    HemeLB has traditionally been used to model cerebral bloodflow and vascular
    remodelling in retinas, but is now being applied to simulating the fully
    coupled human arterial and venous trees.

    HemePure is a optimized verion of HemeLB with improved memory, compilation
    and scaling"""

    homepage = "https://github.com/UCL-CCS/HemePure"
    url = "https://github.com/UCL-CCS/HemePure"
    git = "https://github.com/UCL-CCS/HemePure.git"

    maintainers("nicolin", "connoraird", "tkoskela")
    license("BSD-3-Clause", checked_by="connoraird")

    version("master", branch="master")

    depends_on("cmake@3.18:")  # Or later
    depends_on("openmpi@4:")
    depends_on("boost@1.86:+mpi")
    depends_on("tinyxml")
    depends_on("libtirpc")
    depends_on("parmetis")
    depends_on("metis", when="+parmetis")
    depends_on("ctemplate")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Post Processing
    variant("gmyplus", default=False, description="Use GMY+ format")
    variant("parmetis", default=False, description="Use ParMETIS")

    # Solver Compute
    variant(
        "simd",
        default="auto",
        description="Use SIMD instrinsics",
        values=("sse3", "avx2", "avx512", "auto"),
    )
    variant(
        "mpi_call", default=False, description="Use standard MPI functions when reading blocks"
    )
    variant(
        "mpi_win", default=False, description="Use MPI Domain Split to help load large domains"
    )
    variant("big_mpi", default=False, description="Use Domain Split to help load large domains")

    # Solver BC Vel or Pressure
    # variant('pressure_bc', default=False, description='Use Velocity Boundary Conditions')
    variant(
        "wall_boundary",
        default="SIMPLEBOUNCEBACK",
        description="Boundary conditions at walls",
        values=("BFL", "GZS", "SIMPLEBOUNCEBACK", "JUNKYANG", "GZSElastic"),
    )
    variant(
        "inlet_boundary",
        default="LADDIOLET",
        description="Boundary conditions at inlets",
        values=("NASHZEROTHORDERPRESSUREIOLET", "LADDIOLET"),
    )
    variant(
        "wall_inlet_boundary",
        default="LADDIOLETSBB",
        description="Boundary conditions at wall-inlet corners",
        values=(
            "NASHZEROTHORDERPRESSURESBB",
            "NASHZEROTHORDERPRESSUREBFL",
            "LADDIOLETSBB",
            "LADDIOLETBFL",
            "NASHZEROTHORDERPRESSUREGZSE",
            "LADDIOLETGZSE",
        ),
    )
    variant(
        "outlet_boundary",
        default="NASHZEROTHORDERPRESSUREIOLET",
        description="Boundary conditions at outlets",
        values=("NASHZEROTHORDERPRESSUREIOLET", "LADDIOLET"),
    )
    variant(
        "wall_outlet_boundary",
        default="NASHZEROTHORDERPRESSURESBB",
        description="Boundary conditions at wall-outlet corners",
        values=(
            "NASHZEROTHORDERPRESSURESBB",
            "NASHZEROTHORDERPRESSUREBFL",
            "LADDIOLETSBB",
            "LADDIOLETBFL",
            "NASHZEROTHORDERPRESSUREGZSE",
            "LADDIOLETGZSE",
        ),
    )

    # Lagranian Tracking
    variant("tracer", default=True, description="Use particles as tracers")
    variant("velocity_weight", default=False, description="Use velocity weights file")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        # Setting CMAKE_C_COMILER and CMAKE_CXX_COMPILER seems to mess up include paths for dependencies
        # It's better to let spack set them.
        # CMAKE_BUILD_TYPE is provided as a variant by CMakePackage

        args = [
            self.define("CMAKE_CXX_EXTENSIONS", "OFF"),
            self.define("HEMELB_COMPUTE_ARCHITECTURE", "NEUTRAL"),
            self.define("HEMELB_USE_MPI_PARALLEL_IO", "ON"),
            self.define("HEMELB_USE_VELOCITY_WEIGHTS_FILE", "ON"),
            self.define("HEMELB_LOG_LEVEL", "Info"),
            self.define_from_variant("HEMELB_USE_PARMETIS", "parmetis"),
            self.define_from_variant("HEMELB_USE_GMYPLUS", "gmyplus"),
            self.define_from_variant("HEMELB_USE_MPI_CALL", "mpi_call"),
            self.define_from_variant("HEMELB_USE_MPI_WIN", "mpi_win"),
            self.define_from_variant("HEMELB_USE_BIGMPI", "big_mpi"),
            self.define_from_variant("HEMELB_INLET_BOUNDARY", "inlet_boundary"),
            self.define_from_variant("HEMELB_WALL_INLET_BOUNDARY", "wall_inlet_boundary"),
            self.define_from_variant("HEMELB_OUTLET_BOUNDARY", "outlet_boundary"),
            self.define_from_variant("HEMELB_WALL_OUTLET_BOUNDARY", "wall_outlet_boundary"),
            self.define_from_variant("HEMELB_WALL_BOUNDARY", "wall_boundary"),
            self.define_from_variant("HEMELB_TRACER_PARTICLES", "tracer"),
            self.define_from_variant("HEMELB_USE_VELOCITY_WEIGHTS_FILE", "velocity_weight"),
        ]

        simd = self.spec.variants["simd"].value
        if simd != "auto":
            args.append(self.define(f"-DHEMELB_USE_{simd.upper()}", "ON"))

        return args
