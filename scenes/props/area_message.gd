extends Node
## Shows a few lines once when the area loads (e.g. waking by the river), if
## `requires_flag` is set (or empty) and `once_flag` isn't yet.

## The lines to show (a DialogueData resource; its speaker is shown if set).
@export var message: DialogueData
@export var requires_flag: StringName = &""
## Set after showing, so the message never repeats.
@export var once_flag: StringName = &""
## Seconds to wait after the area appears.
@export var delay: float = 0.6


func _ready() -> void:
	if once_flag != &"" and Game.has_flag(once_flag):
		return
	if requires_flag != &"" and not Game.has_flag(requires_flag):
		return
	await get_tree().create_timer(delay).timeout
	if once_flag != &"":
		Game.set_flag(once_flag)
	if message:
		await Dialogue.say(message.lines, message.speaker)
