from pkg_resources import get_distribution, DistributionNotFound


def get_package_version():
    """Get package version

    Returns:
         str: Installed package version, or 0.0.0.dev if not fully installed
    """
    try:
        return get_distribution(__name__.split('.')[0]).version
    except DistributionNotFound:
        return '0.0.0.dev'
