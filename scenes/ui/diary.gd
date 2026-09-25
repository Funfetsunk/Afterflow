extends CanvasLayer
## The diary ("Diary" autoload): the single UI hub (GDD §13). Diary opens and
## closes it; left/right turn pages. The game pauses while it is open.
##
## Pages are DiaryEntry resources in `entries_dir`, in file-name order. A page
## shows once it starts written or Game has recorded its id.

## Folder of DiaryEntry .tres files.
@export_dir var entries_dir: String = "res://resources/diary"

@onready var book: NinePatchRect = $Book
@onready var title_label: Label = $Book/Title
@onready var text_label: Label = $Book/Text
@onready var footer: Label = $Book/Footer
@onready var notice: Label = $Notice

var entries: Array[DiaryEntry] = []
var page: int = 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	book.visible = false
	notice.visible = false
	for file in DirAccess.get_files_at(entries_dir):
		var path := entries_dir.path_join(file.trim_suffix(".remap"))
		if path.ends_with(".tres"):
			var entry := load(path) as DiaryEntry
			if entry:
				entries.append(entry)
	Game.diary_entry_added.connect(_on_entry_added)


func written() -> Array[DiaryEntry]:
	return entries.filter(func(e: DiaryEntry): return e.starts_written or e.id in Game.diary)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("diary"):
		if book.visible:
			_close()
		elif not Game.input_locked:
			_open()
		get_viewport().set_input_as_handled()
	elif book.visible:
		if event.is_action_pressed("move_left"):
			_turn(-1)
		elif event.is_action_pressed("move_right"):
			_turn(1)
		elif event.is_action_pressed("cancel") or event.is_action_pressed("pause"):
			_close()
		get_viewport().set_input_as_handled()


func _open() -> void:
	var pages := written()
	if pages.is_empty():
		return
	page = pages.size() - 1                        # open at the newest page
	book.visible = true
	get_tree().paused = true
	_show()


func _close() -> void:
	book.visible = false
	get_tree().paused = false


func _turn(step: int) -> void:
	page = clampi(page + step, 0, written().size() - 1)
	_show()


func _show() -> void:
	var pages := written()
	var entry := pages[page]
	title_label.text = entry.title
	text_label.text = entry.text
	footer.text = "%s  %d / %d  %s" % ["<" if page > 0 else " ", page + 1, pages.size(), ">" if page < pages.size() - 1 else " "]


func _on_entry_added(_id: StringName) -> void:
	notice.visible = true
	var tween := create_tween()
	tween.tween_interval(2.5)
	tween.tween_callback(func(): notice.visible = false)
