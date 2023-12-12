# LISA Constants

[![pipeline status](https://gitlab.in2p3.fr/lisa-simulation/constants/badges/master/pipeline.svg)](https://gitlab.in2p3.fr/lisa-simulation/constants/-/commits/master)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.6627346.svg)](https://doi.org/10.5281/zenodo.6627346)

LISA Constants is a Python package providing values sanctioned by the LISA Consortium for physical constants and mission parameters. LISA Constants is intended to be consistently used by other pieces of software related to the simulation of the instrument, of gravitational wave signals, and others.

We provide support for Python projects (as a package), C projects (as a header file), and C++ projects (as a header file). See below how to use the package.

* **Documentation for the latest stable release is available at <https://lisa-simulation.pages.in2p3.fr/constants>**
* Documentation for the current development version is available at <https://lisa-simulation.pages.in2p3.fr/constants/master>

## Contributing

### Report an issue

We use the issue-tracking management system associated with the project provided by Gitlab. If you want to report a bug or request a feature, open an issue at <https://gitlab.in2p3.fr/lisa-simulation/constants/-/issues>. You may also thumb-up or comment on existing issues.

### Development environment

We strongly recommend to use [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

To setup the development environment, use the following commands:

```shell
git clone git@gitlab.in2p3.fr:lisa-simulation/constants.git
cd constants
python -m venv .
source ./bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Workflow

The project's development workflow is based on the issue-tracking system provided by Gitlab, as well as peer-reviewed merge requests. This ensures high-quality standards.

Issues are solved by creating branches and opening merge requests. Only the assignee of the related issue and merge request can push commits on the branch. Once all the changes have been pushed, the "draft" specifier on the merge request is removed, and the merge request is assigned to a reviewer. He can push new changes to the branch, or request changes to the original author by re-assigning the merge request to them. When the merge request is accepted, the branch is merged onto master, deleted, and the associated issue is closed.

### Pylint and unittest

We enforce [PEP 8 (Style Guide for Python Code)](https://www.python.org/dev/peps/pep-0008/) with Pylint syntax checking, and correction of the code using the [pytest](https://docs.pytest.org/) testing framework. Both are implemented in the continuous integration system.

You can run them locally

```shell
pylint lisaconstants/*.py
python -m pytest
```

## Use policy

By releasing LISA Constants as an open source software package we want to foster open science and enable everyone to use it in their research free of charge. To acknowledge the authors of this tool and to ensure that consistent, reproducible, and traceble constant values are used in your project, please cite or add the version-specific DOI (click on the badge above).

## Authors

* Jean-Baptiste Bayle (j2b.bayle@gmail.com)
* Maude Lejeune (lejeune@apc.in2p3.fr)
* Aurelien Hees (aurelien.hees@obspm.fr)
