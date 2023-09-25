# FROM ubuntu@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

# Try using an older Ubuntu image with older GNU compilers.  FMS can't build.
# FROM ubuntu@sha256:9101220a875cee98b016668342c489ff0674f247f6ca20dfc91b91c0f28581ae

# Latest image
FROM ubuntu@sha256:225b8671859bb22eb895a2d97cd5fc56aff22880dfae6cf486650a39a19b64e3

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
    python3 -m pip install -r /tmp/requirements.txt --break-system-packages
