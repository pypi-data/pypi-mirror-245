#!/usr/bin/env python

import numpy as np
from scipy.optimize import least_squares
from sklearn import linear_model
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

from ._equations import __fit_kolber_nop__, __fit_kolber_p__, __fit_single_relaxation__, __fit_triple_relaxation__, __calculate_residual_saturation_p__, __calculate_residual_saturation_nop__, __calculate_residual_saturation_fixedp__, __calculate_residual_single_relaxation__, __calculate_residual_triple_relaxation__, __calculate_bias__, __calculate_rmse__, __calculate_nrmse__, __calculate_fit_errors__
	
def __fit_kpf_saturation__(pfd, flevel, ro, model_type=None, bounds=False, sig_lims=None, ro_lims=None, method='trf', loss='soft_l1', f_scale=0.1, max_nfev=None, xtol=1e-9):

	try:
		# Count number of flashlets excluding NaNs
		nfl = np.count_nonzero(~np.isnan(flevel))
		m = ~np.isnan(flevel)
		flevel = flevel[m]
		pfd = pfd[m]

		# Estimates of saturation parameters
		model = linear_model.HuberRegressor()
		try:
			x = np.arange(0, 8)[:, None] 
			y = flevel[:8]
			fo_model = model.fit(x, y)
			fo = fo_model.intercept_

			x = np.arange(0, 24)[:, None]
			y = flevel[-24:]
			fm_model = model.fit(x, y)
			fm = fm_model.intercept_

		except Exception:
			fo = flevel.iloc[:3].mean()
			fm = flevel[-3:].mean()

		if (fo > fm) or (fo <= 0):
			print('Fo greater than Fm - skipping fit.')
			nan_array = np.repeat(np.nan, 13)
			return tuple(nan_array) + (-2, False)

		fo10 = fo * 0.1
		fm10 = fm * 0.1
		sig = 500

		if model_type == 'calc_ro':
			ro = 0.3
			x0 = [fo, fm, sig, ro]
		else:
			x0 = [fo, fm, sig]

		if bounds:
			if model_type == 'calc_ro':
				bds = [fo - fo10, fm - fm10, sig_lims[0], ro_lims[0]]
				upper_bounds = [fo + fo10, fm + fm10, sig_lims[1], ro_lims[1]]
			else:
				bds = [fo - fo10, fm - fm10, sig_lims[0]]
				upper_bounds = [fo + fo10, fm + fm10, sig_lims[1]]

			bds = [bds, upper_bounds]

			if any(bd[0] > bd[1] for bd in bds):
				print('Lower bounds greater than upper bounds - fitting with no bounds.')
				bds = [-np.inf, np.inf]
		else:
			bds = [-np.inf, np.inf]

		if max_nfev is None:
			opts = {'method': method, 'loss': loss, 'f_scale': f_scale, 'xtol': xtol}
		else:
			opts = {'method': method, 'loss': loss, 'f_scale': f_scale, 'max_nfev': max_nfev, 'xtol': xtol}

		if model_type == 'no_ro':
			popt = least_squares(__calculate_residual_saturation_nop__, x0, bounds=bds, args=(pfd, flevel), **opts)
		elif model_type == 'fixed_ro':
			popt = least_squares(__calculate_residual_saturation_fixedp__, x0, bounds=bds, args=(pfd, flevel, ro), **opts)
		else:
			popt = least_squares(__calculate_residual_saturation_p__, x0, bounds=bds, args=(pfd, flevel), **opts)

		fo = popt.x[0]
		fm = popt.x[1]
		sigma = popt.x[2]      

		# Calculate curve fitting statistical metrics
		if model_type == 'no_ro':
			sol = __fit_kolber_nop__(pfd, *popt.x) 
		elif model_type == 'fixed_ro':
			sol = __fit_kolber_p__(pfd, *popt.x, ro) 
		else:
			sol = __fit_kolber_p__(pfd, *popt.x)

		bias = __calculate_bias__(sol, flevel)
		rmse = __calculate_rmse__(popt.fun, flevel)
		nrmse = __calculate_nrmse__(popt.fun, flevel)
		perr = __calculate_fit_errors__(popt.jac, popt.fun)
		fo_err = (perr[0] / fo) * 100
		fm_err = (perr[1] / fm) * 100
		sigma_err = perr[2]
		snr_raw = np.mean((fm - fo) / flevel[-5:])

		if model_type == 'calc_ro':
			ro = popt.x[3]
			ro_err = perr[3]
		else:
			if model_type == 'fixed_ro':
				ro = ro
			else:
				ro = np.nan
			ro_err = np.nan
	    
		if max_nfev is None:
			nfev = popt.nfev
		else:
			nfev = max_nfev

		flag = popt.status
		success = popt.success

		return fo, fm, sigma, ro, bias, rmse, nrmse, fo_err, fm_err, sigma_err, ro_err, snr_raw, nfl, nfev, flag, success

	except (np.linalg.LinAlgError, Exception) as err:
		print('Unable to calculate fit, skipping sequence.')
		nan_array = np.repeat(np.nan, 13)
		flag = -3 if isinstance(err, np.linalg.LinAlgError) else -1
		return tuple(nan_array) + (flag, False)

