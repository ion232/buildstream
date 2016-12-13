import os
import pytest

from buildstream import Project
from buildstream import LoadError, LoadErrorReason

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)


@pytest.mark.datafiles(os.path.join(DATA_DIR))
def test_missing_project_conf(datafiles):
    directory = os.path.join(datafiles.dirname, datafiles.basename)

    with pytest.raises(LoadError) as exc:
        project = Project(directory)

    assert (exc.value.reason == LoadErrorReason.MISSING_FILE)


@pytest.mark.datafiles(os.path.join(DATA_DIR))
def test_missing_project_name(datafiles):
    directory = os.path.join(datafiles.dirname, datafiles.basename, "missingname")

    with pytest.raises(LoadError) as exc:
        project = Project(directory)

    assert (exc.value.reason == LoadErrorReason.INVALID_DATA)


@pytest.mark.datafiles(os.path.join(DATA_DIR))
def test_load_basic_project(datafiles):
    directory = os.path.join(datafiles.dirname, datafiles.basename, "basic")

    project = Project(directory)

    # User provided
    assert (project.name == "pony")

    # Some of the defaults
    assert (project.environment['USER'] == "tomjon")
    assert (project.environment['TERM'] == "dumb")
    assert (project.environment['PATH'] == "/usr/bin:/bin:/usr/sbin:/sbin")


@pytest.mark.datafiles(os.path.join(DATA_DIR))
def test_override_project_path(datafiles):
    directory = os.path.join(datafiles.dirname, datafiles.basename, "overridepath")

    project = Project(directory)

    # Test the override
    assert (project.environment['PATH'] == "/bin:/sbin")


@pytest.mark.datafiles(os.path.join(DATA_DIR))
def test_project_alias(datafiles):
    directory = os.path.join(datafiles.dirname, datafiles.basename, "alias")

    project = Project(directory)

    # Test the override
    assert (project.translate_url('baserock:foo') == 'git://git.baserock.org/baserock/foo')
    assert (project.translate_url('gnome:bar') == 'git://git.gnome.org/bar')
