class_name Pickup
extends Area2D
## Something Awa picks up by walking over it: a healing leaf, a heart-leaf, a
## small key, a key item (the lantern) or a torn diary page.
##
## One-off pickups set `flag` and never come back once taken.

enum Kind { HEAL, HEART_LEAF, SMALL_KEY, ITEM, DIARY_PAGE }

@export var kind: Kind = Kind.HEAL
## Item id for ITEM pickups (e.g. lantern).
@export var item: StringName = &""
## Set when taken; a pickup whose flag is already set removes itself.
@export var flag: StringName = &""
## Diary entry added when taken (empty: none).
@export var diary_entry: StringName = &""
## Shown in the dialogue box when taken (empty: silent).
@export_multiline var message: String = ""

@onready var sprite: Sprite2D = $Sprite

var _t: float = 0.0


func _ready() -> void:
	if flag != &"" and Game.has_flag(flag):
		queue_free()
		return
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	_t += delta
	sprite.position.y = -4.0 + sin(_t * 4.0) * 1.5


func _on_body_entered(body: Node) -> void:
	if not body is Player:
		return
	match kind:
		Kind.HEAL:
			if Game.health >= Game.max_health:
				return
			Game.damage(-1)
		Kind.HEART_LEAF:
			Game.add_max_health(1)
		Kind.SMALL_KEY:
			Game.add_key()
		Kind.ITEM:
			Game.give_item(item)
	if flag != &"":
		Game.set_flag(flag)
	if diary_entry != &"":
		Game.add_diary_entry(diary_entry)
	set_deferred("monitoring", false)
	visible = false
	if message != "":
		await Dialogue.say(PackedStringArray([message]))
	queue_free()
