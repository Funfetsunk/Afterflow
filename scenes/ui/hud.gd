extends CanvasLayer
## Minimal HUD (GDD §13): health leaves on a sprig top-left, current item bottom-right.
##
## Leaves wilt as Awa takes hits. Item icons are looked up by item id.

const LEAF_FULL := preload("res://assets/ui/leaf_full.png")
const LEAF_WILTED := preload("res://assets/ui/leaf_wilted.png")

## Item id -> icon shown in the frame.
@export var item_icons: Dictionary = {&"lantern": preload("res://assets/ui/lantern.png")}

@onready var leaves: HBoxContainer = $Leaves
@onready var item_icon: TextureRect = $ItemFrame/ItemIcon
@onready var keys_box: HBoxContainer = $Keys
@onready var keys_label: Label = $Keys/Count


func _ready() -> void:
	Game.health_changed.connect(_on_health_changed)
	Game.item_changed.connect(_on_item_changed)
	Game.keys_changed.connect(_on_keys_changed)
	_on_health_changed(Game.health, Game.max_health)
	_on_item_changed(Game.current_item)
	_on_keys_changed(Game.small_keys)


func _on_health_changed(health: int, max_health: int) -> void:
	while leaves.get_child_count() < max_health:
		var leaf := TextureRect.new()
		leaf.texture = LEAF_FULL
		leaves.add_child(leaf)
	while leaves.get_child_count() > max_health:
		leaves.get_child(leaves.get_child_count() - 1).free()
	for i in leaves.get_child_count():
		(leaves.get_child(i) as TextureRect).texture = LEAF_FULL if i < health else LEAF_WILTED


func _on_item_changed(item: StringName) -> void:
	item_icon.texture = item_icons.get(item, null)


func _on_keys_changed(keys: int) -> void:
	keys_box.visible = keys > 0
	keys_label.text = "x%d" % keys
