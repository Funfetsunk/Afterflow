extends Area2D
## Writes a diary page the first time Awa walks in (e.g. entering the Old Wood).

@export var diary_entry: StringName = &""


func _ready() -> void:
	body_entered.connect(func(b): if b is Player and diary_entry != &"": Game.add_diary_entry(diary_entry))
