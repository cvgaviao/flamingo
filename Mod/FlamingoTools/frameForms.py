import FreeCAD,FreeCADGui
import frameCmd
from PySide.QtCore import *
from PySide.QtGui import *

class prototypeForm(QWidget):
  'prototype dialog for frame tools workbench'
  def __init__(self,winTitle='Title',btn1Text='Button1',btn2Text='Button2',initVal='someVal',units='someUnit'):
    super(prototypeForm,self).__init__()
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.setWindowTitle(winTitle)
    self.mainVL=QVBoxLayout()
    self.setLayout(self.mainVL)
    self.inputs=QWidget()
    self.inputs.setLayout(QFormLayout())
    self.edit1=QLineEdit(initVal)
    self.edit1.setMinimumWidth(40)
    self.edit1.setAlignment(Qt.AlignHCenter)
    self.edit1.setMaximumWidth(60)
    self.inputs.layout().addRow(units,self.edit1)
    self.mainVL.addWidget(self.inputs)
    self.radio1=QRadioButton()
    self.radio1.setChecked(True)
    self.radio2=QRadioButton()
    self.radios=QWidget()
    self.radios.setLayout(QFormLayout())
    self.radios.layout().setAlignment(Qt.AlignJustify)
    self.radios.layout().addRow('move',self.radio1)
    self.radios.layout().addRow('copy',self.radio2)
    self.mainVL.addWidget(self.radios)
    self.btn1=QPushButton(btn1Text)
    self.btn1.setDefault(True)
    self.btn2=QPushButton(btn2Text)
    self.buttons=QWidget()
    self.buttons.setLayout(QHBoxLayout())
    self.buttons.layout().addWidget(self.btn1)
    self.buttons.layout().addWidget(self.btn2)
    self.mainVL.addWidget(self.buttons)

class pivotForm(prototypeForm):
  'dialog for pivotTheBeam()'
  def __init__(self):
    super(pivotForm,self).__init__('pivotForm','Rotate','Reverse','90','Angle - deg:')
    self.btn1.clicked.connect(self.rotate)
    self.btn2.clicked.connect(self.reverse)
    self.show()
  def rotate(self):
    FreeCAD.activeDocument().openTransaction('Rotate')
    if self.radio2.isChecked():
      FreeCAD.activeDocument().copyObject(FreeCADGui.Selection.getSelection()[0],True)
      frameCmd.pivotTheBeam(float(self.edit1.text()),ask4revert=False)
    else:
      frameCmd.pivotTheBeam(float(self.edit1.text()),ask4revert=False)
    FreeCAD.activeDocument().commitTransaction()
  def reverse(self):
    FreeCAD.activeDocument().openTransaction('Reverse rotate')
    frameCmd.pivotTheBeam(-2*float(self.edit1.text()),ask4revert=False)
    self.edit1.setText(str(-1*float(self.edit1.text())))
    FreeCAD.activeDocument().commitTransaction()

class shiftForm(prototypeForm):  # OBSOLETE: replaced by translateForm
  'dialog for shiftTheBeam()' 
  def __init__(self):
    super(shiftForm,self).__init__('shiftForm','Shift','Reverse','500','Distance  - mm:')
    self.btn1.clicked.connect(self.shift)
    self.btn2.clicked.connect(self.reverse)
    self.btn3=QPushButton('Get Distance')
    self.btn3.clicked.connect(self.getDist)
    self.buttons.layout().addWidget(self.btn3)
    self.btn1.setFocus()
    self.show()
  def shift(self):    
    edge=frameCmd.edges()[0]
    beam=frameCmd.beams()[0]
    FreeCAD.activeDocument().openTransaction('Shift')
    if self.radio2.isChecked():
      FreeCAD.activeDocument().copyObject(FreeCADGui.Selection.getSelection()[0],True)
      frameCmd.shiftTheBeam(beam,edge,float(self.edit1.text()),ask4revert=False)
    else:
      frameCmd.shiftTheBeam(beam,edge,float(self.edit1.text()),ask4revert=False)
    FreeCAD.activeDocument().commitTransaction()
  def reverse(self):
    FreeCAD.activeDocument().openTransaction('Reverse shift')
    edge=frameCmd.edges()[0]
    beam=frameCmd.beams()[0]
    frameCmd.shiftTheBeam(beam,edge,-2*float(self.edit1.text()),ask4revert=False)
    self.edit1.setText(str(-1*float(self.edit1.text())))
    FreeCAD.activeDocument().commitTransaction()
  def getDist(self):
    L=frameCmd.getDistance()
    if L!=None:
      self.edit1.setText(str(L))
    
class fillForm(prototypeForm):
  'dialog for fillFrame()'
  def __init__(self):
    super(fillForm,self).__init__('fillForm','Select','Fill','<select a beam>','')
    self.beam=None
    self.edit1.setMinimumWidth(150)
    self.btn1.clicked.connect(self.select)
    self.btn2.clicked.connect(self.fill)
    self.radio2.setChecked(True)
    self.btn1.setFocus()
    self.show()
  def fill(self):
    if self.beam!=None and len(frameCmd.edges())>0:
      FreeCAD.activeDocument().openTransaction('Fill frame')
      if self.radio1.isChecked():
        frameCmd.placeTheBeam(self.beam,frameCmd.edges()[0])
      else:
        for edge in frameCmd.edges():
          struct=FreeCAD.activeDocument().copyObject(self.beam,True)
          frameCmd.placeTheBeam(struct,edge)
        FreeCAD.activeDocument().recompute()
      FreeCAD.activeDocument().commitTransaction()
  def select(self):
    if frameCmd.beams()>0:
      self.beam=frameCmd.beams()[0]
      self.edit1.setText(self.beam.Label+':'+self.beam.Profile)
      self.btn2.setFocus()    

