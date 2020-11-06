import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QColorDialog, QLabel

lx = 0
ly = 0
color = (0, 0, 0)

eraser = False

thickness = 5


class BrushPoint:
    def __init__(self, x, y):
        global lx
        global ly
        global color
        self.x = x
        self.y = y
        self.color = color

        lx = self.x
        ly = self.y

        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

    def draw(self, painter):
        if not eraser:
            painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
            painter.setPen(QColor(self.r, self.g, self.b))
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.setPen(QColor(255, 255, 255))
            # painter.drawEllipse(self.x - 5, self.y - 5, 5, 5)


class Line:
    def __init__(self, sx, sy, ex, ey):
        global color
        global thickness
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        if not eraser:
            self.pen = QPen(QColor(color[0], color[1], color[2]))

        else:
            self.pen = QPen(QColor(212, 208, 200))

        self.pen.setWidth(thickness)

    def draw(self, painter):
        if not eraser:
            painter.setBrush(QBrush(QColor(color[0], color[1], color[2])))
            painter.setPen(self.pen)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        else:
            painter.setBrush(QBrush(QColor(212, 208, 200)))
            painter.setPen(self.pen)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Circle:
    def __init__(self, cx, cy, x, y):
        global color
        global thickness
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.pen = QPen(QColor(color[0], color[1], color[2]))

        self.pen.setWidth(thickness)

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(self.pen)
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, 2 * radius, 2 * radius)


class Triangle:
    def __init__(self):
        pass


class Rectangle:
    pass


class Canvas(QWidget):
    def __init__(self):
        super(Canvas, self).__init__()

        self.objects = []
        self.instrument = 'brush'

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.instrument == 'brush':
                self.objects.append(BrushPoint(event.x(), event.y()))
                self.update()
            elif self.instrument == 'line':
                self.objects.append(Line(event.x(), event.y(), event.x(), event.y()))
                self.update()
            elif self.instrument == 'circle':
                self.objects.append(Circle(event.x(), event.y(), event.x(), event.y()))
                self.update()

            elif self.instrument == 'eraser':
                if self.instrument == 'brush':
                    self.objects.append(BrushPoint(event.x(), event.y()))
                    self.update()

    def mouseMoveEvent(self, event):
        global lx
        global ly
        if event.buttons() and Qt.LeftButton:
            if self.instrument == 'brush':
                self.objects.append(Line(lx, ly, event.x(), event.y()))
                self.objects.append(BrushPoint(event.x(), event.y()))
                self.update()

            elif self.instrument == 'line':
                self.objects[-1].ex = event.x()
                self.objects[-1].ey = event.y()
                self.update()

            elif self.instrument == 'circle':
                self.objects[-1].x = event.x()
                self.objects[-1].y = event.y()
                self.update()

    def setBrush(self):
        global eraser
        self.instrument = 'brush'
        eraser = False

    def setLine(self):
        global eraser
        eraser = False
        self.instrument = 'line'

    def setCircle(self):
        global eraser
        self.instrument = 'circle'
        eraser = False

    def setEraser(self):
        global eraser
        eraser = True
        self.instrument = 'brush'

    def color(self):
        global color
        col = QColorDialog.getColor()
        if col.isValid():
            color = col.red(), col.green(), col.blue()

    def triangle(self):
        self.instrument = 'triangle'

    def thin(self):
        global thickness
        thickness = 1

    def not_thin(self):
        global thickness
        thickness = 2.5

    def average(self):
        global thickness
        thickness = 5

    def thick(self):
        global thickness
        thickness = 10

    def very_thick(self):
        global thickness
        thickness = 20


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('paint.ui', self)

        # self.pixmap = QPixmap('white.png')
        # self.image = QLabel(self)

        self.setCentralWidget(Canvas())
        self.brush.triggered.connect(self.centralWidget().setBrush)
        self.line.triggered.connect(self.centralWidget().setLine)
        self.circle.triggered.connect(self.centralWidget().setCircle)
        self.triangle.triggered.connect(self.centralWidget().triangle)
        self.lastik.triggered.connect(self.centralWidget().setEraser)
        self.color.triggered.connect(self.centralWidget().color)
        self.rectangle.triggered.connect(self.centralWidget().rectangle)

        self.thin.triggered.connect(self.centralWidget().thin)
        self.not_thin.triggered.connect(self.centralWidget().not_thin)
        self.average.triggered.connect(self.centralWidget().average)
        self.thick.triggered.connect(self.centralWidget().thick)
        self.very_thick.triggered.connect(self.centralWidget().very_thick)

        self.save.triggered.connect(self.save_)

    def save_(self):
        self.centralWidget().grab().save('img.jpg')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    prog = Program()
    prog.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