def __fit_kpf_relaxation__(seq_time, flevel, model_type=None, sat_flashlets=None, bounds=False, tau1_lims=None, tau2_lims=None, tau3_lims=None, method='trf', loss='soft_l1', f_scale=0.1, max_nfev=None, xtol=1e-9):
	
	# Count number of flashlets excluding NaNs
	nfl = np.count_nonzero(~np.isnan(flevel))
	m = ~np.isnan(flevel)
	flevel = flevel[m]
	seq_time = seq_time[m]

	# Estimates of relaxation parameters
	foRelax = flevel[-3:].mean()
	
	if sat_flashlets is None:
		fmRelax = flevel[:3].mean()
	else:
		fmRelax = flevel[:3+sat_flashlets].mean()
	
	if (foRelax > fmRelax):
		(print('Fo_relax greater than Fm_relax - skipping fit.'))
		nan_array = np.repeat(nan, 21)
		return nan_array + (-2, False)

	fo10 = foRelax * 0.1
	fm10 = fmRelax * 0.1

	if model_type == 'single':
		tau1 = 400
		x0 = [foRelax, fmRelax, tau1]
	else:
		alpha1 = 0.3
		tau1 = 600
		alpha2 = 0.3
		tau2 = 2000
		alpha3 = 0.3
		tau3 = 30000
		x0 = [foRelax, fmRelax, alpha1, tau1, alpha2, tau2, alpha3, tau3]

	if bounds:
		if model_type == 'single':
			bds = [foRelax-fo10, fmRelax-fm10, tau1_lims[0]]
			upper_bounds = [foRelax+fo10, fmRelax+fm10, tau1_lims[1]]
		else:
			bds = [foRelax-fo10, fmRelax-fm10, 0.01, tau1_lims[0], 0.01, tau2_lims[0], 0.01, tau3_lims[0]]
			upper_bounds = [foRelax+fo10, fmRelax+fm10, 1, tau1_lims[1], 1, tau2_lims[1], 1, tau3_lims[1]]

		bds = [bds, upper_bounds]

		if any(bd[0] > bd[1] for bd in bds):
			print('Lower bounds greater than upper bounds - fitting with no bounds.')
			bds = [-np.inf, np.inf]
	else:
		bds = [-np.inf, np.inf]

	if max_nfev is None:
		opts = {'method': method, 'loss': loss, 'f_scale': f_scale, 'xtol': xtol}
	else:
		opts = {'method': method, 'loss': loss, 'f_scale': f_scale, 'max_nfev': max_nfev, 'xtol': xtol}

	try:
		if model_type == 'single':
			popt = least_squares(__calculate_residual_single_relaxation__, x0, bounds=(bds), args=(seq_time, flevel), **opts)
			tau1 = popt.x[2]
			a1, tau2, a2, tau3, a3 = np.repeat(np.nan, 5)
			sol = __fit_single_relaxation__(seq_time, *popt.x)
		else:
			popt = least_squares(__calculate_residual_triple_relaxation__, x0, bounds=(bds), args=(seq_time, flevel), **opts)
			a1 = popt.x[2]
			tau1 = popt.x[3]
			a2 = popt.x[4]
			tau2 = popt.x[5]
			a3 = popt.x[6]
			tau3 = popt.x[7]
			sol = __fit_triple_relaxation__(seq_time, *popt.x)
		
		fo_r =  popt.x[0]
		fm_r = popt.x[1]
		
		bias = __calculate_bias__(sol, flevel)
		rmse = __calculate_rmse__(popt.fun, flevel)		
		nrmse = __calculate_nrmse__(popt.fun, flevel)	
		perr = __calculate_fit_errors__(popt.jac, popt.fun)
		fo_err = (perr[0] / fo_r) * 100
		fm_err = (perr[1] / fm_r) * 100
		
		if model_type == 'single':
			tau1_err = perr[2]
			a1_err, tau2_err, a2_err, tau3_err, a3_err = np.repeat(np.nan, 5)
		else:
			a1_err = perr[2]
			tau1_err = perr[3]
			a2_err = perr[4]
			tau2_err = perr[5]
			a3_err = perr[6]
			tau3_err = perr[7]

		if max_nfev is None:
			nfev = popt.nfev
		else:
			nfev = max_nfev
			
		flag = popt.status
		success = popt.success

		return  fo_r, fm_r, tau1, tau2, tau3, a1, a2, a3, bias, rmse, nrmse, fo_err, fm_err, tau1_err, tau2_err, tau3_err, a1_err, a2_err, a3_err, nfl, nfev, flag, success

	except (np.linalg.LinAlgError, Exception) as err:
		print('Unable to calculate fit, skipping sequence.')
		nan_array = np.repeat(np.nan, 21)
		flag = -3 if isinstance(err, np.linalg.LinAlgError) else -1
		return tuple(nan_array) + (flag, False)
