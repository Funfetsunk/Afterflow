extends Area2D
## A shrine (GDD §12): touching it heals Awa, makes it her respawn point and
## saves. Place over the shrine stamp; the spawn marker named `spawn` is where
## she wakes after a fall.

## Name of the Marker2D (group "spawn") Awa respawns at.
@export var spawn: StringName = &"Shrine"
@export_multiline var message: String = "The stone hums under your hand. You feel rested."

@onready var glow: PointLight2D = $Glow

var _t: float = 0.0


func _ready() -> void:
	add_to_group("interactable")


func _process(delta: float) -> void:
	_t += delta
	glow.energy = 0.55 + 0.15 * sin(_t * 2.0)


func interact(_player: Node) -> void:
	Game.heal_full()
	Game.set_respawn(World.current_area_path, spawn)
	Game.set_flag(&"shrine_touched")
	Game.save_game()
	var tween := create_tween()
	tween.tween_property(glow, "energy", 1.6, 0.15)
	tween.tween_property(glow, "energy", 0.6, 0.6)
	await Dialogue.say(PackedStringArray([message]))
