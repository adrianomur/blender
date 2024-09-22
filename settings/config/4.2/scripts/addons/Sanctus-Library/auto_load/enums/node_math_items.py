from . import _base

class BNodeMath(_base.BStaticEnum):

	ADD = dict(n='Add', d='A + B')
	SUBTRACT = dict(n='Subtract', d='A - B')
	MULTIPLY = dict(n='Multiply', d='A * B')
	DIVIDE = dict(n='Divide', d='A / B')
	MULTIPLY_ADD = dict(n='Multiply Add', d='A * B + C')
	POWER = dict(n='Power', d='A power B')
	LOGARITHM = dict(n='Logarithm', d='Logarithm A base B')
	SQRT = dict(n='Square Root', d='Square root of A')
	INVERSE_SQRT = dict(n='Inverse Square Root', d='1 / Square root of A')
	ABSOLUTE = dict(n='Absolute', d='Magnitude of A')
	EXPONENT = dict(n='Exponent', d='exp(A)')
	MINIMUM = dict(n='Minimum', d='The minimum from A and B')
	MAXIMUM = dict(n='Maximum', d='The maximum from A and B')
	LESS_THAN = dict(n='Less Than', d='1 if A < B else 0')
	GREATER_THAN = dict(n='Greater Than', d='1 if A > B else 0')
	SIGN = dict(n='Sign', d='Returns the sign of A')
	COMPARE = dict(n='Compare', d='1 if (A == B) within tolerance C else 0')
	SMOOTH_MIN = dict(n='Smooth Minimum', d='The minimum from A and B with smoothing C')
	SMOOTH_MAX = dict(n='Smooth Maximum', d='The maximum from A and B with smoothing C')
	ROUND = dict(n='Round', d='Round A to the nearest integer. Round upward if the fraction part is 0.5')
	FLOOR = dict(n='Floor', d='The largest integer smaller than or equal A')
	CEIL = dict(n='Ceil', d='The smallest integer greater than or equal A')
	TRUNC = dict(n='Truncate', d='The integer part of A, removing fractional digits')
	FRACT = dict(n='Fraction', d='The fraction part of A')
	MODULO = dict(n='Modulo', d='Modulo using fmod(A,B)')
	WRAP = dict(n='Wrap', d='Wrap value to range, wrap(A,B)')
	SNAP = dict(n='Snap', d='Snap to increment, snap(A,B)')
	PINGPONG = dict(n='Ping-Pong', d='Wraps a value and reverses every other cycle (A,B)')
	SINE = dict(n='Sine', d='sin(A)')
	COSINE = dict(n='Cosine', d='cos(A)')
	TANGENT = dict(n='Tangent', d='tan(A)')
	ARCSINE = dict(n='Arcsine', d='arcsin(A)')
	ARCCOSINE = dict(n='Arccosine', d='arccos(A)')
	ARCTANGENT = dict(n='Arctangent', d='arctan(A)')
	ARCTAN2 = dict(n='Arctan2', d='The signed angle arctan(A / B)')
	SINH = dict(n='Hyperbolic Sine', d='sinh(A)')
	COSH = dict(n='Hyperbolic Cosine', d='cosh(A)')
	TANH = dict(n='Hyperbolic Tangent', d='tanh(A)')
	RADIANS = dict(n='To Radians', d='Convert from degrees to radians')
	DEGREES = dict(n='To Degrees', d='Convert from radians to degrees')
