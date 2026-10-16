import tkinter as tk
from tkinter import ttk, messagebox


class StationeryOrderManagement:

    def __init__(self, root):
        self.root = root
        self.root.title("Stationery Order Management App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.stationery_items = {
            "NOTEBOOK": 3,
            "PENCIL PACK": 2,
            "PEN SET": 4,
            "ERASER": 1,
            "GEOMETRY BOX": 6,
            "COLOUR PENCILS": 5
        }

        self.exchange_rate = 82

        # Set up background
        self.setup_background()

        frame = ttk.Frame(root, padding=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(
            frame,
            text="Stationery Order Management",
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=15
        )

        self.item_labels = {}
        self.item_quantities = {}

        for index, (item, price) in enumerate(
            self.stationery_items.items(), start=1
        ):
            item_label = ttk.Label(
                frame,
                text=f"{item} (${price:.2f}):",
                font=("Arial", 12)
            )
            item_label.grid(
                row=index,
                column=0,
                sticky="w",
                padx=10,
                pady=5
            )

            self.item_labels[item] = item_label

            quantity_entry = ttk.Entry(frame, width=10)
            quantity_entry.grid(
                row=index,
                column=1,
                padx=10,
                pady=5
            )

            quantity_entry.insert(0, "0")
            self.item_quantities[item] = quantity_entry

        currency_row = len(self.stationery_items) + 1

        ttk.Label(
            frame,
            text="Currency:",
            font=("Arial", 12)
        ).grid(
            row=currency_row,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.currency_var = tk.StringVar(value="USD")

        currency_dropdown = ttk.Combobox(
            frame,
            textvariable=self.currency_var,
            state="readonly",
            width=10,
            values=("USD", "INR")
        )
        currency_dropdown.grid(
            row=currency_row,
            column=1,
            padx=10,
            pady=10
        )

        currency_dropdown.current(0)

        self.currency_var.trace_add(
            "write",
            self.update_item_prices
        )

        ttk.Button(
            frame,
            text="Place Order",
            command=self.place_order
        ).grid(
            row=currency_row + 1,
            column=0,
            columnspan=2,
            pady=10
        )

        ttk.Button(
            frame,
            text="Clear Order",
            command=self.clear_order
        ).grid(
            row=currency_row + 2,
            column=0,
            columnspan=2,
            pady=5
        )

    def setup_background(self):
        self.root.configure(bg="#e8f0f8")

        try:
            self.background_image = tk.PhotoImage(
                file="background.png"
            )

            width = self.background_image.width()
            height = self.background_image.height()

            scale_x = max(1, (width + 799) // 800)
            scale_y = max(1, (height + 599) // 600)

            self.background_image = self.background_image.subsample(
                scale_x, scale_y
            )

            background_label = tk.Label(
                self.root,
                image=self.background_image
            )
            background_label.place(
                x=0, y=0, relwidth=1, relheight=1
            )

        except (tk.TclError, OSError):
            self.root.configure(bg="#e8f0f8")

    def update_item_prices(self, *args):
        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        for item, label in self.item_labels.items():
            price = self.stationery_items[item] * rate

            label.config(
                text=f"{item} ({symbol}{price:.2f}):"
            )

    def place_order(self):
        total_cost = 0
        order_summary = "Stationery Order Summary:\n\n"
        has_order = False

        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        for item, entry in self.item_quantities.items():
            quantity_text = entry.get().strip()

            try:
                quantity = int(quantity_text)

                if quantity < 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Quantity",
                    f"Enter a valid non-negative whole number "
                    f"for {item}."
                )
                entry.focus_set()
                return

            if quantity > 0:
                has_order = True

                price = self.stationery_items[item] * rate
                cost = quantity * price
                total_cost += cost

                order_summary += (
                    f"{item}: {quantity} x "
                    f"{symbol}{price:.2f} = "
                    f"{symbol}{cost:.2f}\n"
                )

        if has_order:
            order_summary += (
                f"\nTotal Cost: {symbol}{total_cost:.2f}"
            )

            messagebox.showinfo(
                "Order Placed",
                order_summary
            )

        else:
            messagebox.showerror(
                "Error",
                "Please order at least one stationery item."
            )

    def clear_order(self):
        for entry in self.item_quantities.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")

if __name__ == "__main__":
    root = tk.Tk()
    app = StationeryOrderManagement(root)
    root.mainloop()
