class_name Player
extends CharacterBody2D
## Awa: 8-way analog movement, 4-way facing, the walking stick, taking hits.
##
## Tuning lives in the Inspector (exports below). The sprite's animations are
## named <anim>_<dir> (idle_s, walk_e, swing_n, ...), built by
## tools/build_sprite_frames.py. Hurt feedback is a blink, never a shader
## (Art Bible §4.3: nothing may recolour Awa).

enum State { MOVE, SWING, SPIN, HURT, DEAD }

const DIR_VECTORS := {"s": Vector2.DOWN, "e": Vector2.RIGHT, "n": Vector2.UP, "w": Vector2.LEFT}
const SLASH_FRAMES := [preload("res://assets/ui/slash_0.png"), preload("res://assets/ui/slash_1.png"), preload("res://assets/ui/slash_2.png")]
const SPIN_FRAMES := [preload("res://assets/ui/spin_0.png"), preload("res://assets/ui/spin_1.png"), preload("res://assets/ui/spin_2.png"), preload("res://assets/ui/spin_3.png")]

@export_group("Movement")
## Top speed in pixels per second (the game runs at 320x180).
@export var max_speed: float = 72.0
## How quickly she reaches top speed, in pixels per second squared.
@export var acceleration: float = 900.0
## How quickly she stops when the stick is released.
@export var friction: float = 1100.0

@export_group("Stick")
## Damage of a normal swing.
@export var swing_damage: int = 1
## Damage of the charged spin.
@export var spin_damage: int = 2
## Seconds the attack button must be held after a swing to charge a spin.
@export var charge_time: float = 0.6
## How far a swing pushes creatures back, in pixels per second.
@export var swing_knockback: float = 170.0

@export_group("Hurt")
## Seconds of invulnerability after a hit.
@export var invulnerable_time: float = 1.0
## Knockback speed when hit, in pixels per second.
@export var hurt_knockback: float = 150.0

@onready var sprite: AnimatedSprite2D = $Sprite
@onready var stick_hitbox: Area2D = $StickHitbox
@onready var stick_shape: CollisionShape2D = $StickHitbox/Shape
@onready var slash: Sprite2D = $Slash
@onready var interact_probe: Area2D = $InteractProbe
@onready var lantern_light: PointLight2D = $LanternLight

var facing: String = "s"
var state: State = State.MOVE
var _hit_this_swing: Array[Node] = []
var _charge: float = 0.0
var _charging: bool = false
var _invulnerable: float = 0.0
var _lantern_on: bool = true


func _ready() -> void:
	add_to_group("player")
	stick_shape.disabled = true
	slash.visible = false
	lantern_light.enabled = false
	sprite.animation_finished.connect(_on_animation_finished)
	Game.item_changed.connect(func(_i): _update_lantern())
	_update_lantern()


func _physics_process(delta: float) -> void:
	_invulnerable = maxf(_invulnerable - delta, 0.0)
	sprite.visible = _invulnerable <= 0.0 or int(_invulnerable * 20.0) % 2 == 0 or state == State.DEAD
	match state:
		State.MOVE:
			_move(delta)
		State.SWING, State.SPIN:
			velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
			move_and_slide()
			_check_stick_hits()
		State.HURT:
			velocity = velocity.move_toward(Vector2.ZERO, friction * 0.5 * delta)
			move_and_slide()
		State.DEAD:
			pass
	_update_charge(delta)


func _move(delta: float) -> void:
	var input := Vector2.ZERO
	if not Game.input_locked:
		input = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input != Vector2.ZERO:
		velocity = velocity.move_toward(input * max_speed, acceleration * delta)
		facing = _direction_of(input)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
	move_and_slide()
	var anim := ("walk_" if input != Vector2.ZERO else "idle_") + facing
	if sprite.animation != anim:
		sprite.play(anim)


func _unhandled_input(event: InputEvent) -> void:
	if Game.input_locked or state == State.DEAD:
		return
	if event.is_action_pressed("attack") and state == State.MOVE:
		_swing()
	elif event.is_action_released("attack"):
		if _charging and _charge >= charge_time and state == State.MOVE:
			_spin()
		_charging = false
		_charge = 0.0
		sprite.modulate = Color.WHITE
	elif event.is_action_pressed("interact") and state == State.MOVE:
		_interact()
	elif event.is_action_pressed("use_item") and state == State.MOVE:
		_use_item()


func _direction_of(v: Vector2) -> String:
	# Keep the current facing on exact diagonals so she doesn't flicker between two.
	if absf(absf(v.x) - absf(v.y)) < 0.05:
		var current := {"e": v.x > 0, "w": v.x < 0, "s": v.y > 0, "n": v.y < 0}
		if current.get(facing, false):
			return facing
	if absf(v.x) > absf(v.y):
		return "e" if v.x > 0 else "w"
	return "s" if v.y > 0 else "n"


