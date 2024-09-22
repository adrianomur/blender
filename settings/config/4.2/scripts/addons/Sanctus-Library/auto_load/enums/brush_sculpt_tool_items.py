from . import _base

class BBrushSculptTool(_base.BStaticEnum):

	DRAW = dict(n='Draw', d='Draw')
	DRAW_SHARP = dict(n='Draw Sharp', d='Draw Sharp')
	CLAY = dict(n='Clay', d='Clay')
	CLAY_STRIPS = dict(n='Clay Strips', d='Clay Strips')
	CLAY_THUMB = dict(n='Clay Thumb', d='Clay Thumb')
	LAYER = dict(n='Layer', d='Layer')
	INFLATE = dict(n='Inflate', d='Inflate')
	BLOB = dict(n='Blob', d='Blob')
	CREASE = dict(n='Crease', d='Crease')
	SMOOTH = dict(n='Smooth', d='Smooth')
	FLATTEN = dict(n='Flatten', d='Flatten')
	FILL = dict(n='Fill', d='Fill')
	SCRAPE = dict(n='Scrape', d='Scrape')
	MULTIPLANE_SCRAPE = dict(n='Multi-plane Scrape', d='Multi-plane Scrape')
	PINCH = dict(n='Pinch', d='Pinch')
	GRAB = dict(n='Grab', d='Grab')
	ELASTIC_DEFORM = dict(n='Elastic Deform', d='Elastic Deform')
	SNAKE_HOOK = dict(n='Snake Hook', d='Snake Hook')
	THUMB = dict(n='Thumb', d='Thumb')
	POSE = dict(n='Pose', d='Pose')
	NUDGE = dict(n='Nudge', d='Nudge')
	ROTATE = dict(n='Rotate', d='Rotate')
	TOPOLOGY = dict(n='Slide Relax', d='Slide Relax')
	BOUNDARY = dict(n='Boundary', d='Boundary')
	CLOTH = dict(n='Cloth', d='Cloth')
	SIMPLIFY = dict(n='Simplify', d='Simplify')
	MASK = dict(n='Mask', d='Mask')
	DRAW_FACE_SETS = dict(n='Draw Face Sets', d='Draw Face Sets')
	DISPLACEMENT_ERASER = dict(n='Multires Displacement Eraser', d='Multires Displacement Eraser')
	DISPLACEMENT_SMEAR = dict(n='Multires Displacement Smear', d='Multires Displacement Smear')
	PAINT = dict(n='Paint', d='Paint')
	SMEAR = dict(n='Smear', d='Smear')
