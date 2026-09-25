extends Node
## Combat feel helpers ("Feedback" autoload, GDD §7.2): hit-stop, screen shake,
## hit sparks and the puff a creature leaves when it goes.

const SPARK := preload("res://assets/ui/hit_spark.png")
const POOF := [preload("res://assets/ui/poof_0.png"), preload("res://assets/ui/poof_1.png"), preload("res://assets/ui/poof_2.png")]

## Game speed during hit-stop.
@export var hit_stop_scale: float = 0.05

var _stopping: bool = false


func hit_stop(seconds: float) -> void:
	if _stopping:
		return
	_stopping = true
	Engine.time_scale = hit_stop_scale
	await get_tree().create_timer(seconds, true, false, true).timeout
	Engine.time_scale = 1.0
	_stopping = false


func shake(strength: float, seconds: float) -> void:
	var camera := get_tree().get_first_node_in_group("camera")
	if camera and camera.has_method("shake"):
		camera.shake(strength, seconds)


func spark(at: Vector2) -> void:
	var s := _effect_sprite(SPARK, at)
	if s:
		var tween := s.create_tween().set_ignore_time_scale(true)
		tween.tween_interval(0.08)
		tween.tween_callback(s.queue_free)


func poof(at: Vector2) -> void:
	var s := _effect_sprite(POOF[0], at)
	if s == null:
		return
	var tween := s.create_tween()
	for tex in POOF:
		tween.tween_callback(func(): s.texture = tex)
		tween.tween_interval(0.07)
	tween.tween_callback(s.queue_free)


func _effect_sprite(tex: Texture2D, at: Vector2) -> Sprite2D:
	var scene := get_tree().current_scene
	if scene == null:
		return null
	var s := Sprite2D.new()
	s.texture = tex
	s.global_position = at
	s.z_index = 5
	scene.add_child(s)
	return s
