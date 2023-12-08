from enum import Enum


_FEATURES = {
    "logging_wrapper": False,
}


class Feature(Enum):
    LoggingWrapper = "logging_wrapper"


def enable_feature(feature: Feature):
    """Enable a feature.

    :param feature: The feature to enable.
    :type feature: str
    """
    if feature not in _FEATURES:
        raise ValueError('Unknown feature: %s' % feature)
    _FEATURES[feature] = True