# --- the walking stick ------------------------------------------------------

func _swing() -> void:
	state = State.SWING
	_charging = true
	_charge = 0.0
	_hit_this_swing.clear()
	sprite.play("swing_" + facing)
	var dir: Vector2 = DIR_VECTORS[facing]
	var rect := RectangleShape2D.new()
	rect.size = Vector2(18, 12) if facing in ["n", "s"] else Vector2(12, 18)
	stick_shape.shape = rect
	stick_shape.position = dir * 12 + Vector2(0, -8)
	stick_shape.disabled = false
	slash.position = dir * 8 + Vector2(0, -10)
	slash.rotation = dir.angle()
	_play_effect(SLASH_FRAMES, 0.04)
	get_tree().create_timer(0.14).timeout.connect(func(): stick_shape.disabled = true)


func _spin() -> void:
	state = State.SPIN
	_hit_this_swing.clear()
	var circle := CircleShape2D.new()
	circle.radius = 20.0
	stick_shape.shape = circle
	stick_shape.position = Vector2(0, -8)
	stick_shape.disabled = false
	slash.position = Vector2(0, -10)
	slash.rotation = 0.0
	sprite.play("swing_" + facing)
	await _play_effect(SPIN_FRAMES, 0.05)
	stick_shape.disabled = true
	if state == State.SPIN:
		state = State.MOVE


func _play_effect(frames: Array, frame_time: float) -> void:
	slash.visible = true
	for tex in frames:
		slash.texture = tex
		await get_tree().create_timer(frame_time).timeout
	slash.visible = false


func _update_charge(delta: float) -> void:
	if not _charging or state == State.DEAD:
		return
	if not Input.is_action_pressed("attack"):
		_charging = false
		return
	_charge += delta
	# a soft pulse tells the player the spin is ready (on the sprite's alpha only, never its colour)
	if _charge >= charge_time and state == State.MOVE:
		sprite.modulate.a = 0.75 + 0.25 * sin(_charge * 30.0)


func _check_stick_hits() -> void:
	if stick_shape.disabled:
		return
	for body in stick_hitbox.get_overlapping_bodies():
		if body in _hit_this_swing or not body.has_method("take_hit"):
			continue
		_hit_this_swing.append(body)
		var damage := spin_damage if state == State.SPIN else swing_damage
		body.take_hit(damage, global_position, swing_knockback)
		Feedback.hit_stop(0.05)
		Feedback.shake(1.5, 0.1)
		Feedback.spark(body.global_position + Vector2(0, -8))
	for area in stick_hitbox.get_overlapping_areas():
		if area in _hit_this_swing or not area.has_method("take_hit"):
			continue
		_hit_this_swing.append(area)
		area.take_hit(swing_damage, global_position, 0.0)


func _on_animation_finished() -> void:
	if state == State.SWING:
		state = State.MOVE
		stick_shape.disabled = true


# --- taking hits ------------------------------------------------------------

func take_hit(damage: int, from: Vector2, _knockback: float = 0.0) -> void:
	if _invulnerable > 0.0 or state == State.DEAD or Game.input_locked:
		return
	Game.damage(damage)
	_invulnerable = invulnerable_time
	_charging = false
	stick_shape.disabled = true
	slash.visible = false
	velocity = (global_position - from).normalized() * hurt_knockback
	Feedback.hit_stop(0.08)
	Feedback.shake(3.0, 0.15)
	if Game.health <= 0:
		_die()
		return
	state = State.HURT
	sprite.play("idle_" + facing)
	await get_tree().create_timer(0.25).timeout
	if state == State.HURT:
		state = State.MOVE


func _die() -> void:
	state = State.DEAD
	velocity = Vector2.ZERO
	sprite.play("idle_s")
	var tween := create_tween()
	tween.tween_property(sprite, "rotation", PI / 2, 0.4)
	await get_tree().create_timer(0.8).timeout
	World.respawn()


# --- interacting and items ----------------------------------------------------

func _interact() -> void:
	interact_probe.position = DIR_VECTORS[facing] * 10 + Vector2(0, -4)
	await get_tree().physics_frame
	var best: Area2D = null
	for area in interact_probe.get_overlapping_areas():
		if area.has_method("interact") and (best == null or area.global_position.distance_to(global_position) < best.global_position.distance_to(global_position)):
			best = area
	if best:
		velocity = Vector2.ZERO
		sprite.play("idle_" + facing)
		best.interact(self)


func _use_item() -> void:
	if Game.current_item == &"lantern":
		_lantern_on = not _lantern_on
		_update_lantern()


func _update_lantern() -> void:
	lantern_light.enabled = Game.has_item(&"lantern") and _lantern_on


func lantern_lit() -> bool:
	return lantern_light.enabled
