import sys
import math
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class XRDReaderPlotQ(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("XRD Data Reader and Plotter with Q values")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.load_btn = QPushButton("Load Data")
        self.load_btn.clicked.connect(self.browse_file)

        self.wavelength_label = QLabel("Wavelength (Å):")
        self.wavelength_input = QLineEdit()
        self.wavelength_input.setText("1.5406")  # 默认值为Cu Kα辐射波长

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.wavelength_label)
        input_layout.addWidget(self.wavelength_input)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(input_layout)
        layout.addWidget(self.load_btn)

        self.central_widget.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XRD Data File", "", "Text files (*.txt);;CSV files (*.csv);;All files (*.*)")

        if file_path:
            self.read_xrd_data(file_path)

    def read_xrd_data(self, file_path):
        data = pd.read_csv(file_path, sep='\s+', header=None, names=['Q', 'Intensity'], error_bad_lines=False)
        wavelength = float(self.wavelength_input.text())  # 从输入框获取波长值
        data['2Theta'] = data['Q'].apply(lambda q: self.convert_q_to_2theta(q, wavelength))
        self.plot_data(data)
        self.save_data_as_xy(data)

    def convert_q_to_2theta(self, q, wavelength):
        return 2 * (180 / math.pi) * (math.asin(q * wavelength / (4 * math.pi)))

    def plot_data(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data['2Theta'], data['Intensity'], marker='o', linestyle='-')
        ax.set_xlabel('2Theta')
        ax.set_ylabel('Intensity')
        ax.set_title('XRD Pattern')

        self.canvas.draw()

    def save_data_as_xy(self, data):
        output_file_path, _ = QFileDialog.getSaveFileName(self, "Save Data as XY", "", "XY files (*.xy);;All files (*.*)")

        if output_file_path:
            if not output_file_path.endswith(".xy"):
                output_file_path += ".xy"

            data[['2Theta', 'Intensity']].to_csv(output_file_path, sep='\t', header=None, index=None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    xrd_reader_plot_q = XRDReaderPlotQ()
    xrd_reader_plot_q.show()
    sys.exit(app.exec_())
