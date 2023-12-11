#!/usr/bin/env python

from ._fitting import __fit_kpf_relaxation__
import numpy as np
import pandas as pd

def fit_relaxation(flevel, seq_time, seq, datetime, blank=0, sat_len=None, rel_len=None, sat_flashlets=0, model_type=None, bounds=True,  tau1_lims=[100, 800], tau2_lims=[800, 2000], tau3_lims=[2000, 50000], method='trf', loss='soft_l1', f_scale=0.1, max_nfev=None, xtol=1e-9):
	"""

	Process the raw transient data and perform the Kolber et al. 1998 relaxation model.

	Parameters
	----------
	seq_time : np.array, dtype=float, shape=[n,] 
		The sequence time of the flashlets in miroseconds.
	flevel : np.array, dtype=float, shape=[n,] 
		The fluorescence yield of the instrument.
	seq : np.array, dtype=int, shape=[n,] 
		The measurement number.
	datetime : np.array, dtype=datetime64, shape=[n,]
		The date & time of each measurement in the numpy np.datetime64 format.
	blank : float, default=0
		The blank value of the measurement.
	sat_len : int, default=None
		The number of flashlets in the saturation sequence.
	rel_len : int, default=None
		The number of flashlets in the relaxation sequence.
	sat_flashlets : int, default=0
		The number of saturation flashlets to include at the start.
	model_type : str, default=None
		Options are 'single' or 'triple'.
	bounds : bool, default=True
		If True, will set lower and upper limit bounds for the estimation, not suitable for methods 'lm'.
	tau1_lims: [int, int], default=[100, 800]
	 	The lower and upper limit bounds for fitting tau1.
	tau2_lims: [int, int], default=[800, 2000]
	 	The lower and upper limit bounds for fitting tau2, not required if model_type = 'triple'.
	tau3_lims: [int, int], default=[2000, 50000]
	 	The lower and upper limit bounds for fitting tau3, not required if model_type = 'triple'.
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
	res: pandas.DataFrame
		The results of the fitting routine with columns as below:
	fo_r : np.array, dtype=float, shape=[n,]
		The minimum fluorescence level of relaxation phase.
	fm_r : np.array, dtype=float, shape=[n,]
		The maximum fluorescence level of relaxation phase
	tau1 : np.array, dtype=float, shape=[n,]
		The rate of QA reoxidation in microseconds.
	tau2 : np.array, dtype=float, shape=[n,]
		The rate of QB reoxidation in microseconds, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	tau3 : np.array, dtype=float, shape=[n,]
		The rate of PQ reoxidation in microseconds, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha1 : np.array, dtype=float, shape=[n,]
		The decay coefficient of tau1, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha2 : np.array, dtype=float, shape=[n,]
		The decay coefficient of tau2, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha3 : np.array, dtype=float, shape=[n,]
		The decay coefficient of tau3, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	bias : np.array, dtype=float, shape=[n,]
		The bias of the fit.
	rmse : np.array, dtype=float, shape=[n,]
		The root mean squared error of the fit.
	nrmse : np.array, dtype=float, shape=[n,]
		The root mean squared error of the fit normalised to the mean of the fluorescence level.
	fo_err : np.array, dtype=float, shape=[n,]
		The fit error of Fo_relax in %.
	fm_err : np.array, dtype=float, shape=[n,]
		The fit error of Fm_relax in %.
	tau1_err : np.array, dtype=float, shape=[n,]
		The fit error of tau1.
	tau2_err : np.array, dtype=float, shape=[n,]
		The fit error of tau2, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	tau3_err : np.array, dtype=float, shape=[n,]
		The fit error of tau3, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha1_err : np.array, dtype=float, shape=[n,]
		The fit error of alpha1, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha2_err : np.array, dtype=float, shape=[n,]
		The fit error of alpha2, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	alpha3_err : np.array, dtype=float, shape=[n,]
		The fit error of alpha3, only returned if model_type is 'triple', value set to numpy np.nan otherwise.
	nfl : np.array, dtype=int, shape=[n,]
		The number of flashlets used for fitting.
	niters : np.array, dype=int, shape=[n,]
		The number of functional evaluations done on the fitting routine.
	flag : np.array, dtype=int, shape=[n,]
		The code associated with the fitting routine success, positive values = SUCCESS, negative values = FAILURE.
		-3 : Unable to calculate parameter errors.
		-2 : FoRelax is greater than FmRelax.
		-1 : improper input parameters status returned from MINPACK.
		0 : the maximum number of function evaluations is exceeded.
		1 : gtol termination condition is satisfied.
		2 : ftol termination condition is satisfied.
		3 : xtol termination condition is satisfied.
		4 : Both ftol and xtol termination conditions are satisfied.
	success : np.array, dtype=bool, shape=[n,]
		A boolean array reporting whether fit was successful (TRUE) or if not successful (FALSE)
	datetime : np.array, dtype=datetime64, shape=[n,]
		The date and time associated with the measurement.

	Example
	-------
	>>> rel = ppu.calculate_relaxation(flevel, seq_time, seq, datetime, blank=0, sat_len=100, rel_len=40, model_type='single', bounds=True, tau1_lims=[100, 50000])
	"""
		
	seq_time = np.array(seq_time)
	flevel = np.array(flevel)
	seq = np.array(seq)
	dt = np.array(datetime)

	if model_type == None:
		raise ValueError('No model type selected. Please select from single or triple.')

	if model_type == 'single':
		opts = {'sat_flashlets':sat_flashlets, 'bounds':bounds, 'tau1_lims':tau1_lims, 'method':method,'loss':loss, 'f_scale':f_scale, 'max_nfev':max_nfev, 'xtol':xtol} 
	else:
		opts = {'sat_flashlets':sat_flashlets, 'bounds':bounds, 'tau1_lims':tau1_lims, 'tau2_lims':tau2_lims, 'tau3_lims':tau3_lims, 'method':method,'loss':loss, 'f_scale':f_scale, 'max_nfev':max_nfev, 'xtol':xtol} 
	
	res = []
    
	for s in np.unique(seq):

		i = seq == s
		x = seq_time[i]
		y = flevel[i]
		x_min = np.nanmin(x[sat_len:])
		x = x[sat_len-sat_flashlets:sat_len+rel_len] - x_min
		y = y[sat_len-sat_flashlets:sat_len+rel_len]
		rel = __fit_kpf_relaxation__(x, y, model_type, **opts)
		
		res.append(pd.Series(rel))

	res = pd.concat(res, axis=1).T

	res.columns = ['fo_r', 'fm_r', 'tau1', 'tau2', 'tau3', 'alpha1', 'alpha2',  'alpha3', 'bias', 'rsme', 'nrmse', 'for_err', 'fmr_err', 'tau1_err', 'tau2_err', 'tau3_err', 'alpha1_err', 'alpha2_err', 'alpha3_err', 'nfl', 'niters', 'flag', 'success']
	res['datetime'] = np.unique(dt)

	return res



