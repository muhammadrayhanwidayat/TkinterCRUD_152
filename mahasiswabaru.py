import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') # Membuka atau membuat file database SQLite
    cursor = conn.cursor()                   # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()                           # Menyimpan perubahan ke database      
    conn.close()                            # Menutup koneksi database




#bagian CRUD

# Fungsi untuk mengambil semua data dari database  (Read)
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')        # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")     # Mengambil semua data dari tabel
    rows = cursor.fetchall()                        # Menyimpan semua hasil query ke dalam `rows`
    conn.close()
    return rows                                     # Mengembalikan data untuk diproses

# Fungsi untuk menyimpan data baru ke database (Create)
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  
    ''', (nama, biologi, fisika, inggris, prediksi))   #VALUES (?, ?, ?, ?, ?)  adalah Placeholder untuk mencegah SQL Injection
    conn.commit()#disimpan secara permanen
    conn.close()#menutup koneksi ke database setelah operasi selesai.

# Fungsi untuk memperbarui data di database (update)
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Mengupdate data berdasarkan ID
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) # Menghapus berdasarkan ID
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:      # Jika nilai biologi terbesar
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:     # Jika nilai fisika terbesar
        return "Teknik"
    elif inggris > biologi and inggris > fisika:    # Jika nilai inggris terbesar
        return "Bahasa"
    else:                                           # Jika nilai sama
        return "Tidak Diketahui"

# Fungsi untuk menambahkan data baru
def submit():
    try:
        nama = nama_var.get()       # Mengambil input dari form
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:                    # Validasi input
            raise ValueError("Nama siswa tidak boleh kosong.")
            #memeriksa apakah variabel nama kosong. Jika kosong, 
            # #maka program akan melemparkan pengecualian (raise ValueError) 
            # #dengan pesan "Nama siswa tidak boleh kosong."

        prediksi = calculate_prediction(biologi, fisika, inggris)     # Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)    # Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()              # Kosongkan input form
        populate_table()            # Perbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        if not selected_record_id.get():    # Validasi apakah data dipilih, selected_record_id.get() mengambil ID data yang dipilih dari tabel.
            raise Exception("Pilih data dari tabel untuk di-update!")
                #Jika tidak ada data yang dipilih (selected_record_id kosong), 
                #program akan memunculkan pengecualian (raise Exception) 
                #dengan pesan bahwa pengguna harus memilih data terlebih dahulu.

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        #Fungsi memeriksa apakah nama kosong. 
        # Jika nama tidak diisi, program akan melempar 
        # pengecualian ValueError dengan pesan 
        # bahwa nama siswa tidak boleh kosong.


        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()  #mengosongkan semua input di form
        populate_table()#memastikan bahwa data yang telah diperbarui langsung terlihat di tabel.
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus input di form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
    #tree.get_children(): Mengambil semua ID baris yang saat ini ada di tabel Treeview.
    #for row in tree.get_children(): Melakukan iterasi pada setiap baris yang ada.
        tree.delete(row)
        #Menghapus baris tersebut dari tabel Treeview.
    for row in fetch_data():
    #fetch_data(): Fungsi (di luar kode ini) yang mengambil data dari database 
    # dalam bentuk daftar baris. 
    # Setiap baris adalah tuple yang berisi kolom-kolom tabel database.
        tree.insert('', 'end', values=row)
        #'': Mengindikasikan bahwa baris ini akan dimasukkan ke akar (root) Treeview.
        #'end': Menentukan posisi baris akan ditambahkan di akhir tabel.
       #values=row: Nilai yang dimasukkan ke dalam kolom tabel.

# Fungsi untuk mengisi form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
#event adalah parameter yang otomatis diterima oleh fungsi handler. 
# Parameter ini menyimpan informasi tentang event yang dipicu.
    try:
        selected_item = tree.selection()[0]
        #tree.selection(): Mengambil daftar item ID dari baris yang dipilih di tabel Treeview.
        #[0]: Mengambil ID pertama dari daftar. Karena hanya satu baris yang bisa dipilih dalam Treeview ini, kita cukup menggunakan indeks 0.
        #Hasilnya adalah ID unik untuk baris yang dipilih.
        #
        selected_row = tree.item(selected_item)['values']
        #tree.item(selected_item): Mengambil semua informasi dari baris yang dipilih. 
        # ['values']: Mengambil hanya nilai dari kolom tabel dalam bentuk tuple.

        #Mengisi Input Form

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()
########################################################################
# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg="#ADD8E6")  # Warna background biru muda

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

#Fungsi: StringVar adalah jenis variabel khusus yang disediakan oleh Tkinter untuk mengelola data string di komponen GUI.
#Variabel ini menghubungkan antara data yang dimasukkan/diperbarui oleh pengguna di komponen GUI (seperti Entry) dengan kode Python di balik layar.
#Jika nilai dalam StringVar berubah, komponen GUI yang terhubung dengannya akan diperbarui secara otomatis, dan sebaliknya.

#Komponen GUI

# Membuat form input
Label(root, text="Nama Siswa", bg="#ADD8E6").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

#penjelasan:
#Label(root, text="Nama Siswa", bg="#ADD8E6"): Membuat label dengan teks "Nama Siswa".
#bg="#ADD8E6" memberikan warna latar belakang biru muda.
#grid(row=0, column=0): Meletakkan label di baris ke-0 dan kolom ke-0.

#Entry(root, textvariable=nama_var): Membuat input box untuk menerima input pengguna.
#textvariable=nama_var: Menghubungkan input box dengan variabel nama_var untuk menyimpan data.
#.grid(row=0, column=1): Meletakkan input box di baris ke-0 dan kolom ke-1.
#padx=10, pady=5: Memberikan jarak horizontal (padding x) dan vertikal (padding y) antara elemen-elemen.


Label(root, text="Nilai Biologi", bg="#ADD8E6").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)
#Ditempatkan di baris ke-1, kolom ke-0 (label) dan kolom ke-1 (input box).

Label(root, text="Nilai Fisika", bg="#ADD8E6").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris", bg="#ADD8E6").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
#command=submit: Ketika tombol ditekan, fungsi submit() akan dipanggil.
#.grid(row=4, column=0): Meletakkan tombol di baris ke-4, kolom ke-0.
#pady=10: Menambahkan jarak vertikal antar baris.

Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
#Membuat tombol dengan teks "Update".
#command=update: Ketika tombol ditekan, fungsi update() akan dipanggil.
#.grid(row=4, column=1): Meletakkan tombol di baris ke-4, kolom ke-1.

Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

#Membuat tombol dengan teks "Delete".
#command=delete: Ketika tombol ditekan, fungsi delete() akan dipanggil.
#.grid(row=4, column=2): Meletakkan tombol di baris ke-4, kolom ke-2.



# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

#columns: Berisi nama kolom tabel, yaitu:
#"id": ID siswa (sebagai kunci unik untuk setiap data).
#"nama_siswa": Nama siswa.
#"biologi", "fisika", "inggris": Nilai mata pelajaran.
#"prediksi_fakultas": Hasil prediksi fakultas berdasarkan nilai.

#ttk.Treeview: Widget untuk membuat tabel di GUI.
#columns=columns: Menentukan kolom yang akan ditampilkan dalam tabel.
#show='headings': Menampilkan hanya bagian heading (judul kolom) tanpa kolom default.






# Menyesuaikan tampilan kolom tabel
for col in columns:
#Iterasi Kolom: Setiap kolom dalam tabel (columns) dikustomisasi.
    tree.heading(col, text=col.capitalize())
    #Memberikan judul kolom dengan teks yang disesuaikan (dengan huruf pertama kapital).
    tree.column(col, anchor='center')
    #Menentukan posisi teks dalam kolom menjadi di tengah (center).

#Menempatkan Tabel di GUI
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

#tree.grid(row=5, column=0, columnspan=3): Menempatkan tabel di baris ke-5 dan menyebar ke 3 kolom (kolom 0 sampai 2).
#padx=10, pady=10: Memberikan jarak antara tabel dengan elemen lainnya.


# Event handling untuk memilih data dari tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)
#Event Listener: Memantau klik pengguna pada tabel.
#<ButtonRelease-1>: Merujuk pada event "klik kiri mouse dilepaskan".
#fill_inputs_from_table: Fungsi yang dipanggil saat pengguna memilih data di tabel.


# Memuat data ke tabel
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()














