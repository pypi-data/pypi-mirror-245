import numpy as np
import xarray as xr
import warnings

from scipy import stats
from scipy import signal
from scipy.stats import t

from .utility import *
from .utility import generate_datatree_dispatcher

@generate_datatree_dispatcher
def calc_linregress_spatial(data_input, dim = 'time', x = None, alternative = 'two-sided', returns_type = 'dataset_returns', engine = 'scipy_linregress'):
    """
    Calculate a linear least-squares regression for spatial data of time.

    Parameters
    ----------
    data_input : :py:class:`xarray.DataArray<xarray.DataArray>` or :py:class:`xarray.Dataset<xarray.Dataset>`
        :py:class:`xarray.DataArray<xarray.DataArray>` or :py:class:`xarray.Dataset<xarray.Dataset>` to be regression.
    dim : str
        Dimension(s) over which to apply linregress. By default linregress is applied over the `time` dimension.
    x : numpy.array
    returns_type: str
    
    Returns
    -------
    result : ``LinregressResult`` Dataset
        The return Dataset have following data_var:

        slope : float
            Slope of the regression line.
        intercept : float
            Intercept of the regression line.
        rvalue : float
            The Pearson correlation coefficient. The square of ``rvalue``
            is equal to the coefficient of determination.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic. See `alternative` above for alternative
            hypotheses.
        stderr : float
            Standard error of the estimated slope (gradient), under the
            assumption of residual normality.
        intercept_stderr : float
            Standard error of the estimated intercept, under the assumption
            of residual normality.

    .. seealso::
        :py:func:`scipy.stats.linregress <scipy:scipy.stats.linregress>`.
    """
    def _calc_linregress_spatial(x, y, dim, alternative):
        # y shape
        n = y[dim].shape[0]

        if x is None:
            # Regression parameter x
            x_data = np.arange(0, y[dim].shape[0])
            x = xr.DataArray(x_data, dims = dim, coords = {dim: y[dim].data})

        x_shape = x.shape[0]
        if x_shape != n:
            raise ValueError('`data_input` array size along dimension `dim` should be the same as the `x` array size, but data_input[dim]: ' + n + '; x: ' + x_shape + '.')
        
        if isinstance(x, np.ndarray):
            warnings.warn(f"Assuming that the coordinate value of '{dim}' in `data_input` and `x` is same. Ignoring.")
            x = xr.DataArray(x, dims = dim, coords = {dim: y[dim].data})
        if isinstance(x, xr.DataArray):
            if x.dims[0] != y[dim].dims[0]:
                raise ValueError('The coordinate name of `data_input` array along dimension `dim` should be the same as the `x`.')
            if (x[dim].data == y[dim].data).all() == False:
                warnings.warn(f"Coordinate value of '{dim}' in `data_input` and `x` is not same. If you are sure that the `x` dimension '{dim}' is the same as the value of the dimension in `data_input`, pass in the numpy array corresponding to `x`, e.g. `x.data`. Ignoring.")
        else:
            raise ValueError("Unsupported input type. Expected numpy.ndarray or xarray.DataArray.")

        x_mean = np.mean(x)
        x_diff = x - x_mean

        slope = (x_diff * y).sum(dim = dim, skipna = False) / (x_diff ** 2).sum(skipna = False)
        intercept = y.mean(dim = dim) - slope * x_mean
        residuals = y - slope *x + intercept

        dof = n - 2  # Degree of freedom
        mse = (residuals **2).sum(dim = dim, skipna = False) / dof  # Mean Square Error
        std_err_unnormalized = np.sqrt(mse)
        std_err = np.sqrt(mse / (x_diff ** 2).sum(skipna = False))

        t_value = slope / std_err
        r_value = xr.corr(x, y, dim = dim)
        intercept_stderr = std_err_unnormalized * np.sqrt(np.mean(x ** 2) / (x_diff ** 2).sum(skipna = False))

        if alternative == 'two-sided':
            p_value_numpy = 2 * (1 - t.cdf(np.abs(t_value), dof))  # Two-sided hypothesis testing
        elif alternative == 'less':
            p_value_numpy = t.cdf(t_value, dof)  # Left-sided hypothesis testing
        elif alternative == 'greater':
            p_value_numpy = 1 - t.cdf(t_value, dof)  # Right-hand side hypothesis testing
        else:
            raise ValueError("Invalid alternative hypothesis. Valid options are 'two-sided', 'less', or 'greater'.")

        p_value = t_value.copy(data = p_value_numpy, deep = True)

        result = xr.Dataset()
        result['slope'] = slope
        result['intercept'] = intercept
        result['rvalue'] = r_value
        result['pvalue'] = p_value
        result['stderr'] = std_err
        result['intercept_stderr'] = intercept_stderr
        return result

    def _calc_linregress_spatial_scipy_linregress(data_input, dim, x, alternative):
        
        if data_input.chunks is not None:
            # Dask routine
            data_input = data_input.chunk({dim: -1})
        else:
            pass
                                    
        # y shape
        n = data_input[dim].shape[0]

        if x is None:
            # Regression parameter x
            x_data = np.arange(0, data_input[dim].shape[0])
            x = xr.DataArray(x_data, dims = dim, coords = {dim: data_input[dim].data})

        x_shape = x.shape[0]
        if x_shape != n:
            raise ValueError('`data_input` array size along dimension `dim` should be the same as the `x` array size, but data_input[dim]: ' + n + '; x: ' + x_shape + '.')
        
        if isinstance(x, np.ndarray):
            warnings.warn(f"Assuming that the coordinate value of '{dim}' in `data_input` and `x` is same. Ignoring.")
            x = xr.DataArray(x, dims = dim, coords = {dim: data_input[dim].data})
        if isinstance(x, xr.DataArray):
            if x.dims[0] != data_input[dim].dims[0]:
                raise ValueError('The coordinate name of `data_input` array along dimension `dim` should be the same as the `x`.')
            if (x[dim].data == data_input[dim].data).all() == False:
                raise ValueError(f"Coordinate value of '{dim}' in `data_input` and `x` is not same. If you are sure that the `x` dimension '{dim}' is the same as the value of the dimension in `data_input`, pass in the numpy array corresponding to `x`, e.g. `x.data`.")
        else:
            raise ValueError("Unsupported input type. Expected numpy.ndarray or xarray.DataArray.")
        
        # `scipy.stats.linregress` only supports numpy arrays
        x = x.data
            
        # scipy function scipy.stats.linregress calculate regression parameter
        def linregress_scipy(data):
            LinregressResult = stats.linregress(x, data, alternative)
            slope = LinregressResult.slope
            intercept = LinregressResult.intercept
            rvalue = LinregressResult.rvalue
            pvalue = LinregressResult.pvalue
            stderr = LinregressResult.stderr
            intercept_stderr = LinregressResult.intercept_stderr
            return np.array([slope, intercept, rvalue, pvalue, stderr, intercept_stderr])

        # Use xarray apply_ufunc to create DataArray
        LinregressResult_dataarray = xr.apply_ufunc(
            linregress_scipy,
            data_input,
            input_core_dims=[[dim]],
            output_core_dims = [["parameter"]],
            output_dtypes=["float64"],
            dask = "parallelized",
            vectorize=True,
            dask_gufunc_kwargs = {"output_sizes": {"parameter": 6}},
        )

        # Transform DataArray to Dataset
        return xr.Dataset(
            data_vars = {'slope': LinregressResult_dataarray[...,0],
                        'intercept':  LinregressResult_dataarray[...,1],
                        'rvalue':  LinregressResult_dataarray[...,2],
                        'pvalue':  LinregressResult_dataarray[...,3],
                        'stderr':  LinregressResult_dataarray[...,4],
                        'intercept_stderr':  LinregressResult_dataarray[...,5],
            }
        )
    
    if engine == 'scipy_linregress':
        return _calc_linregress_spatial_scipy_linregress(data_input, dim, x, alternative)
    elif engine == 'xarray':
        return _calc_linregress_spatial(x, data_input, dim, alternative)

