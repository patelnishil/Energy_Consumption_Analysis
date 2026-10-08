import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from data_manager import load_records, add_record, filter_records, delete_record_by_id
from analysis import calculate_summary, compare_appliances, find_high_usage
from reports import generate_reports


class EnergyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Consumption Management System")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.records = load_records()

        self.appliance_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.units_var = tk.StringVar()
        self.cost_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.period_var = tk.StringVar()

        self.build_ui()
        self.refresh_table()
        self.update_summary()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Energy Consumption Management & Analysis",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=12)

        form = ttk.LabelFrame(self.root, text="Record Energy Observation")
        form.pack(fill="x", padx=15, pady=5)

        labels = ["Appliance", "Category", "Date (YYYY-MM-DD)", "Units (kWh)", "Cost (₹)"]
        for i, text in enumerate(labels):
            ttk.Label(form, text=text).grid(row=0, column=i, padx=8, pady=5)

        ttk.Entry(form, textvariable=self.appliance_var, width=18).grid(row=1, column=0, padx=8)
        ttk.Entry(form, textvariable=self.category_var, width=18).grid(row=1, column=1, padx=8)
        ttk.Entry(form, textvariable=self.date_var, width=18).grid(row=1, column=2, padx=8)
        ttk.Entry(form, textvariable=self.units_var, width=18).grid(row=1, column=3, padx=8)
        ttk.Entry(form, textvariable=self.cost_var, width=18).grid(row=1, column=4, padx=8)

        ttk.Button(form, text="Add Record", command=self.add).grid(row=1, column=5, padx=10, pady=8)
        

        filters = ttk.LabelFrame(self.root, text="Search / Filter")
        filters.pack(fill="x", padx=15, pady=8)

        ttk.Label(filters, text="Appliance:").grid(row=0, column=0, padx=5, pady=8)
        ttk.Entry(filters, textvariable=self.search_var, width=18).grid(row=0, column=1)

        ttk.Label(filters, text="Period YYYY-MM:").grid(row=0, column=2, padx=5)
        ttk.Entry(filters, textvariable=self.period_var, width=15).grid(row=0, column=3)

        ttk.Button(filters, text="Apply Filter", command=self.apply_filter).grid(row=0, column=4, padx=8)
        ttk.Button(filters, text="Show All", command=self.refresh_table).grid(row=0, column=5, padx=8)
        ttk.Button(filters, text="Generate 2 Reports", command=self.make_reports).grid(row=0, column=6, padx=8)
        ttk.Button(filters,text="Delete Selected", command=self.delete_record).grid(row=0, column=7, padx=8)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("id", "appliance", "category", "date", "units", "cost")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {
            "id": "ID", "appliance": "Appliance", "category": "Category",
            "date": "Date", "units": "Units (kWh)", "cost": "Cost (₹)"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        summary = ttk.LabelFrame(self.root, text="Consumption Analysis")
        summary.pack(fill="x", padx=15, pady=8)

        self.summary_label = ttk.Label(summary, text="", font=("Arial", 11))
        self.summary_label.pack(padx=10, pady=8)

        ttk.Button(
            self.root, text="High-Usage Pattern", command=self.show_high_usage
        ).pack(pady=5)

    def add(self):
        try:
            record = add_record(
                self.appliance_var.get(),
                self.category_var.get(),
                self.date_var.get(),
                self.units_var.get(),
                self.cost_var.get()
            )
            self.records.append(record)
            messagebox.showinfo("Success", "Energy observation saved successfully.")
            self.clear_form()
            self.refresh_table()
            self.update_summary()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))

    def delete_record(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an appliance record first."
            )
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        record_id = values[0]
        appliance = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Do you want to delete this record?\n\n"
            f"ID: {record_id}\n"
            f"Appliance: {appliance}"
        )

        if not confirm:
            return

        try:
            delete_record_by_id(record_id)

            messagebox.showinfo(
                "Deleted",
                f"{appliance} record deleted successfully."
            )

            self.refresh_table()
            self.update_summary()

        except Exception as e:
            messagebox.showerror(
                "Delete Error",
                str(e)
            )

    def clear_form(self):
        self.appliance_var.set("")
        self.category_var.set("")
        self.units_var.set("")
        self.cost_var.set("")

    def refresh_table(self):
        self.records = load_records()
        self.show_records(self.records)

    def show_records(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in records:
            self.tree.insert(
                "", "end",
                values=(r["id"], r["appliance"], r["category"],
                        r["date"], r["units_kwh"], r["cost"])
            )

    def apply_filter(self):
        result = filter_records(
            self.records,
            appliance=self.search_var.get(),
            period=self.period_var.get()
        )
        self.show_records(result)

    def update_summary(self):
        summary = calculate_summary(self.records)
        compare = compare_appliances(self.records)

        top = compare.iloc[0]["appliance"] if not compare.empty else "N/A"
        top_units = compare.iloc[0]["units_kwh"] if not compare.empty else 0

        text = (
            f"Total Consumption: {summary['total_units']:.2f} kWh    |    "
            f"Average Consumption: {summary['average_units']:.2f} kWh    |    "
            f"Total Cost: ₹{summary['total_cost']:.2f}    |    "
            f"Highest-Use Appliance: {top} ({top_units:.2f} kWh)"
        )
        self.summary_label.config(text=text)

    def show_high_usage(self):
        result = find_high_usage(self.records)
        if result.empty:
            messagebox.showinfo("High Usage", "No records available.")
            return

        lines = []
        for _, row in result.iterrows():
            lines.append(
                f"{row['appliance']} - {row['units_kwh']:.2f} kWh "
                f"({row['date']})"
            )
        messagebox.showinfo(
            "High-Usage Patterns",
            "Records above the average consumption:\n\n" + "\n".join(lines)
        )

    def make_reports(self):
        try:
            paths = generate_reports(self.records)
            messagebox.showinfo(
                "Reports Generated",
                "Two meaningful reports were generated:\n\n"
                + "\n".join(paths)
            )
        except Exception as e:
            messagebox.showerror("Report Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyApp(root)
    root.mainloop()
