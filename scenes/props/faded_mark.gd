extends Node2D
## Faded writing only the lantern shows (GDD §7.3). The mark's sprite is lit
## "light only", on light mask 2, which only the lantern's light reaches.
## Standing near it with the lantern lit writes its diary page.

## Diary entry written when Awa first reads it.
@export var diary_entry: StringName = &"mark"
## How close Awa must be, in pixels.
@export var read_distance: float = 36.0


func _process(_delta: float) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player == null or not player.lantern_lit():
		return
	if player.global_position.distance_to(global_position) <= read_distance:
		Game.add_diary_entry(diary_entry)
		set_process(false)
