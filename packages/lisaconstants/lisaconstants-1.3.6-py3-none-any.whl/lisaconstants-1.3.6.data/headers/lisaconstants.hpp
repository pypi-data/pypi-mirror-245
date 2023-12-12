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
#pragma once
#include <string>

namespace LisaConstants {

class Constants {
public:

/**
 Speed of light in a vacuum
 Unit: m s^{-1}.

 - P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)
 - http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates' (http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)
**/
static constexpr double SPEED_OF_LIGHT = 299792458.0;

/**
 Speed of light in a vacuum
 Unit: m s^{-1}.

 - P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)
 - http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates' (http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)
**/
static constexpr double c = 299792458.0;

/**
 Speed of light in a vacuum
 Unit: m s^{-1}.

 - P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)
 - http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates' (http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)
**/
static constexpr double C = 299792458.0;

/**
 Planck constant
 Unit: J Hz^{-1}.

 - The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2021-04-28.
 - BIPM. 2018-11-16 (https://web.archive.org/web/20181119214326/https://www.bipm.org/utils/common/pdf/CGPM-2018/26th-CGPM-Resolutions.pdf).
**/
static constexpr double PLANCK_CONSTANT = 6.62607015e-34;

/**
 Planck constant
 Unit: J Hz^{-1}.

 - The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2021-04-28.
 - BIPM. 2018-11-16 (https://web.archive.org/web/20181119214326/https://www.bipm.org/utils/common/pdf/CGPM-2018/26th-CGPM-Resolutions.pdf).
**/
static constexpr double h = 6.62607015e-34;

/**
 Sideral year (in ephemeris days) for the J2000.0 epoch
 Unit: day.

 - J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)
**/
static constexpr double SIDEREALYEAR_J2000DAY = 365.256363004;

/**
 Mean tropical year (in ephemeris days) for the J2000.0 epoch
 Unit: day.

 - J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)
**/
static constexpr double TROPICALYEAR_J2000DAY = 365.242190402;

/**
 Astronomical year
 Unit: s.

 - J.L. Simon, P. Bretagnon, J. Chapront, M. Chapront-Touze, G. Francou, J. Laskar, 1994, 'Numerical expressions for precession formulae and mean elements for the Moon and the planets', A&A, 282, 663 (1994A&A...282..663S)
**/
static constexpr double ASTRONOMICAL_YEAR = 31558149.763545595;

/**
 Astronomical unit
 Unit: m.

 - IAU, August 2012, 'Re-definition of the astronomical unit of length', IAU 2012 Resolution B2 adopted at the XXVIII-th General Assembly of the IAU
**/
static constexpr double ASTRONOMICAL_UNIT = 149597870700.0;

/**
 Astronomical unit
 Unit: m.

 - IAU, August 2012, 'Re-definition of the astronomical unit of length', IAU 2012 Resolution B2 adopted at the XXVIII-th General Assembly of the IAU
**/
static constexpr double au = 149597870700.0;

/**
 Gravitational parameter for the Sun as the central body
 Unit: m^3 s^{-2}.

 - Table 8 from http://ipnpr.jpl.nasa.gov/progress_report/42-196/196C.pdf
**/
static constexpr double SUN_GRAVITATIONAL_PARAMETER = 1.327124400419394e+20;

/**
 Gravitational parameter for the Sun as the central body
 Unit: m^3 s^{-2}.

 - Table 8 from http://ipnpr.jpl.nasa.gov/progress_report/42-196/196C.pdf
**/
static constexpr double GM_SUN = 1.327124400419394e+20;

/**
 Sun Schwarzschild radius
 Unit: m.

**/
static constexpr double SUN_SCHWARZSCHILD_RADIUS = 2953.2500770335273;

/**
 Parsec expressed in meters
 Unit: m.

**/
static constexpr double PARSEC = 3.085677581491367e+16;

/**
 Parsec expressed in meters
 Unit: m.

**/
static constexpr double PARSEC_METER = 3.085677581491367e+16;

/**
 Newton's universal constant of gravitation
 Unit: m^3 kg^{-1} s^{-2}.

 - P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)
 - http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates', http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)
**/
static constexpr double GRAVITATIONAL_CONSTANT = 6.67408e-11;

/**
 Newton's universal constant of gravitation
 Unit: m^3 kg^{-1} s^{-2}.

 - P.J. Mohr, B.N. Taylor, D.B. Newell, 9 July 2015, 'The 2014 CODATA Recommended Values of the Fundamental Physical Constants', National Institute of Standards and Technology, Gaithersburg, MD 20899-8401 (http://www.codata.org/)
 - http://physics.nist.gov/constants (Web Version 7.0). See also the IAU (2009) System of Astronomical Constants (IAU, August 2009, 'IAU 2009 Astronomical Constants', IAU 2009 Resolution B2 adopted at the XXVII-th General Assembly of the IAU. See also IAU, 10 August 2009, 'IAU WG on NSFA Current Best Estimates', http://maia.usno.navy.mil/NSFA/NSFA_cbe.html)
**/
static constexpr double NEWTON_CONSTANT = 6.67408e-11;

/**
 Mass of the Sun
 Unit: kg.

**/
static constexpr double SUN_MASS = 1.98848e+30;

/**
 Mass of the Sun
 Unit: kg.

**/
static constexpr double SOLAR_MASS = 1.98848e+30;

/**
 Obliquity of the ecliptic plane
 Unit: deg.

 - 'Adoption of the P03 Precession Theory and Definition of the Ecliptic', IAU 2006 Resolution B1, XXVIth International Astronomical Union General Assembly
 - 'Precession-nutation procedures consistent with IAU 2006 resolutions', P. T.  Wallace, N.  Capitaine, A&A 459 (3) 981-985 (2006), DOI: 10.1051/0004-6361:20065897
 - 'A new determination of lunar orbital parameters, precession constant and tidal acceleration from LLR measurements', J. Chapront, M. Chapront-Touzé and G. Francou, A&A, 387 2 (2002) 700-709, DOI: https://doi.org/10.1051/0004-6361:20020420
**/
static constexpr double OBLIQUITY = 23.439279444444445;

/**
 Elementary positive charge
 Unit: C.

 - 2018 CODATA Value: elementary charge. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.
**/
static constexpr double ELEMENTARY_CHARGE = 1.602176634e-19;

/**
 Elementary positive charge
 Unit: C.

 - 2018 CODATA Value: elementary charge. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.
**/
static constexpr double e = 1.602176634e-19;

/**
 Elementary positive charge
 Unit: C.

 - 2018 CODATA Value: elementary charge. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.
**/
static constexpr double E = 1.602176634e-19;

/**
 Boltzmann constant
 Unit: J K^{-1}.

 - 2018 CODATA Value: Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 20 May 2019.
**/
static constexpr double BOLTZMANN_CONSTANT = 1.380649e-23;

/**
 Boltzmann constant
 Unit: J K^{-1}.

 - 2018 CODATA Value: Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 20 May 2019.
**/
static constexpr double Kb = 1.380649e-23;

/**
 Boltzmann constant
 Unit: J K^{-1}.

 - 2018 CODATA Value: Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 20 May 2019.
**/
static constexpr double KB = 1.380649e-23;

/**
 Stefan–Boltzmann constant
 Unit: kg s^{-3} K^{-4}.

 - 2018 CODATA Value: Stefan–Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.
**/
static constexpr double STEFAN_BOLTZMANN_CONSTANT = 5.6703744191844294e-08;

/**
 Stefan–Boltzmann constant
 Unit: kg s^{-3} K^{-4}.

 - 2018 CODATA Value: Stefan–Boltzmann constant. The NIST Reference on Constants, Units, and Uncertainty. NIST. 20 May 2019. Retrieved 2019-05-20.
**/
static constexpr double sigma_SB = 5.6703744191844294e-08;

/**
 Magnetic permeability in a vacuum
 Unit: kg m s^{-2} A^{-2}.

**/
static constexpr double VACUUM_PERMEABILITY = 1.25663706143592e-06;

/**
 Magnetic permeability in a vacuum
 Unit: kg m s^{-2} A^{-2}.

**/
static constexpr double MU0 = 1.25663706143592e-06;

/**
 Thermal optical path difference change of fused silica
 Unit: K^{-1}.

**/
static constexpr double FUSED_SILICA_THERMAL_OPD = 9.82e-06;

/**
 Thermal optical path difference change of fused silica
 Unit: K^{-1}.

**/
static constexpr double FOM_Si = 9.82e-06;

/**
 Thermal expansion of fused silica
 Unit: K^{-1}.

**/
static constexpr double FUSED_SILICAL_THERMAL_EXPANSION = 5e-07;

/**
 Thermal expansion of fused silica
 Unit: K^{-1}.

**/
static constexpr double exp_Si = 5e-07;

/**
 Thermal optical path difference change of crystal quartz
 Unit: K^{-1}.

**/
static constexpr double CRYSTAL_QUARTZ_THERMAL_OPD = 6.1e-07;

/**
 Thermal optical path difference change of crystal quartz
 Unit: K^{-1}.

**/
static constexpr double FOM_Qtz = 6.1e-07;

/**
 Thermal expansion of Zerodur
 Unit: K^{-1}.

**/
static constexpr double ZERODUR_THERMAL_EXPANSION = 2e-08;

/**
 Thermal expansion of Zerodur
 Unit: K^{-1}.

**/
static constexpr double exp_zer = 2e-08;

/**
 Thermal expansion of titanium
 Unit: K^{-1}.

**/
static constexpr double TITANIUM_THERMAL_EXPANSION = 8.6e-06;

/**
 Thermal expansion of titanium
 Unit: K^{-1}.

**/
static constexpr double exp_Ti = 8.6e-06;

/**
 Thermal expansion of gold-platinum
 Unit: K^{-1}.

**/
static constexpr double GOLD_PLATINUM_THERMAL_EXPANSION = 1.52e-05;

/**
 Thermal expansion of gold-platinum
 Unit: K^{-1}.

**/
static constexpr double exp_AuPt = 1.52e-05;

/**
 Molecular weight (mass) of water
 Unit: kg.

**/
static constexpr double WATER_MOLECULAR_WEIGHT = 2.99150711295358e-26;

/**
 Molecular weight (mass) of water
 Unit: kg.

**/
static constexpr double H2Omo = 2.99150711295358e-26;

};
}