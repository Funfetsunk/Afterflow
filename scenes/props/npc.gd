extends Area2D
## A villager Awa can talk to. Faces her while talking; the conversation is a
## DialogueData resource (GDD §10: warm but evasive, one line per ambient villager).

@export var dialogue: DialogueData
## Facing textures in the order south, east, north, west.
@export var textures: Array[Texture2D] = []

@onready var sprite: Sprite2D = $Sprite


func _ready() -> void:
	add_to_group("interactable")


func interact(player: Node2D) -> void:
	if dialogue == null:
		return
	_face(player.global_position - global_position)
	var after := dialogue.is_after()
	await Dialogue.say(dialogue.current_lines(), dialogue.speaker)
	if after and dialogue.after_diary_entry != &"":
		Game.add_diary_entry(dialogue.after_diary_entry)
	if dialogue.sets_flag != &"":
		Game.set_flag(dialogue.sets_flag)
	if dialogue.diary_entry != &"":
		Game.add_diary_entry(dialogue.diary_entry)
	_face(Vector2.DOWN)


func _face(v: Vector2) -> void:
	if textures.size() < 4:
		return
	var i := 0
	if absf(v.x) > absf(v.y):
		i = 1 if v.x > 0 else 3
	else:
		i = 0 if v.y > 0 else 2
	sprite.texture = textures[i]