def calc_detrend_data(data_input, time_dim = 'time'):
    """Remove linear trend along axis from data.

    Parameters
    ----------
    data_input : :py:class:`xarray.DataArray<xarray.DataArray>`
         The spatio-temporal data of :py:class:`xarray.DataArray<xarray.DataArray>` to be detrended.
    dim : `str`
        Dimension(s) over which to detrend. By default dimension is applied over the `time` dimension.

    Returns
    -------
    - :py:class:`xarray.DataArray<xarray.DataArray>`.

    .. seealso::
        :py:func:`scipy.signal.detrend <scipy:scipy.signal.detrend>`.
    """

    # Because `scipy.signal.detrend` cannot detrend `np.nan`, 
    # so we need to get the data mask first, then assign `np.nan` to 1 for calculation, 
    # and then remove the mask area again.
    mask_bool = np.isnan(data_input).mean(dim = time_dim)
    mask_float = mask_bool + 0.0

    detrenddata_withoutmask = data_input.fillna(1).reduce(signal.detrend, dim = time_dim)
    result = detrenddata_withoutmask.where(mask_float < 0.5)
    return result

def calc_ttestSpatialPattern_spatial(data_input1, data_input2, dim = 'time'):
    """Calculate the T-test for the means of two independent sptial samples along with other axis (i.e. 'time') of scores.

    Parameters
    ----------
    data_input1 : :py:class:`xarray.DataArray<xarray.DataArray>`
         The first spatio-temporal data of xarray DataArray to be calculated.
    data_input2 : :py:class:`xarray.DataArray<xarray.DataArray>`
         The second spatio-temporal data of xarray DataArray to be calculated.

    .. note::
        The order of `data_input1` and `data_input2` has no effect on the calculation result.

    dim : `str`
        Dimension(s) over which to apply skewness. By default skewness is applied over the `time` dimension.

    Returns
    -------
    - statistic, pvalue: :py:class:`xarray.Dataset<xarray.Dataset>`.

    .. seealso::
        :py:func:`scipy.stats.ttest_ind <scipy:scipy.stats.ttest_ind>`.
    """

    if(data_input1.dims != data_input2.dims):
        raise InterruptedError('data_input1.dims and data_input2.dims must be same!')

    # scipy function scipy.stats.ttest_ind calculate the T-test for the means of two independent samples of scores.
    def _ttest_ind_scipy(data1, data2):
        statistic, pvalue = stats.ttest_ind(data1, data2)
        return np.array([statistic, pvalue])

    # Use xarray apply_ufunc to create DataArray
    ttest_ind_dataarray = xr.apply_ufunc(
        _ttest_ind_scipy,
        data_input1, data_input2,
        input_core_dims=[[dim],[dim]],
        output_core_dims = [["parameter"]],
        output_dtypes=["float64"],
        dask = "parallelized",
        vectorize=True,
        dask_gufunc_kwargs = {"output_sizes": {"parameter": 2}},
        exclude_dims=set(("time",)), # allow change size
    )

    return xr.Dataset(
        data_vars = {'statistic': ttest_ind_dataarray[...,0],
                     'pvalue':  ttest_ind_dataarray[...,1],
        }
    )

