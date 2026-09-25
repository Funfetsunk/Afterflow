extends CanvasLayer
## Dialogue box ("Dialogue" autoload). `await Dialogue.say(lines, speaker)`.
##
## Text types out; interact or attack shows the whole line, then moves on.
## While it is open Awa can't move.

signal finished

## Characters typed per second.
@export var type_speed: float = 45.0

@onready var box: NinePatchRect = $Box
@onready var speaker_label: Label = $Box/Speaker
@onready var text_label: Label = $Box/Text
@onready var more: Label = $Box/More

var _lines: PackedStringArray = []
var _index: int = 0
var _typing: bool = false
var _shown: float = 0.0
var active: bool = false


func _ready() -> void:
	box.visible = false


func say(lines: PackedStringArray, speaker: String = "") -> void:
	if lines.is_empty():
		return
	_lines = lines
	_index = 0
	speaker_label.text = speaker
	speaker_label.visible = speaker != ""
	box.visible = true
	active = true
	Game.input_locked = true
	_show_line()
	await finished


func _show_line() -> void:
	text_label.text = _lines[_index]
	text_label.visible_characters = 0
	_shown = 0.0
	_typing = true
	more.visible = false


func _process(delta: float) -> void:
	if not _typing:
		return
	_shown += type_speed * delta
	text_label.visible_characters = int(_shown)
	if text_label.visible_characters >= text_label.text.length():
		_finish_typing()


func _finish_typing() -> void:
	_typing = false
	text_label.visible_characters = -1
	more.visible = true


func _unhandled_input(event: InputEvent) -> void:
	if not active:
		return
	if event.is_action_pressed("interact") or event.is_action_pressed("attack") or event.is_action_pressed("cancel"):
		get_viewport().set_input_as_handled()
		if _typing:
			_finish_typing()
			return
		_index += 1
		if _index < _lines.size():
			_show_line()
		else:
			_close()


func _close() -> void:
	box.visible = false
	active = false
	# release the controls a frame later, so the closing press doesn't swing the stick
	await get_tree().process_frame
	Game.input_locked = false
	finished.emit()
