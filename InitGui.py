# -*- coding: utf-8 -*-
###################################################################################
#
#  Copyright 2021 Jose Gabriel Egas Ortuno
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################

class MBdynWorkbench (Workbench):
    """Basic 1 workbench object"""
    # this is the icon in XPM format 16x16 pixels
    Icon = """
    /* XPM */
static char * MBDyn_xpm[] = {
"101 84 237 2",
"  	c None",
". 	c #E5C5A6",
"+ 	c #EEAD6F",
"@ 	c #F79538",
"# 	c #FF7D00",
"$ 	c #F98F29",
"% 	c #FB881B",
"& 	c #F2A153",
"* 	c #E3CAB3",
"= 	c #ECB37D",
"- 	c #F59B45",
"; 	c #EAB98A",
"> 	c #E1D1C1",
", 	c #F0A660",
"' 	c #E9B88A",
") 	c #FD830E",
"! 	c #ECB37C",
"~ 	c #E5C4A5",
"{ 	c #F79537",
"] 	c #F0A761",
"^ 	c #F98F2A",
"/ 	c #E7BF98",
"( 	c #F2A052",
"_ 	c #FD820D",
": 	c #FB891C",
"< 	c #D8BEBE",
"[ 	c #D19797",
"} 	c #CB6262",
"| 	c #CC5E5E",
"1 	c #C63B3B",
"2 	c #C74040",
"3 	c #C95353",
"4 	c #CC6A6A",
"5 	c #D49F9F",
"6 	c #DAC3C3",
"7 	c #F49A45",
"8 	c #E7BE97",
"9 	c #EEAC6E",
"0 	c #DA4E1F",
"a 	c #C32C2C",
"b 	c #C53636",
"c 	c #C85050",
"d 	c #C84C4C",
"e 	c #C53939",
"f 	c #C31F1F",
"g 	c #BE0808",
"h 	c #BD0000",
"i 	c #C95858",
"j 	c #D9C2C2",
"k 	c #FC820D",
"l 	c #D9C3C3",
"m 	c #D39D9D",
"n 	c #C95151",
"o 	c #C01313",
"p 	c #BE0000",
"q 	c #C22121",
"r 	c #DEC0C0",
"s 	c #D4A0A0",
"t 	c #C32F2F",
"u 	c #BF0A0A",
"v 	c #D29191",
"w 	c #DAB8B8",
"x 	c #DABFBF",
"y 	c #C21D1D",
"z 	c #DEC5C5",
"A 	c #D9C1C1",
"B 	c #D39999",
"C 	c #BE0A0A",
"D 	c #C84B4B",
"E 	c #C84D4D",
"F 	c #C63C3C",
"G 	c #C43030",
"H 	c #C11B1B",
"I 	c #C74141",
"J 	c #D08282",
"K 	c #C01414",
"L 	c #CB6060",
"M 	c #CD6A6A",
"N 	c #C74949",
"O 	c #C11212",
"P 	c #CE6F6F",
"Q 	c #D39797",
"R 	c #CC6C6C",
"S 	c #C01212",
"T 	c #DEC1C1",
"U 	c #C42C2C",
"V 	c #BF0909",
"W 	c #D4A6A6",
"X 	c #CD6E6E",
"Y 	c #D5A5A5",
"Z 	c #CF7E7E",
"` 	c #D49D9D",
" .	c #C74B4B",
"..	c #C11313",
"+.	c #D5AAAA",
"@.	c #C11D1D",
"#.	c #DABEBE",
"$.	c #DCCBCB",
"%.	c #C42A2A",
"&.	c #C53333",
"*.	c #CC6B6B",
"=.	c #CA5656",
"-.	c #C32222",
";.	c #D9C6C6",
">.	c #C22020",
",.	c #CB2009",
"'.	c #F67E19",
").	c #CF8181",
"!.	c #CF1F00",
"~.	c #FB7500",
"{.	c #D18A8A",
"].	c #C53232",
"^.	c #D32700",
"/.	c #DB927B",
"(.	c #FB7601",
"_.	c #F67812",
":.	c #BF0707",
"<.	c #EC8B45",
"[.	c #BF0809",
"}.	c #FC7904",
"|.	c #E5B089",
"1.	c #BE0001",
"2.	c #BE0002",
"3.	c #BF0808",
"4.	c #C00B0C",
"5.	c #EC9F61",
"6.	c #E5AF88",
"7.	c #BD0002",
"8.	c #FC7B06",
"9.	c #EB9D5F",
"0.	c #C42929",
"a.	c #F07822",
"b.	c #DAC1C1",
"c.	c #DA4415",
"d.	c #FD7B06",
"e.	c #BE0003",
"f.	c #CA5A5A",
"g.	c #CA1700",
"h.	c #E9B889",
"i.	c #BF0004",
"j.	c #C21F1F",
"k.	c #E3CACA",
"l.	c #BE0004",
"m.	c #C53535",
"n.	c #D72F00",
"o.	c #BF0003",
"p.	c #FC7A05",
"q.	c #BE0608",
"r.	c #C53131",
"s.	c #E74E00",
"t.	c #BF0606",
"u.	c #EB5600",
"v.	c #C11515",
"w.	c #BF0B0B",
"x.	c #C20800",
"y.	c #F36600",
"z.	c #BE0005",
"A.	c #BF0708",
"B.	c #C94E4E",
"C.	c #E24600",
"D.	c #F06406",
"E.	c #ED904A",
"F.	c #C53030",
"G.	c #BE0709",
"H.	c #BF0505",
"I.	c #C85151",
"J.	c #BE0707",
"K.	c #BE0606",
"L.	c #C53737",
"M.	c #D49E9E",
"N.	c #CE7676",
"O.	c #BF090A",
"P.	c #C53838",
"Q.	c #C32A2A",
"R.	c #C32121",
"S.	c #BE0909",
"T.	c #C00C0C",
"U.	c #C74747",
"V.	c #C74A4A",
"W.	c #DEBFBF",
"X.	c #BF1313",
"Y.	c #C11A1A",
"Z.	c #D8BDBD",
"`.	c #CF7C7C",
" +	c #CC6464",
".+	c #D6A9A9",
"++	c #C22727",
"@+	c #C74646",
"#+	c #D08383",
"$+	c #DEBDBD",
"%+	c #C74848",
"&+	c #BF0608",
"*+	c #DABABA",
"=+	c #BF1212",
"-+	c #CD7272",
";+	c #C95252",
">+	c #C21C1C",
",+	c #C42D2D",
"'+	c #CF7A7A",
")+	c #BF0607",
"!+	c #CA5959",
"~+	c #D4A1A1",
"{+	c #C84F4F",
"]+	c #C43333",
"^+	c #C32E2E",
"/+	c #CA5B5B",
"(+	c #D07D7D",
"_+	c #C00B0B",
":+	c #D39595",
"<+	c #D8C6C6",
"[+	c #C22222",
"}+	c #D8BFBF",
"|+	c #BF0405",
"1+	c #DEBEBE",
"2+	c #C11919",
"3+	c #CF7777",
"4+	c #BF0304",
"5+	c #D5A9A9",
"6+	c #D5A4A4",
"7+	c #C32727",
"8+	c #EBE3E3",
"9+	c #C31E1E",
"0+	c #C84949",
"a+	c #C00A0A",
"b+	c #D07E7E",
"c+	c #D08484",
"d+	c #DABCBC",
"e+	c #CE7878",
"f+	c #CD7171",
"g+	c #CB6565",
"h+	c #BF1111",
"i+	c #D5A3A3",
"j+	c #CC6969",
"k+	c #D8C2C2",
"l+	c #D29090",
"m+	c #C84545",
"n+	c #C84848",
"                                                                                                                                                                                                          ",
"                                                                                                                                                                                          . + @ # $ % &   ",
"                                                                                                                                                                                  * = @ # # - ; >     > , ",
"  . . ' + ' . . . >                                                                                                                                                       > ' & ) # # $ !                 ",
"      ~ ; , { # # # # @ & ' >                                                                                                                                       . ] ^ # # # $ ! >               ' ; * ",
"                ~ , % # # # # ) & /                                                                                                                           ' & ) # # # % , >                 ' ( >     ",
"                      * , _ # # # # : + >   < [ } | 1 2 3 4 5 6                                                                                         ' 7 # # # # _ ( ~                   8 { ~         ",
"                            9 % # # # # # 0 a b c d e 1 f g h a i j                                                                               ' ^ # # # # # { ;                     * @ (             ",
"                                ! _ # # # k             l m n o p q r                                                                       ' 7 # # # # # % 9 >                       & _ 8               ",
"                                    , # # ,                   s t p u v                                                               ~ & # # # # # # - 8                         ' ) $ >                 ",
"                                      > * w                     x a p y z                                                       > + : # # # # # % 9 >                         * @ # ,                     ",
"                                          p A                     B C p D                                                   ~ & # # # # # # { ;                             + # _ ;                       ",
"                                          E F                       G p H z                                             ~ @ # # # # # # ( *                             ~ : # $ *                         ",
"                                          w p A                     I p h J                                         ' ^ # # # # # _ 9 >                               7 # # -                             ",
"                                            K L                     M p p N                                     ~ @ # # # # # _ 9                                 8 ) # # 9                               ",
"                                            L O                     P p p G                                 * @ # # # # # # 9                                 > @ # # _ 8                                 ",
"                                            Q p Q                   R h p q j                           > & # # # # # # ( >                                 = ) # # $ *                                   ",
"                                              p E                   R h p S T                         + ) # # # # # { *                                 * @ # # # -                                       ",
"                                              U V                   R h p p W                     ~ : # # # # # % 8                                   = # # # _ ;                                         ",
"                                              X p Y                 X p p p Z                 > 7 # # # # # # 9                                   > @ # # # (                                             ",
"                                              Y p L                 ` p p p  .              = ) # # # # # { >                                   = ) # # % ~                                               ",
"                                                p ..                +.h p p @.#.        > @ # # # # # _ ;                                   > 7 # # # $                                                   ",
"                                                U p w               $.%.p p p &.      = ) # # # # # (                                     ~ : # # # (                                                     ",
"                                                X p X                 *.p p p p =.  7 # # # # # % ~                                     = # # # # !                                                       ",
"                                                Y p -.                ;.>.p p p ,.'.# # # # # ,                                       & # # # _ ;                                                         ",
"                                                  p p A                 ).p p !.~.# # # # $ ~                                     * ^ # # # % *                                                           ",
"                                                  f p {.                  ].^.# # # # # 9                                       ~ ) # # # -                                                               ",
"                                                  L h F                   /.(.# # # _.*                                       ; # # # # ;                                                                 ",
"                                                  Q :.p                   @ # # # <.                                        ] # # # # ;                                                                   ",
"                                                    p [.{.              * # # }.|.                                        & # # # _ ~                                                                     ",
"                                                    f 1.F               9 # # *                                         ^ # # # _ *                                                                       ",
"                                                    L 2.3.              9 # 9                                         ^ # # # _ *                                                                         ",
"                                                    Q 4.4.Q             * $ ; + 5.6.                                ^ # # # $ >                                                                           ",
"                                                      p 7.E                 > ( # # 8.9.                          ^ # # # {                                                                               ",
"                                                      V 7.0.                    > a.# # '.*                     ^ # # # (                                                                                 ",
"                                                      0.7.0.                      b.c.# # d.~                 ^ # # # ,                                                                                   ",
"                                                      p e.0.                        f.g.~.# # h.            ^ # # # (                                                                                     ",
"                                                      p i.j.                        k.S g.# # # ;         & # # # $                                                                                       ",
"                                                      p l.p                           m.p n.# # # *     ! # # # $                                                                                         ",
"                                                      0.o.V Q                         {.p p n.# # p.* * # # # _ *                                                                                         ",
"                                                      L q.e.r.                        j 0.p p s.# # d.^ # # # *                                                                                           ",
"                                                      w t.l.t.Y                         D h p p u.# # # # # ;                                                                                             ",
"                                                        U e.e.v.                        ` w.p p x.y.# # # (                                                                                               ",
"                                                        Y t.z.A.B.                        b p p p x.C.D.E.                                                                                                ",
"                                                          F.G.z.H.{.                      ` u p p p p h I.                                                                                                ",
"                                                          A J.i.l.K.Y                       L.p p p p p -.A                                                                                               ",
"                                                            {.:.z.e.V w                     M.u p p p p p N.                                                                                              ",
"                                                              E O.z.e.V w                     P.h p p p p Q.                                                                                              ",
"                                                                R.q.z.e.V w                   s S.p p p p T.m                                                                                             ",
"                                                                  g e.z.e.V w                   U.p p p p p V.                                                                                            ",
"                                                                  w g o.z.e.V Y                 W.X.p p p p Y.Z.                                                                                          ",
"                                                                    Y t.l.z.e.p w                 D p p p p p `.                                                                                          ",
"                                                                      {.t.l.z.e.V w               #.Y.p p p p ].                                                                                          ",
"                                                                        {.t.l.z.e.V w                +p p p p w..+                                                                                        ",
"                                                                          {.t.i.z.e.V w             $.++p p p h @+                                                                                        ",
"                                                                            {.J.e.z.e.V w             #+p p p p o $+                                                                                      ",
"                                                                              w g o.z.e.V w             m.p p p p %+                                                                                      ",
"                                                                                w f &+z.e.:.{.          *+Y.p p p =+r                                                                                     ",
"                                                                                    R.A.z.l.t.{.          -+p p p p ;+                                                                                    ",
"                                                                                      E :.l.l.t.P           m.p p p X.5                                                                                   ",
"                                                                                        `.t.e.l.[.B.        *+>+p p p ].                                                                                  ",
"                                                                                          Y g q.z.[.,+        '+w.p p p *.                                                                                ",
"                                                                                              R.[.l.)+-.A       !+p p p o ~+                                                                              ",
"                                                                                                f.t.o.7.V w       {+p p p ]+                                                                              ",
"                                                                                                  Q g q.e.p {.      ^+p p h /+                                                                            ",
"                                                                                                    A R.[.o.t.(+      U p p _+:+                                                                          ",
"                                                                                                        f.t.7.[.B.    <+]+p p [+<                                                                         ",
"                                                                                                          Q g q.[.B.    }+q p p m.                                                                        ",
"                                                                                                            A R.)+|+-.    1+2+p p 3+                                                                      ",
"                                                                                                                E [.4+-.    5+H p K 5                                                                     ",
"                                                                                                                  `.t.p B.    6+>+p 7+8+                                                                  ",
"                                                                                                                    {.p p Q     M.9+p 0+                                                                  ",
"                                                                                                                      E p a+      B K T.b+                                                                ",
"                                                                                                                        R.p B.      c+u H d+                                                              ",
"                                                                                                                        A g p Q       e+w.b                                                               ",
"                                                                                                                          Q p V         f+u g+                                                            ",
"                                                                                                                            X p ,+        L h+i+                                                          ",
"                                                                                                                              E p B.        U.^+                                                          ",
"                                                                                                                                2 p {.        %.j+                                                        ",
"                                                                                                                                  E p {.      k+7+x                                                       ",
"                                                                                                                                    E p /+      l+m+                                                      ",
"                                                                                                                                      `.V r.Y     ;+d+                                                    ",
"                                                                                                                                        A n+p 7+w v #.                                                    ",
"                                                                                                                                              {.A                                                         "};
    """

    MenuText = "Dynamics"
    ToolTip = "Dynamics workbench"

    def Initialize(self) :
        "This function is executed when FreeCAD starts"
        from PySide import QtCore#, QtGui

        import MBdynGui
    
        toolslist = ['MBdyn_Cm','MBdyn_Cm1',"MBdyn_RecalculateOrientation","MBdyn_RandomColor"]         
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Tools", "Tools")), toolslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Tools", "Tools")), toolslist)        
        
        bodieslist = ["MBdyn_AddRigidBody","MBdyn_AddDummyBody"]         
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Bodies", "Bodies")), bodieslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Bodies", "Bodies")), bodieslist)                
        
        nodeslist = ["MBdyn_AddStructuralDynamicNodeCmd","MBdyn_AddDummyNode","MBdyn_AddStructuralStatic"]         
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Nodes", "Nodes")), nodeslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Nodes", "Nodes")), nodeslist)        
            
        jointslist = ["MBdyn_AddRevolutepin","MBdyn_AddRevolutehinge",
        "MBdyn_AddClamp",'MBdyn_AxialRotation',"MBdyn_AddInLine","MBdyn_AddPrismatic","MBdyn_AddDrivehinge","MBdyn_DeformableDisplacement",
        "MBdyn_AddSphericalHinge","MBdyn_AddInPlane"]         
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Joints", "Joints")), jointslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Joints", "Joints")), jointslist)
        
        simulationlist = ["MBdyn_AddMBD","MBdyn_Run","MBdyn_Animate1",'AnimateStopCmd',"MBdyn_Restore"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Simulation", "Simulation")), simulationlist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Simulation", "Simulation")), simulationlist)       
       
        forceslist = ["MBdyn_AddGravity","MBdyn_AddStructuralForce"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Forces", "Forces")), forceslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Forces", "Forces")), forceslist)       
       
        worldlist = ["MBdyn_AddXYZ"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("World", "World")), worldlist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("World", "World")), worldlist)
        
        postprocesslist = ["MBdyn_Plot","MBdyn_Spreadsheet","MBdyn_Info"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("Post-process data", "Post process data")), postprocesslist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Post-process data", "Post process data")), postprocesslist)        

        loadexampleslist = ['MBdyn_LoadExampleFreeFallingBody1','MBdyn_LoadExampleTennisRacketStable','MBdyn_LoadExampleTennisRacketUnStable',
                            'MBdyn_LoadExampleSimplePendulum1','MBdyn_LoadExampleDoublePendulum1','MBdyn_LoadExampleSlidingPendulum1','MBdyn_LoadExampleServomotor1',
                            'MBdyn_LoadExampleSlidingBody1','MBdyn_LoadExampleMotorBalance1','MBdyn_LoadExampleGyroscopicPrecession1','MBdyn_LoadExampleCrankSlider1',
                            'MBdyn_LoadExampleMassSpringDamper1','MBdyn_LoadExampleVibrationDamping1','MBdyn_LoadExampleJansensLinkage1','MBdyn_LoadExampleRobotGripper1']
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Test cases", "Test cases")), loadexampleslist)          

        loadexampleslist1 = ['MBdyn_LoadExampleFreeFallingBody2','MBdyn_LoadExampleTennisRacketCAD','MBdyn_LoadExampleSimplePendulum2',
                             'MBdyn_LoadExampleDoublePendulum2','MBdyn_LoadExampleSlidingPendulum2','MBdyn_LoadExampleServomotor2',
                             'MBdyn_LoadExampleSlidingBody2','MBdyn_LoadExampleMotorBalance2','MBdyn_LoadExampleGyroscopicPrecession2','MBdyn_LoadExampleCrankSlider2',
                             'MBdyn_LoadExampleMassSpringDamper2','MBdyn_LoadExampleVibrationDamping2','MBdyn_LoadExampleJansensLinkage2','MBdyn_LoadExampleRobotGripper2']
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Test cases-CAD", "Test cases-CAD")), loadexampleslist1)  

        #Log ('Loading Dynamics module... done\n')

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# The workbench is added:
Gui.addWorkbench(MBdynWorkbench())
