import sys
import mysql.connector as mc
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi


class HalloPython(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('FormMahasiswa.ui', self)
        self.setWindowTitle('PYTHON GUI TABLEWIDGET')
        self.sqlLoad()

        # Button connections
        self.pushButton_2.clicked.connect(self.hapus)         
        self.pushButton_4.clicked.connect(self.sqlLoad)  
        self.pushButton.clicked.connect(self.insertkategori)  
        self.pushButton_3.clicked.connect(self.updatekategori)  
        self.pushButton_2.clicked.connect(self.deleteKategori)  
        self.pushButton_5.clicked.connect(self.batal)  
        self.tableWidget.cellClicked.connect(self.isiFormDariTabel)            # Clear tabel tampilan

        # Saat user klik pada cell table, form terisi
        self.tableWidget.cellClicked.connect(self.isiFormDariTabel)

    def hapus(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.label.setText("Tabel dibersihkan (hanya tampilan)")

    def sqlLoad(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_mahasiswa"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM mhs ORDER BY npm ASC")
            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setHorizontalHeaderLabels(
                ['NPM', 'Nama Lengkap', 'Panggilan', 'No HP', 'Email', 'Kelas', 'Matkul', 'Lokasi Kampus']
            )

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.tableWidget.resizeColumnsToContents()
            self.label.setText("Data berhasil ditampilkan")
        except Exception as e:
            self.label.setText(f"Gagal tampilkan data: {e}")
            print("Error sqlLoad():", e)

    def insertkategori(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_mahasiswa"
            )
            cursor = mydb.cursor()
            npm = self.lineEdit_5.text().strip()
            nama_lengkap = self.lineEdit_12.text()
            nama_panggilan = self.lineEdit_11.text()
            no_hp = self.lineEdit_4.text()
            email = self.lineEdit_7.text()
            kelas = self.lineEdit_6.text()
            matkul = self.lineEdit_9.text()
            lokasi_kampus = self.lineEdit_8.text()

            if not npm:
                self.label.setText("NPM tidak boleh kosong")
                return

            cursor.execute("SELECT npm FROM mhs WHERE npm = %s", (npm,))
            if cursor.fetchone():
                self.label.setText("NPM sudah terdaftar")
                return

            sql = "INSERT INTO mhs (npm, nama_lengkap, nama_panggilan, no_hp, email, kelas, matkul, lokasi_kampus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (npm, nama_lengkap, nama_panggilan, no_hp, email, kelas, matkul, lokasi_kampus)
            cursor.execute(sql, val)
            mydb.commit()

            self.label.setText("Data berhasil disimpan")
            self.batal()
            self.sqlLoad()
        except Exception as e:
            self.label.setText(f"Gagal simpan data: {e}")
            print("Error insertkategori():", e)

    def updatekategori(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_mahasiswa"
            )
            cursor = mydb.cursor()
            npm = self.lineEdit_5.text().strip()
            nama_lengkap = self.lineEdit_12.text()
            nama_panggilan = self.lineEdit_11.text()
            no_hp = self.lineEdit_4.text()
            email = self.lineEdit_7.text()
            kelas = self.lineEdit_6.text()
            matkul = self.lineEdit_9.text()
            lokasi_kampus = self.lineEdit_8.text()

            if not npm:
                self.label.setText("NPM harus diisi untuk update")
                return

            sql = """UPDATE mhs 
                     SET nama_lengkap = %s, nama_panggilan = %s, no_hp = %s, email = %s, kelas = %s, matkul = %s, lokasi_kampus = %s 
                     WHERE npm = %s"""
            val = (nama_lengkap, nama_panggilan, no_hp, email, kelas, matkul, lokasi_kampus, npm)
            cursor.execute(sql, val)
            mydb.commit()

            self.label.setText("Data berhasil diupdate")
            self.batal()
            self.sqlLoad()
        except Exception as e:
            self.label.setText(f"Gagal update data: {e}")
            print("Error updatekategori():", e)

    def deleteKategori(self):
        try:
            npm = self.lineEdit_5.text().strip()
            if not npm:
                self.label.setText("NPM harus diisi untuk menghapus")
                return

            print(f"Menghapus NPM: {npm}")  # Log debug

            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_mahasiswa"
            )
            cursor = mydb.cursor()
            sql = "DELETE FROM mhs WHERE npm = %s"
            cursor.execute(sql, (npm,))
            mydb.commit()

            self.label.setText("Data berhasil dihapus")
            self.batal()
            self.sqlLoad()
        except Exception as e:
            self.label.setText(f"Gagal hapus data: {e}")
            print("Error deleteKategori():", e)

    def isiFormDariTabel(self, row, column):
        try:
            self.lineEdit_5.setText(self.tableWidget.item(row, 0).text())
            self.lineEdit_12.setText(self.tableWidget.item(row, 1).text())
            self.lineEdit_11.setText(self.tableWidget.item(row, 2).text())
            self.lineEdit_4.setText(self.tableWidget.item(row, 3).text())
            self.lineEdit_7.setText(self.tableWidget.item(row, 4).text())
            self.lineEdit_6.setText(self.tableWidget.item(row, 5).text())
            self.lineEdit_9.setText(self.tableWidget.item(row, 6).text())
            self.lineEdit_8.setText(self.tableWidget.item(row, 7).text())
        except Exception as e:
            self.label.setText(f"Error isi form: {e}")
            print("Error isiFormDariTabel():", e)

    def batal(self):
        self.lineEdit_5.clear()
        self.lineEdit_12.clear()
        self.lineEdit_11.clear()
        self.lineEdit_4.clear()
        self.lineEdit_7.clear()
        self.lineEdit_6.clear()
        self.lineEdit_9.clear()
        self.lineEdit_8.clear()
        self.label.setText("Form dibersihkan")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = HalloPython()
    form.show()
    sys.exit(app.exec_())
