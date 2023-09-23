#!/bin/bash

ROOT=input_data
OROGRAPHIC_FORCING=$ROOT/orographic_forcing/C12
FORCING=$ROOT/forcing
INITIAL_CONDITIONS=$ROOT/initial_conditions

mkdir -p $OROGRAPHIC_FORCING
mkdir -p $FORCING
mkdir -p $INITIAL_CONDITIONS

gsutil -m -u vcm-ml cp gs://vcm-fv3config/data/orographic_data/v1.0/C12/* $OROGRAPHIC_FORCING/
gsutil -m -u vcm-ml cp -r gs://vcm-ml-experiments/spencerc/2023-09-13-SHiELD-forcing-data/* $FORCING/
gsutil -m -u vcm-ml cp gs://vcm-fv3config/data/initial_conditions/gfs_c12_example/v1.0/* $INITIAL_CONDITIONS/
gsutil -m -u vcm-ml cp gs://vcm-fv3config/config/field_table/TKE-EDMF/v1.1/field_table $ROOT/
