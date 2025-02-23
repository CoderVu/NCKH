import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from home import TimeCostOptimizationApp 

class ProjectOptimizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Tối ưu hóa sơ đồ mạng")
        master.geometry("850x460")
        master.config(bg="#E3F2FD") 
      
        title_label = tk.Label(
            master,
            text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG\nTHEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ",
            font=("Helvetica", 17, "bold"),
            fg="#00796B",
            justify="center",
            padx=20,
            pady=12
        )
        title_label.pack(pady=10)

   
        main_frame = tk.Frame(master, bg="white", bd=3, relief="ridge")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

     
        logo_frame = tk.Frame(main_frame, bg="white")
        logo_frame.pack(side="left", padx=15, pady=15)

        try:
            logo = Image.open("src/image/logo.png")
            logo = logo.resize((100, 100), Image.LANCZOS)
            logo_image = ImageTk.PhotoImage(logo)

            logo_label = tk.Label(logo_frame, image=logo_image, bg="white")
            logo_label.image = logo_image
            logo_label.pack()
        except Exception as e:
            print("Lỗi khi tải ảnh:", e)

    
        author_label = tk.Label(
            main_frame,
            text="Sinh viên: Nguyễn Thị Thanh Huyền\nMSSV: 19110197\nKhoa Quản Lý Dự Án - Ngành Kinh Tế Xây Dựng",
            font=("Arial", 10),
            fg="#1E3D59",
            bg="white",
            justify="left"
        )
        author_label.pack(side="left", padx=5, pady=5)

        input_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        input_frame.pack(side="right", padx=20, pady=20)

        input_title = tk.Label(
            input_frame,
            text="Nhập các thông số của dự án",
            font=("Arial", 12, "bold"),
            fg="black",
            bg="white"
        )
        input_title.grid(row=0, column=0, columnspan=2, pady=5)

     
        tk.Label(input_frame, text="Tên dự án", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_name = tk.Entry(input_frame, width=25)
        self.entry_name.grid(row=1, column=1, padx=5, pady=2)

      

  
        tk.Label(input_frame, text="Đơn vị thời gian", font=("Arial", 11), bg="white").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.entry_time_unit = tk.Entry(input_frame, width=25)
        self.entry_time_unit.grid(row=3, column=1, padx=5, pady=2)

       
        button_frame = tk.Frame(input_frame, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        execute_button = tk.Button(
            button_frame, text="Thực hiện", font=("Arial", 11, "bold"),
            bg="#4CAF50", fg="white", width=10, command=self.validate_and_proceed
        )
        execute_button.pack(side="left", padx=5)

        cancel_button = tk.Button(
            button_frame, text="Hủy bỏ", font=("Arial", 11, "bold"),
            bg="#D32F2F", fg="white", width=10, command=master.quit
        )
        cancel_button.pack(side="left", padx=5)

   
    def validate_and_proceed(self):
        """Kiểm tra dữ liệu nhập và mở form tiếp theo nếu hợp lệ."""
        name = self.entry_name.get().strip()
        time_unit = self.entry_time_unit.get().strip()

     
        if not name or not time_unit:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return 

    
        self.master.destroy()

        root = tk.Tk()
        app = TimeCostOptimizationApp(root, name, time_unit)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectOptimizationApp(root)
    root.mainloop()
