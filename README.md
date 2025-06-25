# Aplikasi Menggambar 2D dengan Transformasi & Clipping

Aplikasi menggambar sederhana berbasis Python menggunakan Tkinter. Memungkinkan pengguna untuk menggambar berbagai bentuk 2D, memilih warna dan ukuran kuas, serta melakukan transformasi dasar seperti translasi, rotasi, dan skala. Aplikasi ini juga dilengkapi dengan fitur clipping menggunakan algoritma Cohen-Sutherland.

## Fitur Utama

* **Alat Menggambar:** Garis, Lingkaran, Persegi, Poligon.
* **Pengaturan Kuas:** Pemilihan warna dan ukuran kuas.
* **Transformasi:**
    * Translasi (pergeseran)
    * Rotasi
    * Skala (pembesaran/pengecilan)
* **Clipping (Pemotongan):** Menggunakan algoritma Cohen-Sutherland untuk memotong objek di luar area jendela yang ditentukan.
* **Interaktif:** Pemilihan objek untuk transformasi.
* **Antarmuka Pengguna:** Berbasis GUI (Graphical User Interface) menggunakan Tkinter.

## Persyaratan

* Python 3.x
* Tkinter (biasanya sudah termasuk dalam instalasi Python standar)

## Cara Menjalankan

1.  Pastikan Anda memiliki Python 3.x terinstal.
2.  Simpan kode `aplikasi_menggambar.py` ke komputer Anda.
3.  Buka terminal atau command prompt.
4.  Navigasi ke direktori tempat Anda menyimpan file.
5.  Jalankan aplikasi dengan perintah:
    ```bash
    python aplikasi_menggambar.py
    ```

## Penggunaan

Setelah aplikasi berjalan:

1.  **Pilih Alat:** Klik tombol alat (Garis, Lingkaran, dll.) di bagian atas.
2.  **Gambar:** Klik dan seret di kanvas untuk menggambar.
3.  **Pilih Warna/Ukuran:** Gunakan tombol "Pilih Warna" atau slider "Ukuran Kuas".
4.  **Transformasi:**
    * Pilih objek dengan alat "Pilih Objek".
    * Pilih mode transformasi (Translasi, Rotasi, Skala).
    * Atur nilai transformasi yang diinginkan dan klik "Terapkan".
5.  **Clipping:**
    * Pilih mode "Windowing".
    * Definisikan area clipping di kanvas.
    * Gambar objek, atau terapkan clipping pada objek yang sudah ada.

## Kontributor

[Nama Anda/Nama Kontributor lain jika ada]
