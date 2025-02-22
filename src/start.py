import tkinter as tk
from tkinter import Menu
from newproject import ProjectOptimizationApp

class MainAppWindow:
    def __init__(self, master):
        self.master = master
        master.title("Chương Trình Tối Ưu Hóa Sơ Đồ Mạng")
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
        title_label.pack(pady=5)

        main_frame = tk.Frame(master, bg="white", bd=3, relief="ridge")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=450)

        try:
            logo_image = tk.PhotoImage(file="e:/Python/nghiencuu/GIT/NCKH/src/image/logo.png")
            logo_image = logo_image.subsample(10, 10) 
            logo_label = tk.Label(main_frame, image=logo_image, bg="white")
            logo_label.image = logo_image 
            logo_label.pack(pady=10)
        except Exception as e:
            print("Lỗi khi tải ảnh:", e)

        project_title = tk.Label(
            main_frame,
            text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG\nTHEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ",
            font=("Helvetica", 17, "bold"),
            fg="#00796B",
            justify="center",
            padx=20,
            pady=12
        )
        project_title.pack(pady=10)

        author_info = tk.Label(
            main_frame,
            text="Sinh viên: Nguyễn Thị Thanh Huyền\nMSSV: 19110197\nKhoa Quản Lý Dự Án - Ngành Kinh Tế Xây Dựng",
            font=("Helvetica", 14),
            fg="#1E3D59",
            bg="white"
        )
        author_info.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=20)

        new_project_button = tk.Button(
            button_frame,
            text="Tạo mới dự án",
            font=("Arial", 14, "bold"),
            bg="#4CAF50", 
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            relief="raised",
            bd=3,
            padx=20,
            pady=10,
            width=15,
            command=self.start_app
        )
        new_project_button.pack(pady=10)

        new_project_button.bind("<Enter>", lambda e: new_project_button.config(bg="#388E3C"))
        new_project_button.bind("<Leave>", lambda e: new_project_button.config(bg="#4CAF50"))

    def start_app(self):
        self.master.destroy()
        root = tk.Tk()
        app = ProjectOptimizationApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainAppWindow(root)
    root.mainloop()
