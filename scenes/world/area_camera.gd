class_name AreaCamera
extends Camera2D
## Follows its parent (Awa) outdoors, clamped to the area's map; in dungeons,
## snaps room by room with a slide (GDD §13).
##
## Limits come from the TileMapLayer set in the Inspector. With `room_size`
## set, the camera instead holds the room Awa is in and slides to the next.

## The area's ground layer; its used rectangle becomes the camera limits.
@export var bounds_layer: TileMapLayer
## Room size in pixels for room-by-room areas (dungeons); zero = free follow.
@export var room_size: Vector2 = Vector2.ZERO
## Seconds a room-to-room slide takes.
@export var slide_time: float = 0.35

var _shake_strength: float = 0.0
var _shake_time: float = 0.0
var _room: Vector2i = Vector2i(-999, -999)
var _sliding: bool = false


func _ready() -> void:
	add_to_group("camera")
	if bounds_layer != null:
		var rect := bounds_layer.get_used_rect()
		var size := bounds_layer.tile_set.tile_size
		limit_left = rect.position.x * size.x
		limit_top = rect.position.y * size.y
		limit_right = rect.end.x * size.x
		limit_bottom = rect.end.y * size.y
	if room_size != Vector2.ZERO:
		top_level = true
		_snap_to_room(true)


func _process(delta: float) -> void:
	if room_size != Vector2.ZERO:
		_snap_to_room(false)
	if _shake_time > 0.0:
		_shake_time -= delta
		offset = Vector2(randf_range(-1, 1), randf_range(-1, 1)).round() * _shake_strength
		if _shake_time <= 0.0:
			offset = Vector2.ZERO


func shake(strength: float, seconds: float) -> void:
	_shake_strength = strength
	_shake_time = seconds


func _snap_to_room(instant: bool) -> void:
	var player := get_parent() as Node2D
	var room := Vector2i((player.global_position / room_size).floor())
	if room == _room or _sliding:
		return
	_room = room
	var target := Vector2(room) * room_size + room_size / 2.0
	if instant:
		global_position = target
		return
	_sliding = true
	Game.input_locked = true
	get_tree().paused = true
	process_mode = Node.PROCESS_MODE_ALWAYS
	var tween := create_tween()
	tween.tween_property(self, "global_position", target, slide_time)
	await tween.finished
	get_tree().paused = false
	Game.input_locked = false
	_sliding = false