class extendForm(prototypeForm):
  'dialog for frameCmd.extendTheBeam()'
  def __init__(self):
    super(extendForm,self).__init__('extendForm','Target','Extend','<select a target shape>','')
    self.target=None
    self.edit1.setMinimumWidth(150)
    self.btn1.clicked.connect(self.getTarget)
    self.btn1.setFocus()
    self.btn2.clicked.connect(self.extend)
    self.radios.hide()
    self.show()
  def getTarget(self):
    selex = FreeCADGui.Selection.getSelectionEx()
    if len(selex[0].SubObjects)>0 and hasattr(selex[0].SubObjects[0],'ShapeType'):
      self.target=selex[0].SubObjects[0]
      self.edit1.setText(selex[0].Object.Label+':'+self.target.ShapeType)
  def extend(self):
    if self.target!=None and len(frameCmd.beams())>0:
      FreeCAD.activeDocument().openTransaction('Extend beam')
      for beam in frameCmd.beams():
        frameCmd.extendTheBeam(beam,self.target)
      FreeCAD.activeDocument().commitTransaction()
      
class stretchForm(prototypeForm):
  'dialog for stretchTheBeam()'
  def __init__(self):
    super(stretchForm,self).__init__('stretchForm','Get Length','Stretch','1000','mm')
    self.btn1.clicked.connect(self.getL)
    self.btn2.clicked.connect(self.stretch)
    self.btn1.setFocus()
    self.radios.hide()
    self.show()
  def getL(self):
    L=frameCmd.getDistance()
    if L!=None:
      self.edit1.setText(str(L))
  def stretch(self):
    FreeCAD.activeDocument().openTransaction('Stretch beam')
    for beam in frameCmd.beams():
      frameCmd.stretchTheBeam(beam,float(self.edit1.text()))
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
    
class translateForm(prototypeForm):   #add selection options in getDisp()
  'dialog for moving blocks'
  def __init__(self):
    super(translateForm,self).__init__('translateForm','Displacement','Vector','0','x - mm')
    self.btn1.clicked.connect(self.getDisp)
    self.btn1.setFocus()
    self.btn2.clicked.connect(self.getVect)
    self.edit1.setMaximumWidth(120)
    self.edit2=QLineEdit('0')
    self.edit2.setMinimumWidth(40)
    self.edit2.setAlignment(Qt.AlignHCenter)
    self.edit2.setMaximumWidth(120)
    self.inputs.layout().addRow('y - mm',self.edit2)
    self.edit3=QLineEdit('0')
    self.edit3.setMinimumWidth(40)
    self.edit3.setAlignment(Qt.AlignHCenter)
    self.edit3.setMaximumWidth(120)
    self.inputs.layout().addRow('z - mm',self.edit3)
    self.edit4=QLineEdit('1')
    self.edit4.setMinimumWidth(40)
    self.edit4.setAlignment(Qt.AlignHCenter)
    self.edit4.setMaximumWidth(120)
    self.inputs.layout().addRow('Multiple',self.edit4)
    self.btn3=QPushButton('Translate')
    self.btn3.clicked.connect(self.translateTheBeams)
    self.buttons2=QWidget()
    self.buttons2.setLayout(QHBoxLayout())
    self.buttons2.layout().addWidget(self.btn3)
    self.mainVL.addWidget(self.buttons2)
    self.show()
  def getDisp(self):
    shapes=[y for x in FreeCADGui.Selection.getSelectionEx() for y in x.SubObjects if hasattr(y,'ShapeType')][:2]
    if len(shapes)>1:
      base,target=shapes[:2]
      disp=None
      if base.ShapeType==target.ShapeType=='Vertex':
        disp=target.Point-base.Point
      if base.ShapeType==target.ShapeType=='Edge':
        disp=target.CenterOfMass-base.CenterOfMass
      if base.ShapeType=='Vertex' and target.ShapeType=='Face':
        disp=frameCmd.intersection(base.Point,target.normalAt(0,0),target)-base.Point
      if base.ShapeType=='Face' and target.ShapeType=='Vertex':
        disp=target.Point-frameCmd.intersection(target.Point,base.normalAt(0,0),base)
      if disp!=None:
        dx,dy,dz=list(disp)
        self.edit1.setText(str(round(dx,3)))
        self.edit2.setText(str(round(dy,3)))
        self.edit3.setText(str(round(dz,3)))
        self.edit4.setText('1')
  def getVect(self):
    if len(frameCmd.edges())>0:
      edge=frameCmd.edges()[0]
      dx,dy,dz=list(edge.tangentAt(0))
      self.edit1.setText(str(round(dx,3)))
      self.edit2.setText(str(round(dy,3)))
      self.edit3.setText(str(round(dz,3)))
      self.edit4.setText(str(edge.Length))
  def translateTheBeams(self):
    disp=FreeCAD.Vector(float(self.edit1.text()),float(self.edit2.text()),float(self.edit3.text())).scale(float(self.edit4.text()),float(self.edit4.text()),float(self.edit4.text()))
    FreeCAD.activeDocument().openTransaction('Translate')    
    if self.radio2.isChecked():
      for o in set(FreeCADGui.Selection.getSelection()):
        FreeCAD.activeDocument().copyObject(o,True)
    for o in set(FreeCADGui.Selection.getSelection()):
      o.Placement.move(disp)
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()    

