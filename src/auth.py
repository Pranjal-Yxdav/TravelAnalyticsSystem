import sqlite3
import os
import customtkinter as ctk
from tkinter import messagebox


def register_user():

    window = ctk.CTkToplevel()

    window.title(
        "Register User"
    )

    window.geometry(
        "400x350"
    )

    ctk.CTkLabel(
        window,
        text="Register User",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    name_entry = ctk.CTkEntry(
        window,
        placeholder_text="Name",
        width=250
    )

    name_entry.pack(pady=10)

    email_entry = ctk.CTkEntry(
        window,
        placeholder_text="Email",
        width=250
    )

    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(
        window,
        placeholder_text="Password",
        show="*",
        width=250
    )

    password_entry.pack(pady=10)

    def save_user():

        name = name_entry.get()

        email = email_entry.get()

        password = password_entry.get()

        if not name or not email or not password:

            messagebox.showerror(
                "Error",
                "All fields are required"
            )

            return

        try:

            conn = sqlite3.connect(
                "database/travel.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO users
            (
                name,
                email,
                password
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                name,
                email,
                password
            ))

            conn.commit()

            conn.close()

            os.makedirs(
                f"reports/{name}",
                exist_ok=True
            )

            messagebox.showinfo(
                "Success",
                "Registration Successful"
            )

            window.destroy()

        except:

            messagebox.showerror(
                "Error",
                "User already exists"
            )

    ctk.CTkButton(
        window,
        text="Register",
        command=save_user
    ).pack(pady=20)


def login_user():

    login_window = ctk.CTkToplevel()

    login_window.title(
        "Login"
    )

    login_window.geometry(
        "400x300"
    )

    result = {
        "user": None
    }

    ctk.CTkLabel(
        login_window,
        text="User Login",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    email_entry = ctk.CTkEntry(
        login_window,
        placeholder_text="Email",
        width=250
    )

    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(
        login_window,
        placeholder_text="Password",
        show="*",
        width=250
    )

    password_entry.pack(pady=10)

    def verify_user():

        email = email_entry.get()

        password = password_entry.get()

        conn = sqlite3.connect(
            "database/travel.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE email=?
        AND password=?
        """,
        (
            email,
            password
        ))

        user = cursor.fetchone()

        conn.close()

        if user:

            result["user"] = user

            messagebox.showinfo(
                "Success",
                f"Welcome {user[1]}"
            )

            login_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Credentials"
            )

    ctk.CTkButton(
        login_window,
        text="Login",
        command=verify_user
    ).pack(pady=20)

    login_window.wait_window()

    return result["user"]

