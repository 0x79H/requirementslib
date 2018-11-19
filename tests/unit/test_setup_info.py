# -*- coding=utf-8 -*-

import pytest
import sys
import os

from requirementslib.models.requirements import Requirement


@pytest.mark.parametrize(
    'test_artifact', [
        {"name": "environ_config", "as_artifact": False},
        {"name": "environ_config", "as_artifact": True},
    ], indirect=True
)
def test_local_req(test_artifact):
    r = Requirement.from_line(test_artifact.as_posix())
    assert r.name == "environ-config"
    setup_dict = r.req.setup_info.as_dict()
    assert sorted(list(setup_dict.get("requires").keys())) == ["attrs",]


@pytest.mark.parametrize(
    'url_line, name, requires', [
        ["https://github.com/requests/requests/archive/v2.20.1.zip", "requests", ["urllib3", "chardet", "certifi", "idna"]],
        ["https://github.com/dropbox/pyannotate/archive/v1.0.4.zip", "pyannotate", ["six", "mypy-extensions", "typing"]]
    ],
)
def test_remote_req(url_line, name, requires):
    r = Requirement.from_line(url_line)
    assert r.name == name
    setup_dict = r.req.setup_info.as_dict()
    if "typing" in requires and not sys.version_info < (3, 5):
        requires.remove("typing")
    assert sorted(list(setup_dict.get("requires").keys())) == sorted(requires)


def test_no_duplicate_egg_info():
    """When the package has 'src' directory, do not write egg-info in base dir."""
    base_dir = os.path.abspath(os.getcwd())
    r = Requirement.from_line("-e {}".format(base_dir))
    egg_info_name = "{}.egg-info".format(r.name.replace("-", "_"))
    assert os.path.isdir(os.path.join(base_dir, "src", egg_info_name))
    assert not os.path.isdir(os.path.join(base_dir, egg_info_name))