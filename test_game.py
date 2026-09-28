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
            "talk_to_npc",
            "end_chapter_two",
        }:
            exec(compile(ast.Module(body=[node], type_ignores=[]), "game", "exec"), namespace)

    return namespace


def test_normal_enemy_turn_limit_reached():
    functions = load_game_functions()

    assert functions["normal_enemy_turn_limit_reached"]("goblin", 4) is False
    assert functions["normal_enemy_turn_limit_reached"]("goblin", 5) is True
    assert functions["normal_enemy_turn_limit_reached"]("Yseut", 5) is False


def test_talk_to_npc_returns_dialogue():
    functions = load_game_functions()

    mara_dialogue = functions["talk_to_npc"]("Mara")
    assert "Mara" in mara_dialogue
    assert "hello" in mara_dialogue.lower()

    missing_dialogue = functions["talk_to_npc"]("Ghost")
    assert "not here" in missing_dialogue.lower()


def test_end_chapter_two_returns_to_be_continued():
    functions = load_game_functions()

    chapter_end = functions["end_chapter_two"]()
    assert "to be continued" in chapter_end.lower()
