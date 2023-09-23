# SHiELD-minimal

This repository contains a workflow that will build and test the latest
public version of SHiELD in a docker image.  To try things out, first make sure
to download and extract the required input data for the tests from [here on
Google
Drive](https://drive.google.com/file/d/1YpPkW0rfHWrMs4fL2pdtsq1-vfCcMJP7/view?usp=sharing)
into the top-level directory. 

```
$ tar -xvf input_data.tar
```

Then initialize the submodules, build the docker image, and run the tests:

```
$ make update_submodules
$ make build
$ make test
```

The tests may or may not pass depending on the build.  Try this out several
times running

```
$ docker system prune --all
```

in between builds to clear out the docker cache and build fresh each time.  One
can observe that the tests sometimes pass and sometimes fail.  For a
particular docker image, however, the model always seems to produce the same
result (as verified by the test that repeatedly runs the model 5 times to see
that each time it produces the same result for a given build); it is only when
we completely rebuild the image that results have the potential to change,
suggesting this is a build-time issue.

This workflow is carried out in CircleCI and if we re-run the workflow from
scratch several times, we can reproduce this behavior. 
