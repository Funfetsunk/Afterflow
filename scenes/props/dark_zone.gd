extends Area2D
## A dark place: while Awa is inside, the area's CanvasModulate dims to
## `darkness`, so only the lantern (and glows) light the way.

## The area's CanvasModulate.
@export var canvas_modulate: CanvasModulate
@export var darkness: Color = Color(0.08, 0.07, 0.12)
@export var fade_time: float = 0.4

var _light: Color = Color.WHITE


func _ready() -> void:
	if canvas_modulate:
		_light = canvas_modulate.color
	body_entered.connect(func(b): if b is Player: _fade(darkness))
	body_exited.connect(func(b): if b is Player: _fade(_light))


func _fade(to: Color) -> void:
	if canvas_modulate == null:
		return
	create_tween().tween_property(canvas_modulate, "color", to, fade_time)
