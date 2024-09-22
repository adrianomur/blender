from . import _base

class BRenderPassType(_base.BStaticEnum):

	COMBINED = dict(n='Combined', d='Combined')
	Z = dict(n='Z', d='Z')
	SHADOW = dict(n='Shadow', d='Shadow')
	AO = dict(n='Ambient Occlusion', d='Ambient Occlusion')
	POSITION = dict(n='Position', d='Position')
	NORMAL = dict(n='Normal', d='Normal')
	VECTOR = dict(n='Vector', d='Vector')
	OBJECT_INDEX = dict(n='Object Index', d='Object Index')
	UV = dict(n='UV', d='UV')
	MIST = dict(n='Mist', d='Mist')
	EMIT = dict(n='Emit', d='Emit')
	ENVIRONMENT = dict(n='Environment', d='Environment')
	MATERIAL_INDEX = dict(n='Material Index', d='Material Index')
	DIFFUSE_DIRECT = dict(n='Diffuse Direct', d='Diffuse Direct')
	DIFFUSE_INDIRECT = dict(n='Diffuse Indirect', d='Diffuse Indirect')
	DIFFUSE_COLOR = dict(n='Diffuse Color', d='Diffuse Color')
	GLOSSY_DIRECT = dict(n='Glossy Direct', d='Glossy Direct')
	GLOSSY_INDIRECT = dict(n='Glossy Indirect', d='Glossy Indirect')
	GLOSSY_COLOR = dict(n='Glossy Color', d='Glossy Color')
	TRANSMISSION_DIRECT = dict(n='Transmission Direct', d='Transmission Direct')
	TRANSMISSION_INDIRECT = dict(n='Transmission Indirect', d='Transmission Indirect')
	TRANSMISSION_COLOR = dict(n='Transmission Color', d='Transmission Color')
	SUBSURFACE_DIRECT = dict(n='Subsurface Direct', d='Subsurface Direct')
	SUBSURFACE_INDIRECT = dict(n='Subsurface Indirect', d='Subsurface Indirect')
	SUBSURFACE_COLOR = dict(n='Subsurface Color', d='Subsurface Color')
