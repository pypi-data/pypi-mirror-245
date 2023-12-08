#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BSD 3-Clause License
#
# Copyright (c) 2022, California Institute of Technology and CNRS.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
C/C++ header generation.

This module provides utility functions such as generation of C/C++ header files.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
    Aurelien Hees <aurelien.hees@obspm.fr>
    Maude Lejeune <lejeune@apc.in2p3.fr>
"""

from inspect import cleandoc


class HeaderGenerator:
    """Generate a C/C++ header file defining constants."""

    def __init__(self, constants):
        """Initialize a header generator.

        Args:
            constants: dictionary of `Constant` instances
        """
        self.constants = constants

    def write(self, filename, language):
        """Generate header file from python constants.

        Args:
            filename: path to generated header file
            language: programming language ['c' or 'c++']

        Raises:
            ValueError for invalid langugage.
        """
        print(f"installing {language.capitalize()} header file -> {filename}")

        content = self.copyright(language)
        content += "\n"
        content += self.header(language)
        content += "\n\n"
        for name, constant in self.constants.items():
            content += self.constant(name, constant, language)
            content += "\n\n"
        content += self.footer(language)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def constant(name, constant, language):
        """Return definition of constant.

        C constants are prefixed with 'LISA_' to make up for the lack of namespace.

        Args:
            name: constant name
            constant: instance of `Constant`
            language: programming language, see `write()`
        """
        if language == 'c++':
            const = 'constexpr'
            prefix = ''
        elif language == 'c':
            const = 'const'
            prefix = 'LISA_'
        else:
            raise ValueError(f"unsupported language: {language}")

        content = "/**\n"
        content += f" {constant.description}\n"
        content += f" Unit: {constant.unit}.\n\n"
        for reference in constant.references:
            content += f" - {reference}\n"
        content += "**/\n"
        content += f"static {const} double {prefix}{name} = {constant.value};"
        return content

    @staticmethod
    def copyright(language):
        """Return copyrights.

        Args:
            language: programming language, see `write()`
        """
        if language in ['c', 'c++']:
            return cleandoc("""
                //
                // LISA Constants.
                //
                // This header provides values sanctioned by the LISA Consortium for physical constants and mission parameters.
                //
                // LISA Constants is intended to be consistently used by other pieces of software related to the simulation of
                // the instrument, of gravitational wave signals, and others.
                //
                // Authors:
                //    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
                //    Aurelien Hees <aurelien.hees@obspm.fr>
                //    Maude Lejeune <lejeune@apc.in2p3.fr>
                //
                """)
        raise ValueError(f"unsupported language: {language}")

    @staticmethod
    def header(language):
        """Return header of file.

        Args:
            language: programming language, see `write()`
        """
        if language in ['c++']:
            return cleandoc("""
                #pragma once
                #include <string>

                namespace LisaConstants {

                class Constants {
                public:
                """)
        if language == 'c':
            return cleandoc("""
                #ifndef LISACONSTANTS_H
                #define LISACONSTANTS_H
                #include <stdbool.h>
                """)
        raise ValueError(f"unsupported language: {language}")

    @staticmethod
    def footer(language):
        """Return footer of file.

        Args:
            language: programming language, see `write()`
        """
        if language in ['c++']:
            return cleandoc("""
                };
                }

                """)
        if language == 'c':
            return cleandoc("""
                #endif
                """)
        raise ValueError(f"unsupported language: {language}")
