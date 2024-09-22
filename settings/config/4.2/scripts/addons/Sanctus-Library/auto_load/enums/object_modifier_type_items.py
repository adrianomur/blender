from . import _base

class BObjectModifierType(_base.BStaticEnum):

	DATA_TRANSFER = dict(n='Data Transfer', d='Transfer several types of data (vertex groups, UV maps, vertex colors, custom normals) from one mesh to another')
	MESH_CACHE = dict(n='Mesh Cache', d='Deform the mesh using an external frame-by-frame vertex transform cache')
	MESH_SEQUENCE_CACHE = dict(n='Mesh Sequence Cache', d='Deform the mesh or curve using an external mesh cache in Alembic format')
	NORMAL_EDIT = dict(n='Normal Edit', d='Modify the direction of the surface normals')
	WEIGHTED_NORMAL = dict(n='Weighted Normal', d='Modify the direction of the surface normals using a weighting method')
	UV_PROJECT = dict(n='UV Project', d='Project the UV map coordinates from the negative Z axis of another object')
	UV_WARP = dict(n='UV Warp', d='Transform the UV map using the difference between two objects')
	VERTEX_WEIGHT_EDIT = dict(n='Vertex Weight Edit', d='Modify of the weights of a vertex group')
	VERTEX_WEIGHT_MIX = dict(n='Vertex Weight Mix', d='Mix the weights of two vertex groups')
	VERTEX_WEIGHT_PROXIMITY = dict(n='Vertex Weight Proximity', d='Set the vertex group weights based on the distance to another target object')
	ARRAY = dict(n='Array', d='Create copies of the shape with offsets')
	BEVEL = dict(n='Bevel', d='Generate sloped corners by adding geometry to the mesh’s edges or vertices')
	BOOLEAN = dict(n='Boolean', d='Use another shape to cut, combine or perform a difference operation')
	BUILD = dict(n='Build', d='Cause the faces of the mesh object to appear or disappear one after the other over time')
	DECIMATE = dict(n='Decimate', d='Reduce the geometry density')
	EDGE_SPLIT = dict(n='Edge Split', d='Split away joined faces at the edges')
	NODES = dict(n='Geometry Nodes', d='Geometry Nodes')
	MASK = dict(n='Mask', d='Dynamically hide vertices based on a vertex group or armature')
	MIRROR = dict(n='Mirror', d='Mirror along the local X, Y and/or Z axes, over the object origin')
	MESH_TO_VOLUME = dict(n='Mesh to Volume', d='Mesh to Volume')
	MULTIRES = dict(n='Multiresolution', d='Subdivide the mesh in a way that allows editing the higher subdivision levels')
	REMESH = dict(n='Remesh', d='Generate new mesh topology based on the current shape')
	SCREW = dict(n='Screw', d='Lathe around an axis, treating the input mesh as a profile')
	SKIN = dict(n='Skin', d='Create a solid shape from vertices and edges, using the vertex radius to define the thickness')
	SOLIDIFY = dict(n='Solidify', d='Make the surface thick')
	SUBSURF = dict(n='Subdivision Surface', d='Split the faces into smaller parts, giving it a smoother appearance')
	TRIANGULATE = dict(n='Triangulate', d='Convert all polygons to triangles')
	VOLUME_TO_MESH = dict(n='Volume to Mesh', d='Volume to Mesh')
	WELD = dict(n='Weld', d='Find groups of vertices closer than dist and merge them together')
	WIREFRAME = dict(n='Wireframe', d='Convert faces into thickened edges')
	ARMATURE = dict(n='Armature', d='Deform the shape using an armature object')
	CAST = dict(n='Cast', d='Shift the shape towards a predefined primitive')
	CURVE = dict(n='Curve', d='Bend the mesh using a curve object')
	DISPLACE = dict(n='Displace', d='Offset vertices based on a texture')
	HOOK = dict(n='Hook', d='Deform specific points using another object')
	LAPLACIANDEFORM = dict(n='Laplacian Deform', d='Deform based a series of anchor points')
	LATTICE = dict(n='Lattice', d='Deform using the shape of a lattice object')
	MESH_DEFORM = dict(n='Mesh Deform', d='Deform using a different mesh, which acts as a deformation cage')
	SHRINKWRAP = dict(n='Shrinkwrap', d='Project the shape onto another object')
	SIMPLE_DEFORM = dict(n='Simple Deform', d='Deform the shape by twisting, bending, tapering or stretching')
	SMOOTH = dict(n='Smooth', d='Smooth the mesh by flattening the angles between adjacent faces')
	CORRECTIVE_SMOOTH = dict(n='Smooth Corrective', d='Smooth the mesh while still preserving the volume')
	LAPLACIANSMOOTH = dict(n='Smooth Laplacian', d='Reduce the noise on a mesh surface with minimal changes to its shape')
	SURFACE_DEFORM = dict(n='Surface Deform', d='Transfer motion from another mesh')
	WARP = dict(n='Warp', d='Warp parts of a mesh to a new location in a very flexible way thanks to 2 specified objects')
	WAVE = dict(n='Wave', d='Adds a ripple-like motion to an object’s geometry')
	VOLUME_DISPLACE = dict(n='Volume Displace', d='Deform volume based on noise or other vector fields')
	CLOTH = dict(n='Cloth', d='Cloth')
	COLLISION = dict(n='Collision', d='Collision')
	DYNAMIC_PAINT = dict(n='Dynamic Paint', d='Dynamic Paint')
	EXPLODE = dict(n='Explode', d='Break apart the mesh faces and let them follow particles')
	FLUID = dict(n='Fluid', d='Fluid')
	OCEAN = dict(n='Ocean', d='Generate a moving ocean surface')
	PARTICLE_INSTANCE = dict(n='Particle Instance', d='Particle Instance')
	PARTICLE_SYSTEM = dict(n='Particle System', d='Spawn particles from the shape')
	SOFT_BODY = dict(n='Soft Body', d='Soft Body')
	SURFACE = dict(n='Surface', d='Surface')