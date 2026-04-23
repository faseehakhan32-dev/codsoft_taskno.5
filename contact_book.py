import customtkinter as ctk
import json
import os
import uuid
from typing import List, Dict, Optional

# Set up the theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Premium Color Palette ---
SPACE_CADET = "#1B263B"    # Deeper, richer blue
SLATE_GRAY = "#415A77"     # Muted steel blue
TAN = "#D5B893"            # Now matches ACCENT_COLOR for total consistency
COFFEE = "#778DA9"         # Secondary slate for cards
CAPUT_MORTUUM = "#0D1B2A"  # Darkest blue for depth
ACCENT_COLOR = "#D5B893"    # Original Tan as the premium accent

# Semantic Assignments
BACKGROUND_COLOR = SPACE_CADET
SIDEBAR_COLOR = SPACE_CADET
CARD_COLOR = "#2C3E50"      # Slightly different for the details card
PRIMARY_COLOR = ACCENT_COLOR
SEPARATOR_COLOR = SLATE_GRAY

# Text Colors
TEXT_ON_BG = TAN
TEXT_ON_SIDEBAR = TAN
TEXT_ON_CARD = ACCENT_COLOR
DANGER_COLOR = "#E63946" # Modern red for danger

DATA_FILE = "contacts.json"


class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Contact Book - Classic Edition")
        self.geometry("950x650")
        self.minsize(850, 550)
        self.configure(fg_color=BACKGROUND_COLOR)

        # State
        self.contacts: List[Dict] = []
        self.selected_contact_id: Optional[str] = None
        self.search_query = ctk.StringVar()
        self.search_query.trace_add("write", self.on_search_change)

        # Load Data
        self.load_contacts()

        # UI Configuration
        self.grid_columnconfigure(0, weight=1, minsize=400) # Sidebar
        self.grid_columnconfigure(1, weight=3)              # Main Content
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=SIDEBAR_COLOR, corner_radius=0, border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Contacts", 
            font=ctk.CTkFont(family="Georgia", size=36, weight="bold"),
            text_color=ACCENT_COLOR
        )
        self.header_label.grid(row=0, column=0, padx=30, pady=(40, 20), sticky="w")

        # Search Bar
        self.search_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search contacts...",
            textvariable=self.search_query,
            border_width=0,
            fg_color=CAPUT_MORTUUM,
            text_color=TAN,
            placeholder_text_color=SLATE_GRAY,
            corner_radius=12,
            height=50,
            font=ctk.CTkFont(family="Georgia", size=15)
        )
        self.search_entry.pack(fill="x")

        # Contact List
        self.contact_list_frame = ctk.CTkScrollableFrame(
            self.sidebar_frame, 
            fg_color="transparent",
            scrollbar_fg_color="transparent",
            scrollbar_button_color=SLATE_GRAY,
            scrollbar_button_hover_color=ACCENT_COLOR,
            corner_radius=0,
            border_width=0
        )
        self.contact_list_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        # Add Button
        self.add_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="+ New Contact", 
            command=self.open_add_form,
            fg_color=ACCENT_COLOR,
            text_color=CAPUT_MORTUUM,
            hover_color=TAN,
            corner_radius=15,
            height=55,
            font=ctk.CTkFont(family="Georgia", size=16, weight="bold")
        )
        self.add_btn.grid(row=3, column=0, padx=30, pady=30, sticky="ew")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.details_frame = None
        self.empty_state_frame = None
        
        self.show_empty_state()
        self.refresh_contact_list()

    # --- Data Management ---
    
    def load_contacts(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.contacts = json.load(f)
            except Exception as e:
                print(f"Error loading contacts: {e}")
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.contacts, f, indent=2)
        except Exception as e:
            print(f"Error saving contacts: {e}")

    # --- UI Logic ---

    def on_search_change(self, *args):
        self.refresh_contact_list()

    def get_filtered_contacts(self):
        query = self.search_query.get().lower()
        if not query:
            return sorted(self.contacts, key=lambda x: x['name'].lower())
        
        filtered = [
            c for c in self.contacts 
            if query in c['name'].lower() or query in c['phone']
        ]
        return sorted(filtered, key=lambda x: x['name'].lower())

    def refresh_contact_list(self):
        # Clear existing
        for widget in self.contact_list_frame.winfo_children():
            widget.destroy()

        filtered_contacts = self.get_filtered_contacts()

        if not filtered_contacts:
            lbl = ctk.CTkLabel(
                self.contact_list_frame, 
                text="No contacts found", 
                text_color=SPACE_CADET,
                font=ctk.CTkFont(family="Georgia", size=16, slant="italic")
            )
            lbl.pack(pady=30)
            return

        for contact in filtered_contacts:
            self.create_contact_card(contact)

    def create_contact_card(self, contact):
        is_active = self.selected_contact_id == contact['id']
        bg_color = SLATE_GRAY if is_active else "transparent"
        hover_color = "#2C3E50" if not is_active else SLATE_GRAY
        
        # Container frame for the card row
        card_row = ctk.CTkFrame(self.contact_list_frame, fg_color="transparent")
        card_row.pack(fill="x", padx=5, pady=4)
        card_row.grid_columnconfigure(1, weight=1)
        
        # Avatar (initials)
        initials = "".join([n[0] for n in contact['name'].split() if n]).upper()[:2]
        avatar_bg = ACCENT_COLOR if is_active else CAPUT_MORTUUM
        avatar_fg = CAPUT_MORTUUM if is_active else ACCENT_COLOR
        
        avatar = ctk.CTkLabel(
            card_row, 
            text=initials,
            width=50, height=50,
            corner_radius=25,
            fg_color=avatar_bg,
            text_color=avatar_fg,
            font=ctk.CTkFont(family="Georgia", weight="bold", size=18)
        )
        avatar.grid(row=0, column=0, padx=(10, 10), pady=8)
        
        # Text button (name + phone)
        display_text = f"{contact['name']}\n{contact['phone']}"
        text_color = ACCENT_COLOR
        
        card_btn = ctk.CTkButton(
            card_row, 
            text=display_text,
            fg_color=bg_color,
            hover_color=hover_color,
            corner_radius=12,
            height=70,
            anchor="w",
            text_color=text_color,
            font=ctk.CTkFont(family="Georgia", size=16),
            command=lambda c_id=contact['id']: self.select_contact(c_id)
        )
        card_btn.grid(row=0, column=1, sticky="ew", padx=(0, 5))

    def select_contact(self, contact_id):
        self.selected_contact_id = contact_id
        self.refresh_contact_list()
        self.show_contact_details()

    def show_empty_state(self):
        if self.details_frame:
            self.details_frame.destroy()
            
        if not self.empty_state_frame:
            self.empty_state_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.empty_state_frame.grid(row=0, column=0, sticky="nsew")
            self.empty_state_frame.grid_columnconfigure(0, weight=1)
            self.empty_state_frame.grid_rowconfigure(0, weight=1)
            
            inner_frame = ctk.CTkFrame(self.empty_state_frame, fg_color="transparent")
            inner_frame.grid(row=0, column=0)
            
            icon_lbl = ctk.CTkLabel(
                inner_frame, 
                text="📖", 
                font=ctk.CTkFont(size=72),
                text_color=ACCENT_COLOR
            )
            icon_lbl.pack(pady=(0, 15))
            
            title_lbl = ctk.CTkLabel(
                inner_frame, 
                text="Address Book", 
                font=ctk.CTkFont(family="Georgia", size=32, weight="bold"),
                text_color=ACCENT_COLOR
            )
            title_lbl.pack(pady=5)
            
            desc_lbl = ctk.CTkLabel(
                inner_frame, 
                text="Select a contact to view details or create a new entry.", 
                text_color=ACCENT_COLOR,
                font=ctk.CTkFont(family="Georgia", size=16, slant="italic")
            )
            desc_lbl.pack()

    def show_contact_details(self):
        if not self.selected_contact_id:
            self.show_empty_state()
            return
            
        contact = next((c for c in self.contacts if c['id'] == self.selected_contact_id), None)
        if not contact:
            self.show_empty_state()
            return

        if self.empty_state_frame:
            self.empty_state_frame.destroy()
            self.empty_state_frame = None

        if self.details_frame:
            self.details_frame.destroy()

        self.details_frame = ctk.CTkFrame(self.main_frame, fg_color=CARD_COLOR, corner_radius=20, border_width=1, border_color=TAN)
        self.details_frame.grid(row=0, column=0, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)

        # Header Profile
        header = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=40)
        
        initials = "".join([n[0] for n in contact['name'].split() if n]).upper()[:2]
        avatar = ctk.CTkLabel(
            header, 
            text=initials,
            width=90, height=90,
            corner_radius=45,
            fg_color=TAN,
            text_color=SPACE_CADET,
            font=ctk.CTkFont(family="Georgia", size=36, weight="bold")
        )
        avatar.pack(side="left", padx=(0, 25))
        
        name_lbl = ctk.CTkLabel(
            header, 
            text=contact['name'], 
            font=ctk.CTkFont(family="Georgia", size=38, weight="bold"),
            text_color=TEXT_ON_CARD
        )
        name_lbl.pack(side="left", anchor="center")
        
        # Action Buttons
        actions_frame = ctk.CTkFrame(header, fg_color="transparent")
        actions_frame.pack(side="right", anchor="center")
        
        edit_btn = ctk.CTkButton(
            actions_frame, 
            text="Edit", 
            width=90, height=36,
            command=lambda: self.open_edit_form(contact),
            fg_color="transparent",
            border_width=2,
            border_color=TAN,
            text_color=TAN,
            hover_color=SPACE_CADET,
            corner_radius=6,
            font=ctk.CTkFont(family="Georgia", weight="bold")
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            actions_frame, 
            text="Delete", 
            width=90, height=36,
            command=lambda: self.delete_contact(contact['id']),
            fg_color="transparent",
            border_width=2,
            border_color=ACCENT_COLOR,
            text_color=ACCENT_COLOR,
            hover_color=CAPUT_MORTUUM,
            corner_radius=6,
            font=ctk.CTkFont(family="Georgia", weight="bold")
        )
        delete_btn.pack(side="left", padx=5)

        # Info Section separator
        sep = ctk.CTkFrame(self.details_frame, height=2, fg_color=TAN)
        sep.pack(fill="x", padx=40)

        # Info Section
        info_container = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        info_container.pack(fill="both", expand=True, padx=40, pady=30)

        def add_info_row(label, value):
            row = ctk.CTkFrame(info_container, fg_color="transparent")
            row.pack(fill="x", pady=15)
            
            lbl = ctk.CTkLabel(
                row, 
                text=label, 
                width=100, 
                text_color=TAN, 
                font=ctk.CTkFont(family="Georgia", size=16, weight="bold"), 
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                row, 
                text=value or "—", 
                text_color=ACCENT_COLOR, 
                font=ctk.CTkFont(family="Georgia", size=18), 
                anchor="w"
            )
            val.pack(side="left", fill="x", expand=True, padx=10)

        add_info_row("Phone", contact.get('phone', ''))
        add_info_row("Email", contact.get('email', ''))
        add_info_row("Address", contact.get('address', ''))

    # --- Forms ---

    def open_add_form(self):
        ContactFormWindow(self, title="New Contact", on_save=self.handle_save_contact)

    def open_edit_form(self, contact):
        ContactFormWindow(self, title="Edit Contact", contact=contact, on_save=self.handle_save_contact)

    def handle_save_contact(self, contact_data, contact_id=None):
        if contact_id:
            # Edit
            for idx, c in enumerate(self.contacts):
                if c['id'] == contact_id:
                    self.contacts[idx] = {**c, **contact_data}
                    break
        else:
            # Add
            new_contact = {
                'id': str(uuid.uuid4()),
                **contact_data
            }
            self.contacts.append(new_contact)
            self.selected_contact_id = new_contact['id']

        self.save_contacts()
        self.refresh_contact_list()
        self.show_contact_details()

    def delete_contact(self, contact_id):
        # Using a simple dialog to confirm
        dialog = ctk.CTkInputDialog(text="Type 'yes' to delete this contact:", title="Confirm Delete")
        if dialog.get_input() == 'yes':
            self.contacts = [c for c in self.contacts if c['id'] != contact_id]
            self.selected_contact_id = None
            self.save_contacts()
            self.refresh_contact_list()
            self.show_empty_state()


