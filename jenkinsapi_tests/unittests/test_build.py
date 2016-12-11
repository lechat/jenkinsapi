import pytest
import pytz
from . import configs
import datetime
from jenkinsapi.build import Build
from jenkinsapi.job import Job


@pytest.fixture(scope='function')
def jenkins(mocker):
    return mocker.MagicMock()


@pytest.fixture(scope='function')
def job(monkeypatch, jenkins):
    def fake_poll(cls, tree=None):   # pylint: disable=unused-argument
        return configs.JOB_DATA

    monkeypatch.setattr(Job, '_poll', fake_poll)

    fake_job = Job('http://', 'Fake_Job', jenkins)
    return fake_job


@pytest.fixture(scope='function')
def build(job, monkeypatch):
    def fake_poll(cls, tree=None):   # pylint: disable=unused-argument
        return configs.BUILD_DATA

    monkeypatch.setattr(Build, '_poll', fake_poll)

    return Build('http://', 97, job)


def test_timestamp(build):
    assert isinstance(build.get_timestamp(), datetime.datetime)

    expected = pytz.utc.localize(
        datetime.datetime(2013, 5, 31, 23, 15, 40))

    assert build.get_timestamp() == expected


def test_name(build):
    with pytest.raises(AttributeError):
        build.id()
    assert build.name == 'foo #1'


def test_duration(build):
    expected = datetime.timedelta(milliseconds=5782)
    assert build.get_duration() == expected
    assert build.get_duration().seconds == 5
    assert build.get_duration().microseconds == 782000
    assert str(build.get_duration()) == '0:00:05.782000'


def test_get_causes(build):
    assert build.get_causes() == [{
        'shortDescription': 'Started by user anonymous',
        'userId': None,
        'userName': 'anonymous'
    }]


def test_get_description(build):
    assert build.get_description() == 'Best build ever!'


def test_get_slave(build):
    assert build.get_slave() == 'localhost'


def test_get_revision_no_scm(build):
    """ with no scm, get_revision should return None """
    assert build.get_revision() is None


def test_downstream(build):
    expected = ['test1', 'test2']
    assert build.get_downstream_job_names() == expected
