class_name DiaryEntry
extends Resource
## One diary page. Old and new entries share one hand and voice (GDD §3.5):
## write them all as Awa, never marking which are "new".

@export var id: StringName = &""
@export var title: String = ""
@export_multiline var text: String = ""
## Pages Awa wakes with are already in the diary.
@export var starts_written: bool = false
