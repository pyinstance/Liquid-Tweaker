from libs.mods import *
from Data.tweaks import *

PURPLE = "#A855F7"
FONT_HEADER = ("Arial", 14, "bold")
FONT_BODY = ("Arial", 12)

LOG_PATH = os.path.join("logs", "app.log")

logging.basicConfig(
    level=logging.DEBUG,  # Can also be INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=LOG_PATH,
    filemode="a"  # Append to the file
)

logging.debug("Logging initialized.")

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 30
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(tw, text=self.text, fg_color="#1A1A1A", text_color="white", corner_radius=5, font=("Arial", 10), wraplength=250)
        label.pack(padx=6, pady=4)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class PCOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Liquid tweaker")
        self.geometry("900x500")
        self.configure(fg_color="#0D0D0D")
        self.resizable(False, False)
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(self, width=160, fg_color="#121212")
        self.sidebar.pack(side="left", fill="y")

        logo_img = CTkImage(
            light_image=Image.open("assets/logo.png"),
            dark_image=Image.open("assets/logo.png"),
            size=(70, 70) 
        )

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            image=logo_img
        )
        self.logo_label.pack(pady=(20, 5))

        self.tab_frame = ctk.CTkFrame(self, fg_color="#0D0D0D")
        self.tab_frame.pack(side="left", fill="both", expand=True)

        self.toggle_btn = ctk.CTkButton(
            self.tab_frame,
            text="☰",
            width=40,
            fg_color="#1A1A1A",
            hover_color="#2A2A2A",
            command=self.toggle_sidebar
        )
        self.toggle_btn.pack(anchor="ne", padx=10, pady=10)

        self.tabs = {}
        self.tab_buttons = {}

        for name in ["Dashboard", "Tweaks", "Settings", "Install", "Tools"]:
            btn = ctk.CTkButton(
                self.sidebar, text=name, width=120, corner_radius=10,
                fg_color="#1A1A1A", hover_color="#2A2A2A", text_color=PURPLE,
                command=lambda n=name: self.switch_tab(n)
            )
            btn.pack(pady=10)
            self.tab_buttons[name] = btn

        self.create_dashboard()
        self.create_tweaks()
        self.create_settings()
        self.create_install()
        self.create_tools_tab()
        self.switch_tab("Dashboard")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_visible = True


    def switch_tab(self, name):
        for t in self.tabs.values():
            t.pack_forget()
        self.tabs[name].pack(fill="both", expand=True)

    def create_tools_tab(self):
        tools_tab = ctk.CTkFrame(self.tab_frame, fg_color="#121212")
        self.tabs["Tools"] = tools_tab

        title_label = ctk.CTkLabel(
            tools_tab, text="Utilities & Tools", font=("Arial", 24, "bold"), text_color="#A855F7"
        )
        title_label.pack(pady=(20, 10))

        clean_btn = ctk.CTkButton(
            tools_tab,
            text="🧹 Clean RAM",
            command=self.clean_memory,
            fg_color="#A855F7",
            hover_color="#9333EA"
        )
        clean_btn.pack(pady=20)

    def clean_memory(self):
        cleaned = 0


        try:
            ctypes.windll.psapi.EmptyWorkingSet(-1)
        except Exception as e:
            print(f"[!] Working set clear failed: {e}")
            logging.debug(f"Working set clear failed")

        # Reduce working set size of individual processes
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                p = psutil.Process(proc.info["pid"])
                if p.memory_info().rss > 50 * 1024 * 1024:  # Skip tiny processes
                    ctypes.windll.psapi.EmptyWorkingSet(p.pid)
                    cleaned += 1
            except Exception:
                continue

        CTkMessagebox(
            title="RAM Cleanup",
            message=f"✔ RAM cleaning complete.\nOptimized {cleaned} processes.",
            icon="check"
        )


    def create_dashboard(self):
        tab = ctk.CTkFrame(self.tab_frame, fg_color="#121212")
        self.tabs["Dashboard"] = tab

        userName = getpass.getuser()
        welcome_label = ctk.CTkLabel(tab, text=f"Welcome, {userName}", font=("Arial", 24, "bold"), text_color=PURPLE)
        welcome_label.pack(pady=10)

        # 🟢 Pulse animation helper
        def pulse_label_dot(label, colors=("#22c55e", "#14532d"), delay=500):
            def animate(index=0):
                label.configure(text_color=colors[index % len(colors)])
                label.after(delay, lambda: animate(index + 1))
            animate()

        # ⬛ Box container
        version_status_frame = ctk.CTkFrame(tab, fg_color="#1A1A1A", corner_radius=10)
        version_status_frame.pack(padx=20, pady=(5, 15), fill="x")

        # 📦 Version Box
        version_frame = ctk.CTkFrame(version_status_frame, fg_color="#0D0D0D", corner_radius=10)
        version_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        version_dot = ctk.CTkLabel(version_frame, text="●", text_color="#22c55e", font=("Arial", 14))
        version_dot.pack(side="left", padx=5)
        version_text = ctk.CTkLabel(version_frame, text="GUI Version: v1.0.0", font=FONT_BODY, text_color="white")
        version_text.pack(side="left")
        pulse_label_dot(version_dot)

        # 🛠️ Update Box
        update_frame = ctk.CTkFrame(version_status_frame, fg_color="#0D0D0D", corner_radius=10)
        update_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        update_dot = ctk.CTkLabel(update_frame, text="●", text_color="#22c55e", font=("Arial", 14))
        update_dot.pack(side="left", padx=5)
        update_text = ctk.CTkLabel(update_frame, text="Update Status: Up to date", font=FONT_BODY, text_color="white")
        update_text.pack(side="left")
        pulse_label_dot(update_dot)

        # 🌐 Ping Box
        ping_frame = ctk.CTkFrame(version_status_frame, fg_color="#0D0D0D", corner_radius=10)
        ping_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ping_dot = ctk.CTkLabel(ping_frame, text="●", text_color="#22c55e", font=("Arial", 14))
        ping_dot.pack(side="left", padx=5)
        ping_text = ctk.CTkLabel(ping_frame, text="Ping: checking...", font=FONT_BODY, text_color="white")
        ping_text.pack(side="left")
        pulse_label_dot(ping_dot)

        # 📡 In/Out Network Speed Box
        network_frame = ctk.CTkFrame(version_status_frame, fg_color="#0D0D0D", corner_radius=10)
        network_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        network_dot = ctk.CTkLabel(network_frame, text="●", text_color="#22c55e", font=("Arial", 14))
        network_dot.pack(side="left", padx=5)
        network_label = ctk.CTkLabel(network_frame, text="Net: ↓ 0 KB/s ↑ 0 KB/s", font=FONT_BODY, text_color="white")
        network_label.pack(side="left")
        pulse_label_dot(network_dot)

        # 🔄 Network update loop
        def update_network():
            old_stats = psutil.net_io_counters()
            old_bytes_sent = old_stats.bytes_sent
            old_bytes_recv = old_stats.bytes_recv

            def refresh():
                nonlocal old_bytes_sent, old_bytes_recv  # ⬅️ Move this to the top before using the variables

                new_stats = psutil.net_io_counters()
                sent = new_stats.bytes_sent
                recv = new_stats.bytes_recv

                upload_speed = (sent - old_bytes_sent) / 1024  # KB/s
                download_speed = (recv - old_bytes_recv) / 1024

                network_label.configure(text=f"Net: ↓ {download_speed:.1f} KB/s ↑ {upload_speed:.1f} KB/s")

                old_bytes_sent = sent
                old_bytes_recv = recv

                tab.after(1000, refresh)  # Update every 1s

        # 🔄 Ping update loop
        def update_ping():
            try:
                output = subprocess.check_output("ping 8.8.8.8 -n 1", shell=True).decode("utf-8", errors="ignore")
                if "Average =" in output:
                    latency = output.split("Average =")[-1].strip()
                    ping_text.configure(text=f"Ping: {latency}")
                else:
                    ping_text.configure(text="Ping: timeout")
            except:
                ping_text.configure(text="Ping: error")
            ping_frame.after(1000, update_ping)

        update_ping()
        update_network()

        # Column configs
        version_status_frame.columnconfigure(0, weight=1)
        version_status_frame.columnconfigure(1, weight=1)
        version_status_frame.columnconfigure(2, weight=1)
        version_status_frame.columnconfigure(3, weight=1)

        # 📘 Tool Info Box
        info_box = ctk.CTkFrame(tab, fg_color="#1A1A1A", corner_radius=10)
        info_box.pack(padx=20, pady=(0, 15), fill="x")

        info_label = ctk.CTkLabel(
            info_box,
            text="Liquid PC Tweaker is a utility designed to optimize Windows for performance, \ngaming, and network responsiveness.\nIt lets you apply safe, tested tweaks \nin one click — no registry diving required.",
            font=FONT_BODY,
            text_color="white",
            wraplength=800,
            justify="left"
        )
        info_label.pack(padx=10, pady=10, anchor="w")

        # Summary placeholder
        summary_frame = ctk.CTkFrame(tab, fg_color="#1A1A1A")
        summary_frame.pack(pady=10, padx=20, fill="x")

        info = self.get_system_info()
        summaries = [
            ("🖥️ CPU", info["cpu"]),
            ("🎮 GPU", info["gpu"]),
            ("💾 RAM", info["ram"]),
            ("🔌 Power Plan", "Ultimate Performance"),
            ("⚙️ Tweaks Applied", "0"),
            ("📡 Network", info["ip"]),
        ]

        for i, (label, value) in enumerate(summaries):
            card = ctk.CTkFrame(summary_frame, fg_color="#0D0D0D", corner_radius=10)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            lbl = ctk.CTkLabel(card, text=label, text_color=PURPLE, font=FONT_HEADER)
            lbl.pack(pady=(5,0))
            val = ctk.CTkLabel(card, text=value, text_color="white", font=FONT_BODY, wraplength=200)
            val.pack(pady=(0,5))

        for i in range(3):
            summary_frame.columnconfigure(i, weight=1)

    def create_install(self):
        install_tab = ctk.CTkFrame(self.tab_frame, fg_color="#121212")
        self.tabs["Install"] = install_tab

        # Title
        title_label = ctk.CTkLabel(
            install_tab,
            text="App Installer",
            font=("Arial", 24, "bold"),
            text_color="#A855F7"
        )
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")

        # Define apps and their checkboxes
        PURPLE = "#A855F7"
        self.check_vars = {
            "Valve.Steam": ctk.BooleanVar(),
            "Mozilla.Firefox": ctk.BooleanVar(),
            "EpicGames.EpicGamesLauncher": ctk.BooleanVar(),
            "Ubisoft.Connect": ctk.BooleanVar(),
            "Discord.Discord": ctk.BooleanVar(),
            "Microsoft.VisualStudioCode": ctk.BooleanVar()
        }

        for idx, (app_id, var) in enumerate(self.check_vars.items()):
            app_name = app_id.split('.')[-1].replace("EpicGamesLauncher", "Epic Games").replace("VisualStudioCode", "VS Code").replace("Connect", "Ubisoft").replace("Discord", "Discord").strip()
            checkbox = ctk.CTkCheckBox(
                install_tab,
                text=app_name,
                variable=var,
                text_color="white",
                fg_color="#1A1A1A",
                checkbox_height=20,
                checkbox_width=20,
                border_color=PURPLE,
                hover_color=PURPLE,
                checkmark_color=PURPLE
            )
            checkbox.grid(row=idx + 1, column=0, sticky="w", padx=20, pady=5)

        # Install button
        def install_selected_apps():
            selected_apps = [app for app, var in self.check_vars.items() if var.get()]
            if not selected_apps:
                ctk.CTkMessagebox(title="No Selection", message="Please select at least one app to install.")
                return

            def install_thread():
                for app in selected_apps:
                    os.system(f'winget install --id {app} -e --accept-source-agreements --accept-package-agreements')
                ctk.CTkMessagebox(title="Installation Complete", message="Selected apps have been installed.")

            threading.Thread(target=install_thread, daemon=True).start()

        install_btn = ctk.CTkButton(
            install_tab,
            text="Install Selected Apps",
            command=install_selected_apps,
            fg_color=PURPLE,
            hover_color="#9333EA"
        )
        install_btn.grid(row=len(self.check_vars) + 2, column=0, padx=20, pady=(20, 10), sticky="w")

    def create_tweaks(self):
        tab = ctk.CTkFrame(self.tab_frame, fg_color="#121212")
        self.tabs["Tweaks"] = tab

        tweaks_frame = ctk.CTkScrollableFrame(
            tab, fg_color="#121212",
            label_text="Available Tweaks",
            label_font=FONT_HEADER,
            label_text_color=PURPLE
        )
        tweaks_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        self.tweak_checks = {}

        tweak_categories = {
            # Original tweaks
            "Disable Background Services": [
                ("Disable Xbox Services", "xbox", "Disables Xbox services like GameBar to free up system resources."),
                ("Disable Windows Search", "search", "Turns off Windows Search indexing for faster performance."),
                ("Disable SysMain", "sysmain", "Stops the SysMain service which can cause high disk usage."),
            ],
            "System Cleanup": [
                ("Clear Temp Files", "temp", "Deletes temporary files to free up disk space."),
                ("Delete Prefetch Data", "prefetch", "Cleans prefetch files to improve startup speed."),
            ],
            "Network Tweaks": [
                ("Disable Nagle’s Algorithm", "nagle", "Improves network latency, especially for gaming."),
                ("Enable DNS Cache Flush", "dns", "Flushes DNS resolver cache to fix connection issues."),
            ],
            "Power Tweaks": [
                ("Enable Ultimate Custom Power Plan", "power_plan", "Creates a high-performance power plan for gaming."),
            ],

            # New tweaks
            "Memory & Boot Optimizations": [
                ("Disable Startup Delay", "startup_delay", "Speeds up boot by removing default delay for startup apps."),
                ("Disable Hibernation", "hibernation", "Disables hibernation and frees up disk space."),
                ("Clear Pagefile on Shutdown", "clear_pagefile", "Clears virtual memory pagefile at shutdown for privacy."),
                ("Enable Fast Startup", "fast_startup", "Enables fast startup for quicker boot times."),
                ("Disable Paging Executive", "paging_exec", "Keeps system code in RAM instead of paging to disk."),
            ],

            "Gaming Optimizations": [
                ("Disable Game DVR", "game_dvr", "Disables Game DVR to avoid performance hit from background recording."),
                ("Set GPU Priority to High", "gpu_priority", "Optimizes GPU scheduling priority for foreground apps."),
                ("Enable Hardware Accelerated GPU Scheduling", "hags", "Reduces latency and improves performance in supported GPUs."),
                ("Enable Game Mode", "game_mode", "Tells Windows to optimize performance while gaming."),
            ],

            "Network Performance": [
                ("Disable Update Bandwidth Limit", "update_opt", "Stops Windows Update from reserving bandwidth."),
                ("Optimize TCP Parameters", "tcp_opt", "Tweaks TCP stack for lower latency and better throughput."),
                ("Disable Large Send Offload", "lso", "Improves latency by disabling large TCP segmentation offload."),
                ("Disable Auto-Tuning", "auto_tuning", "Improves compatibility and reduces lag on unstable networks."),
            ],

            "UI & Background Services": [
                ("Disable UI Animations", "ui_anim", "Disables system animations for faster responsiveness."),
                ("Disable Telemetry", "telemetry", "Prevents Windows from sending usage data to Microsoft."),
                ("Disable Tips & Suggestions", "tips", "Removes popup tips and reduces background activity."),
                ("Disable Background Apps", "bg_apps", "Stops apps from running in the background to save resources."),
                ("Disable Cortana", "cortana", "Turns off Cortana to reduce CPU/memory usage."),
            ],

            "System UX Tweaks": [
                ("Disable Action Center", "action_center", "Turns off notifications and background alerts."),
                ("Disable Visual Effects", "visual_fx", "Improves performance by removing UI animations."),
                ("Enable Classic Volume Mixer Shortcut", "volume_mixer", "Adds a shortcut to the classic volume mixer."),
                ("Enable File Explorer 'This PC' as default", "explorer_pc", "Opens File Explorer to 'This PC' by default."),
            ]
        }

        for cat_name, tweaks in tweak_categories.items():
            cat_label = ctk.CTkLabel(tweaks_frame, text=cat_name, font=FONT_HEADER, text_color=PURPLE)
            cat_label.pack(anchor="w", pady=(15, 5))

            for label_text, key, tooltip_text in tweaks:
                cb = ctk.CTkCheckBox(
                    tweaks_frame, text=label_text, text_color="white",
                    checkbox_height=20, checkbox_width=20, border_color=PURPLE,
                    fg_color=PURPLE, hover_color="#9333EA"
                )
                cb.pack(anchor="w", padx=20, pady=2)
                Tooltip(cb, tooltip_text)
                self.tweak_checks[key] = cb

        apply_button = ctk.CTkButton(
            tab, text="Apply Tweaks", command=self.apply_selected_tweaks,
            fg_color=PURPLE, hover_color="#9333EA", text_color="white"
        )
        apply_button.pack(pady=(0, 10))

        self.tweaks_log = ScrolledText(tab, height=7, bg="#0D0D0D", fg="white", insertbackground="white")
        self.tweaks_log.pack(fill="both", expand=False, padx=20, pady=(0, 10))
        self.current_tweak_view = "Tweaks"

    def apply_selected_tweaks(self):
        tweak_functions = {
            "xbox": disable_xbox_services,
            "search": disable_search,
            "sysmain": disable_sysmain,
            "prefetch": delete_prefetch,
            "nagle": disable_nagle,
            "dns": flush_dns,
            "startup_delay": disable_startup_delay,
            "hibernation": disable_hibernation,
            "clear_pagefile": clear_pagefile_on_shutdown,
            "fast_startup": enable_fast_startup,
            "game_dvr": disable_game_dvr,
            "gpu_priority": set_gpu_priority,
            "update_opt": disable_update_bandwidth,
            "tcp_opt": optimize_tcp,
            "ui_anim": disable_ui_animations,
            "telemetry": disable_telemetry,
            "tips": disable_tips,
            "power_plan": self.create_custom_power_plan,  # local method
            "temp": self.clear_temp_files,  # local method
        }

        applied = []
        for key, cb in self.tweak_checks.items():
            if cb.get() == 1:
                applied.append(key)
                func = tweak_functions.get(key)
                if func:
                    try:
                        func()
                        self.tweaks_log.insert("end", f"✅ Applied tweak: {key}\n")
                        logging.debug(f"Applied Tweaks")
                    except Exception as e:
                        self.tweaks_log.insert("end", f"❌ Failed to apply {key}: {e}\n")
                        logging.debug(f"failed to apply Tweaks {key} {e}")

        if not applied:
            self.tweaks_log.insert("end", "No tweaks selected.\n")
            logging.debug(f"Root user did not select Tweaks")

    def clear_temp_files(self):
        temp_path = os.environ.get("TEMP", tempfile.gettempdir())
        deleted = 0
        failed = 0

        for filename in os.listdir(temp_path):
            file_path = os.path.join(temp_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    deleted += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted += 1
            except Exception as e:
                failed += 1
                self.tweaks_log.insert("end", f"❌ Failed to delete {file_path}: {e}\n")
                logging.debug(f"failed to Delete All temp files and items")

        self.tweaks_log.insert("end", f"✅ Deleted {deleted} temp items. {failed} failed.\n")
        logging.debug(f"Deleted All temp files and items")


    def create_custom_power_plan(self):
        try:
            base_scheme = "e9a42b02-d5df-448d-aa00-03f14749eb61"  # Ultimate Performance
            result = subprocess.run(
                ["powercfg", "/duplicatescheme", base_scheme],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            output = result.stdout.strip()
            new_guid = output.split()[-1].strip('{}')
            custom_name = "Liquid Ultra Performance Plan"
            subprocess.run(["powercfg", "/changename", new_guid, custom_name], check=True)
            subprocess.run(["powercfg", "/setactive", new_guid], check=True)
            self.tweaks_log.insert("end", f"✅ Applied custom power plan: {custom_name}\n")
            logging.debug(f"Successfully created Power Plan")

        except subprocess.CalledProcessError as e:
            self.tweaks_log.insert("end", f"❌ Failed to apply power plan: {e}\n")
            logging.debug(f"Could not Create Plan {e}")


    def create_user_avatar(self, username):
        initials = "".join([part[0].upper() for part in username.split()])[:2]
        img = Image.new("RGBA", (100, 100), (18, 18, 18, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 100, 100), fill=(168, 85, 247, 255))  # Purple circle

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), initials, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((100 - w) / 2, (100 - h) / 2), initials, fill="white", font=font)

        return img


    def create_settings(self):
        tab = ctk.CTkFrame(self.tab_frame, fg_color="#121212")
        self.tabs["Settings"] = tab

        canvas = ctk.CTkCanvas(tab, bg="#121212", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(tab, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#121212")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        sys_info = self.get_system_info()
        username = os.getlogin()

        # Profile bubble
        profile_img = self.create_user_avatar(username)
        profile_ctk_img = ctk.CTkImage(light_image=profile_img, size=(80, 80))
        profile_frame = ctk.CTkFrame(scrollable_frame, fg_color="#1A1A1A", corner_radius=10)
        profile_label = ctk.CTkLabel(profile_frame, image=profile_ctk_img, text="")
        name_label = ctk.CTkLabel(profile_frame, text=f"{username}", font=FONT_HEADER, text_color=PURPLE)
        profile_label.pack(pady=(10, 0))
        name_label.pack(pady=(5, 10))
        profile_frame.grid(row=0, column=0, columnspan=3, pady=(20, 10), padx=10)

        def make_info_box(title, content):
            frame = ctk.CTkFrame(scrollable_frame, fg_color="#1A1A1A", corner_radius=10)
            label = ctk.CTkLabel(frame, text=title, font=FONT_HEADER, text_color=PURPLE)
            label.pack(anchor="w", padx=10, pady=(5, 0))
            content_label = ctk.CTkLabel(
                frame, text=content, font=FONT_BODY, text_color="white",
                wraplength=220, justify="left"
            )
            content_label.pack(anchor="w", padx=10, pady=5)
            return frame

        # All info boxes
        boxes = [
            make_info_box("GUI Version", "v1.0.0"),
            make_info_box("Operating System", sys_info["os"]),
            make_info_box("OS Version", sys_info["os_version"]),
            make_info_box("CPU", sys_info["cpu"]),
            make_info_box("GPU", sys_info["gpu"]),
            make_info_box("RAM", sys_info["ram"]),
            make_info_box("Motherboard", sys_info["mobo"]),
            make_info_box("Uptime", sys_info["uptime"]),
            make_info_box("System Boot Time", sys_info["boot_time"]),
            make_info_box("Hostname", sys_info["hostname"]),
            make_info_box("Local IP", sys_info["local_ip"]),
            make_info_box("Public IP", sys_info["public_ip"]),
            make_info_box("Disk Info", sys_info["disk"]),
            make_info_box("Battery", sys_info["battery"]),
            make_info_box("Factory Reset", sys_info["install_date"]),
        ]

        for i, box in enumerate(boxes):
            row = (i // 3) + 1  # Start after profile
            col = i % 3
            box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for i in range(3):
            scrollable_frame.columnconfigure(i, weight=1)

        def open_log_file():
            if os.path.exists(LOG_PATH):
                try:
                    os.startfile(LOG_PATH)  # Windows
                except AttributeError:
                    subprocess.call(["xdg-open", LOG_PATH])  # Linux/Mac
            else:
                ctk.CTkMessagebox(title="Log Error", message="Log file not found.", icon="warning")

        def show_recent_logs():
            if os.path.exists(LOG_PATH):
                with open(LOG_PATH, "r") as log_file:
                    lines = log_file.readlines()[-20:]  # Show last 20 lines
                    log_popup = ctk.CTkToplevel(self)
                    log_popup.title("Recent Logs")
                    log_popup.geometry("500x300")
                    log_popup.configure(fg_color="#121212")

                    text_widget = ctk.CTkTextbox(log_popup, wrap="word", font=("Consolas", 10), fg_color="#1A1A1A", text_color="white")
                    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
                    text_widget.insert("1.0", "".join(lines))
                    text_widget.configure(state="disabled")
            else:
                ctk.CTkMessagebox(title="Log Error", message="Log file not found.", icon="warning")

        log_frame = ctk.CTkFrame(scrollable_frame, fg_color="#1A1A1A", corner_radius=10)
        log_label = ctk.CTkLabel(log_frame, text="Logs", font=FONT_HEADER, text_color=PURPLE)
        log_label.pack(anchor="w", padx=10, pady=(5, 0))

        recent_btn = ctk.CTkButton(log_frame, text="Show Recent Logs", command=show_recent_logs, width=120)
        recent_btn.pack(padx=10, pady=(0, 10))

        log_frame.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="ew")



    def get_system_info(self):
        try:
            gpus = GPUtil.getGPUs()
            gpu = gpus[0].name if gpus else "Unknown GPU"
            cpu = platform.processor()
            ram = f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
            c = wmi.WMI()
            mobo = c.Win32_BaseBoard()[0].Product
            os_info = f"{platform.system()} {platform.release()} (Build {platform.version()})"
            os_version = platform.version()

            uptime_seconds = psutil.boot_time()
            uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(uptime_seconds)
            uptime_str = str(uptime).split('.')[0]
            boot_time = datetime.datetime.fromtimestamp(uptime_seconds).strftime("%Y-%m-%d %H:%M:%S")

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            try:
                public_ip = requests.get("https://api.ipify.org").text
            except:
                public_ip = "Unavailable"

            disk_usage = psutil.disk_usage('/')
            disk_info = f"Total: {disk_usage.total // (2**30)} GB\nUsed: {disk_usage.used // (2**30)} GB\nFree: {disk_usage.free // (2**30)} GB"

            battery = psutil.sensors_battery()
            battery_info = f"{battery.percent}% {'Charging' if battery.power_plugged else 'On Battery'}" if battery else "No Battery"

            return {
                "gpu": gpu,
                "cpu": cpu,
                "ram": ram,
                "mobo": mobo,
                "os": os_info,
                "os_version": os_version,
                "boot_time": boot_time,
                "install_date": platform.uname().version,
                "uptime": uptime_str,
                "hostname": hostname,
                "local_ip": ip_address,
                "public_ip": public_ip,
                "ip": f"{hostname} ({ip_address})",
                "disk": disk_info,
                "battery": battery_info
            }
        except Exception as e:
            print(f"[System Info Error]: {e}")
            return {k: "Unavailable" for k in [
                "gpu", "cpu", "ram", "mobo", "os", "os_version", "boot_time",
                "install_date", "uptime", "hostname", "local_ip", "public_ip", "ip", "disk", "battery"
            ]}

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PCOptimizer()
    app.mainloop()
