import tkinter as tk
from tkinter import ttk
import csv

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Onion Web Crawl Results Viewer")
root.geometry("1400x600")

# ---------------- COLUMNS ----------------
columns = [
    "Crawl Timestamp",
    "URL",
    "Title",
    "Content Preview",
    "Site Type",
    "Detected Keywords",
    "Risk Level",
    "Status"
]

# ---------------- TREEVIEW ----------------
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180, anchor="w")

# Adjust column widths for readability
tree.column("URL", width=300)
tree.column("Content Preview", width=500)
tree.column("Detected Keywords", width=250)

tree.pack(fill=tk.BOTH, expand=True)

# ---------------- SCROLLBARS ----------------
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

vsb.pack(side=tk.RIGHT, fill=tk.Y)
hsb.pack(side=tk.BOTTOM, fill=tk.X)

# ---------------- ROW COLORS ----------------
tree.tag_configure("HIGH", background="#ffcccc")     # Red
tree.tag_configure("MEDIUM", background="#fff2cc")   # Yellow
tree.tag_configure("LOW", background="#ccffcc")      # Green
tree.tag_configure("FAILED", background="#e6e6e6")   # Grey

# ---------------- LOAD TSV ----------------
def load_data():
    try:
        with open("output.tsv", "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter="\t")
            next(reader, None)  # skip header

            for row in reader:
                if len(row) != len(columns):
                    continue

                risk = row[6]
                status = row[7]

                if status == "Failed":
                    tag = "FAILED"
                elif risk == "High":
                    tag = "HIGH"
                elif risk == "Medium":
                    tag = "MEDIUM"
                else:
                    tag = "LOW"

                tree.insert("", tk.END, values=row, tags=(tag,))
    except FileNotFoundError:
        print("output.tsv not found. Run crawler first.")

load_data()

# ---------------- RUN ----------------
root.mainloop()
