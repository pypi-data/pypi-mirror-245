from collections.abc import Generator

import pytest

from sts import iscsi, lio
from sts.utils.cmdline import run


@pytest.fixture()
def _log_check() -> Generator:
    last_dump = run('coredumpctl -1', msg='Checking dumps before test').stdout
    yield
    recent_dump = run('coredumpctl -1', msg='Checking dumps after test').stdout
    assert recent_dump == last_dump, 'New coredump appeared during the test'


@pytest.fixture()
def _iscsi_localhost_test(_log_check) -> Generator:  # noqa: ANN001
    """Installs userspace utilities and makes cleanup before and after the test."""
    assert lio.lio_install()
    assert iscsi.install()
    iscsi.cleanup()
    lio.lio_clearconfig()
    yield
    iscsi.cleanup()
    lio.lio_clearconfig()
