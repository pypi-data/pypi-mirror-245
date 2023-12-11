#!/usr/bin/env python

from ._equations import __calculate_residual_etr__, __calculate_residual_phi__, __calculate_residual_beta__, __calculate_residual_mbeta__, __calculate_alpha_model__, __calculate_beta_model__, __calculate_modified_alpha_model__, __calculate_modified_beta_model__, __calculate_bias__, __calculate_fit_errors__, __calculate_rmse__, __calculate_nrmse__
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import warnings

def calculate_amplitude_etr(fo, fm, sigma, par, alpha_phase=True, light_independent=True, dark_sigma=False, etrmax_fitting=True, serodio_sigma=False, light_step_size=None, last_steps_average=False, outlier_multiplier=3, return_data=False, bounds=True, alpha_lims=[0,4], etrmax_lims=[0,2000], method='trf', loss='soft_l1', f_scale=0.1, max_nfev=None, xtol=1e-9):
      
	"""
	
	Convert the processed transient data into an electron transport rate and perform a fit using the Webb Model.

	Parameters
	----------
	fo : np.array, dtype=float, shape=[n,]
		The minimum fluorescence level.
	fm : np.array, dtype=float, shape=[n,] 
		The maximum fluorescence level.
	sigma : np.array, dtype=float, shape=[n,] 
		The effective absorption cross-section of PSII in angstrom squared.
	par : np.array, dtype=float, shape=[n,]
		The actinic light levels in microEinsteins per meter squared per second.
	alpha_phase : bool, default=True
		If True, will fit the data without photoinhibition. If False, will fit the data with the photoinhibition paramater beta.
	light_independent : bool, default=True
		If True, will use the method outlined in Silsbe & Kromkamp 2012. 
	dark_sigma : bool
		If True, will use mean of sigmaPSII under 0 actinic light for calculation. If False, will use sigmaPSII and sigmaPSII' for calculation.
	etrmax_fitting : bool
		If True, will fit alpha_ETR and ETR_max and manually calculate Ek. If False, will fit alpha_ETR and Ek and manually calculate ETR_max.
	serodio_sigma : bool
		If True, will apply a Serodio correction for samples that have dark relaxation.
	light_step_size : int
		The number of measurements for initial light step.
	last_steps_average : bool, default=False,
		If True, means will be created from the last 3 measurements per light step. Else, mean will be created from entire light step excluding outliers.
	outlier_multiplier : int, default=3
		The multiplier to apply to the standard deviation for determining the upper and lower limits.
	return_data : bool, default=False
		If True, will return the final data used for the fit.
	bounds : bool, default=True
		If True, will set lower and upper limit bounds for the estimation, not suitable for methods 'lm'.
	alpha_lims : [int, int], default=[0,4]
		The lower and upper limit bounds for fitting alpha_ETR.
	etrmax_lims : [int, int], default=[0,2000]
	 	The lower and upper limit bounds for fitting ETR_max, or bounds for Ek if etrmax_fitting is False.
	fit_method : str, default='trf'
		The algorithm to perform minimization. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	loss_method : str, default='soft_l1'
		The loss function to be used. Note: Method ‘lm’ supports only ‘linear’ loss. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	fscale : float, default=0.1
	 	The soft margin value between inlier and outlier residuals. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	max_nfev : int, default=None		
		The number of iterations to perform fitting routine. If None, the value is chosen automatically. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	xtol : float, default=1e-9			
		The tolerance for termination by the change of the independent variables. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.

	Returns
	-------
	
	Results are returned as pd.Series with the following parameters.

	etr_max : float
		The maximum electron transport rate, ETR_max.
	slope : float
		The light limited slope of electron transport, alpha_ETR.
	ek : float
		The photoacclimation parameter of ETR, Ek.
	alpha_bias : float
		The bias of the alpha fit. If alpha_phase is False, value is np.nan.
	alpha_rmse : float
		The root mean squared error of the alpha fit. If alpha_phase is False, value is np.nan.
	alpha_nrmse : float
		The normalised root mean squared error of the alpha fit. If alpha_phase is False, value is np.nan.
	beta_bias : float
		The bias of the beta fit. If alpha_phase is True, value is np.nan.
	beta_rmse : float
		The root mean squared error of the beta fit. If alpha_phase is True, value is np.nan.
	beta_nrmse : float
		The normalised root mean squared error of the beta fit. If alpha_phase is True, value is np.nan.
	etrmax_err : float
		The fit error of ETR_max. If etrmax_fitting is False and alpha_phase is True, value returned is np.nan.
	slope_err : float
		The fit error of αlpha_ETR.
	ek_err : float
		The fit error of Ek. If etrmax_fitting is True, value returned is np.nan.
	alpha_nfev : np.array, dype=int, shape=[n,]
		The number of functional evaluations done on the alpha phase fitting routine.
	alpha_flag : np.array, dtype=int, shape=[n,]
		The code associated with the fitting routine success.
		0 : the maximum number of function evaluations is exceeded.
		1 : gtol termination condition is satisfied.
		2 : ftol termination condition is satisfied.
		3 : xtol termination condition is satisfied.
		4 : Both ftol and xtol termination conditions are satisfied.
	alpha_success : np.array, dtype=bool, shape=[n,]
		A boolean array reporting whether fit was successful (TRUE) or if not successful (FALSE)
	beta_nfev : np.array, dype=int, shape=[n,]
		The number of functional evaluations done on the beta phase fitting routine. If alpha_phase is True, value returned is np.nan.
	beta_flag : np.array, dtype=int, shape=[n,]
		The code associated with the fitting routine success. If alpha_phase is True, value returned is np.nan.
		0 : the maximum number of function evaluations is exceeded.
		1 : gtol termination condition is satisfied.
		2 : ftol termination condition is satisfied.
		3 : xtol termination condition is satisfied.
		4 : Both ftol and xtol termination conditions are satisfied.
	beta_success : np.array, dtype=bool, shape=[n,]
		A boolean array reporting whether fit was successful (TRUE) or if not successful (FALSE). If alpha_phase is True, value returned is np.nan.
	data : [np.array, np.array]
		Optional, the final data used for the fitting procedure.


	Example
	-------
	>>> res = ppu.calculate_etr(fo, fm, sigma, par, return_data=False)
	"""

	warnings.simplefilter(action = "ignore", category = RuntimeWarning)

	fo, fm, sigma, par = map(np.array, [fo, fm, sigma, par])
	fvfm = (fm - fo) / fm

	sigma_etr = np.nanmean(sigma[0:light_step_size])
		
	if light_independent:
		if serodio_sigma:
			dff = pd.DataFrame([par, fo, fm, sigma])
			dff = dff.T
			dff.columns = ['par', 'fo', 'fm', 'sigma']
			if last_steps_average:
				dff = dff.groupby('par').apply(lambda x: x.iloc[-3:].mean()).reset_index(drop=True)
			else:
				dff = dff.groupby('par').mean().reset_index()
			
			idx = dff.fm.idxmax() + 1
			sigma_etr = dff.sigma.iloc[:idx].max()
			fo[:dff.fo.idxmax()] = dff.fo.max()
			fm[:dff.fm.idxmax()] = dff.fm.max()
			fvfm = (fm - fo) / fm
			etr = fvfm / np.nanmean(fvfm[0:light_step_size])

		else:
			fvfm = (fm - fo) / fm 
			etr = fvfm / np.nanmean(fvfm[0:light_step_size])
	else:
		if dark_sigma:
			etr = (par * np.nanmean(sigma[0:light_step_size]) * (fvfm / np.nanmean(fvfm[0:light_step_size]))) * 6.022e-3

		else:
			f_o = np.nanmean(fo[0:light_step_size]) / (np.nanmean(fvfm[0:light_step_size]) + (np.nanmean(fo[0:light_step_size])/fm))
			fqfv = (fm - fo) / (fm - f_o)
			etr = par * sigma * fqfv * 6.022e-3

	df = pd.DataFrame([par, etr])
	df = df.T
	df.columns = ['par', 'etr']

	# create means of each light step using last n measurements
	if last_steps_average:
		df = df.groupby('par').apply(lambda x: x.iloc[-3:].mean()).reset_index(drop=True)
	else:
		# exclude outliers if more than mean ± (stdev * multiplier)
		grouped = df.groupby('par')
		grouped_mean = grouped['etr'].transform('mean')
		grouped_stdev = grouped['etr'].transform('std')

		ulim = (grouped_mean + grouped_stdev * outlier_multiplier)
		llim = (grouped_mean - grouped_stdev * outlier_multiplier)

		df['etr'] = df.apply(lambda row: row['etr'] if (row['etr'] <= ulim[row.name]) and (row['etr'] >= llim[row.name]) else np.nan, axis=1)

		df = df.groupby('par').mean().reset_index()

	# Define data for fitting and estimates of ETRmax and alpha
	P = np.array(df.etr)
	E = np.array(df.par)

	p0 = [1000, 1]

	# Mask missing data
	if light_independent:
		mask = np.isnan(P) | np.isnan(E) | (P < 0) | (E == 0)
	else:
		mask = np.isnan(P) | np.isnan(E)
	
	E = E[~mask]
	P = P[~mask]

	if bounds:
		bds = [etrmax_lims[0], alpha_lims[0]],[etrmax_lims[1], alpha_lims[1]]
		if (bds[0][0] > bds[1][0]) | (bds[0][1] > bds[1][1]):
			print('Lower bounds greater than upper bounds - fitting with no bounds.')
			bds = [-np.inf, np.inf]
	else:
		bds = [-np.inf, np.inf]

	if max_nfev is None:
		opts = {'method':method, 'loss':loss, 'f_scale':f_scale, 'xtol':xtol} 
	else:
		opts = {'method':method, 'loss':loss, 'f_scale':f_scale, 'max_nfev':max_nfev, 'xtol':xtol} 

	try:
		if light_independent:
			
			popt = least_squares(__calculate_residual_phi__, p0, args=(E, P), bounds=(bds), **opts)
			sol = __calculate_modified_alpha_model__(E, *popt.x)
			
			if alpha_phase:
				beta_vars = {k: np.nan for k in ["beta_bias", "beta_rmse", "beta_nrmse", "beta_nfev", "beta_flag", "beta_success"]}
				beta_bias, beta_rmse, beta_nrmse, beta_nfev, beta_flag, beta_success = beta_vars.values()

				if etrmax_fitting:				
					etr_max = popt.x[0] * sigma_etr * 6.022e-3
					slope = popt.x[1] * sigma_etr * 6.022e-3
					ek = etr_max / slope
				else:
					ek = popt.x[0] 
					slope = popt.x[1] * sigma_etr * 6.022e-3
					etr_max = ek * slope
			else:
				eB = popt.x[0]
				a = popt.x[1]
				popt_beta = least_squares(__calculate_residual_mbeta__, p0, args=(E, P, a, eB), **opts)
				solb = __calculate_modified_beta_model__(E, *popt_beta.x, a, eB)
				ek = popt.x[0]
				slope = popt.x[1]
				etr_max = popt_beta.x[0]
				beta_nfev = max_nfev if max_nfev is not None else popt_beta.nfev
				beta_flag = popt_beta.status
				beta_success = popt_beta.success
				beta_bias = __calculate_bias__(solb, P)
				beta_rmse = __calculate_rmse__(popt_beta.fun, P)
				beta_nrmse = __calculate_nrmse__(popt_beta.fun, P)
				beta_perr = __calculate_fit_errors__(popt_beta.jac, popt_beta.fun)	

		else:
			
			popt = least_squares(__calculate_residual_etr__, p0, args=(E, P), bounds=(bds), **opts)
			sol = __calculate_alpha_model__(E, *popt.x)
			
			if alpha_phase:
				beta_vars = {k: np.nan for k in ["beta_bias", "beta_rmse", "beta_nrmse", "beta_nfev", "beta_flag", "beta_success"]}
				beta_bias, beta_rmse, beta_nrmse, beta_nfev, beta_flag, beta_success = beta_vars.values()
				
				if etrmax_fitting:				
					etr_max = popt.x[0] * sigma_etr * 6.022e-3
					slope = popt.x[1] * sigma_etr * 6.022e-3
					ek = etr_max / slope
				else:
					ek = popt.x[0] 
					slope = popt.x[1] * sigma_etr * 6.022e-3
					etr_max = ek * slope
			else:
				eB = popt.x[0]
				a = popt.x[1]
				popt_beta = least_squares(__calculate_residual_beta__, p0, args=(E, P, a, eB), **opts)
				solb = __calculate_modified_beta_model__(E, *popt_beta.x, a, eB)
				ek = popt.x[0]
				slope = popt.x[1]
				etr_max = popt_beta.x[0]
				beta_nfev = max_nfev if max_nfev is not None else popt_beta.nfev
				beta_flag = popt_beta.status
				beta_success = popt_beta.success
				beta_bias = __calculate_bias__(solb, P)
				beta_rmse = __calculate_rmse__(popt_beta.fun, P)
				beta_nrmse = __calculate_nrmse__(popt_beta.fun, P)
				beta_perr = __calculate_fit_errors__(popt_beta.jac, popt_beta.fun)


		alpha_bias = __calculate_bias__(sol, P)
		alpha_rmse = __calculate_rmse__(popt.fun, P)
		alpha_nrmse = __calculate_nrmse__(popt.fun, P)
		alpha_perr = __calculate_fit_errors__(popt.jac, popt.fun)
		alpha_flag = popt.status
		alpha_success = popt.success
		alpha_nfev = max_nfev if max_nfev is not None else popt.nfev

		if etrmax_fitting:
			etr_max_err = alpha_perr[0]
			slope_err = alpha_perr[1]
			ek_err = np.nan
		else:
			if alpha_phase:
				ek_err = alpha_perr[0]
				slope_err = alpha_perr[1]
				etr_max_err = np.nan
			else:
				ek_err = alpha_perr[0]
				slope_err = alpha_perr[1]
				etr_max_err = beta_perr[0]
	
	except Exception as e:
		if str(e) == "x0 is infeasible":
			print("x0 is infeasible.")

		alpha_flag = -1
		alpha_success = False
		beta_flag = -1
		beta_success = False
		etr_max, slope, ek, etr_max_err, slope_err, ek_err, alpha_bias, alpha_rmse, alpha_nrmse, alpha_nfev, beta_bias, beta_rmse, beta_nrmse, beta_nfev = [np.nan] * 14

	results = pd.Series({
		"etr_max": etr_max,
		"slope": slope,
		"ek": ek,
		"etr_max_err": etr_max_err,
		"slope_err": slope_err,
		"ek_err": ek_err,
		"alpha_bias": alpha_bias,
		"alpha_rmse": alpha_rmse,
		"alpha_nrmse": alpha_nrmse,
		"alpha_nfev": alpha_nfev,
		"alpha_flag": alpha_flag,
		"alpha_success": alpha_success,
		"beta_bias": beta_bias,
		"beta_rmse": beta_rmse,
		"beta_nrmse": beta_nrmse,
		"beta_nfev": beta_nfev,
		"beta_flag": beta_flag,
		"beta_success": beta_success,
	})

	if return_data:
		return results, [E, P]
	else:
		return results
