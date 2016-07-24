# FreeCAD Polar Tools module  
# (c) 2016 Riccardo Treu LGPL

# import FreeCAD modules
import FreeCAD, FreeCADGui,inspect

# helper -------------------------------------------------------------------
# FreeCAD TemplatePyMod module  
# (c) 2007 Juergen Riegel LGPL

def addCommand(name,cmdObject):
	(list,num) = inspect.getsourcelines(cmdObject.Activated)
	pos = 0
	# check for indentation
	while(list[1][pos] == ' ' or list[1][pos] == '\t'):
		pos += 1
	source = ""
	for i in range(len(list)-1):
		source += list[i+1][pos:]
	FreeCADGui.addCommand(name,cmdObject,source)

#---------------------------------------------------------------------------
# The command classes
#---------------------------------------------------------------------------

class drawPolygon:
  def Activated(self):
    import polarUtilsCmd as puc
    import FreeCAD, FreeCADGui
    from PySide import QtGui as qg
    if (FreeCADGui.Selection.countObjectsOfType('Sketcher::SketchObject')==0):
      qg.QMessageBox().information(None,'Incorrect input','First select at least one sketch.')
    else:
      n=int(qg.QInputDialog.getText(None,"draw a Polygon","Number of sides?")[0])
      R=float(qg.QInputDialog.getText(None,"draw a Polygon","Radius of circumscribed circle?")[0])
      for sk in FreeCADGui.Selection.getSelection():
        if sk.TypeId=="Sketcher::SketchObject":
          puc.disegna(sk,puc.cerchio(R,n))
    
  def GetResources(self):
    return{'Pixmap':str(FreeCAD.getResourceDir() + "Mod/FlamingoTools/poligono.svg"),'MenuText':'Make-a-polygon','ToolTip':'Draws n-polygon in a circle'}

class drawFromFile():
  def Activated(self):
    import polarUtilsCmd as puc
    import FreeCAD
    doc=FreeCAD.activeDocument()
    sketch=doc.addObject("Sketcher::SketchObject","imported")
    sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
    puc.disegna(sketch,puc.getFromFile())
    
  def GetResources(self):
    return{'Pixmap':str(FreeCAD.getResourceDir() + "Mod/FlamingoTools/daFile.svg"),'MenuText':'Polygon from file','ToolTip':'The file .csv must be ";" separated: column A = radius, column B = angle'}

#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
addCommand('drawPolygon',drawPolygon()) 
addCommand('drawFromFile',drawFromFile())