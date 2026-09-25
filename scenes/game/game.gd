extends Node
## Game state autoload ("Game"): health, items, story flags, respawn point, saving.
##
## Everything that must survive an area change or a save lives here. Areas and
## props read and write it; the HUD listens to its signals.

signal health_changed(health: int, max_health: int)
signal item_changed(item: StringName)
signal keys_changed(keys: int)
signal flag_set(flag: StringName)
signal diary_entry_added(entry_id: StringName)

const SAVE_PATH := "user://save.json"

## Starting health, in leaves (one hit wilts one leaf).
@export var start_max_health: int = 5

var max_health: int = 5
var health: int = 5
var items: Array[StringName] = []
var current_item: StringName = &""
var small_keys: int = 0
var flags: Dictionary = {}
var diary: Array[StringName] = []
var respawn_area: String = ""
var respawn_point: StringName = &""

## True while a dialogue, the diary or a transition owns the controls.
var input_locked: bool = false


func _ready() -> void:
	max_health = start_max_health
	health = max_health


# --- health -------------------------------------------------------------

func damage(amount: int) -> void:
	health = maxi(health - amount, 0)
	health_changed.emit(health, max_health)


func heal_full() -> void:
	health = max_health
	health_changed.emit(health, max_health)


func add_max_health(amount: int) -> void:
	max_health += amount
	health = max_health
	health_changed.emit(health, max_health)


# --- items, keys, flags, diary -------------------------------------------

func give_item(item: StringName) -> void:
	if item not in items:
		items.append(item)
	current_item = item
	item_changed.emit(item)


func has_item(item: StringName) -> bool:
	return item in items


func add_key(amount: int = 1) -> void:
	small_keys += amount
	keys_changed.emit(small_keys)


func use_key() -> bool:
	if small_keys <= 0:
		return false
	small_keys -= 1
	keys_changed.emit(small_keys)
	return true


func set_flag(flag: StringName) -> void:
	if not flags.get(flag, false):
		flags[flag] = true
		flag_set.emit(flag)


func has_flag(flag: StringName) -> bool:
	return flags.get(flag, false)


func add_diary_entry(entry_id: StringName) -> void:
	if entry_id not in diary:
		diary.append(entry_id)
		diary_entry_added.emit(entry_id)


# --- respawn and saving ---------------------------------------------------

func set_respawn(area_path: String, point: StringName) -> void:
	respawn_area = area_path
	respawn_point = point


func save_game() -> void:
	var data := {
		"max_health": max_health, "items": items.map(func(i): return String(i)),
		"current_item": String(current_item), "small_keys": small_keys, "flags": flags,
		"diary": diary.map(func(d): return String(d)),
		"respawn_area": respawn_area, "respawn_point": String(respawn_point),
		"area": World.current_area_path, "spawn": String(World.current_spawn),
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data, "\t"))


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


## Loads the save into this state; returns [area_path, spawn] to resume at.
func load_game() -> Array:
	var data = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if typeof(data) != TYPE_DICTIONARY:
		return []
	max_health = int(data.get("max_health", start_max_health))
	health = max_health
	items.assign(data.get("items", []).map(func(i): return StringName(i)))
	current_item = StringName(data.get("current_item", ""))
	small_keys = int(data.get("small_keys", 0))
	flags = data.get("flags", {})
	diary.assign(data.get("diary", []).map(func(d): return StringName(d)))
	respawn_area = data.get("respawn_area", "")
	respawn_point = StringName(data.get("respawn_point", ""))
	health_changed.emit(health, max_health)
	item_changed.emit(current_item)
	keys_changed.emit(small_keys)
	return [data.get("area", ""), StringName(data.get("spawn", ""))]


func reset() -> void:
	max_health = start_max_health
	health = max_health
	items.clear()
	current_item = &""
	small_keys = 0
	flags.clear()
	diary.clear()
	respawn_area = ""
	respawn_point = &""
