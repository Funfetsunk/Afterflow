extends Node2D
## The boss room's aftermath: when the warden falls, its rewards (children of
## this node) appear, its diary page is written and the way out opens.

@export var warden: Warden
@export var diary_entry: StringName = &"warden"
@export_multiline var message: String = "The great tree lets out a long, slow breath. Somewhere above, roots are drawing back from a way out."


func _ready() -> void:
	var done := Game.has_flag(&"warden_defeated")
	for c in get_children():
		c.visible = done
		c.process_mode = Node.PROCESS_MODE_INHERIT if done else Node.PROCESS_MODE_DISABLED
	if warden and not done:
		warden.defeated.connect(_on_defeated)


func _on_defeated() -> void:
	for c in get_children():
		c.visible = true
		c.process_mode = Node.PROCESS_MODE_INHERIT
	Game.add_diary_entry(diary_entry)
	Game.save_game()
	await Dialogue.say(PackedStringArray([message]))
