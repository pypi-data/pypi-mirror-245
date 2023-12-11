#!/usr/bin/env python

from ._equations import __fit_kolber_p__, __fit_kolber_nop__, __fit_single_relaxation__, __fit_triple_relaxation__, __calculate_alpha_model__, __calculate_modified_alpha_model__
import matplotlib.pyplot as plt
import numpy as np

def plot_saturation_data(fyield, pfd, fo=None, fm=None, sigma=None, ro=None, rmse=None, nrmse=None):

	"""
	Parameters
	----------

	fyield : np.array, dtype=float, shape=[n,]
		The raw fluorescence data.
	pfd : np.array, dtype=float, shape=[n,]
		The photon flux density.
	fo : float, default=None
		The minimum fluorescence value.
	fm : float, default=None
		The maximum fluorescence value.
	sigma: float, default=None
		The effective absorption cross-section value in angstroms squared.
	ro: float, default=None
		The connectivity coefficient.
	rmse: float, default=None
		The RMSE value of the fit.
	nrmse: float, defalt=None
		The normalised RMSE value of the fit.

	Returns
	-------

	ax : object
		A matplotlib figure object.

	Example
	-------
	>>> plot_saturation_data(fyield, pfd, fo=fo, fm=fm, sigma=sigma, ro=None, rmse=rmse, nrmse=nrmse)
	"""

	if fo is None:
		raise ValueError("Please provide a value for 'fo'.")
	if fm is None:
		raise ValueError("Please provide a value for 'fm'.")
	if sigma is None:
		raise ValueError("Please provide a value for 'sigma'.")
	if rmse is None:
		raise ValueError("Please provide a value for 'rmse'.")
	if nrmse is None:
		raise ValueError("Please provide a value for 'nrmse'.")

	fyield = np.array(fyield)
	pfd = np.array(pfd)
	fvfm = (fm - fo)/fm
	x = np.arange(0,len(fyield),1)

	plt.close()

	fig, ax = plt.subplots(1, 1, figsize=[5,4], dpi=100)

	ax.plot(x, fyield, marker='o', lw=0, label='Raw Data', color='0.5')
	ax.set_ylabel('Fluorescence Yield')
	ax.set_xlabel('Flashlet Number')

	if ro is None:
		params = [fo, fm, sigma]
		formula = r"F$_v$/F$_m$ = {:.2f}""\n""$\u03C3$$_{{PSII}}$ = {:.2f}""\n""RMSE = {:.2f}""\n""nRMSE = {:.2f}".format(fvfm, sigma, rmse, nrmse)
		ax.plot(x, __fit_kolber_nop__(pfd, *params), color='k', label='{}'.format(formula))
	else:
		params = [fo, fm, sigma, ro]
		formula = r"F$_v$/F$_m$ = {:.2f}""\n""$\u03C3$$_{{PSII}}$ = {:.2f}""\n""RMSE = {:.2f}""\n""nRMSE = {:.2f}".format(fvfm, sigma, rmse, nrmse)
		ax.plot(x, __fit_kolber_p__(pfd, *params), color='k', label='{}'.format(formula))

	ax.legend()
	

	return ax

