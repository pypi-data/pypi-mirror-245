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
LISA Python Constants.

This module provides values sanctioned by the LISA Consortium for physical constants and mission parameters.

LISA Python Constants is intended to be consistently used by other pieces of software related to the simulation of
the instrument, of gravitational wave signals, and others.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
    Aurelien Hees <aurelien.hees@obspm.fr>
    Maude Lejeune <lejeune@apc.in2p3.fr>
"""
# pylint: disable=line-too-long


from typing import Dict


class Constant:
    """Defines a constant with associated metadata."""

    ALL: Dict[str, 'Constant'] = {}

    @classmethod
    def alias(cls, name, original):
        """Give an existing constant an alias name.

        Args:
            name (str): alias name
            original (str): original name
        """
        constant = cls.ALL[original]
        constant.names.append(name)
        cls.ALL[name] = constant

    def __init__(self, name, value, unit, description, error=None, references=None, longdescr=None):
        """Initialize a constant with attributes.

        Args:
            name (str): constant name
            value (any): constant value
            unit (str or None): associated unit, or None
            description (str): short one-liner description
            error (str or None): uncertainty on value, or None
            references (list or None): list of references, or None
            longdescr (str or None): long multi-line description
        """
        self.names = [name]
        self.value = value
        self.description = description
        self.unit = unit
        self.error = error
        self.longdescr = longdescr

        if references is None:
            self.references = []
        elif isinstance(references, str):
            self.references = [references]
        else:
            self.references = references

        # Add to list of defined constants
        self.ALL[name] = self

    def __repr__(self):
        if self.unit is None:
            return f'<{self.names[0]} ({self.value})>'
        return f'<{self.names[0]} ({self.value} {self.unit})'


Constant('SPEED_OF_LIGHT',
    value=299792458.0,
    unit='m s^{-1}',
    description="Speed of light in a vacuum",
    error='Exact',
    references=[
        "P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)",
        "http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates' (http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)",
    ],
)

Constant.alias('c', 'SPEED_OF_LIGHT')
Constant.alias('C', 'SPEED_OF_LIGHT')

Constant('PLANCK_CONSTANT',
    value=6.62607015E-34,
    unit='J Hz^{-1}',
    description="Planck constant",
    error='Exact',
    references=[
        "The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2021-04-28.",
        "BIPM. 2018-11-16 (https://web.archive.org/web/20181119214326/https://www.bipm.org/utils/common/pdf/CGPM-2018/26th-CGPM-Resolutions.pdf).",
    ],
)

Constant.alias('h', 'PLANCK_CONSTANT')

Constant('SIDEREALYEAR_J2000DAY',
    value=365.256363004,
    unit='day',
    description="Sideral year (in ephemeris days) for the J2000.0 epoch",
    references=[
        "J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)",
    ],
    longdescr="A sidereal year is the time taken by the Earth to orbit the Sun once with respect to the fixed stars. Hence, it is also the time taken for the Sun to return to the same position with respect to the fixed stars after apparently travelling once around the ecliptic."
)

Constant('TROPICALYEAR_J2000DAY',
    value=365.242190402,
    unit='day',
    description="Mean tropical year (in ephemeris days) for the J2000.0 epoch",
    references=[
        "J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)",
    ],
    longdescr="A tropical year (also known as a solar year) is the time that the Sun takes to return to the same position in the cycle of seasons, as seen from Earth; for example, the time from vernal equinox to vernal equinox, or from summer solstice to summer solstice. This differs from the time it takes Earth to complete one full orbit around the Sun as measured with respect to the fixed stars (the sidereal year) by about 20 minutes because of the precession of the equinoxes."
)

Constant('ASTRONOMICAL_YEAR',
    value=Constant.ALL["SIDEREALYEAR_J2000DAY"].value * 60 * 60 * 24,
    unit='s',
    description="Astronomical year",
    references=[
        "J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)",
    ],
)

Constant('ASTRONOMICAL_UNIT',
    value=149597870700.0,
    unit='m',
    description="Astronomical unit",
    references=[
        "IAU, August 2012, 'Re-definition of the astronomical unit of length', IAU 2012 Resolution B2 adopted at the XXVIII-th General Assembly of the IAU",
    ],
    longdescr="The astronomical unit (symbol: au) is a unit of length, roughly the distance from Earth to the Sun and equal to about 150 million kilometres (93 million miles) or ~8 light minutes. The actual distance varies by about 3% as Earth orbits the Sun, from a maximum (aphelion) to a minimum (perihelion) and back again once each year. The astronomical unit was originally conceived as the average of Earth's aphelion and perihelion; however, since 2012 it has been defined as exactly 149597870700 m.",
)

Constant.alias('au', 'ASTRONOMICAL_UNIT')

Constant("SUN_GRAVITATIONAL_PARAMETER",
    value=1.327124400419394e+20,
    unit='m^3 s^{-2}',
    description="Gravitational parameter for the Sun as the central body",
    references=[
        "Table 8 from http://ipnpr.jpl.nasa.gov/progress_report/42-196/196C.pdf",
    ],
    longdescr="The standard gravitational parameter of a celestial body is the product of the gravitational constant and the mass of the body.",
)

Constant.alias('GM_SUN', 'SUN_GRAVITATIONAL_PARAMETER')

Constant("SUN_SCHWARZSCHILD_RADIUS",
    value=2 * Constant.ALL["GM_SUN"].value / Constant.ALL["c"].value**2,
    unit='m',
    description="Sun Schwarzschild radius",
)

Constant("PARSEC",
    value=3.0856775814913674e+16,
    unit='m',
    description="Parsec expressed in meters",
    longdescr="The parsec is obtained by the use of parallax and trigonometry, and is defined as the distance at which 1 au subtends an angle of one arcsecond.",
)

Constant.alias('PARSEC_METER', 'PARSEC')

Constant("GRAVITATIONAL_CONSTANT",
    value=6.674080e-11,
    unit='m^3 kg^{-1} s^{-2}',
    description="Newton's universal constant of gravitation",
    references=[
        "P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)",
        "http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates', http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)",
    ],
    longdescr="In Newton's law, it is the proportionality constant connecting the gravitational force between two bodies with the product of their masses and the inverse square of their distance. In the Einstein field equations, it quantifies the relation between the geometry of spacetime and the energy–momentum tensor (also referred to as the stress–energy tensor).",
)

Constant.alias('NEWTON_CONSTANT', 'GRAVITATIONAL_CONSTANT')

Constant("SUN_MASS",
    value=1.98848e+30,
    unit='kg',
    description="Mass of the Sun",
)

Constant.alias('SOLAR_MASS', 'SUN_MASS')

Constant("OBLIQUITY",
    value=84381.406 / (60 * 60),
    unit='deg',
    description="Obliquity of the ecliptic plane",
    longdescr="The Earth obliquity, or axial tilt angle, is the angle between Earth’s axis of rotation and the normal to the Earth's orbital plane around the Sun. It the IAU 2006 value for the obliquity of the ecliptic plane at J2000.0.",
    references=[
        "'Adoption of the P03 Precession Theory and Definition of the Ecliptic', IAU 2006 Resolution B1, XXVIth International Astronomical Union General Assembly",
        "'Precession-nutation procedures consistent with IAU 2006 resolutions', P. T.  Wallace, N.  Capitaine, A&A 459 (3) 981-985 (2006), DOI: 10.1051/0004-6361:20065897",
        "'A new determination of lunar orbital parameters, precession constant and tidal acceleration from LLR measurements', J. Chapront, M. Chapront-Touzé and G. Francou, A&A, 387 2 (2002) 700-709, DOI: https://doi.org/10.1051/0004-6361:20020420",
    ],
)

Constant("ELEMENTARY_CHARGE",
    value=1.602176634E-19,
    unit='C',
    description="Elementary positive charge",
    error='Exact',
    references=[
        "2018 CODATA Value: elementary charge. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.",
    ],
    longdescr="The elementary charge is the electric charge carried by a single proton or, equivalently, the magnitude of the negative electric charge carried by a single electron.",
)

Constant.alias('e', "ELEMENTARY_CHARGE")
Constant.alias('E', "ELEMENTARY_CHARGE")

Constant("BOLTZMANN_CONSTANT",
    value=1.380649E-23,
    unit='J K^{-1}',
    description="Boltzmann constant",
    error='Exact',
    references=[
        "2018 CODATA Value: Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 20 May 2019.",
    ],
    longdescr="The Boltzmann constant is the proportionality factor that relates the average relative kinetic energy of particles in a gas with the thermodynamic temperature of the gas.",
)

Constant.alias('Kb', "BOLTZMANN_CONSTANT")
Constant.alias('KB', "BOLTZMANN_CONSTANT")

Constant("STEFAN_BOLTZMANN_CONSTANT",
    value=5.670374419184429453970E-8,
    unit='kg s^{-3} K^{-4}',
    description="Stefan–Boltzmann constant",
    error='Exact (numerical approximation)',
    references=[
         "2018 CODATA Value: Stefan–Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.",
    ],
    longdescr="The Stefan-Boltzmann constant is the constant of proportionality in the Stefan–Boltzmann law: 'the total intensity radiated over all wavelengths increases as the temperature increases', of a black body which is proportional to the fourth power of the thermodynamic temperature.",
)

Constant.alias('sigma_SB', "STEFAN_BOLTZMANN_CONSTANT")

Constant("VACUUM_PERMEABILITY",
    value=1.25663706143592E-06,
    unit='kg m s^{-2} A^{-2}',
    description="Magnetic permeability in a vacuum",
)

Constant.alias('MU0', "VACUUM_PERMEABILITY")

Constant("FUSED_SILICA_THERMAL_OPD",
    value=9.82E-6,
    unit='K^{-1}',
    description="Thermal optical path difference change of fused silica",
)

Constant.alias('FOM_Si', "FUSED_SILICA_THERMAL_OPD")

Constant("FUSED_SILICAL_THERMAL_EXPANSION",
    value=5E-7,
    unit='K^{-1}',
    description="Thermal expansion of fused silica",
)

Constant.alias('exp_Si', "FUSED_SILICAL_THERMAL_EXPANSION")

Constant("CRYSTAL_QUARTZ_THERMAL_OPD",
    value=6.1E-7,
    unit='K^{-1}',
    description="Thermal optical path difference change of crystal quartz",
)

Constant.alias('FOM_Qtz', "CRYSTAL_QUARTZ_THERMAL_OPD")

Constant("ZERODUR_THERMAL_EXPANSION",
    value=2E-8,
    unit='K^{-1}',
    description="Thermal expansion of Zerodur",
)

Constant.alias('exp_zer', "ZERODUR_THERMAL_EXPANSION")

Constant("TITANIUM_THERMAL_EXPANSION",
    value=8.6E-6,
    unit='K^{-1}',
    description="Thermal expansion of titanium",
)

Constant.alias('exp_Ti', "TITANIUM_THERMAL_EXPANSION")

Constant("GOLD_PLATINUM_THERMAL_EXPANSION",
    value=1.52E-5,
    unit='K^{-1}',
    description="Thermal expansion of gold-platinum",
)

Constant.alias('exp_AuPt', "GOLD_PLATINUM_THERMAL_EXPANSION")

Constant("WATER_MOLECULAR_WEIGHT",
    value=2.99150711295358E-26,
    unit='kg',
    description="Molecular weight (mass) of water",
)

Constant.alias('H2Omo', "WATER_MOLECULAR_WEIGHT")
