import os

class CustomView():
	def __init__(self, obj):
		obj.addExtension("Gui::ViewProviderGroupExtensionPython", self)
		obj.Proxy = self

	def getIcon(self):
         return os.path.join(os.path.dirname(__file__), "icons", "MBDyn.png") 