def plot_relaxation_data(fyield, seq_time, sat_len=None, foRelax=None, fmRelax=None, tau=None, alpha=None, rmse=None, nrmse=None):
	"""
	Parameters
	----------

	fyield : np.array, dtype=float, shape=[n,]
		The raw fluorescence data.
	seq_time : np.array, dtype=float, shape=[n,]
		The time of the flashlet measurements.
	sat_len : float, default=None
		The length of the saturation sequence for flashlets number to be plotted correct.
	foRelax : float, default=None
		The minimum fluorescence value in the relaxation phase.
	fmRelax : float, default=None
		The maximum fluorescence value in the relaxation phase.
	tau: float, default=None
		The rate of reoxidation in microseconds.
	alpha: float, default=None
		The ratio of reoxidisation components.
	rmse: float, default=None
		The RMSE value of the fit.
	nrmse: float, defalt=None
		The normalised RMSE value of the fit.

	Returns
	-------

	ax : object
		A matplotlib figure object.
	
	Example
	-------
	>>> ppu.plot_relaxation_data(fyield, seq_time, fo_relax=fo_r, fm_relax=fm_r, tau=(tau1, tau2, tau3), alpha=(alpha1, alpha2, alpha3), rmse=rmse, nrmse=nrmse)
	"""

	if sat_len is None:
		raise ValueError("Please provide a value for 'sat_len'.")
	if foRelax is None:
		raise ValueError("Please provide a value for 'foRelax'.")
	if fmRelax is None:
		raise ValueError("Please provide a value for 'fmRelax'.")
	if tau is None:
		raise ValueError("Please provide a value for 'tau'.")
	if alpha is None:
		raise ValueError("Please provide a value for 'alpha'.")
	if rmse is None:
		raise ValueError("Please provide a value for 'rmse'.")
	if nrmse is None:
		raise ValueError("Please provide a value for 'nrmse'.")

	fyield = np.array(fyield)
	seq_time = np.array(seq_time)

	x = np.arange(0,len(fyield),1)+sat_len

	plt.close()

	fig, ax = plt.subplots(1, 1, figsize=[5,4], dpi=100)

	ax.plot(x, fyield, marker='o', lw=0, label='Raw Data', color='0.5')
	ax.set_ylabel('Fluorescence Yield')
	ax.set_xlabel('Flashlet Number')

	if alpha is None:
		params = [foRelax, fmRelax, tau]
	
		formula = r"F$_o$$_{{Relax}}$ = {:.2f}; F$_m$$_{{Relax}}$ = {:.2f}""\n""$\U0001D70F$ = {:.2f}""\n""RMSE = {:.2f}""\n""nRMSE = {:.2f}".format(foRelax, fmRelax, tau, rmse, nrmse)
		ax.plot(x, __fit_single_relaxation__(seq_time, *params), color='k', label='{}'.format(formula))

	else:
		params = [foRelax, fmRelax, alpha[0], tau[0], alpha[1], tau[1], alpha[2], tau[2]]

		formula = r"F$_o$$_{{Relax}}$ = {:.2f}; F$_m$$_{{Relax}}$ = {:.2f}""\n""$\U0001D70F$$_1$ = {:.2f}; $\U0001D70F$$_2$ = {:.2f}""\n""$\U0001D70F$$_3$ = {:.2f}""\n""RMSE = {:.2f}""\n""nRMSE = {:.2f}".format(foRelax, fmRelax, tau[0], tau[1], tau[2], rmse, nrmse)
		ax.plot(x, __fit_triple_relaxation__(seq_time, *params), color='k', label='{}'.format(formula))

	ax.legend()


	return ax


def plot_fluorescence_light_curve(par, etr, etrmax=None, alpha=None, rmse=None, nrmse=None, sigma=None, phi=False):
	
	"""
	Parameters
	----------

	par : np.array, dtype=float
		The actinic light data from the fluorescence light curve.
	etr : np.array, dtype=float
		The electron transport rate data.
	etrmax : float, default=None
		The maximum electron transport rate.
	alpha : float, default=None
		The light limited slope of electron transport.
	rmse: float, default=None
		The RMSE value of the fit.
	nrmse: float, defalt=None
		The normalised RMSE value of the fit.
	sigma: float, default=None
		The effective absorption-cross section in angstroms squared.
	phi: bool, default=False
		If True, etr data is phi and the modified Webb et al. (1974) fit is used.

	Returns
	-------

	ax : object
		A matplotlib figure object.

	Example
	-------
	>>> ppu.plot_fluorescence_light_curve(par, etr, etrmax=etr_max, alpha=alpha, rmse=rmse, nrmse=nrmse, sigma=sigma, phi=True)
	"""

	if etrmax is None:
		raise ValueError("Please provide a value for 'etrmax'.")
	if alpha is None:
		raise ValueError("Please provide a value for 'alpha'.")
	if rmse is None:
		raise ValueError("Please provide a value for 'rmse'.")
	if nrmse is None:
		raise ValueError("Please provide a value for 'nrmse'.")

	x = np.array(par)
	y = np.array(etr)
	
	plt.close()

	fig, ax = plt.subplots(1, 1, figsize=[5,4], dpi=100)

	ax.plot(x, y, marker='o', lw=0, label='Raw Data', color='0.5')
	formula = r"ETR$_{{max}}$ = {:.2f}""\n""$\u03B1$$^{{ETR}}$ = {:.2f}""\n""RMSE = {:.2f}""\n""nRMSE = {:.2f}".format(etrmax, alpha, rmse, nrmse)
	ax.set_xlabel('Actinic Light ($\u03BC$mol photons m$^{-2}$ s${-1}$)')
	
	if phi == False:
		params = [etrmax, alpha]
		ax.plot(x, __calculate_alpha_model__(x, *params), color='k', label='{}'.format(formula))
		ax.set_ylabel('ETR (mol e$^{-1}$ mol RCII$^{-1}$ s$^{-1}$)')
	
	else:
		if sigma is None:
			raise ValueError('UserError - no sigma data provided.')
		sig = sigma*6.022e-3
		params = [etrmax/sig, alpha/sig]
		ax.plot(x, __calculate_modified_alpha_model__(x, *params), color='k', label='{}'.format(formula))
		ax.set_xscale('log')
		ax.set_ylabel('\u03D5')
	
	ax.legend()

	
	return ax
