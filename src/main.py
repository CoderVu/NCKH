import tkinter as tk
from PIL import Image, ImageTk
from start import MainAppWindow

class IntroductionWindow:
    def __init__(self, master):
        self.master = master
        master.title("Giới thiệu")
        master.geometry("750x550")
        master.config(bg="#E3F2FD") 

        title_frame = tk.Frame(master, bg="#0D47A1", padx=20, pady=10) 
        title_frame.pack(fill="x")

        title_label = tk.Label(
            title_frame,
            text="TRƯỜNG ĐẠI HỌC BÁCH KHOA ĐÀ NẴNG\nĐẠI HỌC ĐÀ NẴNG",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#0D47A1"
        )
        title_label.pack()

        main_frame = tk.Frame(master, bg="white", bd=5, relief="ridge")  
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=680, height=460)

        logo_frame = tk.Frame(main_frame, bg="white")
        logo_frame.pack(pady=10)

        try:
            logo = Image.open("e:/Python/nghiencuu/GIT/NCKH/src/image/logo.png")
            logo = logo.resize((85, 85), Image.LANCZOS)
            logo_image = ImageTk.PhotoImage(logo)

            logo_label = tk.Label(logo_frame, image=logo_image, bg="white")
            logo_label.image = logo_image 
            logo_label.pack(side="left", padx=10)
        except Exception as e:
            print("Lỗi khi tải ảnh:", e)

        project_title = tk.Label(
            main_frame,
            text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG\nTHEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ",
            font=("Helvetica", 17, "bold"),
            fg="white",
            bg="#00796B", 
            justify="center",
            padx=20,
            pady=12
        )
        project_title.pack(pady=10)

        label_department = tk.Label(
            main_frame,
            text="KHOA QUẢN LÝ DỰ ÁN\nNGÀNH KINH TẾ XÂY DỰNG",
            font=("Helvetica", 14),
            fg="#DC143C",
            bg="white"
        )
        label_department.pack(pady=5)

        self.label_student = tk.Label(
            main_frame,
            text="GV hướng dẫn: ThS. Phạm Thị Trang",
            font=("Helvetica", 14),
            fg="#1E3D59",
            bg="white"
        )
        self.label_student.pack(pady=5)

        self.entry_gv = tk.Entry(main_frame, font=("Helvetica", 14))
        self.entry_gv.insert(0, "ThS. Phạm Thị Trang")
        self.entry_gv.pack(pady=5)

        self.entry_sv = tk.Entry(main_frame, font=("Helvetica", 14))
        self.entry_sv.insert(0, "Nguyễn Thị Thanh Huyền")
        self.entry_sv.pack(pady=5)

        self.entry_mssv = tk.Entry(main_frame, font=("Helvetica", 14))
        self.entry_mssv.insert(0, "19110197")
        self.entry_mssv.pack(pady=5)

        update_button = tk.Button(
            main_frame,
            text="CẬP NHẬT",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            cursor="hand2",
            relief="raised",
            bd=3,
            padx=15,
            pady=8,
            width=15,
            command=self.update_and_start
        )
        update_button.pack(pady=10)

        start_button = tk.Button(
            main_frame,
            text="BẮT ĐẦU",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            cursor="hand2",
            relief="raised",
            bd=3,
            padx=15,
            pady=8,
            width=15,
            command=self.start_app
        )
        start_button.pack(pady=10)

        start_button.bind("<Enter>", lambda e: start_button.config(bg="#388E3C"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#4CAF50"))

    def update_and_start(self):
        self.update_label()
        self.start_app()

    def update_label(self):
        gv = self.entry_gv.get()
        sv = self.entry_sv.get()
        mssv = self.entry_mssv.get()
        self.label_student.config(text=f"GV hướng dẫn: {gv}\nSinh viên: {sv}\nMSSV: {mssv}")

    def start_app(self):
        self.master.destroy()
        root = tk.Tk() 
        app = MainAppWindow(root) 
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    intro = IntroductionWindow(root)
    root.mainloop()