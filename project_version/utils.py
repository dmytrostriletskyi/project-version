"""
Provide utils for command line interface.
"""


def parse_project_version(version):
    """
    Parse project version to a tuple of integer.

    That can be used for a lexicographical comparison of values.

    Arguments:
        version (str): project version code as a string.

    Returns:
        Parsed project version as a tuple with integer values.
    """
    components = version.split('.')

    return tuple(int(component) for component in components)
