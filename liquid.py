import os
import subprocess
import sys
import threading
from libs.mods import *
from Util.main import PCOptimizer
from PIL import Image
import customtkinter as ctk


class GradientLabel(ctk.CTkCanvas):
    def __init__(self, parent, text, font=("Arial", 20, "bold"), gradient_colors=["#A855F7", "#800020"], **kwargs):
        self.text = text
        self.font = font
        self.colors = gradient_colors

        # Temporarily create a dummy font object to measure text
        from tkinter.font import Font
        self.tk_font = Font(family=self.font[0], size=self.font[1], weight=self.font[2] if len(self.font) > 2 else "normal")

        # Dynamically compute total width
        total_width = sum([self.tk_font.measure(char) for char in self.text])
        super().__init__(parent, width=total_width + 20, height=40, bg="#0D0D0D", highlightthickness=0, **kwargs)

        self.draw_gradient_text()

    def draw_gradient_text(self):
        try:
            steps = len(self.text)
            r1, g1, b1 = self.winfo_rgb(self.colors[0])
            r2, g2, b2 = self.winfo_rgb(self.colors[1])

            x = 10  # left padding
            for i, char in enumerate(self.text):
                r = int(r1 + (r2 - r1) * i / steps) >> 8
                g = int(g1 + (g2 - g1) * i / steps) >> 8
                b = int(b1 + (b2 - b1) * i / steps) >> 8
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.create_text(x, 20, text=char, font=self.tk_font, fill=color, anchor="w")
                x += self.tk_font.measure(char)

        except Exception as e:
            print(f"[!] Failed to draw gradient text: {e}")
            logging.debug(f"Fao;ed to draw Graidient text {e}")


class LoadingScreen(ctk.CTk):
    def __init__(self, on_finish_callback, logo_path=None):
        super().__init__()
        self.title("Liquid Tweaker")
        self.geometry("400x380")
        self.configure(fg_color="#0D0D0D")
        self.resizable(False, False)

        if logo_path:
            try:
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(150, 150))
                self.logo_label = ctk.CTkLabel(self, image=logo_img, text="")
                self.logo_label.pack(pady=(20, 5))
            except Exception as e:
                print(f"[!] Logo load failed: {e}")
                logging.debug(f"Loading Screen image load failed {e}")

        self.gradient_title = GradientLabel(self, text="Liquid Labsr", font=("Arial", 20, "bold"))


        self.status_label = ctk.CTkLabel(self, text="Preparing launch...", font=("Arial", 14), text_color="#A855F7")
        self.status_label.pack(pady=(30, 10))

        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", width=220, progress_color="#A855F7")
        self.progress.pack(pady=(10, 10))
        self.progress.set(0)

        self.on_finish_callback = on_finish_callback
        self.after(300, self.install_and_load)

    def install_and_load(self):
        self.install_requirements(lambda: self.animate_progress())

    def install_requirements(self, callback):
        req_path = os.path.join("assets", "requirements.txt")
        if not os.path.exists(req_path):
            self.status_label.configure(text="[!] requirements.txt not found.")
            self.after(2000, callback)
            return

        with open(req_path, "r") as f:
            modules = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        self.current_module = 0
        self.modules = modules
        self.total_modules = len(modules)
        self.run_next_install(callback)

    def run_next_install(self, callback):
        if self.current_module >= self.total_modules:
            self.status_label.configure(text="Modules loaded ✔")
            self.after(500, callback)
            return

        module = self.modules[self.current_module]
        self.status_label.configure(text=f"Installing {module}...")

        def install_module():
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", module, "--user"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.after(0, lambda: self.status_label.configure(text=f"Installed {module} ✔"))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"[!] Failed: {module}"))

            self.current_module += 1
            self.after(600, lambda: self.run_next_install(callback))

        threading.Thread(target=install_module, daemon=True).start()

    def animate_progress(self):
        progress = self.progress.get()
        if progress < 1.0:
            self.progress.set(progress + 0.02)
            self.after(50, self.animate_progress)
        else:
            self.destroy()
            self.on_finish_callback()



if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    def launch_dashboard():
        app = PCOptimizer()
        app.mainloop()

    loading = LoadingScreen(on_finish_callback=launch_dashboard, logo_path="assets/logo.png")
    loading.mainloop()
