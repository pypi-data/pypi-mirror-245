import os
import sys
from pathlib import Path
from unittest.mock import Mock, call, ANY
import zipfile
import json

import pytest

from ploomber_cloud.cli import cli
from ploomber_cloud import init, api, zip_

CMD_NAME = "ploomber-cloud"


def test_set_key(monkeypatch, fake_ploomber_dir):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "key", "somekey"])

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert (
        "cloud_key: somekey"
        in (fake_ploomber_dir / "stats" / "config.yaml").read_text()
    )


@pytest.mark.parametrize(
    "args", [[CMD_NAME, "init"], [CMD_NAME, "init", "--from-existing"]]
)
def test_init(monkeypatch, fake_ploomber_dir, capsys, args):
    Path("ploomber-cloud.json").touch()

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert "Error: Project already initialized" in capsys.readouterr().err


def test_init_flow(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["docker"]))
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/docker",
        headers={"accept": "application/json", "access_token": "somekey"},
    )


def test_init_flow_with_server_error(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["sometype"]))
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/sometype",
        headers={"accept": "application/json", "access_token": "somekey"},
    )

    assert (
        "Error: An error occurred: some error\n"
        "If you need help, contact us at: https://ploomber.io/community\n"
    ) in capsys.readouterr().err


def test_init_infers_project_type_if_dockerfile_exists(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "confirm", Mock(side_effect=["y"]))
    mock_requests_post = Mock(name="requests.post")
    Path("Dockerfile").touch()

    def requests_post(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/docker",
        headers={"accept": "application/json", "access_token": "somekey"},
    )


def test_init_from_existing_flow(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init", "--from-existing"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["someid"]))
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={"projects": [{"id": "someid"}], "type": "sometype"}
            ),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Delete ploomber-cloud.json if it exists
    path_to_json = Path("ploomber-cloud.json")
    if path_to_json.exists():
        path_to_json.unlink()

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert path_to_json.exists()
    with open(path_to_json) as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "sometype",
        }
    assert excinfo.value.code == 0
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects",
                headers={"accept": "application/json", "access_token": "somekey"},
            ),
            call(
                "https://cloud-prod.ploomber.io/projects/someid",
                headers={"accept": "application/json", "access_token": "somekey"},
            ),
        ]
    )


def test_init_from_existing_no_project_message(monkeypatch, set_key, capsys):
    # Try to init from existing with no existing projects
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init", "--from-existing"])
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={
                    "projects": [],
                }
            ),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    with pytest.raises(SystemExit):
        cli()

    assert (
        "You have no existing projects. Initialize without --from-existing."
        in capsys.readouterr().out
    )


def test_deploy_error_if_missing_key(monkeypatch, fake_ploomber_dir, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert (
        "Error: API key not found. Please run 'ploomber-cloud key YOURKEY'\n"
        in capsys.readouterr().err
    )


def test_deploy(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "access_token": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
    )

    with zipfile.ZipFile("app-someuuid.zip") as z:
        mapping = {}
        for name in z.namelist():
            mapping[name] = z.read(name)

    assert mapping == {
        "Dockerfile": b"FROM python:3.11",
        "app.py": b"print('hello world')",
        "fake-ploomber-dir/stats/config.yaml": b"cloud_key: somekey",
    }
