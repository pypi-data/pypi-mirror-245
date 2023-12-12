# -*- coding: utf-8 -*-

# (C) Copyright 2023 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


import os

from setuptools import find_packages, setup

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

# NOTE: The lists below require each requirement on a separate line,
# putting multiple requirements on the same line will prevent qiskit-bot
# from correctly updating the versions for the qiskit packages.
requirements = ["qiskit==0.45.0", "backoff==2.2.1", "qiskit_qasm3_import==0.4.1"]

setup(
    name="qiskit-transpiler-service",
    version="0.1.3",
    description="A library to use Qiskit Transpiler service(https://docs.quantum.ibm.com/transpile/qiskit-transpiler-service) and the AI transpiler passes(https://docs.quantum.ibm.com/transpile/ai-transpiler-passes)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
    author="Data & Intelligence team, IBM Quantum",
    author_email="",
    license="Apache 2.0",
    py_modules=[],
    packages=find_packages(),
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
    keywords=["qiskit", "ai", "transpiler", "routing"],
    install_requires=requirements,
    project_urls={
        "Bug Tracker": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service/issues",
        "Documentation": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
        "Source Code": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
    },
    include_package_data=True,
    python_requires=">=3.8",
)
