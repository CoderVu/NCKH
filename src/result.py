import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time_cost_optimization import gantt_chart, plot_diagonal_chart

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
        
        self.create_widgets(summary)
    
    def create_widgets(self, summary):
        # Định nghĩa các cột
        columns = self.initial_columns
        
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
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
            label = tk.Label(self.master, text=line, anchor='w', bg="#f4f4f4", fg="blue", font=("Arial", 10, "bold"))
            label.grid(row=1 + i, column=0, columnspan=5, padx=10, pady=2, sticky='w')

        # Khung chứa các nút bấm
        button_frame = tk.Frame(self.master, bg="#f4f4f4")
        button_frame.grid(row=1 + len(summary_lines), column=0, columnspan=5, pady=10)

        # Nút đóng cửa sổ
        close_button = tk.Button(button_frame, text="Đóng", command=self.master.destroy, bg="gray", fg="white", font=("Arial", 10, "bold"))
        close_button.grid(row=0, column=0, padx=5)

        # Nút lưu kết quả
        save_button = tk.Button(button_frame, text="Lưu kết quả", command=self.save_results, bg="gray", fg="white", font=("Arial", 10, "bold"))
        save_button.grid(row=0, column=1, padx=5)

        # Nút hiển thị sơ đồ Gantt
        gantt_button = tk.Button(button_frame, text="Hiển thị biểu đồ Gantt", command=self.show_gantt_chart, bg="gray", fg="white", font=("Arial", 10, "bold"))
        gantt_button.grid(row=0, column=2, padx=5)

        # Nút hiển thị biểu đồ đường chéo
        diagonal_button = tk.Button(button_frame, text="Hiển thị biểu đồ đường chéo", command=self.show_diagonal_chart, bg="gray", fg="white", font=("Arial", 10, "bold"))
        diagonal_button.grid(row=0, column=3, padx=5)

        # Nút hiển thị thông tin chi tiết
        details_button = tk.Button(button_frame, text="Hiển thị chi tiết", command=self.show_details, bg="gray", fg="white", font=("Arial", 10, "bold"))
        details_button.grid(row=0, column=4, padx=5)

        # Nút trở về kết quả trước
        back_button = tk.Button(button_frame, text="Quay lại", command=self.show_initial_results, bg="gray", fg="white", font=("Arial", 10, "bold"))
        back_button.grid(row=0, column=5, padx=5)

    def save_results(self):
        # Implement the save functionality here
        pass

    def show_gantt_chart(self):
        fig = gantt_chart(self.tasks, self.dates, size_x=10, size_y=6, return_fig=True)  # Kích thước lớn hơn
        self.display_chart(fig)

    def show_diagonal_chart(self):
        fig = plot_diagonal_chart(self.tasks, self.dates, size_x=10, size_y=6, return_fig=True)  # Kích thước lớn hơn
        self.display_chart(fig)

    def show_details(self):
        # Xóa các mục hiện tại trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Định nghĩa lại các cột để bao gồm ES, EF, LS, LF, Slack
        columns = ("Tên công việc", "ES", "EF", "LS", "LF", "Slack")
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm dữ liệu vào bảng với các cột mới
        for result in self.results:
            self.tree.insert("", "end", values=(result[0], result[9], result[10], result[11], result[12], result[13]))

    def show_initial_results(self):
        # Xóa các mục hiện tại trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Định nghĩa lại các cột ban đầu
        columns = self.initial_columns
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm dữ liệu vào bảng với các cột ban đầu
        for result in self.initial_results:
            self.tree.insert("", "end", values=result)

    def display_chart(self, fig):
        # Tạo cửa sổ mới để hiển thị biểu đồ
        chart_window = tk.Toplevel(self.master)
        chart_window.title("Biểu đồ")
        chart_window.geometry("1000x800")  # Kích thước cửa sổ lớn hơn

        # Tạo khung để chứa biểu đồ
        chart_frame = tk.Frame(chart_window)
        chart_frame.grid(row=0, column=0, sticky='nsew')

        # Nhúng biểu đồ vào khung
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Thêm thanh cuộn dọc cho khung
        scrollbar = ttk.Scrollbar(chart_window, orient="vertical", command=chart_frame.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        chart_frame.configure(yscrollcommand=scrollbar.set)

def open_result_window(results, summary, tasks, dates):
    root = tk.Tk()
    app = ResultWindow(root, results, summary, tasks, dates)
    root.mainloop()