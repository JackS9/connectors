#!/bin/sh

cd /home/jacks9/geoedf-dev/connectors/wqpinput

hpccm --recipe recipe.hpccm --format singularity --singularity-version=3.5 > Singularity

sudo singularity build WQPInput.sif Singularity

cp WQPInput.sif /images