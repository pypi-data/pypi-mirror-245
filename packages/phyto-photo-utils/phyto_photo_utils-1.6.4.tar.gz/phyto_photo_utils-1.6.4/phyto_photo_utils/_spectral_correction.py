#!/usr/bin/env python

import numpy as np
import pandas as pd
import os

def calculate_chl_specific_absorption(aptot, blank, ap_lambda, depig=None, chl=None, vol=None, betac1=None, betac2=None, diam=None, bricaud_slope=False, norm_750=False):
	"""

	Process the raw np.absorbance data to produce chlorophyll specific phytoplankton np.absorption.

	Parameters
	----------

	aptot : np.np.array, dtype=float, shape=[n,]
		The raw absorbance data.
	blank : np.np.array, dtype=float, shape=[n,]
	 	The blank absorbance data.
	ap_lambda : np.np.array, dtype=float, shape=[n,]
		The wavelengths corresponding to the measurements.
	depig : np.np.array, dtype=float, shape=[n,] 
		The raw depigmented absorbance data.
	chl : float, default=None
		The chlorophyll concentration, in mg per metre cubed, associated with the measurement.
	vol : int, default=None
		The volume of water filtered in mL.
	betac1 : int, default=None
		The pathlength amplification coefficient 1 (see Stramski et al. 2015). For transmittance mode, 0.679, for transmittance-reflectance mode, 0.719, and for integrating sphere mode, 0.323.
	betac2 : int, default=None
		The pathlength amplification coefficient 2 (see Stramski et al. 2015). For transmittance mode, 1.2804, for transmittance-reflectance mode, 1.2287, and for integrating sphere mode, 1.0867.
	diam : float, default=None		
		The diameter of filtrate in mm.
	bricaud_slope : bool, default=True
	 	If True, will theoretically calculate detrital slope (see Bricaud & Stramski 1990). If False, will subtract depigmented absorption from total absorption.
	norm_750 : bool, default=False
		If True, will normalise the data to the value at 750 nm.

	Returns
	-------

	aphy : np.np.array, dtype=float, shape=[n,]
		The chlorophyll specific phytoplankton np.absorption data.

	Example
	-------
	>>> aphy = ppu.calculate_chl_specific_np.absorption(pa_data, blank, wavelength, chl=0.19, vol=2000, betac1=0.323, betac2=1.0867, diam=15, bricaud_slope=True, phycobilin=True, norm750=False)
	   
	"""

	if vol is None:
		raise ValueError("Please provide a value for 'vol'.")
	if betac1 is None:
		raise ValueError("Please provide a value for 'betac1'.")
	if betac2 is None:
		raise ValueError("Please provide a value for 'betac2'.")
	if diam is None:
		raise ValueError("Please provide a value for 'diam'.")

	# Define internal helper functions

	def apply_blank_correction(data, blank):
		data -= blank
		data[data < 0] = 0
		return data

	def convert_absorbance_to_absorption(data, ap_lambda, diam, vol, betac1, betac2):
		diam = np.pi * ((diam / 2000) ** 2)
		divol = ((vol / 1e6) / diam)
		data *= 2.303
		data /= divol
		data  = betac1 * data**betac2
		return data

	def normalize_to_750nm(aptot, ap_lambda):
		if aptot is None or ap_lambda is None:
			raise ValueError("aptot and ap_lambda must not be None.")

		if not np.any(aptot) or not np.any(ap_lambda):
			raise ValueError("aptot and ap_lambda must not be empty.")

		index_750nm = np.argmin(np.abs(ap_lambda - 750))
		dmin = aptot[index_750nm]
		normalized_aptot = aptot - dmin

		return normalized_aptot

	def calculate_bricaud_slope(ap_lambda, aptot, phycobilin):
		# Find unique indices based upon wavelengths measured
		idx380 = np.argmin(np.abs(ap_lambda - 380))
		idx505 = np.argmin(np.abs(ap_lambda - 505))
		idx580 = np.argmin(np.abs(ap_lambda - 580))
		#idx600 = np.argmin(np.abs(ap_lambda - 600))
		idx692 = np.argmin(np.abs(ap_lambda - 692))
		idx750 = np.argmin(np.abs(ap_lambda - 750))

		# Constants
		constant_a = 0.99
		constant_b = 0.92
		constant_c = 0.03

		ap750 = aptot[idx750]
		R1 = (constant_a * aptot[idx380]) - aptot[idx505]

		R2 = aptot[idx580] - (constant_b * aptot[idx692])

		if (R1 <= 0) or (R2 <= 0):
			S = 0
		else:
			R = R1 / R2
			S = 0.0001
			L1 = (constant_a * np.exp(-380 * S)) - np.exp(-505 * S)
			L2 = np.exp(-580 * S) - (constant_b * np.exp(-692 * S))

			L = L1 / L2

			while (S < constant_c):
				S += 0.0001
				L = (constant_a * np.exp(-380 * S) - constant_a * np.exp(-505 * S))

				if phycobilin:
					L /= (np.exp(-widx * S) - (constant_b * np.exp(-692 * S)))
				else:
					L /= (np.exp(-580 * S) - (constant_b * np.exp(-692 * S)))

				if (L / R) >= 1:
					break #raise value error here

		if (S == 0) or (S == constant_c):
			A = 0
		else:
			A = (constant_a * aptot[idx380] - aptot[idx505]) / (constant_a * np.exp(-380 * S) - np.exp(-505 * S))

		slope = A * np.exp(-S * ap_lambda) - A * np.exp(-750 * S)

	    # Calculate phytoplankton specific np.absorption
		aphy = aptot - slope

		return aphy


	aptot = np.array(aptot)
	ap_lambda = np.array(ap_lambda)
	
	aptot = apply_blank_correction(aptot, blank)
	aptot = convert_absorbance_to_absorption(aptot, ap_lambda, diam, vol, betac1, betac2)

	# Normalise to minimum value (~750 nm)
	if norm_750:
		aptot = normalize_to_750nm(aptot, ap_lambda)

	if bricaud_slope: # See Bricaud & Stramski 1990 for more details
		aphy = calculate_bricaud_slope(ap_lambda, aptot, phycobilin)

	else:
		if depig is None:
			raise ValueError('UserError - no depigmented data provided.')
		# Convert from np.absorbance to np.absorption
		depig = apply_blank_correction(depig, blank)
		depig = convert_absorbance_to_absorption(depig, ap_lambda, diam, vol, betac1, betac2)

 		# Normalise to minimum value (~750 nm)
		if norm_750:
			depig = normalize_to_750nm(depig, ap_lambda)

		# Calculate phytoplankton specific np.absorption
		aphy = aptot - depig
	
	if chl is None:
		return aphy
	
	else:
		aphy /= chl
		return aphy
	

