from . import _base

class BObjectGreasepencilModifierType(_base.BStaticEnum):

	GP_TEXTURE = dict(n='Texture Mapping', d='Change stroke uv texture values')
	GP_TIME = dict(n='Time Offset', d='Offset keyframes')
	GP_WEIGHT_ANGLE = dict(n='Vertex Weight Angle', d='Generate Vertex Weights base on stroke angle')
	GP_WEIGHT_PROXIMITY = dict(n='Vertex Weight Proximity', d='Generate Vertex Weights base on distance to object')
	GP_ARRAY = dict(n='Array', d='Create array of duplicate instances')
	GP_BUILD = dict(n='Build', d='Create duplication of strokes')
	GP_DASH = dict(n='Dot Dash', d='Generate dot-dash styled strokes')
	GP_ENVELOPE = dict(n='Envelope', d='Create an envelope shape')
	GP_LENGTH = dict(n='Length', d='Extend or shrink strokes')
	GP_LINEART = dict(n='Line Art', d='Generate line art strokes from selected source')
	GP_MIRROR = dict(n='Mirror', d='Duplicate strokes like a mirror')
	GP_MULTIPLY = dict(n='Multiple Strokes', d='Produce multiple strokes along one stroke')
	GP_OUTLINE = dict(n='Outline', d='Convert stroke to perimeter')
	GP_SIMPLIFY = dict(n='Simplify', d='Simplify stroke reducing number of points')
	GP_SUBDIV = dict(n='Subdivide', d='Subdivide stroke adding more control points')
	GP_ARMATURE = dict(n='Armature', d='Deform stroke points using armature object')
	GP_HOOK = dict(n='Hook', d='Deform stroke points using objects')
	GP_LATTICE = dict(n='Lattice', d='Deform strokes using lattice')
	GP_NOISE = dict(n='Noise', d='Add noise to strokes')
	GP_OFFSET = dict(n='Offset', d='Change stroke location, rotation or scale')
	SHRINKWRAP = dict(n='Shrinkwrap', d='Project the shape onto another object')
	GP_SMOOTH = dict(n='Smooth', d='Smooth stroke')
	GP_THICK = dict(n='Thickness', d='Change stroke thickness')
	GP_COLOR = dict(n='Hue/Saturation', d='Apply changes to stroke colors')
	GP_OPACITY = dict(n='Opacity', d='Opacity of the strokes')
	GP_TINT = dict(n='Tint', d='Tint strokes with new color')
