import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time_cost_optimization import gantt_chart, plot_diagonal_chart
import pandas as pd
from tkinter import filedialog

class ResultWindow:
    def __init__(self, master, results, summary, tasks, dates):
        self.master = master
        self.tasks = tasks
        self.dates = dates
        self.results = results
        self.initial_columns = ("Tên công việc", "Critical", "T.gian b.thường", "T.gian khẩn", "T.gian đề xuất", "Cp.bình thường", "Cp.khẩn trương", "Cp bổ sung", "Trước")
        self.initial_results = [result[:9] for result in results]  # Chỉ lưu trữ các cột đầu tiên
        master.title("Kết quả tối ưu hóa")
        master.state('zoomed')
        self.master.configure(bg="#f0f8ff")
        self.create_widgets(summary)
        self.save_initial_treeview_format()

    def create_widgets(self, summary):
        # Định nghĩa các cột
        columns = self.initial_columns
        
        style = ttk.Style()

       
        style.configure("Treeview", rowheight=30, borderwidth=1, relief="solid", background="#f0f8ff")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4CAF50", foreground="black")  # Đặt màu nền header xanh và màu chữ đen
        style.map("Treeview", background=[("selected", "#347083"), ("active", "#e6f2ff")])

        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        
        # Cập nhật tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=100)
        
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Thêm thanh cuộn dọc
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=4, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Thêm dữ liệu vào bảng
        for result in self.initial_results:
            self.tree.insert("", "end", values=result)

        # Tách phần tổng kết thành các thông tin riêng biệt và thêm màu sắc
        summary_lines = summary.split('\n')
        for i, line in enumerate(summary_lines):
            label = tk.Label(self.master, text=line, anchor='w', bg="#f0f8ff", fg="blue", font=("Arial", 10, "bold"))
            label.grid(row=1 + i, column=0, columnspan=5, padx=10, pady=2, sticky='w')

        # Khung chứa các nút bấm
        button_frame = tk.Frame(self.master, bg="#f0f8ff")
        button_frame.grid(row=1 + len(summary_lines), column=0, columnspan=5, pady=10)

        button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 10, "bold"), "padx": 10, "pady": 5}

        # Hàm hiệu ứng hover cho nút bấm
        def on_enter(e):
            e.widget['background'] = '#45a049'

        def on_leave(e):
            e.widget['background'] = '#4CAF50'

        # Nút đóng cửa sổ
        close_button = tk.Button(button_frame, text="Đóng", command=self.master.destroy, **button_style)
        close_button.grid(row=0, column=0, padx=5)
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        # Nút lưu kết quả
        save_button = tk.Button(button_frame, text="Lưu kết quả", command=self.save_results, **button_style)
        save_button.grid(row=0, column=1, padx=5)
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)

        # Nút hiển thị sơ đồ Gantt
        gantt_button = tk.Button(button_frame, text="Hiển thị biểu đồ Gantt", command=self.show_gantt_chart, **button_style)
        gantt_button.grid(row=0, column=2, padx=5)
        gantt_button.bind("<Enter>", on_enter)
        gantt_button.bind("<Leave>", on_leave)

        # Nút hiển thị biểu đồ đường chéo
        diagonal_button = tk.Button(button_frame, text="Hiển thị biểu đồ đường chéo", command=self.show_diagonal_chart, **button_style)
        diagonal_button.grid(row=0, column=3, padx=5)
        diagonal_button.bind("<Enter>", on_enter)
        diagonal_button.bind("<Leave>", on_leave)

        # Nút hiển thị thông tin chi tiết
        details_button = tk.Button(button_frame, text="Hiển thị chi tiết", command=self.show_details, **button_style)
        details_button.grid(row=0, column=4, padx=5)
        details_button.bind("<Enter>", on_enter)
        details_button.bind("<Leave>", on_leave)

        # Nút trở về kết quả trước
        back_button = tk.Button(button_frame, text="Quay lại", command=self.show_initial_results, **button_style)
        back_button.grid(row=0, column=5, padx=5)
        back_button.bind("<Enter>", on_enter)
        back_button.bind("<Leave>", on_leave)

    def save_initial_treeview_format(self):
        self.initial_treeview_format = {
            "columns": self.tree["columns"],
            "show": self.tree["show"],
            "headings": {col: self.tree.heading(col) for col in self.tree["columns"]},
            "columns_width": {col: self.tree.column(col) for col in self.tree["columns"]}
        }

    def restore_initial_treeview_format(self):
        self.tree["columns"] = self.initial_treeview_format["columns"]
        self.tree["show"] = self.initial_treeview_format["show"]
        for col in self.tree["columns"]:
            self.tree.heading(col, text=self.initial_treeview_format["headings"][col]["text"], anchor=self.initial_treeview_format["headings"][col]["anchor"])
            self.tree.column(col, width=self.initial_treeview_format["columns_width"][col]["width"])

    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="results.xlsx")

        if file_path:
            if self.tree["columns"] == ("Tên công việc", "ES", "EF", "LS", "LF", "Slack"):
                detailed_results = [(self.tree.item(item)["values"]) for item in self.tree.get_children()]
                columns = ("Tên công việc", "ES", "EF", "LS", "LF", "Slack")
                df = pd.DataFrame(detailed_results, columns=columns)
            else:
                df = pd.DataFrame(self.initial_results, columns=self.initial_columns)

            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Thành công", "Kết quả đã được lưu thành công!")
                self.show_initial_results() 
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu kết quả: {e}")

    def show_gantt_chart(self):
        fig = gantt_chart(self.tasks, self.dates, size_x=10, size_y=6, return_fig=True)  # Kích thước lớn hơn
        self.display_chart(fig)

    def show_diagonal_chart(self):
        fig = plot_diagonal_chart(self.tasks, self.dates, size_x=10, size_y=6, return_fig=True)  # Kích thước lớn hơn
        self.display_chart(fig)

    def show_details(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        columns = ("Tên công việc", "ES", "EF", "LS", "LF", "Slack")
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=100)
        
        for result in self.results:
            self.tree.insert("", "end", values=(result[0], result[9], result[10], result[11], result[12], result[13]))

    def show_initial_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.restore_initial_treeview_format()
        
        for result in self.initial_results:
            self.tree.insert("", "end", values=result)

    def display_chart(self, fig):
        chart_window = tk.Toplevel(self.master)
        chart_window.title("Biểu đồ")
        chart_window.geometry("1000x800")

        chart_frame = tk.Frame(chart_window)
        chart_frame.grid(row=0, column=0, sticky='nsew')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        scrollbar = ttk.Scrollbar(chart_window, orient="vertical", command=chart_frame.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        chart_frame.configure(yscrollcommand=scrollbar.set)

def open_result_window(results, summary, tasks, dates):
    root = tk.Tk()
    app = ResultWindow(root, results, summary, tasks, dates)
    root.mainloop()
