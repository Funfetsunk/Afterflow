class_name DialogueData
extends Resource
## One conversation: who speaks and what they say, one box per line.

@export var speaker: String = ""
@export_multiline var lines: PackedStringArray = []
## Lines used instead once `after_flag` is set (e.g. after the lantern is found).
@export var after_flag: StringName = &""
@export_multiline var after_lines: PackedStringArray = []
## Diary entry added when the `after_lines` conversation finishes (empty: none).
@export var after_diary_entry: StringName = &""
## Flag set when this conversation finishes (empty: none).
@export var sets_flag: StringName = &""
## Diary entry added when this conversation finishes (empty: none).
@export var diary_entry: StringName = &""


func is_after() -> bool:
	return after_flag != &"" and Game.has_flag(after_flag) and not after_lines.is_empty()


func current_lines() -> PackedStringArray:
	return after_lines if is_after() else lines
