import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import webbrowser
import os

from auth import register_user, login_user
from app import import_user_data

from analytics import (
    total_records,
    unique_places,
    calculate_distance,
    most_visited,
    user_history
)

from export_csv import export_results
from map_generator import generate_map
from visualization import generate_chart


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

current_user = None
current_user_name = None


def launch_gui():

    app = ctk.CTk()

    app.title("Travel Analytics System")

    app.geometry("1200x700")

    app.minsize(1200, 700)

    main_frame = ctk.CTkFrame(app)

    main_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    sidebar = ctk.CTkFrame(
        main_frame,
        width=220
    )

    sidebar.pack(
        side="left",
        fill="y",
        padx=5,
        pady=5
    )

    sidebar.pack_propagate(False)

    content = ctk.CTkFrame(main_frame)

    content.pack(
        side="right",
        fill="both",
        expand=True,
        padx=5,
        pady=5
    )

    title = ctk.CTkLabel(
        sidebar,
        text="🗺 Travel Analytics",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    status_label = ctk.CTkLabel(
        sidebar,
        text="Not Logged In",
        font=("Arial", 14)
    )

    status_label.pack(pady=10)

    cards_frame = ctk.CTkFrame(content)

    cards_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    def create_card(title_text):

        card = ctk.CTkFrame(
            cards_frame,
            width=180,
            height=100
        )

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        label = ctk.CTkLabel(
            card,
            text=f"{title_text}\n0",
            font=("Arial", 18)
        )

        label.pack(expand=True)

        return label

    records_card = create_card("Records")
    places_card = create_card("Places")
    distance_card = create_card("Distance")
    visits_card = create_card("Visits")

    history_label = ctk.CTkLabel(
        content,
        text="Recent Travel History",
        font=("Arial", 20, "bold")
    )

    history_label.pack(
        pady=(10, 5)
    )

    table_frame = ctk.CTkFrame(content)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    history_table = ttk.Treeview(
        table_frame,
        columns=(
            "Timestamp",
            "Latitude",
            "Longitude"
        ),
        show="headings"
    )

    history_table.heading(
        "Timestamp",
        text="Timestamp"
    )

    history_table.heading(
        "Latitude",
        text="Latitude"
    )

    history_table.heading(
        "Longitude",
        text="Longitude"
    )

    history_table.column(
        "Timestamp",
        width=250
    )

    history_table.column(
        "Latitude",
        width=150
    )

    history_table.column(
        "Longitude",
        width=150
    )

    history_table.pack(
        fill="both",
        expand=True
    )

    def refresh_dashboard():

        if current_user is None:
            return

        records_card.configure(
            text=f"Records\n{total_records(current_user)}"
        )

        places_card.configure(
            text=f"Places\n{unique_places(current_user)}"
        )

        distance_card.configure(
            text=f"Distance\n{calculate_distance(current_user)} KM"
        )

        place = most_visited(current_user)

        if place:

            visits_card.configure(
                text=f"Visits\n{place[1]}"
            )

        for item in history_table.get_children():

            history_table.delete(item)

        for row in user_history(current_user):

            history_table.insert(
                "",
                "end",
                values=row
            )

    def register():

        register_user()

    def login():

        global current_user
        global current_user_name

        user = login_user()

        if user:

            current_user = user[0]
            current_user_name = user[1]

            status_label.configure(
                text=f"Logged In\n{current_user_name}"
            )

            refresh_dashboard()

            messagebox.showinfo(
                "Success",
                f"Welcome {current_user_name}"
            )

    def import_csv_gui():

        if current_user is None:

            messagebox.showwarning(
                "Warning",
                "Please Login First"
            )

            return

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not file_path:
            return

        try:

            import_user_data(
                current_user,
                current_user_name,
                file_path
            )

            refresh_dashboard()

            messagebox.showinfo(
                "Success",
                "Data Imported Successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def export_csv_gui():

        if current_user is None:
            return

        file = export_results(
            current_user,
            current_user_name
        )

        messagebox.showinfo(
            "Export Complete",
            file
        )

    def map_gui():

        if current_user is None:
            return

        file = generate_map(
            current_user,
            current_user_name
        )

        if file:

            absolute_path = os.path.abspath(
                file
            )

            webbrowser.open(
                f"file:///{absolute_path}"
            )

    def chart_gui():

        if current_user is None:
            return

        generate_chart(
            current_user
        )

    def logout():

        global current_user
        global current_user_name

        current_user = None
        current_user_name = None

        status_label.configure(
            text="Not Logged In"
        )

        records_card.configure(
            text="Records\n0"
        )

        places_card.configure(
            text="Places\n0"
        )

        distance_card.configure(
            text="Distance\n0"
        )

        visits_card.configure(
            text="Visits\n0"
        )

        for item in history_table.get_children():

            history_table.delete(item)

    buttons = [
        ("Register", register),
        ("Login", login),
        ("Import CSV", import_csv_gui),
        ("Export CSV", export_csv_gui),
        ("Generate Map", map_gui),
        ("Show Chart", chart_gui),
        ("Logout", logout),
        ("Exit", app.destroy)
    ]

    for text, command in buttons:

        ctk.CTkButton(
            sidebar,
            text=text,
            command=command,
            width=180,
            height=40
        ).pack(
            pady=8,
            padx=10
        )

    app.mainloop()

