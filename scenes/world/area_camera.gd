class_name AreaCamera
extends Camera2D
## Follows its parent (Awa) and stays inside the area's map.
##
## Limits come from the TileMapLayer set in the Inspector, so a new area only
## needs its ground layer assigned.

## The area's ground layer; its used rectangle becomes the camera limits.
@export var bounds_layer: TileMapLayer


func _ready() -> void:
	if bounds_layer == null:
		return
	var rect := bounds_layer.get_used_rect()
	var size := bounds_layer.tile_set.tile_size
	limit_left = rect.position.x * size.x
	limit_top = rect.position.y * size.y
	limit_right = rect.end.x * size.x
	limit_bottom = rect.end.y * size.y
