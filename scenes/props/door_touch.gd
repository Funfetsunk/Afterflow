extends Area2D
## The interact area of a locked door; passes the interaction to the door.


func interact(_player: Node) -> void:
	get_parent().try_open()
