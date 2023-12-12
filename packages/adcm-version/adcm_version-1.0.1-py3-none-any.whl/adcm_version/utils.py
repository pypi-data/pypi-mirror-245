from re import match

from version_utils import rpm

PATTERN_OLD_ADCM_VERSION = r"^\d{4}\.\d{2}\.\d{2}\.\d{2}$"


def is_legacy(adcm_version: str) -> bool:
    """
    Check ADCM version

    :param adcm_version: An ADCM version
    :return: True (if ``version`` is old), False (else)
    """

    if match(pattern=PATTERN_OLD_ADCM_VERSION, string=adcm_version):
        return True

    return False


def compare_adcm_versions(version_a: str, version_b: str) -> int:
    """
    Compare two ADCM version strings

    :param version_a: An ADCM version
    :param version_b: An ADCM version
    :return: 1 (if ``a`` is newer), 0 (if versions are equal), or -1
        (if ``b`` is newer)
    """

    if is_legacy(adcm_version=version_a) != is_legacy(adcm_version=version_b):
        if is_legacy(adcm_version=version_a):
            return -1

        return 1

    return rpm.compare_versions(version_a=version_a, version_b=version_b)


def compare_prototype_versions(version_a: str, version_b: str) -> int:
    """
    Compare two prototype version strings for ADCM objects

    :param version_a: An prototype version
    :param version_b: An prototype version
    :return: 1 (if ``a`` is newer), 0 (if versions are equal), or -1
        (if ``b`` is newer)
    """

    return rpm.compare_versions(version_a=version_a, version_b=version_b)
