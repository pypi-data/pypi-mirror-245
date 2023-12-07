from setuptools_scm import ScmVersion


def version_func(version: ScmVersion):
    print(version)
    from setuptools_scm.version import guess_next_version
    print(guess_next_version)
    return version.format_next_version(guess_next_version, '{guessed}b{distance}')