class ContactFormWindow(ctk.CTkToplevel):
    def __init__(self, master, title, on_save, contact=None):
        super().__init__(master)
        
        self.title(title)
        self.geometry("450x650")
        self.minsize(450, 650)
        self.configure(fg_color=SPACE_CADET)
        self.transient(master) # Keep on top of main window
        self.grab_set() # Make it modal
        
        self.on_save = on_save
        self.contact_id = contact['id'] if contact else None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=(20, 20))
        
        # Title
        ctk.CTkLabel(
            main_frame, 
            text=title, 
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold"),
            text_color=ACCENT_COLOR
        ).pack(pady=(0, 30), anchor="w")

        # Form Fields
        self.name_var = ctk.StringVar(value=contact['name'] if contact else "")
        self.phone_var = ctk.StringVar(value=contact['phone'] if contact else "")
        self.email_var = ctk.StringVar(value=contact['email'] if contact else "")
        self.address_var = ctk.StringVar(value=contact['address'] if contact else "")

        self.create_input(main_frame, "Full Name *", self.name_var)
        self.create_input(main_frame, "Phone Number *", self.phone_var)
        self.create_input(main_frame, "Email Address", self.email_var)
        self.create_input(main_frame, "Address", self.address_var)

        self.error_label = ctk.CTkLabel(main_frame, text="", text_color=DANGER_COLOR, font=ctk.CTkFont(family="Georgia", size=14, weight="bold"))
        self.error_label.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(30, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            command=self.destroy,
            fg_color="transparent",
            border_width=2,
            border_color=ACCENT_COLOR,
            text_color=ACCENT_COLOR,
            hover_color=SLATE_GRAY,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold")
        )
        cancel_btn.pack(side="left", expand=True, padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            btn_frame, 
            text="Save Contact", 
            command=self.save,
            fg_color=ACCENT_COLOR,
            text_color=CAPUT_MORTUUM,
            hover_color="#C0A070",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold")
        )
        save_btn.pack(side="left", expand=True, padx=(10, 0))

    def create_input(self, parent, label_text, variable):
        lbl = ctk.CTkLabel(
            parent, 
            text=label_text, 
            anchor="w", 
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold"),
            text_color=ACCENT_COLOR
        )
        lbl.pack(fill="x", pady=(15, 5))
        
        entry = ctk.CTkEntry(
            parent, 
            textvariable=variable, 
            height=45,
            fg_color=CAPUT_MORTUUM,
            border_color=ACCENT_COLOR,
            border_width=1,
            text_color=TAN,
            corner_radius=8,
            font=ctk.CTkFont(family="Georgia", size=16)
        )
        entry.pack(fill="x")

    def save(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        
        if not name or not phone:
            self.error_label.configure(text="Name and Phone are required fields.")
            return
            
        contact_data = {
            'name': name,
            'phone': phone,
            'email': self.email_var.get().strip(),
            'address': self.address_var.get().strip()
        }
        
        self.on_save(contact_data, self.contact_id)
        self.destroy()

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()
