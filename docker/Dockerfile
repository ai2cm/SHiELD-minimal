FROM ubuntu@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    cmake \
    gcc \
    gfortran \
    g++ \
    git \
    libmpich-dev \
    libnetcdf-dev \
    libnetcdff-dev \
    m4 \
    make \
    mpich \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools

ENV SHiELD_FC=mpif90
ENV SHiELD_CC=mpicc
ENV SHiELD_CXX=mpicxx
ENV SHiELD_LD=mpif90

ENV SUBMODULE_DIR=/SHiELD
COPY submodules ${SUBMODULE_DIR}/

# Build FMS, NCEPlibs, and SHiELD using SHiELD_build
# FMS_CPPDEFS needed to address https://github.com/NOAA-GFDL/FMS/issues/426
RUN cd ${SUBMODULE_DIR}/SHiELD_build/Build && \
    FMS_CPPDEFS="-DHAVE_GETTID" \
    FC=${SHiELD_FC} \
    CC=${SHiELD_CC} \
    CXX=${SHiELD_CXX} \
    LD=${SHiELD_LD} \
    TEMPLATE=site/gnu.mk \
    AVX_LEVEL=-march=native \
    ./COMPILE shield 64bit gnu

COPY requirements.txt /tmp
RUN \
    FC=${SHiELD_FC} \
    CC=${SHiELD_CC} \
    CXX=${SHiELD_CXX} \
    LD=${SHiELD_LD} \
    python3 -m pip install -r /tmp/requirements.txt
