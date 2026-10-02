from graph.nodes import validate_node as validate_module

def test_validate_node_pass(tmp_path, monkeypatch):
    fake_file = tmp_path / "fake_tasks.py"
    fake_temp = tmp_path / "fake_tasks_temp.py"

    monkeypatch.setattr(validate_module, "demo_app_path", fake_file)
    monkeypatch.setattr(validate_module, "temp_path", fake_temp)

    state = {"proposed_fix": "print('hello')"}
    result = validate_module.validate_node(state)

    assert result["validation_passed"] is True
    assert fake_file.read_text() == "print('hello')"

def test_validate_node_fail(tmp_path, monkeypatch):
    fake_file = tmp_path / "fake_tasks.py"
    fake_temp = tmp_path / "fake_tasks_temp.py"

    monkeypatch.setattr(validate_module, "demo_app_path", fake_file)
    monkeypatch.setattr(validate_module, "temp_path", fake_temp)

    state = {"proposed_fix": "def broken(:", "attempt_count": 1, "max_attempts": 2}
    result = validate_module.validate_node(state)

    assert result["validation_passed"] is False
    assert "SyntaxError" in result["validation_feedback"]