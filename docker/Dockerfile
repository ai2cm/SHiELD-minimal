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
    python3-setuptools \
    python3-venv

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

RUN python3 -m venv /opt/wrapper-env
ENV VIRTUAL_ENV=/opt/wrapper-env
ENV PATH=/opt/wrapper-env/bin:${PATH}
COPY requirements.txt /tmp
RUN \
    FC=${SHiELD_FC} \
    CC=${SHiELD_CC} \
    CXX=${SHiELD_CXX} \
    LD=${SHiELD_LD} \
    python3 -m pip install -r /tmp/requirements.txt