def calc_skewness_spatial(data_input, dim = 'time'):
    """Calculate the skewness of the spatial field on the time axis and its significance test.

    The :math:`k` th statistical moment about the mean is given by

    .. math::
        m_k = \\sum_{i=1}^{N} \\frac{(x_i-\\bar{x})^k}{N}

    where :math:`x_i` is the :math:`i` th observation, :math:`\\bar{x}` the mean and :math:`N` the number of observations.

    One definition of the coefficient of skewness is

    .. math::
        a_3 = \\frac{m_3}{(m_2)^{3/2}}

    Skewness is a measure of the asymmetry of a distribution and is zero for a normal distribution. If the longer wing of a distribution 
    occurs for values of :math:`x` higher than the mean, that distribution is said to have positive skewness. If thelonger wing occurs for 
    values of :math:`x` lower than the mean, the distribution is said to have negative skewness.
    
    Parameters
    ----------
    data_input : :py:class:`xarray.DataArray<xarray.DataArray>`
         The spatio-temporal data of xarray DataArray to be calculated.
    dim : str
        Dimension(s) over which to apply skewness. By default skewness is applied over the `time` dimension.

    Returns
    -------
    - skewness, pvalue: :py:class:`xarray.Dataset<xarray.Dataset>`.
    
    Reference
    --------------
    White, G. H. (1980). Skewness, Kurtosis and Extreme Values of 
    Northern Hemisphere Geopotential Heights, Monthly Weather Review, 108(9), 1446-1455. 
    Website: https://journals.ametsoc.org/view/journals/mwre/108/9/1520-0493_1980_108_1446_skaevo_2_0_co_2.xml

    .. seealso::
        :py:func:`scipy.stats.skew <scipy:scipy.stats.skew>`, :py:func:`scipy.stats.normaltest <scipy:scipy.stats.normaltest>`.
    """
    # Find the index of `dim` in the xarray DataArray for `time`.
    time_dim_index = find_dims_axis(data_input, dim = dim)

    # Calculate skewness
    def _calc_skew_core(data_input, data_all):
        time_length = data_input[dim].shape[0]
        m_3 = (((data_input - data_all) **3)/time_length).sum(dim = dim)
        m_2 = (((data_input - data_all) **2)/time_length).sum(dim = dim)
        return m_3/ (m_2 **(3/2))
 
    data_all = data_input.mean(dim = dim)
    skewness = _calc_skew_core(data_input, data_all)

    # Significance test
    k2, p_numpy = stats.normaltest(data_input, axis = time_dim_index, nan_policy = 'propagate')
    format_coordniate = data_all
    p = format_coordniate.copy(data = p_numpy, deep = True)

    # Merge multiple :py:class:`xarray.DataArray<xarray.DataArray>`s into one `xarray.Dataset`.
    dateset = xr.Dataset(data_vars = {'skewness': skewness, 'pvalue': p})

    return dateset

