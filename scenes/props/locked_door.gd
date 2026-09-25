extends StaticBody2D
## A door that opens with a small key (or, for the boss door, the big key flag).
## Once opened it stays open (flag).

## Set when opened; an already-open door removes itself.
@export var flag: StringName = &""
## If set, this flag opens the door instead of a small key.
@export var needs_flag: StringName = &""
@export_multiline var locked_message: String = "It's locked."


func _ready() -> void:
	if flag != &"" and Game.has_flag(flag):
		queue_free()
		return
	$Touch.add_to_group("interactable")


func try_open() -> void:
	var opens := Game.has_flag(needs_flag) if needs_flag != &"" else Game.use_key()
	if not opens:
		await Dialogue.say(PackedStringArray([locked_message]))
		return
	if flag != &"":
		Game.set_flag(flag)
	Feedback.shake(1.0, 0.15)
	var tween := create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.25)
	await tween.finished
	queue_free()
