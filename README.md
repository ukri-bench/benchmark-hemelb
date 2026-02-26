# Template benchmark

The repository demonstrates/describes the structure of a repository for a 
benchmark released as part of the UKRI Living Benchmarks project.

## Status

Alpha

## Maintainers

- [Tuomas Koskela](https://www.github.com/tkoskela)

## Overview

### Software

- [HemePure](https://github.com/UCL-CCS/HemePure)
- [HemePure-GPU](https://github.com/UCL-CCS/HemePure-GPU)

### Architectures

- CPU: Tested on x86
- GPU: Tested on NVIDIA, AMD in progress

### Languages and programming models

- Programming languages: C++
- Parallel models: MPI, OpenMP
- Accelerator offload models: CUDA, HIP

### Seven 'dwarfs'

- [ ] Dense linear algebra
- [ ] Sparse linear algebra
- [ ] Spectral methods
- [ ] N-body methods
- [ ] Structured grids
- [ ] Unstructured grids
- [ ] Monte Carlo

## Building the benchmark

The benchmark can be built using Spack or manually using CMake. If you are using the 
ReFrame method to run the benchmark described below, it will automatically
perform the build step for you.

Once it has been built the CPU benchmark executable is called `hemepure`

### Spack build

A Spack package is provided in `spack/`:

```bash
spack repo add ./spack
spack info hemepure
```

Varios configuration options and boundary conditions are set at compile time and are exposed as variants in the
Spack package.

```
Variants:
    big_mpi [false]                                          false, true
        Use Domain Split to help load large domains

    build_system [cmake]                                     cmake
        Build systems supported by the package

    build_type [Release]                                     Debug, MinSizeRel, RelWithDebInfo, Release
      when  build_system=cmake
        CMake build type

    generator [make]                                         none
      when  build_system=cmake
        the build system generator to use

    gmyplus [false]                                          false, true
        Use GMY+ format

    inlet_boundary [LADDIOLET]                               LADDIOLET, NASHZEROTHORDERPRESSUREIOLET
        Boundary conditions at inlets

    ipo [false]                                              false, true
      when  build_system=cmake ^cmake@3.9:
        CMake interprocedural optimization

    mpi_call [false]                                         false, true
        Use standard MPI functions when reading blocks

    mpi_win [false]                                          false, true
        Use MPI Domain Split to help load large domains

    outlet_boundary [NASHZEROTHORDERPRESSUREIOLET]           LADDIOLET, NASHZEROTHORDERPRESSUREIOLET
        Boundary conditions at outlets

    parmetis [false]                                         false, true
        Use ParMETIS

    simd [auto]                                              auto, avx2, avx512, sse3
        Use SIMD instrinsics

    tracer [true]                                            false, true
        Use particles as tracers

    velocity_weight [false]                                  false, true
        Use velocity weights file

    wall_boundary [SIMPLEBOUNCEBACK]                         BFL, GZS, GZSElastic, JUNKYANG, SIMPLEBOUNCEBACK
        Boundary conditions at walls

    wall_inlet_boundary [LADDIOLETSBB]                       LADDIOLETBFL, LADDIOLETGZSE, LADDIOLETSBB, NASHZEROTHORDERPRESSUREBFL,
                                                             NASHZEROTHORDERPRESSUREGZSE, NASHZEROTHORDERPRESSURESBB
        Boundary conditions at wall-inlet corners

    wall_outlet_boundary [NASHZEROTHORDERPRESSURESBB]        LADDIOLETBFL, LADDIOLETGZSE, LADDIOLETSBB, NASHZEROTHORDERPRESSUREBFL,
                                                             NASHZEROTHORDERPRESSUREGZSE, NASHZEROTHORDERPRESSURESBB
        Boundary conditions at wall-outlet corners

```


Note: to use Spack, you must have Spack installed on the system you are using and
a valid Spack system configuration. Example Spack configurations are available
in a separate repository: [https://github.com/ukri-bench/system-configs]

### Manual build

Manual build instructions using CMake are given in [the HemePure README](https://github.com/UCL-CCS/HemePure?tab=readme-ov-file#compilation). To compile these benchmarks, build the `hemepure` application using the following CMake options (replacing the C and CXX compilers as appropriate).

```bash
cmake -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_COMPILER=g++ \
      -DHEMELB_COMPUTE_ARCHITECTURE=NEUTRAL \
      -DCMAKE_CXX_EXTENSIONS=OFF \
      -DHEMELB_USE_VELOCITY_WEIGHTS_FILE=OFF \
      -DHEMELB_INLET_BOUNDARY=NASHZEROTHORDERPRESSUREIOLET \
      -DHEMELB_WALL_INLET_BOUNDARY=NASHZEROTHORDERPRESSURESBB \
      -DHEMELB_OUTLET_BOUNDARY=NASHZEROTHORDERPRESSUREIOLET \
      -DHEMELB_WALL_OUTLET_BOUNDARY=NASHZEROTHORDERPRESSURESBB \
      -DHEMELB_LOG_LEVEL="Info" \
      -DHEMELB_USE_MPI_PARALLEL_IO=OFF \
      -DCMAKE_BUILD_TYPE=Release \
```

## Running the benchmark

The benchmark can be run using ReFrame or manually. 

If you use ReFrame, then ReFrame will build the software, run the benchmark,
test for correctness, extract the performance/figure of merit (FoM) for you and
report them.

### Running using ReFrame

The ReFrame test configuration is available in the `reframe/` subdirectory.

To run reframe for this benchmark, use

```
reframe -c reframe/hemepure.py -r
```

Note: to use ReFrame, you must have ReFrame installed on the system you are using and
a valid ReFrame system configuration. Example ReFrame configurations are available
in a separate repository: [https://github.com/ukri-bench/system-configs]

### Running manually

Input data for the benchmarks can be retrieved from [Zenodo](https://zenodo.org/records/14859634). 
To run the benchmarks, extract the data, then run `hemepure` with
```
mpirun -np xx hemepure -in input.xml -out results
```

Performance Figure of Merit (FoM) can be extracted from the output file report.xml. 
The FoM is millions of lattice updates per second (MLUPS). This is calculated as

`number_of_sites * number_of_timesteps / (runtime * 1e6)`

- ADD: Example of how to test correctness

## Example performance data

This section contains example performance data from selected HPC systems.

ADD: Example performance data

## License

This benchmark description and associated files are released under the MIT license.
