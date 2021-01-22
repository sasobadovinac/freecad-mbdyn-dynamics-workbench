import os

class DeformableDisplacementCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "spring.png") 

class PrismaticCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "prismatic.png") 
         
class DynamicNodeCustomView():
	def __init__(self, obj):
         obj.Proxy = self

	def getIcon(self):
         return os.path.join(os.path.dirname(__file__), "icons", "StructuralDynamic.png") 
         
class DummyNodeCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "StructuralDummy.png")
         
class StaticNodeCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "StructuralStatic.png") 

class RigidBodyCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "viga.png") 
         
class DummyBodyCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "viga1.png") 
         
class RevolutePinCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "hinge.png") 
         
class RevoluteHingeCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "hinge1.png") 

class ClampCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "clamp.png") 

class InLineCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "in-line.png") 

class InPlaneCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "in-plane.png") 

class AxialCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "axial.png")          
         
class StructuralForceCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "force.png")  
         
         
class DriveHingeCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "drivehinge.png")      
         
class SphericalCustomView():
	def __init__(self, obj):
		obj.Proxy = self

	def getIcon(self):
	        return os.path.join(os.path.dirname(__file__), "icons", "spherical.png")