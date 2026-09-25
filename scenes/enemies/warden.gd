class_name Warden
extends CharacterBody2D
## The Hollow Oak's guardian (boss). Challenging but fair (GDD §9): every move
## is telegraphed, and there is always a safe answer.
##
##   CHARGE  arms up and a shiver, then a straight rush at Awa. If it hits a wall
##           it is dazed (eye closed): the only time the stick hurts it.
##   SLAM    every third attack: arms up for longer, then a shockwave around it.
##           Step away while the arms are up.
##   CALL    once, at half health: two mosslings climb out of the roots.
## Hitting it when it isn't dazed just clunks off the bark.

signal defeated

const POSES := {
	"idle": preload("res://assets/enemies/warden/warden_idle.png"),
	"raise": preload("res://assets/enemies/warden/warden_raise.png"),
	"dazed": preload("res://assets/enemies/warden/warden_dazed.png"),
}
const MOSSLING := preload("res://scenes/enemies/mossling.tscn")

enum State { ASLEEP, IDLE, TELEGRAPH, CHARGE, SLAM_WINDUP, SLAM, DAZED, HURT, DEAD }

@export var max_health: int = 10
@export var contact_damage: int = 1
@export var charge_speed: float = 170.0
@export var charge_time: float = 1.2
@export var telegraph_time: float = 0.7
@export var slam_windup: float = 1.0
@export var slam_radius: float = 44.0
@export var dazed_time: float = 1.8
@export var idle_time: float = 0.8
## The room Awa must be in to wake it (global rect).
@export var arena: Rect2 = Rect2(320, 0, 320, 176)

@onready var sprite: Sprite2D = $Sprite
@onready var hitbox: Area2D = $Hitbox
@onready var shockwave: Sprite2D = $Shockwave

var health: int
var state: State = State.ASLEEP
var _timer: float = 0.0
var _dir: Vector2 = Vector2.ZERO
var _attacks: int = 0
var _called: bool = false


func _ready() -> void:
	health = max_health
	add_to_group("enemies")
	shockwave.visible = false
	if Game.has_flag(&"warden_defeated"):
		queue_free()


func _physics_process(delta: float) -> void:
	if Game.input_locked and state != State.ASLEEP:
		return
	_timer -= delta
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player == null:
		return
	match state:
		State.ASLEEP:
			if arena.has_point(player.global_position) and not Game.input_locked:
				_set_state(State.IDLE, 1.0)
		State.IDLE:
			velocity = Vector2.ZERO
			if _timer <= 0.0:
				_attacks += 1
				if _attacks % 3 == 0:
					_set_state(State.SLAM_WINDUP, slam_windup)
				else:
					_dir = (player.global_position - global_position).normalized()
					_set_state(State.TELEGRAPH, telegraph_time)
		State.TELEGRAPH, State.SLAM_WINDUP:
			velocity = Vector2.ZERO
			sprite.position.x = sin(_timer * 70.0) * 1.5
			if _timer <= 0.0:
				sprite.position.x = 0.0
				if state == State.TELEGRAPH:
					_set_state(State.CHARGE, charge_time)
				else:
					_slam()
		State.CHARGE:
			velocity = _dir * charge_speed
			if _timer <= 0.0:
				_set_state(State.IDLE, idle_time)
		State.SLAM:
			velocity = Vector2.ZERO
			if _timer <= 0.0:
				shockwave.visible = false
				_set_state(State.IDLE, idle_time)
		State.DAZED, State.HURT:
			velocity = velocity.move_toward(Vector2.ZERO, 500.0 * delta)
			if _timer <= 0.0:
				_set_state(State.IDLE, idle_time)
		State.DEAD:
			return
	move_and_slide()
	if state == State.CHARGE and get_slide_collision_count() > 0:
		var hit := get_last_slide_collision().get_collider()
		if not hit is Player:
			Feedback.shake(4.0, 0.3)
			_set_state(State.DAZED, dazed_time)
	if state != State.DAZED and state != State.ASLEEP:
		for body in hitbox.get_overlapping_bodies():
			if body is Player:
				body.take_hit(contact_damage, global_position)


func _set_state(s: State, t: float) -> void:
	state = s
	_timer = t
	match s:
		State.TELEGRAPH, State.SLAM_WINDUP:
			sprite.texture = POSES["raise"]
		State.DAZED:
			sprite.texture = POSES["dazed"]
		_:
			sprite.texture = POSES["idle"]


func _slam() -> void:
	_set_state(State.SLAM, 0.4)
	sprite.texture = POSES["idle"]
	Feedback.shake(5.0, 0.3)
	shockwave.visible = true
	shockwave.scale = Vector2(0.3, 0.3)
	var tween := create_tween()
	tween.tween_property(shockwave, "scale", Vector2(1, 1), 0.2)
	var player := get_tree().get_first_node_in_group("player") as Player
	if player and player.global_position.distance_to(global_position) <= slam_radius:
		player.take_hit(1, global_position)


func take_hit(damage: int, from: Vector2, _knockback: float = 0.0) -> void:
	if state == State.DEAD or state == State.ASLEEP:
		return
	if state != State.DAZED:
		Feedback.spark(global_position + Vector2(0, -16))    # clunk: the bark turns the stick
		return
	health -= damage
	_flash()
	velocity = (global_position - from).normalized() * 60.0
	if health <= 0:
		_die()
		return
	if not _called and health * 2 <= max_health:
		_called = true
		_call_mosslings()


func _flash() -> void:
	var mat := sprite.material as ShaderMaterial
	if mat == null:
		return
	mat.set_shader_parameter("flash", 1.0)
	await get_tree().create_timer(0.12).timeout
	if is_instance_valid(self):
		mat.set_shader_parameter("flash", 0.0)


func _call_mosslings() -> void:
	for offset in [Vector2(-40, 10), Vector2(40, 10)]:
		var m := MOSSLING.instantiate()
		m.global_position = global_position + offset
		m.leaf_drop_chance = 1.0
		get_parent().add_child.call_deferred(m)
		Feedback.poof(global_position + offset)


func _die() -> void:
	state = State.DEAD
	velocity = Vector2.ZERO
	sprite.texture = POSES["dazed"]
	Game.set_flag(&"warden_defeated")
	Feedback.hit_stop(0.2)
	Feedback.shake(6.0, 0.6)
	var tween := create_tween()
	tween.tween_property(sprite, "modulate:a", 0.0, 1.2)
	await tween.finished
	Feedback.poof(global_position + Vector2(0, -16))
	defeated.emit()
	queue_free()
