#!/usr/bin/env python
	
from ._fitting import __fit_kpf_saturation__
import pandas as pd
import numpy as np

def fit_saturation(pfd, flevel, seq, datetime, blank=0, sat_len=100, skip=0, ro=0.3, model_type=None, bounds=True, sig_lims =[100, 2200], ro_lims=[0.01, 1.0], datetime_unique=False, method='trf', loss='soft_l1', f_scale=0.1, max_nfev=None, xtol=1e-9):
    
	"""
	Process the raw transient data and perform the Kolber et al. 1998 saturation model.


	Parameters
	----------
	pfd : np.array, dtype=float, shape=[n,] 
		The photon flux density of the instrument in micromole photons per meter squared per second.
	flevel : np.array, dtype=float, shape=[n,] 
		The fluorescence yield of the instrument.
	seq : np.array, dtype=int, shape=[n,] 
		The measurement number.
	datetime : np.array, dtype=datetime64, shape=[n,]
		The date & time of each measurement.
	blank : float, default=0
		The blank value of the measurement.
	sat_len : int, default=100
		The number of flashlets in saturation sequence.
	skip : int, default=0
		the number of flashlets to skip at start.
	ro : float, default=0.3
		The fixed value of the connectivity coefficient. Required if model type is 'fixed_ro'.
	model_type : str, default=None
		Options are 'no_ro', 'fixed_ro' or 'calc_ro'.
	bounds : bool, default=True
		If True, will set lower and upper limit bounds for the estimation, not suitable for methods 'lm'.
	sig_lims : [int, int], default=[100, 2200]
	 	The lower and upper limit bounds for fitting sigmaPSII.
	ro_lims: [float, float], default=[0.01, 1.0]
		The lower and upper limit bounds for fitting the connectivity coefficient. Not required if no_ro and fixed_ro are False.
	datatime_unique: bool, default=False
		If True, will find the unique datetime values for each fit.
	method : str, default='trf'
		The algorithm to perform minimization. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	loss : str, default='soft_l1'
		The loss function to be used. Note: Method ‘lm’ supports only ‘linear’ loss. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	f_scale : float, default=0.1
	 	The soft margin value between inlier and outlier residuals. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	max_nfev : int, default=None		
		The number of iterations to perform fitting routine. If None, the value is chosen automatically. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.
	xtol : float, default=1e-9			
		The tolerance for termination by the change of the independent variables. See ``scipy.optimize.least_squares`` documentation for more information on non-linear least squares fitting options.

	Returns
	-------

	res: pandas.DataFrame
		The results of the fitting routine with columns as below:
	fo : np.array, dtype=float, shape=[n,]
		The minimum fluorescence level.
	fm : np.array, dtype=float, shape=[n,]
		The maximum fluorescence level.
	sigma : np.array, dtype=float, shape=[n,]
		The effective absorption cross-section of PSII, sigmaPSII, in angstroms squared.
	fvfm : np.array, dtype=float, shape=[n,]
		The maximum photochemical efficiency.
	ro : np.array, dtype=float, shape=[n,]
		The connectivity coefficient, ro. If model_type is no_ro the value is np.nan.
	bias : np.array, dtype=float, shape=[n,]
		The bias of the fit.
	rmse : np.array, dtype=float, shape=[n,]
		The root mean squared error of the fit.
	nrmse : np.array, dtype=float, shape=[n,]
		The root mean squared error of the fit normalised to the mean of the fluorescence level.
	fo_err : np.array, dtype=float, shape=[n,]
		The fit error of Fo in %.
	fm_err : np.array, dtype=float, shape=[n,]
		The fit error of Fm in %.
	sigma_err : np.array, dtype=float, shape=[n,]
		The fit error of sigmaPSII.
	ro_err : np.array, dtype=float, shape=[n,]
		The fit error of ro, if model_type is no_ro and fixed_ro the value is np.nan.
	snr_raw : np.array, dtype=float, shape=[n,]
		Fv normalised to the last 5 flevel measurements.
	nfl : np.array, dtype=int, shape=[n,]
		The number of flashlets used for fitting.
	niters : np.array, dype=int, shape=[n,]
		The number of functional evaluations done on the fitting routine.
	flag : np.array, dtype=int, shape=[n,]
		The code associated with the fitting routine success, positive values = SUCCESS, negative values = FAILURE.
		-3 : Unable to calculate parameter errors.
		-2 : Fo is greater than Fm.
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
	>>> sat = ppu.calculate_saturation(pfd, flevel, seq, datetime, blank=0, sat_len=100, skip=0, ro=0.3, no_ro=False, fixed_ro=True, sig_lims =[100,2200])
	"""

	pfd = np.array(pfd)
	flevel = np.array(flevel)
	seq = np.array(seq)
	dt = np.array(datetime)

	if model_type == None:
		raise ValueError('No model type selected. Please select from no_ro, fixed_ro or calc_ro.')
	if (model_type == 'fixed_ro') & (ro == None) | (ro == 0):
		raise ValueError('When running fixed_ro fitting you must provide a value for ro, which must be greater than 0.')

	if model_type == 'calc_ro':
		opts = {'bounds':bounds, 'sig_lims':sig_lims, 'ro_lims':ro_lims, 'method':method,'loss':loss, 'f_scale':f_scale, 'max_nfev':max_nfev, 'xtol':xtol} 
	else:
		opts = {'bounds':bounds, 'sig_lims':sig_lims,  'method':method,'loss':loss, 'f_scale':f_scale, 'max_nfev':max_nfev, 'xtol':xtol} 

	res = []

	for s in np.unique(seq):
		i = seq == s
		x = pfd[i]
		y = flevel[i]
		sat = __fit_kpf_saturation__(x[skip:sat_len], y[skip:sat_len], ro, model_type, **opts)
		res.append(pd.Series(sat))

	res = pd.concat(res, axis=1).T
	res.columns = ['fo', 'fm', 'sigma', 'ro', 'bias', 'rmse', 'nrmse', 'fo_err', 'fm_err', 'sigma_err', 'ro_err', 'snr_raw', 'nfl', 'niters', 'flag', 'success']
	res['fo'] -= blank
	res['fm'] -= blank
	fvfm = (res.fm - res.fo) / res.fm
	res.insert(3, "fvfm", fvfm)

	if datetime_unique:
		res['datetime'] = np.unique(dt)
	else:
		res['datetime'] = dt[0]
	
	return res
