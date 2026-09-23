import pytest

from hackflow.storage import load_json, save_json


def test_save_and_load_json(tmp_path):
    data_path = tmp_path / "teams.json"
    data = [{"id": 1, "name": "CodePulse"}]

    save_json(data_path, data)
    loaded_data = load_json(data_path)

    assert loaded_data == data


def test_invalid_json_raises_error(tmp_path):
    data_path = tmp_path / "broken.json"
    data_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError):
        load_json(data_path)
