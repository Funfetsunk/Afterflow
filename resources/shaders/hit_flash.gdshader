shader_type canvas_item;
// White hit flash for the world's creatures (never used on Awa: Art Bible §4.3).
uniform float flash : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	COLOR = vec4(mix(c.rgb, vec3(1.0), flash), c.a);
}
