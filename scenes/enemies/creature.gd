class_name Creature
extends CharacterBody2D
## One of the world's creatures (GDD §8): wanders, notices Awa, attacks with a
## clear telegraph. Hit flash, knockback and a puff when it's beaten.
##
## HOPPER (mossling): squashes down, then hops at Awa.
## CHARGER (barkling): shivers, then rushes in a straight line; stunned if it
## meets a wall.

signal defeated

enum Behaviour { HOPPER, CHARGER }
enum State { WANDER, TELEGRAPH, ATTACK, REST, HURT }

@export var behaviour: Behaviour = Behaviour.HOPPER
## Facing textures in the order south, east, north, west.
@export var textures: Array[Texture2D] = []
@export var max_health: int = 2
## Damage its body deals to Awa on contact.
@export var contact_damage: int = 1
## Notices Awa within this many pixels.
@export var sight: float = 80.0
@export var wander_speed: float = 14.0
## Speed of the hop or the charge, pixels per second.
@export var attack_speed: float = 110.0
## Seconds of warning before it attacks.
@export var telegraph_time: float = 0.4
@export var attack_time: float = 0.3
@export var rest_time: float = 0.6
## Chance (0-1) of dropping a leaf that heals Awa.
@export var leaf_drop_chance: float = 0.3

const LEAF_PICKUP := preload("res://scenes/props/leaf_pickup.tscn")

@onready var sprite: Sprite2D = $Sprite
@onready var hitbox: Area2D = $Hitbox

var health: int
var state: State = State.WANDER
var _timer: float = 0.0
var _dir: Vector2 = Vector2.ZERO
var _home: Vector2


func _ready() -> void:
	health = max_health
	_home = global_position
	add_to_group("enemies")
	sprite.material = sprite.material.duplicate() if sprite.material else null
	_pick_wander()


func _physics_process(delta: float) -> void:
	if Game.input_locked:                       # the world holds still while Awa reads or talks
		return
	_timer -= delta
	var player := get_tree().get_first_node_in_group("player") as Node2D
	var to_player := (player.global_position - global_position) if player else Vector2.INF
	match state:
		State.WANDER:
			velocity = _dir * wander_speed
			if _timer <= 0.0:
				_pick_wander()
			if player and to_player.length() < sight and not Game.input_locked:
				_start_telegraph(to_player)
		State.TELEGRAPH:
			velocity = Vector2.ZERO
			if behaviour == Behaviour.HOPPER:
				sprite.scale = Vector2(1.2, 0.8)
			else:
				sprite.position.x = sin(_timer * 80.0)
			if _timer <= 0.0:
				_start_attack()
		State.ATTACK:
			velocity = _dir * attack_speed
			if behaviour == Behaviour.HOPPER:
				sprite.scale = Vector2(0.85, 1.15)
				sprite.position.y = -sin((1.0 - _timer / attack_time) * PI) * 6.0
			if _timer <= 0.0:
				_start_rest(rest_time)
		State.REST, State.HURT:
			velocity = velocity.move_toward(Vector2.ZERO, 600.0 * delta)
			if _timer <= 0.0:
				state = State.WANDER
				_pick_wander()
	var collided := move_and_slide()
	if state == State.ATTACK and behaviour == Behaviour.CHARGER and collided and get_slide_collision_count() > 0:
		if not get_last_slide_collision().get_collider() is Player:
			Feedback.shake(1.5, 0.1)
			_start_rest(rest_time * 1.8)          # dazed after hitting a wall: the opening
	_face(velocity if velocity.length() > 1.0 else _dir)
	for body in hitbox.get_overlapping_bodies():
		if body is Player and state != State.HURT:
			body.take_hit(contact_damage, global_position)


func _pick_wander() -> void:
	_timer = randf_range(0.8, 1.8)
	var back := (_home - global_position)
	_dir = back.normalized() if back.length() > 40.0 else Vector2.from_angle(randf() * TAU) * (1.0 if randf() > 0.3 else 0.0)


func _start_telegraph(to_player: Vector2) -> void:
	state = State.TELEGRAPH
	_timer = telegraph_time
	_dir = to_player.normalized()


func _start_attack() -> void:
	state = State.ATTACK
	_timer = attack_time
	sprite.position = Vector2(0, 0)
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player and behaviour == Behaviour.HOPPER:
		_dir = (player.global_position - global_position).normalized()


func _start_rest(seconds: float) -> void:
	state = State.REST
	_timer = seconds
	sprite.scale = Vector2.ONE
	sprite.position = Vector2.ZERO


func _face(v: Vector2) -> void:
	if textures.size() < 4 or v == Vector2.ZERO:
		return
	var i := 0
	if absf(v.x) > absf(v.y):
		i = 1 if v.x > 0 else 3
	else:
		i = 0 if v.y > 0 else 2
	sprite.texture = textures[i]


func take_hit(damage: int, from: Vector2, knockback: float = 150.0) -> void:
	health -= damage
	state = State.HURT
	_timer = 0.35
	sprite.scale = Vector2.ONE
	sprite.position = Vector2.ZERO
	velocity = (global_position - from).normalized() * knockback
	_flash()
	if health <= 0:
		_die()


func _flash() -> void:
	var mat := sprite.material as ShaderMaterial
	if mat == null:
		return
	mat.set_shader_parameter("flash", 1.0)
	await get_tree().create_timer(0.1).timeout
	if is_instance_valid(self):
		mat.set_shader_parameter("flash", 0.0)


func _die() -> void:
	set_physics_process(false)
	Feedback.poof(global_position + Vector2(0, -6))
	if randf() < leaf_drop_chance:
		var leaf := LEAF_PICKUP.instantiate()
		leaf.global_position = global_position
		get_parent().add_child.call_deferred(leaf)
	defeated.emit()
	queue_free()
