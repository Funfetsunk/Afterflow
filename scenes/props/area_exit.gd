extends Area2D
## Walking into this takes Awa to another area, at the named spawn marker.

@export_file("*.tscn") var target_area: String
@export var target_spawn: StringName = &""
## Optional flag that must be set before the exit works (with a hint otherwise).
@export var requires_flag: StringName = &""
@export_multiline var blocked_message: String = ""


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node) -> void:
	if not body is Player or World.changing:
		return
	if requires_flag != &"" and not Game.has_flag(requires_flag):
		if blocked_message != "":
			body.velocity = Vector2.ZERO
			await Dialogue.say(PackedStringArray([blocked_message]))
		return
	World.change_area(target_area, target_spawn)