def calc_kurtosis_spatial(data_input, dim = 'time'):
    """Calculate the kurtosis of the spatial field on the time axis and its significance test.

    The :math:`k` th statistical moment about the mean is given by

    .. math::
        m_k = \\sum_{i=1}^{N} \\frac{(x_i-\\bar{x})^k}{N}

    where :math:`x_i` is the :math:`i` th observation, :math:`\\bar{x}` the mean and :math:`N` the number of observations.

    The coefficient of kurtosis is defined by

    .. math::
        a_4 = \\frac{m_4}{(m_2)^{2}}

    The kurtosis of a normal distribution is 3. If a distribution has a large central region which is flatter than a normal distribution
    with the same mean and variance, it has a kurtosis of less than 3. If the distribution has a central maximum more peaked and with
    longer wings than the equivalent normal distribution, its kurtosis is higher than 3 (Brooks and Carruthers, 1954). 
    Extreme departures from the mean will cause very high values of kurtosis. Consequently, high kurtosis has been used as
    an indicator of bad data (Craddock and Flood, 1969). For the same reason, high values of kurtosis can be a result of one or two
    extreme events in a period of several years.

    Parameters
    ----------
    data_input : :py:class:`xarray.DataArray<xarray.DataArray>`
         The spatio-temporal data of xarray DataArray to be calculated.
    dim : str
        Dimension(s) over which to apply kurtosis. By default kurtosis is applied over the `time` dimension.

    Returns
    -------
    - kurtosis: :py:class:`xarray.DataArray<xarray.DataArray>`.   
    
    Reference
    --------------
    White, G. H. (1980). Skewness, Kurtosis and Extreme Values of 
    Northern Hemisphere Geopotential Heights, Monthly Weather Review, 108(9), 1446-1455. 
    Website: https://journals.ametsoc.org/view/journals/mwre/108/9/1520-0493_1980_108_1446_skaevo_2_0_co_2.xml

    Køie, M., Brooks, C.E., & Carruthers, N. (1954). Handbook of Statistical Methods in Meteorology. Oikos, 4, 202.

    Craddock, J.M. and Flood, C.R. (1969), Eigenvectors for representing the 500 mb geopotential 
    surface over the Northern Hemisphere. Q.J.R. Meteorol. Soc., 95: 576-593. 
    doi: https://doi.org/10.1002/qj.49709540510

    .. seealso::
        :py:func:`scipy.stats.kurtosis <scipy:scipy.stats.kurtosis>`.
    """

    # Calculate kurtosis
    def _calc_kurt_core(data_input, data_all):
        time_length = data_input[dim].shape[0]
        m_4 = (((data_input - data_all) **4)/time_length).sum(dim = dim)
        m_2 = (((data_input - data_all) **2)/time_length).sum(dim = dim)
        return m_4/ (m_2 **2)
 
    data_all = data_input.mean(dim = dim)
    kurtosis = _calc_kurt_core(data_input, data_all)

    return kurtosis