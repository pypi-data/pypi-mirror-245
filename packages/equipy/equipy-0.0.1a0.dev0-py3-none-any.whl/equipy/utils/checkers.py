import numpy as np
import warnings

def _check_metric(y):
    """
    Check that it is regression and not classification.

    Parameters
    ----------
    y : array of shape (n_samples,)
        Observed, true values.

    Raises
    ------
    Warning 
        If it is classification.
    """
    if np.all(np.isin(y, [0, 1])):
        warnings.warn(
            "You used mean squared error as metric but it looks like you are using classification scores")


def _check_nb_observations(sensitive_features):
    if sensitive_features.ndim == 1 & len(sensitive_features) == 1:
        raise ValueError("Fairness can't be applied on a single observation")
    if sensitive_features.ndim == 2 & np.shape(sensitive_features)[1] == 1:
        raise ValueError("Fairness can't be applied on a single observation")


def _check_shape(y, sensitive_feature):
    """
    Check the shape and data types of input arrays y and sensitive_feature.

    Parameters
    ----------
    y : array-like
        Target values of the data.
    sensitive_feature : array-like
        Input samples representing the sensitive attribute.

    Raises
    ------
    ValueError
        If the input arrays have incorrect shapes or data types.
    """
    if not isinstance(sensitive_feature, np.ndarray):
        raise ValueError('sensitive_features must be an array')

    if not isinstance(y, np.ndarray):
        raise ValueError('y must be an array')

    if len(sensitive_feature) != len(y):
        raise ValueError(
            'sensitive_features and y should have the same length')

    if len(np.unique(sensitive_feature)) == 1:
        raise ValueError(
            "At least one of your sensitive attributes contains only one modality and so it is already fair. Remove it from your sensitive features.")

    if not (np.issubdtype(y.dtype, np.floating) or np.issubdtype(y.dtype, np.integer)):
        raise ValueError('y should contain only float or integer numbers')


def _check_mod(modalities_calib, modalities_test):
    """
    Check if modalities in test data are included in calibration data's modalities.

    Parameters
    ----------
    modalities_calib : list
        Modalities from the calibration data.
    modalities_test : list
        Modalities from the test data.

    Raises
    ------
    ValueError
        If modalities in test data are not present in calibration data.
    """
    missing_modalities = set(modalities_test) - set(modalities_calib)
    if len(missing_modalities) != 0:
        raise ValueError(
            f"The following modalities of the test sensitive features are not in modalities of the calibration sensitive features: {missing_modalities}")


def _check_epsilon(epsilon):
    """
    Check if epsilon (fairness parameter) is within the valid range [0, 1].

    Parameters
    ----------
    epsilon : float
        Fairness parameter controlling the trade-off between fairness and accuracy.

    Raises
    ------
    ValueError
        If epsilon is outside the valid range [0, 1].
    """
    if epsilon < 0 or epsilon > 1:
        raise ValueError(
            'epsilon must be between 0 and 1')


def _check_epsilon_size(epsilon, sensitive_features):
    """
    Check if the epsilon list matches the number of sensitive features.

    Parameters
    ----------
    epsilon : list, shape (n_sensitive_features,)
        Fairness parameters controlling the trade-off between fairness and accuracy for each sensitive feature.

    sensitive_features : array-like, shape (n_samples, n_sensitive_features)
        Test samples representing multiple sensitive attributes.

    Raises
    ------
    ValueError
        If the length of epsilon does not match the number of sensitive features.
    """

    if sensitive_features.ndim == 1:
        if len(epsilon) != 1:
            raise ValueError(
                'epsilon must have the same length than the number of sensitive features')
    else:
        if len(epsilon) != np.shape(sensitive_features)[1]:
            raise ValueError(
                'epsilon must have the same length than the number of sensitive features')
