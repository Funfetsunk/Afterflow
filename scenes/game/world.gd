extends CanvasLayer
## Area changes, spawn points, fades, respawn ("World" autoload scene).
##
## Every area scene holds its own Player and Marker2D spawn points in the
## "spawn" group; World loads the area, moves Awa to the named spawn, fades in
## and autosaves (GDD §12).

signal area_entered(area_path: String)

## Fade duration in seconds, each way.
@export var fade_time: float = 0.25

@onready var fade: ColorRect = $Fade

var current_area_path: String = ""
var current_spawn: StringName = &""
var changing: bool = false


func _ready() -> void:
	fade.color.a = 0.0
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var scene := get_tree().current_scene
	if scene:
		current_area_path = scene.scene_file_path


func change_area(area_path: String, spawn: StringName, autosave: bool = true) -> void:
	if changing:
		return
	changing = true
	Game.input_locked = true
	await _fade_to(1.0)
	get_tree().change_scene_to_file(area_path)
	await get_tree().scene_changed
	current_area_path = area_path
	current_spawn = spawn
	_place_player(spawn)
	area_entered.emit(area_path)
	if autosave:
		Game.save_game()
	await _fade_to(0.0)
	Game.input_locked = false
	changing = false


func respawn() -> void:
	Game.heal_full()
	var area := Game.respawn_area if Game.respawn_area != "" else current_area_path
	change_area(area, Game.respawn_point, false)


func _place_player(spawn: StringName) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		return
	for marker in get_tree().get_nodes_in_group("spawn"):
		if marker.name == spawn:
			player.global_position = marker.global_position
			if marker.has_meta("facing"):
				player.facing = marker.get_meta("facing")
			break
	var camera := player.get_node_or_null("Camera") as Camera2D
	if camera:
		camera.reset_smoothing()


func _fade_to(alpha: float) -> void:
	var tween := create_tween()
	tween.tween_property(fade, "color:a", alpha, fade_time)
	await tween.finished
