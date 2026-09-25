class_name Player
extends CharacterBody2D
## Awa: 8-way analog movement on the input map, facing and animating in 4 directions.
##
## Tuning lives in the Inspector (exports below). The sprite's animations are
## named <anim>_<dir> (idle_s, walk_e, ...), built by tools/build_sprite_frames.py.

## Top speed in pixels per second (the game runs at 320x180).
@export var max_speed: float = 72.0
## How quickly she reaches top speed, in pixels per second squared.
@export var acceleration: float = 900.0
## How quickly she stops when the stick is released.
@export var friction: float = 1100.0

@onready var sprite: AnimatedSprite2D = $Sprite

var facing: String = "s"


func _physics_process(delta: float) -> void:
	var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input != Vector2.ZERO:
		velocity = velocity.move_toward(input * max_speed, acceleration * delta)
		facing = _direction_of(input)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
	move_and_slide()
	_animate(input != Vector2.ZERO)


func _direction_of(v: Vector2) -> String:
	# Keep the current facing on exact diagonals so she doesn't flicker between two.
	if absf(absf(v.x) - absf(v.y)) < 0.05:
		var current := {"e": v.x > 0, "w": v.x < 0, "s": v.y > 0, "n": v.y < 0}
		if current.get(facing, false):
			return facing
	if absf(v.x) > absf(v.y):
		return "e" if v.x > 0 else "w"
	return "s" if v.y > 0 else "n"


func _animate(moving: bool) -> void:
	var anim := ("walk_" if moving else "idle_") + facing
	if sprite.animation != anim:
		sprite.play(anim)
