extends Node2D
## A dungeon room's reward: when every creature under this node is beaten,
## its reward child (hidden until then) appears with a chime of shake.
## Once earned it stays earned (flag), and the creatures don't come back.

## Set when the room is cleared.
@export var flag: StringName = &""
## The node revealed on clearing (e.g. a key Pickup).
@export var reward: Node2D


func _ready() -> void:
	if reward:
		reward.visible = false
		reward.process_mode = Node.PROCESS_MODE_DISABLED
	if flag != &"" and Game.has_flag(flag):
		for c in get_children():
			if c is Creature:
				c.queue_free()
		_reveal()
		return
	for c in get_children():
		if c is Creature:
			c.defeated.connect(_on_defeated.bind(c))


func _on_defeated(creature: Node) -> void:
	await get_tree().process_frame
	for c in get_children():
		if c is Creature and c != creature and is_instance_valid(c) and not c.is_queued_for_deletion():
			return
	if flag != &"":
		Game.set_flag(flag)
	Feedback.shake(1.0, 0.2)
	_reveal()


func _reveal() -> void:
	if reward and is_instance_valid(reward):
		reward.visible = true
		reward.process_mode = Node.PROCESS_MODE_INHERIT
