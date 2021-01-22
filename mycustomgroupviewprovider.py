class MyCustomGroupViewProvider():
	def __init__(self, obj):
		obj.addExtension("Gui::ViewProviderGroupExtensionPython", self)
		obj.Proxy = self

	def getIcon(self):
	        '''Return the icon in XPM format which will appear in the tree view. This method is\
	                optional and if not defined a default icon is shown.'''
	        return """
	            /* XPM */
	            static const char * ViewProviderBox_xpm[] = {
	            "16 16 6 1",
	            "   c None",
	            ".  c #141010",
	            "+  c #615BD2",
	            "@  c #C39D55",
	            "#  c #000000",
	            "$  c #57C355",
	            "        ........",
	            "   ......++..+..",
	            "   .@@@@.++..++.",
	            "   .@@@@.++..++.",
	            "   .@@  .++++++.",
	            "  ..@@  .++..++.",
	            "###@@@@ .++..++.",
	            "##$.@@$#.++++++.",
	            "#$#$.$$$........",
	            "#$$#######      ",
	            "#$$#$$$$$#      ",
	            "#$$#$$$$$#      ",
	            "#$$#$$$$$#      ",
	            " #$#$$$$$#      ",
	            "  ##$$$$$#      ",
	            "   #######      "};
	            """
