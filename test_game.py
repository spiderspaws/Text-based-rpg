import ast
from pathlib import Path


def load_game_functions():
    source = Path("game").read_text(encoding="utf-8")
    module = ast.parse(source)
    namespace = {}

    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name in {
            "normal_enemy_turn_limit_reached",
            "fight",
        }:
            exec(compile(ast.Module(body=[node], type_ignores=[]), "game", "exec"), namespace)

    return namespace


def test_normal_enemy_turn_limit_reached():
    functions = load_game_functions()

    assert functions["normal_enemy_turn_limit_reached"]("goblin", 4) is False
    assert functions["normal_enemy_turn_limit_reached"]("goblin", 5) is True
    assert functions["normal_enemy_turn_limit_reached"]("Yseut", 5) is False
