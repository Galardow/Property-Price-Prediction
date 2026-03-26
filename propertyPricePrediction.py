import tkinter as tk
from tkinter import messagebox
import numpy as np

class PropertyPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Property Price Prediction")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.nearby_size = []
        self.nearby_bedroom = []
        self.nearby_bathroom = []
        self.nearby_distance = []
        self.nearby_price = []

        self.create_widgets()

    def create_widgets(self):
        ref_frame = tk.LabelFrame(self.root, text="Tambahkan Data Referensi Sekitar", padx=10, pady=10)
        ref_frame.pack(padx=15, pady=10, fill="x")

        # Labels & Entries
        tk.Label(ref_frame, text="Size (m2):").grid(row=0, column=0, sticky="w")
        self.ent_ref_size = tk.Entry(ref_frame)
        self.ent_ref_size.grid(row=0, column=1, pady=3, padx=5)

        tk.Label(ref_frame, text="Bedroom total:").grid(row=1, column=0, sticky="w")
        self.ent_ref_bed = tk.Entry(ref_frame)
        self.ent_ref_bed.grid(row=1, column=1, pady=3, padx=5)

        tk.Label(ref_frame, text="Bathroom total:").grid(row=2, column=0, sticky="w")
        self.ent_ref_bath = tk.Entry(ref_frame)
        self.ent_ref_bath.grid(row=2, column=1, pady=3, padx=5)

        tk.Label(ref_frame, text="Distance to city (km):").grid(row=3, column=0, sticky="w")
        self.ent_ref_dist = tk.Entry(ref_frame)
        self.ent_ref_dist.grid(row=3, column=1, pady=3, padx=5)

        tk.Label(ref_frame, text="Price:").grid(row=4, column=0, sticky="w")
        self.ent_ref_price = tk.Entry(ref_frame)
        self.ent_ref_price.grid(row=4, column=1, pady=3, padx=5)

        self.btn_add_ref = tk.Button(ref_frame, text="Add Reference", command=self.add_reference, bg="#d9edf7")
        self.btn_add_ref.grid(row=5, column=0, columnspan=2, pady=10, ipadx=10)

        self.lbl_count = tk.Label(ref_frame, text="Total Reference Data Added: 0", fg="blue")
        self.lbl_count.grid(row=6, column=0, columnspan=2)

        your_frame = tk.LabelFrame(self.root, text="Your Property Data", padx=10, pady=10)
        your_frame.pack(padx=15, pady=10, fill="x")

        tk.Label(your_frame, text="Your Size (m2):").grid(row=0, column=0, sticky="w")
        self.ent_your_size = tk.Entry(your_frame)
        self.ent_your_size.grid(row=0, column=1, pady=3, padx=5)

        tk.Label(your_frame, text="Your Bedroom total:").grid(row=1, column=0, sticky="w")
        self.ent_your_bed = tk.Entry(your_frame)
        self.ent_your_bed.grid(row=1, column=1, pady=3, padx=5)

        tk.Label(your_frame, text="Your Bathroom total:").grid(row=2, column=0, sticky="w")
        self.ent_your_bath = tk.Entry(your_frame)
        self.ent_your_bath.grid(row=2, column=1, pady=3, padx=5)

        tk.Label(your_frame, text="Your Distance to city (km):").grid(row=3, column=0, sticky="w")
        self.ent_your_dist = tk.Entry(your_frame)
        self.ent_your_dist.grid(row=3, column=1, pady=3, padx=5)

        self.btn_predict = tk.Button(your_frame, text="Predict Price", command=self.predict_price, bg="#dff0d8", font=("Arial", 10, "bold"))
        self.btn_predict.grid(row=4, column=0, columnspan=2, pady=15, ipadx=20)

        self.lbl_result = tk.Label(self.root, text="Price Predicted: -", font=("Arial", 14, "bold"), fg="green")
        self.lbl_result.pack(pady=5)

    def add_reference(self):
        try:
            size = float(self.ent_ref_size.get())
            bed = float(self.ent_ref_bed.get())
            bath = float(self.ent_ref_bath.get())
            dist = float(self.ent_ref_dist.get())
            price = float(self.ent_ref_price.get())

            self.nearby_size.append(size)
            self.nearby_bedroom.append(bed)
            self.nearby_bathroom.append(bath)
            self.nearby_distance.append(dist)
            self.nearby_price.append(price)

            total_data = len(self.nearby_size)
            self.lbl_count.config(text=f"Total Reference Data Added: {total_data}")

            self.ent_ref_size.delete(0, tk.END)
            self.ent_ref_bed.delete(0, tk.END)
            self.ent_ref_bath.delete(0, tk.END)
            self.ent_ref_dist.delete(0, tk.END)
            self.ent_ref_price.delete(0, tk.END)

            self.ent_ref_size.focus()

        except ValueError:
            messagebox.showerror("Input Error", "Please make sure to fill the field using numerical data.")

    def predict_price(self):
        if len(self.nearby_size) == 0:
            messagebox.showwarning("Data is Empty", "Please add at least 1 reference.")
            return

        try:
            your_size = float(self.ent_your_size.get())
            your_bed = float(self.ent_your_bed.get())
            your_bath = float(self.ent_your_bath.get())
            your_dist = float(self.ent_your_dist.get())

            nearbyData = np.column_stack([
                np.ones(len(self.nearby_size)), 
                self.nearby_size, 
                self.nearby_bedroom, 
                self.nearby_bathroom, 
                self.nearby_distance
            ])
            nearbyPrice = np.array(self.nearby_price)

            yourProperty = np.array([1, your_size, your_bed, your_bath, your_dist])

            prediction = np.linalg.lstsq(nearbyData, nearbyPrice, rcond=None)[0]
            
            final_price = np.round(prediction @ yourProperty, 2)

            self.lbl_result.config(text=f"Predicted Price: {final_price}")

        except ValueError:
            messagebox.showerror("Input Error", "Please make sure to fill the field using numerical data.")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PropertyPredictorApp(root)
    root.mainloop()