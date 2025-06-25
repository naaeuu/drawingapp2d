# --- Impor Library ---
# Mengimpor library tkinter untuk membuat antarmuka pengguna (GUI). 'tk' adalah alias umum.
import tkinter as tk
# Mengimpor modul colorchooser dari tkinter, yang menyediakan dialog untuk memilih warna.
from tkinter import colorchooser
# Mengimpor library math untuk operasi matematika, seperti sinus dan kosinus yang digunakan dalam rotasi.
import math

# --- Definisi Kelas Utama Aplikasi ---
# Mendefinisikan kelas DrawingApp yang akan menampung semua komponen dan logika aplikasi.
class DrawingApp:
    # --- Fungsi Inisialisasi (Konstruktor) ---
    # Fungsi __init__ adalah metode khusus yang dijalankan saat sebuah objek dari kelas ini dibuat.
    # Tujuannya adalah untuk menyiapkan jendela utama dan semua variabel yang dibutuhkan aplikasi.
    # 'self' merujuk pada objek itu sendiri, dan 'root' adalah jendela utama dari tkinter.
    def __init__(self, root):
        # Menyimpan referensi ke jendela utama (root) agar bisa diakses di seluruh kelas.
        self.root = root
        # Mengatur judul jendela aplikasi.
        self.root.title("Aplikasi Menggambar 2D dengan Transformasi & Clipping")
        # Mengatur ukuran awal jendela (lebar x tinggi).
        self.root.geometry("900x600")
        # Mengizinkan jendela untuk diubah ukurannya baik secara horizontal maupun vertikal.
        self.root.resizable(True, True)
        # Mengatur konfigurasi dasar jendela: warna latar belakang, lebar border, dan gaya border.
        self.root.config(bg="#C0C0C0", bd=2, relief=tk.RAISED)

        # --- Inisialisasi Variabel Aplikasi ---
        # Variabel untuk menyimpan alat yang sedang aktif (misalnya 'Pencil', 'Line', dll.).
        self.current_tool = 'Pencil'
        # Variabel untuk menyimpan warna gambar yang sedang dipilih.
        self.draw_color = 'black'
        # Variabel untuk warna latar belakang kanvas.
        self.bg_color = 'white'
        # Variabel untuk menyimpan ukuran kuas (ketebalan garis).
        self.brush_size = 5
        # Variabel boolean (True/False) untuk menentukan apakah bentuk akan diisi warna atau tidak.
        self.fill_shape = False

        # --- Inisialisasi Variabel Transformasi ---
        # Variabel untuk menyimpan objek yang sedang dipilih untuk transformasi.
        self.selected_object = None
        # Variabel untuk menyimpan mode transformasi yang aktif (misalnya 'Translate', 'Rotate').
        self.transform_mode = None
        # Variabel untuk menyimpan posisi awal mouse saat memulai transformasi.
        self.transform_start_mouse_pos = None
        # Variabel untuk menyimpan ID dari kotak seleksi yang ditampilkan di sekitar objek.
        self.selection_box_id = None

        # --- Inisialisasi Variabel Menggambar ---
        # Variabel untuk menyimpan koordinat x awal saat mulai menggambar.
        self.start_x = None
        # Variabel untuk menyimpan koordinat y awal saat mulai menggambar.
        self.start_y = None
        # Variabel boolean untuk menandakan apakah proses menggambar (menahan mouse) sedang berlangsung.
        self.is_drawing = False
        # List (daftar) untuk menyimpan semua data objek yang telah digambar di kanvas.
        self.drawn_objects = []
        # Variabel untuk menyimpan ID dari bentuk pratinjau yang ditampilkan saat menggambar.
        self.current_preview_id = None
        # List untuk menyimpan titik-titik dari garis yang digambar dengan alat 'Pencil'.
        self.active_line_points = []

        # --- Inisialisasi Variabel Windowing & Clipping ---
        # Variabel untuk menyimpan koordinat dari jendela windowing/clipping (xmin, ymin, xmax, ymax).
        self.window_coords = None
        # Variabel boolean untuk menandakan apakah pengguna sedang menggambar area window.
        self.is_drawing_window = False
        # Variabel untuk menyimpan ID dari persegi panjang pratinjau saat menggambar window.
        self.window_rect_id = None

        # --- Palet Warna ---
        # List yang berisi string nama-nama warna standar untuk palet cepat.
        self.colors = [
            "black", "gray", "silver", "maroon", "red", "purple", "fuchsia",
            "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua"
        ]
        
        # Variabel untuk menyimpan warna yang digunakan untuk menyorot objek saat windowing.
        self.window_highlight_color = "red"

        # --- Memanggil Fungsi Pembuat UI dan Status Bar ---
        # Memanggil metode _create_ui untuk membangun semua elemen antarmuka.
        self._create_ui()
        # Memanggil metode _update_status_bar untuk menginisialisasi teks di status bar.
        self._update_status_bar()

    # --- Fungsi untuk Membuat Antarmuka Pengguna (UI) ---
    # Metode ini bertanggung jawab untuk membuat semua widget (tombol, slider, kanvas, dll.)
    # dan menatanya di dalam jendela utama.
    def _create_ui(self):
        # Membuat frame utama yang akan menampung semua widget lain.
        main_frame = tk.Frame(self.root, bg="#C0C0C0", bd=0)
        # Menempatkan frame utama agar mengisi seluruh jendela.
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Membuat frame untuk toolbar di sisi kiri.
        left_toolbar = tk.Frame(main_frame, bg="#C0C0C0", width=150, bd=2, relief=tk.RAISED)
        # Menempatkan toolbar di sisi kiri dan membuatnya mengisi tinggi jendela.
        left_toolbar.pack(side="left", fill="y", padx=(2, 0), pady=2)

        # Membuat label teks untuk bagian "Alat Menggambar".
        tk.Label(left_toolbar, text="Alat Menggambar", bg="#C0C0C0",
                 font=("Segoe UI", 9, "bold")).pack(pady=5)
        # Membuat frame untuk menampung tombol-tombol alat menggambar.
        tools_frame = tk.Frame(left_toolbar, bg="#C0C0C0")
        # Menempatkan frame alat.
        tools_frame.pack()
        # Daftar yang berisi informasi untuk setiap tombol alat (nama internal, ikon, nama tooltip).
        tools = [
            ("Pencil", "✏", "Pensil"), ("Point", "•", "Titik"), ("Line", "╱", "Garis"),
            ("Rectangle", "◼", "Persegi"), ("Ellipse", "⬭", "Elips")
        ]
        # Dictionary untuk menyimpan referensi ke setiap tombol alat.
        self.tool_buttons = {}
        # Looping untuk membuat setiap tombol alat dari daftar 'tools'.
        for tool, icon, name in tools:
            # Membuat sebuah tombol.
            btn = tk.Button(tools_frame, text=icon, font=("Segoe UI", 12), width=3, height=2,
                            bd=2, relief=tk.RAISED, bg="#C0C0C0",
                            # 'command' menentukan fungsi yang akan dipanggil saat tombol diklik.
                            # 'lambda t=tool:' digunakan untuk memastikan nilai 'tool' yang benar dikirim.
                            command=lambda t=tool: self.set_tool(t))
            # Menempatkan tombol di sisi kiri dalam frame-nya.
            btn.pack(side="left", padx=1, pady=1)
            # Menyimpan referensi tombol ke dalam dictionary.
            self.tool_buttons[tool] = btn

        # Membuat label teks untuk bagian "Alat Transformasi".
        tk.Label(left_toolbar, text="Alat Transformasi", bg="#C0C0C0",
                 font=("Segoe UI", 9, "bold")).pack(pady=(10,5))
        # Membuat frame untuk menampung tombol-tombol alat transformasi.
        transform_frame = tk.Frame(left_toolbar, bg="#C0C0C0")
        # Menempatkan frame transformasi.
        transform_frame.pack()
        # Daftar informasi untuk setiap tombol transformasi.
        transforms = [
            ("Select", "☐", "Pilih"), ("Translate", "↔", "Geser"), ("Rotate", "↻", "Putar"),
            ("Scale", "⇲", "Skala"), ("Window", "⧉", "Windowing"), ("Clip", "✂", "Clipping")
        ]
        # Dictionary untuk menyimpan referensi ke setiap tombol transformasi.
        self.transform_buttons = {}
        # Looping untuk membuat setiap tombol transformasi.
        for trans, icon, name in transforms:
            # Membuat sebuah tombol transformasi.
            btn = tk.Button(transform_frame, text=icon, font=("Segoe UI", 12), width=3, height=2,
                            bd=2, relief=tk.RAISED, bg="#C0C0C0",
                            # Menetapkan fungsi 'set_transform_mode' sebagai callback.
                            command=lambda t=trans: self.set_transform_mode(t))
            # Menempatkan tombol.
            btn.pack(side="left", padx=1, pady=1)
            # Menyimpan referensi tombol.
            self.transform_buttons[trans] = btn

        # Membuat label teks untuk bagian "Pengaturan".
        tk.Label(left_toolbar, text="Pengaturan", bg="#C0C0C0",
                 font=("Segoe UI", 9, "bold")).pack(pady=(10,5))

        # Membuat label teks untuk "Ukuran Kuas".
        tk.Label(left_toolbar, text="Ukuran Kuas:", bg="#C0C0C0", font=("Segoe UI", 9)).pack()
        # Membuat widget Scale (slider) untuk mengatur ukuran kuas.
        self.brush_slider = tk.Scale(left_toolbar, from_=1, to=20, orient="horizontal",
                                     bg="#C0C0C0", highlightbackground="#C0C0C0",
                                     troughcolor="#E0E0E0", length=100,
                                     # Menetapkan fungsi _on_brush_size_change untuk dipanggil saat nilai slider berubah.
                                     command=self._on_brush_size_change)
        # Mengatur nilai awal slider sesuai dengan variabel self.brush_size.
        self.brush_slider.set(self.brush_size)
        # Menempatkan slider.
        self.brush_slider.pack(fill="x", padx=5)

        # Membuat variabel khusus tkinter untuk checkbox (menyimpan nilai True/False).
        self.fill_var = tk.BooleanVar(value=self.fill_shape)
        # Membuat widget Checkbutton.
        tk.Checkbutton(left_toolbar, text="Isi Bentuk", variable=self.fill_var,
                       bg="#C0C0C0", font=("Segoe UI", 9), relief=tk.FLAT,
                       # Menetapkan fungsi _on_fill_toggle untuk dipanggil saat status checkbox berubah.
                       command=self._on_fill_toggle).pack(pady=5)

        # Membuat tombol untuk membersihkan seluruh kanvas.
        tk.Button(left_toolbar, text="Bersihkan Kanvas", font=("Segoe UI", 9),
                 bd=2, relief=tk.RAISED, bg="#C0C0C0",
                 command=self.clear_canvas).pack(pady=10)
        
        # Membuat tombol untuk menghapus efek windowing/clipping.
        tk.Button(left_toolbar, text="Hapus Window", font=("Segoe UI", 9),
                 bd=2, relief=tk.RAISED, bg="#C0C0C0",
                 command=self._clear_window).pack(pady=5)

        # Membuat frame kontainer untuk kanvas dengan efek 'sunken' (tenggelam).
        canvas_container = tk.Frame(main_frame, bg="#808080", bd=2, relief=tk.SUNKEN)
        # Menempatkan kontainer kanvas.
        canvas_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        # Membuat widget Canvas, tempat semua gambar akan ditampilkan.
        self.canvas = tk.Canvas(canvas_container, bg=self.bg_color, bd=0, highlightthickness=0)
        # Menempatkan kanvas agar mengisi seluruh area kontainernya.
        self.canvas.pack(fill="both", expand=True)

        # Membuat widget Label yang berfungsi sebagai status bar di bagian bawah.
        self.status_bar = tk.Label(main_frame, text="Siap", bd=1, relief=tk.SUNKEN,
                                     anchor="w", bg="#C0C0C0", fg="black", font=("Segoe UI", 9))
        # Menempatkan status bar di bagian bawah jendela.
        self.status_bar.pack(fill="x", padx=2, pady=(0,2))

        # --- Binding Event Mouse ke Kanvas ---
        # Mengikat event "klik tombol kiri mouse" ke fungsi _on_mouse_down.
        self.canvas.bind("<Button-1>", self._on_mouse_down)
        # Mengikat event "gerakan mouse sambil menahan tombol kiri" ke fungsi _on_mouse_move.
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        # Mengikat event "melepas tombol kiri mouse" ke fungsi _on_mouse_up.
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

        # Mengatur alat default saat aplikasi pertama kali dijalankan.
        self.set_tool("Pencil")

        # Membuat frame untuk palet warna di bawah kanvas.
        color_palette_frame = tk.Frame(main_frame, bg="#C0C0C0")
        # Menempatkan frame palet warna.
        color_palette_frame.pack(fill="x", padx=5, pady=(0, 5))

        # Membuat frame di dalam frame palet warna (untuk penataan grid).
        palette_frame = tk.Frame(color_palette_frame, bg="#C0C0C0")
        # Menempatkan frame.
        palette_frame.pack()
        # Looping untuk membuat tombol untuk setiap warna di daftar self.colors.
        for i, color in enumerate(self.colors):
            # Membuat tombol kecil yang warnanya sesuai dengan daftar.
            btn = tk.Button(palette_frame, bg=color, width=2, height=1, bd=1, relief=tk.RAISED,
                            command=lambda c=color: self.set_draw_color(c))
            # Menempatkan tombol dalam layout grid.
            btn.grid(row=0, column=i, padx=1, pady=1)

    # --- Fungsi untuk Mengatur Alat Gambar ---
    def set_tool(self, tool):
        # Mengatur variabel current_tool dengan alat yang dipilih.
        self.current_tool = tool
        # Menonaktifkan mode transformasi.
        self.transform_mode = None
        # Memastikan mode menggambar window tidak aktif.
        self.is_drawing_window = False 
        # Jika ada pratinjau window, hapus.
        if self.window_rect_id: 
            self.canvas.delete(self.window_rect_id)
            self.window_rect_id = None
        # Mengembalikan semua tombol alat ke gaya 'raised' (tidak ditekan).
        for btn in self.tool_buttons.values(): btn.config(relief="raised")
        # Mengubah gaya tombol yang dipilih menjadi 'sunken' (ditekan).
        self.tool_buttons[tool].config(relief="sunken")
        # Mengembalikan semua tombol transformasi ke gaya 'raised'.
        for btn in self.transform_buttons.values(): btn.config(relief="raised")
        # Memperbarui teks di status bar.
        self._update_status_bar()
        # Membatalkan pilihan objek apa pun.
        self._unselect_object()

    # --- Fungsi untuk Mengatur Mode Transformasi ---
    def set_transform_mode(self, mode):
        # Mengatur variabel transform_mode dengan mode yang dipilih.
        self.transform_mode = mode
        # Menonaktifkan alat gambar.
        self.current_tool = None
        # Memastikan mode menggambar window tidak aktif.
        self.is_drawing_window = False 
        # Jika ada pratinjau window, hapus.
        if self.window_rect_id: 
            self.canvas.delete(self.window_rect_id)
            self.window_rect_id = None
        # Mengembalikan semua tombol alat ke gaya 'raised'.
        for btn in self.tool_buttons.values(): btn.config(relief="raised")
        # Mengembalikan semua tombol transformasi ke gaya 'raised'.
        for btn in self.transform_buttons.values(): btn.config(relief="raised")
        # Mengubah gaya tombol transformasi yang dipilih menjadi 'sunken'.
        self.transform_buttons[mode].config(relief="sunken")
        # Jika mode adalah 'Select', batalkan pilihan objek.
        if mode == "Select": self._unselect_object()
        # Jika mode adalah 'Window' atau 'Clip', batalkan pilihan objek.
        elif mode in ["Window", "Clip"]: self._unselect_object()
        # Memperbarui status bar.
        self._update_status_bar()

    # --- Fungsi Penanganan Event: Mouse Ditekan ---
    # Fungsi ini dieksekusi ketika pengguna menekan tombol kiri mouse di atas kanvas.
    def _on_mouse_down(self, event):
        # Mengambil koordinat x dan y dari event mouse.
        x, y = event.x, event.y
        # Memeriksa apakah sedang dalam mode transformasi.
        if self.transform_mode:
            # Menyimpan posisi awal mouse untuk perhitungan transformasi.
            self.transform_start_mouse_pos = (x, y)
            # Jika modenya 'Select', panggil fungsi untuk memilih objek.
            if self.transform_mode == "Select":
                self._select_object(x, y)
            # Jika modenya 'Window' atau 'Clip', mulai proses menggambar window.
            elif self.transform_mode in ["Window", "Clip"]:
                self.is_drawing_window = True
                self.start_x, self.start_y = x, y
        # Jika tidak dalam mode transformasi (berarti mode menggambar).
        else:
            # Aktifkan flag is_drawing.
            self.is_drawing = True
            # Simpan koordinat awal gambar.
            self.start_x, self.start_y = x, y
            # Jika alatnya 'Pencil', inisialisasi daftar titik.
            if self.current_tool == 'Pencil':
                self.active_line_points = [(x, y)]


            # INI POINT
            elif self.current_tool == 'Point':
                # Tambahkan data objek titik ke dalam daftar drawn_objects.
                self.drawn_objects.append({
                    'type': 'point', 'points': [(x, y)], 'color': self.draw_color,
                    'width': self.brush_size, 'rotation_angle': 0.0,
                    'original_color': self.draw_color 
                })
                # Gambar ulang seluruh kanvas untuk menampilkan titik baru.
                self.redraw_all()

    # --- Fungsi Penanganan Event: Mouse Bergerak (sambil ditekan) ---
    # Fungsi ini dieksekusi ketika mouse bergerak sementara tombol kiri ditahan.
    def _on_mouse_move(self, event):
        # Mengambil koordinat x dan y dari event mouse.
        x, y = event.x, event.y
        # Jika dalam mode transformasi dan ada objek yang dipilih.
        if self.transform_mode and self.transform_start_mouse_pos and self.selected_object:
            # Dapatkan posisi mouse sebelumnya.
            prev_x, prev_y = self.transform_start_mouse_pos
            # Hitung perubahan posisi (delta x, delta y).
            dx, dy = x - prev_x, y - prev_y
            # Panggil fungsi transformasi yang sesuai berdasarkan mode.
            if self.transform_mode == "Translate": self._translate_object(dx, dy)
            elif self.transform_mode == "Rotate": self._rotate_object(x, y)
            elif self.transform_mode == "Scale": self._scale_object(dy)
            # Perbarui posisi mouse untuk gerakan selanjutnya.
            self.transform_start_mouse_pos = (x, y)
            # Gambar ulang kanvas untuk menunjukkan perubahan.
            self.redraw_all()
        # Jika sedang dalam proses menggambar window.
        elif self.is_drawing_window: 
            # Hapus pratinjau window sebelumnya.
            if self.window_rect_id: self.canvas.delete(self.window_rect_id)
            # Tentukan warna garis pratinjau (hijau untuk Clip, biru untuk Window).
            outline_color = "green" if self.transform_mode == "Clip" else "blue"
            # Buat persegi panjang pratinjau baru.
            self.window_rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y, outline=outline_color, dash=(5, 2), width=2
            )
        # Jika sedang dalam mode menggambar biasa.
        elif self.is_drawing:
            # Hapus bentuk pratinjau sebelumnya jika ada.
            if self.current_preview_id:
                self.canvas.delete(self.current_preview_id)
                self.current_preview_id = None
            # Siapkan opsi untuk bentuk pratinjau.
            options = {
                'fill': self.draw_color if self.fill_shape else '',
                'outline': self.draw_color, 'width': self.brush_size
            }
            # Buat pratinjau sesuai dengan alat yang aktif.
            if self.current_tool == 'Pencil':
                # Tambahkan titik baru ke daftar.
                self.active_line_points.append((x, y))
                # Jika sudah ada lebih dari satu titik, gambar garis pratinjau.
                if len(self.active_line_points) > 1:
                    self.current_preview_id = self.canvas.create_line(
                        self.active_line_points, fill=self.draw_color,
                        width=self.brush_size, capstyle=tk.ROUND, joinstyle=tk.ROUND
                    )
            elif self.current_tool == 'Line':
                self.current_preview_id = self.canvas.create_line(self.start_x, self.start_y, x, y, **options)
            elif self.current_tool == 'Rectangle':
                self.current_preview_id = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, **options)
            elif self.current_tool == 'Ellipse':
                self.current_preview_id = self.canvas.create_oval(self.start_x, self.start_y, x, y, **options)

    # --- Fungsi Penanganan Event: Mouse Dilepas ---
    # Fungsi ini dieksekusi ketika pengguna melepas tombol kiri mouse.
    def _on_mouse_up(self, event):
        # Mengambil koordinat x dan y dari event mouse.
        x, y = event.x, event.y
        # Jika sedang dalam mode transformasi.
        if self.transform_mode:
            # Reset posisi awal mouse.
            self.transform_start_mouse_pos = None
            # Jika proses menggambar window baru saja selesai.
            if self.is_drawing_window:
                # Nonaktifkan flag.
                self.is_drawing_window = False
                # Hapus persegi panjang pratinjau.
                if self.window_rect_id:
                    self.canvas.delete(self.window_rect_id) 
                    self.window_rect_id = None
                
                # Tentukan koordinat final dari window (xmin, ymin, xmax, ymax).
                clip_window = (min(self.start_x, x), min(self.start_y, y),
                               max(self.start_x, x), max(self.start_y, y))

                # Jika modenya 'Window', terapkan efek sorotan warna.
                if self.transform_mode == "Window":
                    self.window_coords = clip_window
                    self._apply_windowing_effect() 
                # Jika modenya 'Clip', lakukan operasi clipping.
                elif self.transform_mode == "Clip":
                    self._perform_clipping(clip_window)
                
                # Gambar ulang kanvas untuk menampilkan hasil.
                self.redraw_all()
        # Jika sedang dalam mode menggambar biasa.
        elif self.is_drawing:
            # Nonaktifkan flag menggambar.
            self.is_drawing = False
            # Hapus bentuk pratinjau.
            if self.current_preview_id:
                self.canvas.delete(self.current_preview_id)
                self.current_preview_id = None
            
            # Siapkan dictionary untuk data objek baru.
            new_object_data = {
                'color': self.draw_color, 'width': self.brush_size,
                'fill': self.fill_shape, 'rotation_angle': 0.0,
                'original_color': self.draw_color 
            }

        
            # Tambahkan data spesifik bentuk ke dictionary.
            if self.current_tool == 'Pencil' and len(self.active_line_points) > 1:
                new_object_data.update({'type': 'line', 'points': self.active_line_points.copy()})
            elif self.current_tool == 'Line':
                new_object_data.update({'type': 'line', 'points': [(self.start_x, self.start_y), (x, y)]})
            elif self.current_tool == 'Rectangle':
                rect_corners = self._get_rect_corners(self.start_x, self.start_y, x, y)
                new_object_data.update({'type': 'rectangle', 'points': rect_corners})
            elif self.current_tool == 'Ellipse':

                # Elips disimulasikan sebagai poligon dengan banyak sisi.
                num_segments = 60 
                center_x, center_y = (self.start_x + x) / 2, (self.start_y + y) / 2
                radius_x, radius_y = abs(x - self.start_x) / 2, abs(y - self.start_y) / 2
                if radius_x == 0: radius_x = 0.01 # Hindari pembagian dengan nol
                if radius_y == 0: radius_y = 0.01 # Hindari pembagian dengan nol
                ellipse_points = []
                # Hitung posisi titik-titik di sekeliling elips.
                for i in range(num_segments + 1): 
                    angle = (i / num_segments) * 2 * math.pi
                    point_x = center_x + radius_x * math.cos(angle)
                    point_y = center_y + radius_y * math.sin(angle)
                    ellipse_points.append((point_x, point_y))
                new_object_data.update({'type': 'ellipse', 'points': ellipse_points})
            
            # Jika objek berhasil dibuat, tambahkan ke daftar objek.
            if 'type' in new_object_data:
                self.drawn_objects.append(new_object_data)
            # Gambar ulang kanvas.
            self.redraw_all()


    # --- FUNGSI LOGIKA CLIPPING ---
    # Fungsi ini mengecek apakah sebuah objek (berdasarkan bounding box-nya)
    # bersinggungan dengan area window yang diberikan.
    def _object_intersects_window(self, obj, window):
        # Jika objek tidak punya titik (misalnya, setelah gagal di-clip), anggap tidak bersinggungan.
        if not obj.get('points'):
            return False
        
        # Dapatkan semua koordinat x dan y dari objek.
        xs = [p[0] for p in obj['points']]
        ys = [p[1] for p in obj['points']]
        # Tentukan bounding box objek (xmin, ymin, xmax, ymax).
        obj_bbox = (min(xs), min(ys), max(xs), max(ys))

        # Ambil koordinat window.
        win_xmin, win_ymin, win_xmax, win_ymax = window
        # Ambil koordinat bounding box objek.
        obj_xmin, obj_ymin, obj_xmax, obj_ymax = obj_bbox

        # Cek kondisi di mana mereka TIDAK mungkin bersinggungan.
        # Jika bounding box objek sepenuhnya di kiri, kanan, atas, atau bawah window,
        # maka tidak ada persinggungan.
        if obj_xmax < win_xmin or obj_xmin > win_xmax or obj_ymax < win_ymin or obj_ymin > win_ymax:
            return False
        # Jika tidak ada kondisi di atas yang terpenuhi, berarti mereka bersinggungan.
        return True

    # Fungsi utama untuk melakukan operasi clipping.
    # Cara kerja:
    # 1. Membuat sebuah list kosong baru (`new_drawn_objects`) untuk menampung hasil.
    # 2. Melakukan iterasi pada setiap objek yang ada di kanvas (`self.drawn_objects`).
    # 3. Untuk setiap objek, ia memanggil `_object_intersects_window` untuk memeriksa
    #    apakah objek tersebut perlu diproses atau tidak.
    # 4. Jika TIDAK bersinggungan, objek tersebut langsung ditambahkan ke list baru tanpa diubah.
    # 5. Jika BERSINGGUNGAN, maka algoritma clipping yang sesuai (Cohen-Sutherland untuk garis,
    #    Sutherland-Hodgman untuk poligon) akan dijalankan pada objek tersebut.
    # 6. Hasil dari clipping (yang bisa jadi objek yang lebih kecil atau tidak ada sama sekali)
    #    ditambahkan ke list baru.
    # 7. Setelah semua objek diproses, list `self.drawn_objects` yang lama diganti dengan
    #    `new_drawn_objects` yang berisi hasil akhir.
    def _perform_clipping(self, clip_window):
        # List sementara untuk menyimpan objek hasil clipping dan objek yang tidak terpengaruh.
        new_drawn_objects = []
        # Loop melalui setiap objek yang saat ini ada di kanvas.
        for obj in self.drawn_objects:
            # Cek dulu apakah objek ini bersinggungan dengan jendela clipping.
            if not self._object_intersects_window(obj, clip_window):
                # Jika tidak, objek ini aman. Langsung tambahkan ke daftar baru.
                new_drawn_objects.append(obj)
                # Lanjutkan ke objek berikutnya dalam loop.
                continue

            # Jika kode sampai di sini, berarti objek bersinggungan dan perlu di-clip.
            if obj['type'] == 'point':
                # Untuk titik, cek sederhana apakah ia di dalam persegi panjang.
                if self._is_point_in_rect(obj['points'][0], clip_window):
                    new_drawn_objects.append(obj)
            
            elif obj['type'] == 'line':
                # Jika ini adalah polyline (dari alat pensil), proses setiap segmennya.
                if len(obj['points']) > 2:
                    for i in range(len(obj['points']) - 1):
                        p1, p2 = obj['points'][i], obj['points'][i+1]
                        # Jalankan algoritma clipping Cohen-Sutherland pada segmen.
                        clipped_segment = self._cohen_sutherland_clip(p1, p2, clip_window)
                        # Jika ada hasil (garis tidak sepenuhnya di luar),
                        if clipped_segment:
                            # Buat objek baru untuk segmen ini agar propertinya (warna, tebal) ikut.
                            new_obj_segment = obj.copy()
                            new_obj_segment['points'] = clipped_segment
                            new_drawn_objects.append(new_obj_segment)
                else: # Jika ini garis biasa (hanya 2 titik).
                    # Jalankan algoritma clipping.
                    clipped_line = self._cohen_sutherland_clip(obj['points'][0], obj['points'][1], clip_window)
                    # Jika ada hasil.
                    if clipped_line:
                        # Perbarui titik-titik pada objek asli.
                        obj['points'] = clipped_line
                        # Tambahkan objek yang telah diubah ke daftar baru.
                        new_drawn_objects.append(obj)
            
            elif obj['type'] in ['rectangle', 'ellipse']:
                # Untuk poligon, jalankan algoritma Sutherland-Hodgman.
                clipped_polygon = self._sutherland_hodgman_clip(obj['points'], clip_window)
                # Jika ada poligon hasil clipping.
                if clipped_polygon:
                    # Perbarui titik-titik pada objek asli.
                    obj['points'] = clipped_polygon
                    # Tambahkan objek yang telah diubah ke daftar baru.
                    new_drawn_objects.append(obj)

        # Ganti daftar objek lama dengan daftar baru yang sudah final.
        self.drawn_objects = new_drawn_objects
        # Batalkan seleksi objek.
        self._unselect_object()

    # --- Implementasi Algoritma Cohen-Sutherland ---
    # Variabel konstanta untuk merepresentasikan 4-bit 'outcode'.
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    # Fungsi untuk menghitung outcode sebuah titik terhadap clip_window.
    def _compute_outcode(self, p, clip_window):
        x, y = p
        xmin, ymin, xmax, ymax = clip_window
        code = self.INSIDE  # Awalnya anggap di dalam.
        if x < xmin: code |= self.LEFT    # Jika di kiri, set bit pertama.
        elif x > xmax: code |= self.RIGHT # Jika di kanan, set bit kedua.
        if y < ymin: code |= self.BOTTOM  # Jika di bawah, set bit ketiga.
        elif y > ymax: code |= self.TOP   # Jika di atas, set bit keempat.
        return code

    # Fungsi clipping garis Cohen-Sutherland.
    # Cara kerja:
    # 1. Hitung 'outcode' untuk kedua titik ujung garis (p1, p2).
    # 2. Masuk ke loop yang akan berhenti jika garis diterima atau ditolak.
    # 3. Cek Trivial Accept: Jika outcode p1 DAN p2 adalah 0 (keduanya INSIDE),
    #    maka seluruh garis ada di dalam. Terima dan kembalikan garis asli.
    # 4. Cek Trivial Reject: Jika hasil operasi bitwise AND dari outcode p1 dan p2 tidak nol,
    #    artinya kedua titik berada di luar pada sisi yang sama (misal, keduanya di atas).
    #    Garis pasti di luar. Tolak dan kembalikan None.
    # 5. Jika bukan keduanya, garis perlu dipotong. Pilih satu titik yang di luar.
    # 6. Hitung titik potong (interseksi) antara garis dan batas window.
    # 7. Ganti titik yang di luar tadi dengan titik potong yang baru dihitung.
    # 8. Ulangi loop dengan segmen garis yang sudah diperbarui.
    def _cohen_sutherland_clip(self, p1, p2, clip_window):
        x1, y1 = p1; x2, y2 = p2
        xmin, ymin, xmax, ymax = clip_window
        outcode1 = self._compute_outcode(p1, clip_window)
        outcode2 = self._compute_outcode(p2, clip_window)
        while True:
            if not (outcode1 | outcode2): return [(x1, y1), (x2, y2)] # Trivial accept
            elif outcode1 & outcode2: return None # Trivial reject
            else:
                x, y = 0, 0
                outcode_out = outcode1 if outcode1 else outcode2
                # Hitung titik potong berdasarkan sisi mana titik itu berada.
                if outcode_out & self.TOP:
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                    y = ymax
                elif outcode_out & self.BOTTOM:
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                    y = ymin
                elif outcode_out & self.RIGHT:
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                    x = xmax
                elif outcode_out & self.LEFT:
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                    x = xmin
                # Perbarui koordinat titik yang berada di luar dengan titik potong.
                if outcode_out == outcode1:
                    x1, y1 = x, y
                    outcode1 = self._compute_outcode((x1, y1), clip_window)
                else:
                    x2, y2 = x, y
                    outcode2 = self._compute_outcode((x2, y2), clip_window)

    # Fungsi helper untuk memotong poligon pada satu sisi (edge) dari clip window.
    def _clip_polygon_edge(self, subject_polygon, edge, is_vertical, value, is_less_than):
        input_list = subject_polygon
        output_list = []
        if not input_list: return output_list
        p1 = input_list[-1]
        for p2 in input_list:
            p1_coord = p1[1] if is_vertical else p1[0]
            p2_coord = p2[1] if is_vertical else p2[0]
            p1_inside = p1_coord <= value if is_less_than else p1_coord >= value
            p2_inside = p2_coord <= value if is_less_than else p2_coord >= value
            # Terapkan 4 aturan Sutherland-Hodgman
            if p1_inside and p2_inside: output_list.append(p2) # Aturan 1
            elif p1_inside and not p2_inside: # Aturan 2
                if p2_coord != p1_coord:
                    if is_vertical:
                        ix = p1[0] + (p2[0] - p1[0]) * (value - p1_coord) / (p2_coord - p1_coord)
                        output_list.append((ix, value))
                    else:
                        iy = p1[1] + (p2[1] - p1[1]) * (value - p1_coord) / (p2_coord - p1_coord)
                        output_list.append((value, iy))
            elif not p1_inside and p2_inside: # Aturan 3
                if p2_coord != p1_coord:
                    if is_vertical:
                        ix = p1[0] + (p2[0] - p1[0]) * (value - p1_coord) / (p2_coord - p1_coord)
                        output_list.append((ix, value))
                    else:
                        iy = p1[1] + (p2[1] - p1[1]) * (value - p1_coord) / (p2_coord - p1_coord)
                        output_list.append((value, iy))
                output_list.append(p2)
            # Aturan 4 (keduanya di luar) tidak melakukan apa-apa.
            p1 = p2
        return output_list

    # Fungsi clipping poligon Sutherland-Hodgman.
    # Cara kerja:
    # 1. Mengambil daftar titik poligon sebagai input.
    # 2. Memproses poligon secara sekuensial terhadap setiap sisi dari clip window (kiri, kanan, bawah, atas).
    # 3. Untuk setiap sisi, ia memanggil helper `_clip_polygon_edge`.
    # 4. `_clip_polygon_edge` menerapkan 4 aturan dasar:
    #    - Jika kedua titik segmen di dalam: simpan titik kedua.
    #    - Jika titik pertama di dalam dan kedua di luar: hitung & simpan titik potong.
    #    - Jika titik pertama di luar dan kedua di dalam: hitung & simpan titik potong, lalu simpan titik kedua.
    #    - Jika kedua titik di luar: tidak ada yang disimpan.
    # 5. Daftar titik hasil potongan dari satu sisi menjadi input untuk sisi berikutnya.
    # 6. Hasil akhirnya adalah daftar titik dari poligon yang telah terpotong oleh keempat sisi.
    def _sutherland_hodgman_clip(self, subject_polygon, clip_window):
        xmin, ymin, xmax, ymax = clip_window
        output_list = subject_polygon
        # Potong terhadap sisi kiri, lalu kanan, lalu bawah, lalu atas.
        output_list = self._clip_polygon_edge(output_list, 'left', False, xmin, False)
        output_list = self._clip_polygon_edge(output_list, 'right', False, xmax, True)
        output_list = self._clip_polygon_edge(output_list, 'bottom', True, ymax, True)
        output_list = self._clip_polygon_edge(output_list, 'top', True, ymin, False)
        return output_list
    
    # Fungsi untuk memilih objek di kanvas.
    def _select_object(self, x, y):
        # Batalkan pilihan sebelumnya.
        self._unselect_object()
        # Toleransi piksel untuk klik.
        tolerance = 5
        # Temukan ID item kanvas terdekat dengan titik klik.
        clicked_tk_id = self.canvas.find_closest(x, y, halo=tolerance)
        # Jika ada item yang ditemukan.
        if clicked_tk_id:
            # Ambil ID pertama dari tuple hasil.
            clicked_tk_id = clicked_tk_id[0] 
            # Loop melalui objek yang digambar (dari yang terbaru) untuk menemukan data objek yang cocok.
            for obj in reversed(self.drawn_objects):
                if 'tk_id' in obj and obj['tk_id'] == clicked_tk_id:
                    # Jika cocok, set sebagai objek terpilih.
                    self.selected_object = obj
                    # Gambar kotak seleksi di sekitarnya.
                    self._draw_selection_box()
                    # Hentikan loop karena objek sudah ditemukan.
                    break

    # Fungsi untuk menggambar kotak seleksi.
    def _draw_selection_box(self):
        # Hapus kotak seleksi lama.
        if self.selection_box_id: self.canvas.delete(self.selection_box_id)
        # Pastikan ada objek yang dipilih dan objek tersebut punya titik.
        if not self.selected_object or not self.selected_object.get('points'): return
        # Dapatkan semua koordinat x dan y untuk mencari bounding box.
        xs = [p[0] for p in self.selected_object['points']]
        ys = [p[1] for p in self.selected_object['points']]
        if not xs or not ys: return 
        # Hitung bounding box (xmin, ymin, xmax, ymax).
        bbox = [min(xs), min(ys), max(xs), max(ys)]
        # Beri sedikit padding (jarak) agar kotak tidak terlalu mepet.
        padding = 5
        bbox = [b - padding if i < 2 else b + padding for i, b in enumerate(bbox)]
        # Buat persegi panjang putus-putus sebagai kotak seleksi.
        self.selection_box_id = self.canvas.create_rectangle(
            bbox, outline="red", dash=(4,2), width=1, tags="selection_box"
        )

    # Fungsi untuk membatalkan pilihan objek.
    def _unselect_object(self):
        # Hapus kotak seleksi dari kanvas jika ada.
        if self.selection_box_id: self.canvas.delete(self.selection_box_id)
        # Reset variabel.
        self.selection_box_id = None
        self.selected_object = None

    # Fungsi untuk mendapatkan 4 titik sudut dari sebuah persegi panjang.
    def _get_rect_corners(self, x1, y1, x2, y2):
        return [(min(x1,x2), min(y1,y2)), (max(x1,x2), min(y1,y2)), 
                (max(x1,x2), max(y1,y2)), (min(x1,x2), max(y1,y2))]

    # Fungsi untuk menghitung titik tengah (centroid) dari sebuah bentuk.
    def _get_shape_center(self, points):
        if not points: return 0, 0
        xs = [p[0] for p in points]; ys = [p[1] for p in points]
        return sum(xs) / len(xs), sum(ys) / len(ys)

    # Fungsi untuk memutar sekumpulan titik mengelilingi sebuah pusat (center).
    def _rotate_points(self, points, center, angle):
        cx, cy = center
        rotated_points = []
        for x, y in points:
            # Pindahkan titik ke origin (0,0).
            temp_x, temp_y = x - cx, y - cy
            # Terapkan rumus rotasi 2D.
            rotated_x = temp_x * math.cos(angle) - temp_y * math.sin(angle)
            rotated_y = temp_x * math.sin(angle) + temp_y * math.cos(angle)
            # Kembalikan titik ke posisi semula.
            rotated_points.append((rotated_x + cx, rotated_y + cy))
        return rotated_points

    # Fungsi untuk menggeser (translasi) objek yang dipilih.
    def _translate_object(self, dx, dy):
        if not self.selected_object: return
        # Tambahkan dx dan dy ke setiap titik dari objek.
        self.selected_object['points'] = [(x + dx, y + dy) for x, y in self.selected_object['points']]

    # Fungsi untuk memutar objek yang dipilih.
    def _rotate_object(self, current_mouse_x, current_mouse_y):
        if not self.selected_object or not self.transform_start_mouse_pos: return
        prev_mouse_x, prev_mouse_y = self.transform_start_mouse_pos
        # Dapatkan pusat rotasi objek.
        cx, cy = self._get_shape_center(self.selected_object['points'])
        # Hitung sudut dari pusat ke posisi mouse sebelumnya.
        start_angle = math.atan2(prev_mouse_y - cy, prev_mouse_x - cx)
        # Hitung sudut dari pusat ke posisi mouse saat ini.
        current_angle = math.atan2(current_mouse_y - cy, current_mouse_x - cx)
        # Selisih sudut adalah besar rotasi yang harus diterapkan.
        delta_angle = current_angle - start_angle
        # Akumulasi total sudut rotasi.
        self.selected_object['rotation_angle'] += delta_angle
        # Putar semua titik objek.
        self.selected_object['points'] = self._rotate_points(
            self.selected_object['points'], (cx, cy), delta_angle
        )

    # Fungsi untuk mengubah skala objek yang dipilih.
    def _scale_object(self, dy):
        if not self.selected_object: return
        # Tentukan faktor skala berdasarkan gerakan vertikal mouse.
        scale_factor = max(0.01, 1.0 + dy / 100.0)
        # Jika objek adalah titik, ubah saja lebarnya.
        if self.selected_object['type'] == 'point':
            self.selected_object['width'] = max(1, self.selected_object['width'] * scale_factor)
            return
        # Dapatkan pusat skala.
        cx, cy = self._get_shape_center(self.selected_object['points'])
        new_points = []
        for x, y in self.selected_object['points']:
            # Hitung posisi baru setiap titik berdasarkan faktor skala dan pusat.
            scaled_x = (x - cx) * scale_factor + cx
            scaled_y = (y - cy) * scale_factor + cy
            new_points.append((scaled_x, scaled_y))
        # Perbarui titik-titik objek.
        self.selected_object['points'] = new_points
        # Perbarui juga lebar garis/outline objek.
        if self.selected_object['type'] in ['line', 'rectangle', 'ellipse']:
            self.selected_object['width'] = max(1, self.selected_object['width'] * scale_factor)
                
    # Fungsi sederhana untuk mengecek apakah sebuah titik ada di dalam persegi panjang.
    def _is_point_in_rect(self, point, rect):
        px, py = point; rx1, ry1, rx2, ry2 = rect
        return rx1 <= px <= rx2 and ry1 <= py <= ry2

    # Fungsi untuk menerapkan efek windowing (mengubah warna objek).
    def _apply_windowing_effect(self):
        # Jika tidak ada window aktif, kembalikan semua warna ke aslinya.
        if not self.window_coords:
            for obj in self.drawn_objects: obj['color'] = obj['original_color']
            return
        # Loop melalui setiap objek.
        for obj in self.drawn_objects:
            # Jika objek bersinggungan dengan window.
            if self._object_intersects_window(obj, self.window_coords):
                # Ubah warnanya menjadi warna sorotan.
                obj['color'] = self.window_highlight_color
            else:
                # Jika tidak, kembalikan ke warna asli.
                obj['color'] = obj['original_color'] 

    # Fungsi untuk menghapus window aktif.
    def _clear_window(self):
        if self.window_rect_id: self.canvas.delete(self.window_rect_id)
        self.window_rect_id = None
        self.window_coords = None
        # Panggil apply_windowing_effect untuk mengembalikan warna semua objek.
        self._apply_windowing_effect() 
        self.redraw_all() 
        self._update_status_bar()

    # Fungsi untuk menggambar ulang seluruh isi kanvas.
    def redraw_all(self):
        # Hapus semua item yang ada di kanvas.
        self.canvas.delete("all")
        # Jika ada window aktif, terapkan efek warnanya terlebih dahulu.
        if self.window_coords: self._apply_windowing_effect()
        # Loop melalui setiap objek dalam daftar data.
        for obj in self.drawn_objects:
            # Lewati objek yang tidak memiliki titik (misalnya hasil clip yang kosong).
            if not obj.get('points'): continue
            # Siapkan opsi visual untuk item kanvas.
            obj_options = {
                'fill': obj['color'] if obj.get('fill', False) else '',
                'outline': obj['color'], 'width': obj['width']
            }
            tk_id = None
            # Buat item kanvas berdasarkan tipe objek.
            if obj['type'] == 'point':
                x, y = obj['points'][0]
                r = obj['width'] 
                tk_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=obj['color'], outline=obj['color'])
            elif obj['type'] == 'line' and len(obj['points']) >= 2:
                tk_id = self.canvas.create_line(obj['points'], fill=obj['color'], width=obj['width'],
                                                 capstyle=tk.ROUND, joinstyle=tk.ROUND)
            elif obj['type'] in ['rectangle', 'ellipse'] and len(obj['points']) >= 3:
                flat_points = [c for p in obj['points'] for c in p]
                tk_id = self.canvas.create_polygon(flat_points, **obj_options)
            # Simpan ID item kanvas ke dalam data objek untuk referensi nanti (misal, untuk diseleksi).
            if tk_id: obj['tk_id'] = tk_id
        # Jika ada objek yang dipilih, gambar ulang kotak seleksinya.
        if self.selected_object: self._draw_selection_box()
        # Jika sedang menggambar window, pastikan pratinjaunya ada di lapisan paling atas.
        if self.is_drawing_window and self.window_rect_id: self.canvas.lift(self.window_rect_id)

    # Fungsi untuk membersihkan seluruh kanvas.
    def clear_canvas(self):
        # Kosongkan daftar objek.
        self.drawn_objects = []
        # Batalkan pilihan objek.
        self._unselect_object()
        # Hapus window aktif.
        self._clear_window() 
        # Gambar ulang kanvas yang kini kosong.
        self.redraw_all()

    # Fungsi untuk mengatur warna gambar.
    def set_draw_color(self, color):
        self.draw_color = color
        self._update_status_bar()

    # Fungsi untuk menangani perubahan ukuran kuas dari slider.
    def _on_brush_size_change(self, value):
        self.brush_size = int(value)
        self._update_status_bar()

    # Fungsi untuk menangani perubahan status checkbox 'Isi Bentuk'.
    def _on_fill_toggle(self):
        self.fill_shape = self.fill_var.get()
        self._update_status_bar()

    # Fungsi untuk memperbarui teks di status bar.
    def _update_status_bar(self):
        # Bangun string status berdasarkan kondisi aplikasi saat ini.
        mode = f"Mode: {self.transform_mode}" if self.transform_mode else f"Alat: {self.current_tool}"
        win_status = "Windowing: Aktif" if self.window_coords else "Windowing: Nonaktif"
        color_status = f"Warna: {self.draw_color} | Ukuran: {self.brush_size}"
        fill_status = "Isi: Aktif" if self.fill_shape else "Isi: Nonaktif"
        selection_status = f" | Objek dipilih: {self.selected_object['type']}" if self.selected_object else ""
        # Atur teks pada widget status bar.
        self.status_bar.config(text=f"{mode} | {win_status} | {color_status} | {fill_status}{selection_status}")

# --- Titik Masuk Utama Program ---
# Blok ini hanya akan dieksekusi jika file ini dijalankan sebagai script utama.
if __name__ == "__main__":
    # Membuat jendela utama (root window) dari tkinter.
    root = tk.Tk()
    # Membuat instance (objek) dari kelas DrawingApp kita.
    app = DrawingApp(root)
    # Memulai event loop utama tkinter. Jendela akan ditampilkan dan menunggu interaksi pengguna.
    root.mainloop()