#! /usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import astropy.units as u
from p_winds import tools


data_test_url = 'https://raw.githubusercontent.com/ladsantos/p-winds/main/data/solar_spectrum_scaled_lambda.dat'


# Test the nearest_index function
def test_nearest_index():
    array = np.linspace(1, 10, 10)
    ind = tools.nearest_index(array, np.pi)
    assert ind == 2


# Test the make_spectrum_from_file function
def test_make_spectrum_from_file(precision_threshold=1E-6):
    units = {'wavelength': u.angstrom, 'flux': u.erg / u.s / u.cm ** 2 /
                                               u.angstrom}
    spectrum = tools.make_spectrum_from_file(data_test_url, units)
    test_value = (spectrum['flux_lambda'][0] * spectrum['flux_unit']).to(
        u.W / u.m ** 2 / u.angstrom).value
    assert abs((test_value - 2.08405464e-11) / test_value) < precision_threshold


# Test the generate_muscles_spectrum function
def test_generate_muscles_spectrum(precision_threshold=1E-6):
    spectrum = tools.generate_muscles_spectrum('gj436',
                                               semi_major_axis=2.0,
                                               muscles_dir='https://archive.stsci.edu/missions/hlsp/muscles/gj436/')
    test_value = (spectrum['flux_lambda'][0] * spectrum['flux_unit']).to(
        u.W / u.m ** 2 / u.angstrom).value
    assert abs((test_value - 0.0170225) / test_value) < precision_threshold