def calculate_instrument_led_correction(aphy, ap_lambda, method=None, chl=None, e_background=None, e_insitu=None, e_actinic=None, depth=None, e_led=None, wl=None):
	"""

	Calculate the spectral correction factor.

	TO DO: Add in functionality to calculate mixed excitation wavelength spectra for FastOcean when using more than wavelength

	Parameters
	----------

	aphy : np.ndarray, dtype=float, shape=[n,]
		The wavelength specific phytoplankton np.absorption coefficients.
	ap_lambda : np.ndarray, dtype=int, shape=[n,]
		The wavelengths associated with the aphy and aphy_star.
	method : 'sigma', 'actinic', default=None
		Choose spectral correction method to either correct sigmaPSII or correct the background actinic light.
	e_background : 'insitu', 'actinic', default=None
		For sigma spectral correction factor, select either insitu light (e.g. for underway or insitu measurements) or actinic light (e.g. for fluorescence light curves) as the background light source
	e_insitu : np.ndarray, dtype=int, shape=[n,], default=None
		The in situ irradiance field, if None is passed then will theoretically calculate in situ light field.
	chl : dtype=float, default=None
		Chlorophyll-a concentration (mg per metre cubed) for estimation of Kbio for theoretical in situ light field. Must be set if theoretically calculating e_insitu.
	e_actinic : 'fastact', default=None
		Actinic light spectrum e.g. Spectra of the Actinic lights within the FastAct illuminating during Fluorescence Light Curves etc. Must be defined for 'actinic' method.
	depth : float, default=None
		The depth of the measurement. Must be set if theoretically calculating e_insitu.
	e_led : 'fire','fasttracka_ii', 'fastocean', default=None
		The excitation spectra of the instrument for sigma spectral corrections.
	wl : '450nm', '530nm', 624nm', None, default=None
		For FastOcean only. Select the excitation wavelength. Future PPU versions will provide option to mix LEDs.

	Returns
	-------

	scf : float
		The spectral correction factor to correct sigmaPSII or actinic background light depending on method.

	Example
	-------
	>>> ppu.calculate_instrument_led_correction(aphy, wavelength, e_led='fire')

	"""
	# Define path directory to constants for spectal correction
	module_dir = os.path.dirname(__file__)
	data_dir = os.path.join(module_dir, 'data')
	data_file = os.path.join(data_dir, 'spectral_correction_constants.csv')

	df = pd.read_csv(data_file, index_col=0)
	df = df.sort_index()

	aphy = np.array(aphy)
	ap_lambda = np.array(ap_lambda)

	# Reindex the data to be 1 nm resolution from 400-700nm
	aphy = pd.DataFrame(aphy, index=ap_lambda)
	aphy = np.squeeze(aphy.reindex(np.arange(400, 701, 1)).values)
	aphy = aphy / np.nanmax(aphy)

	if method is None:
		raise ValueError('User must select spectral correction method for correcting sigma or correcting actinic light')

	if method == 'sigma':
		if e_background is None:
			raise ValueError("User must define either actinic or in situ or provide spectra for sigma correction")
		elif isinstance(e_background, str): # Check if e_background is a string
			if e_background == 'insitu':				
				if e_insitu is None:
					if depth is None and chl is None:
						raise ValueError('User must define depth and chlorophyll-a concentration in mg per metre cubed for calculating in situ light spectra')
					else:
						kd = df.a_W + df.bb_W + (df.chi * chl ** df.e)
						e_background = df.Ezero * np.exp(-kd * depth)

			elif e_background == 'actinic':
				e_background = df.fastact.values

		else:
			if not isinstance(e_background, np.ndarray):
				raise ValueError("Invalid data type for e_background. Provide either a string or a numpy np.array.")

		e_background = e_background / np.nanmax(e_background)

		if e_led is None:
			raise ValueError("No instrument selected. Unable to calculate sigma spectral correction factor.")
		elif isinstance(e_led, str):  # Check if e_led is a string
			if e_led == 'fire':
				e_led = df.fire.values
			elif e_led == 'fasttracka_ii':
				e_led = df.fasttracka_ii.values
			elif e_led == 'fastocean':
				if wl is None:
					raise ValueError("User must select single excitation wavelength for FastOcean.")
				elif wl == '450nm':
					e_led = df.fastocean_450.values
				elif wl == '530nm':
					e_led = df.fastocean_530.values
				elif wl == '624nm':
					e_led = df.fastocean_624.values
		        else:
					raise ValueError("Invalid excitation wavelength choice for FastOcean.")
			else:
				raise ValueError("Invalid instrument choice for e_led.")
		else:
			if not isinstance(e_led, np.ndarray):
				raise ValueError("Invalid data type for e_led. Provide either a string or a numpy np.array.")
		
		e_led = e_led / np.nanmax(e_led)
		
		# Perform SCF calculation for sigma
		scf = (np.nansum(aphy * e_background) * np.nansum(e_led)) / (np.nansum(aphy * e_led) * np.nansum(e_background))

	if method == 'actinic':
		if e_insitu is None:
			if depth and chl is None:
				raise ValueError('User must define depth and chlorophyll-a concentration in mg per metre cubed for calculating in situ light spectra')
			else:
				kd = df.a_W + df.bb_W + (df.chi * chl ** df.e)
				e_insitu = df.Ezero * np.exp(-kd * depth)
		else:
			if not isinstance(e_insitu, np.ndarray):
				raise ValueError("Invalid data type for e_insitu. Provide a numpy np.array for in situ spectra.")
	        
		e_insitu = e_insitu / np.nanmax(e_insitu)

		if e_actinic == 'fastact':
			e_actinic = df.fastact.values
			e_actinic = e_actinic / np.nanmax(e_actinic)
		elif isinstance(e_actinic, np.ndarray):
			e_actinic = e_actinic / np.nanmax(e_actinic)
		else:
			raise ValueError("Invalid data type for e_actinic. Provide either 'fastact' or a numpy np.array.")

		# Perform SCF calculation for the actinic light
		scf = (np.nansum(aphy * e_actinic) * np.nansum(e_insitu)) / (np.nansum(aphy * e_insitu) * np.nansum(e_actinic))

	return scf


