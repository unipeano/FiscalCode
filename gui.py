"""
Italian Fiscal Code Calculator - Modern GUI
A modern, minimal desktop application for calculating Italian fiscal codes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from fiscalcode import FiscalCodeGenerator, parse_date


class FiscalCodeGUI:
    """Modern GUI for Italian Fiscal Code Generator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Italian Fiscal Code Calculator")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        
        # Configure style
        self.setup_styles()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Build UI
        self.build_ui()
    
    def setup_styles(self):
        """Configure the visual style of the application."""
        style = ttk.Style()
        
        # Modern color scheme
        bg_color = "#f5f5f5"
        fg_color = "#2c3e50"
        accent_color = "#3498db"
        
        # Configure root window
        self.root.configure(bg=bg_color)
        
        style.theme_use('clam')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 18, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_color, foreground="#7f8c8d", font=('Segoe UI', 9))
        style.configure('TEntry', fieldbackground='white', foreground=fg_color, font=('Segoe UI', 10))
        style.configure('TCombobox', fieldbackground='white', foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#2980b9')])
    
    def build_ui(self):
        """Build the user interface."""
        # Title
        title = ttk.Label(
            self.main_frame,
            text="Italian Fiscal Code Calculator",
            style='Title.TLabel'
        )
        title.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        
        subtitle = ttk.Label(
            self.main_frame,
            text="Calculate your Italian Fiscal Code",
            style='Subtitle.TLabel'
        )
        subtitle.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        # Input fields
        row = 2
        
        # Surname
        ttk.Label(self.main_frame, text="Surname (Cognome)").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        self.surname_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.surname_var, width=40).grid(row=row+1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 2
        
        # First Name
        ttk.Label(self.main_frame, text="First Name (Nome)").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        self.name_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.name_var, width=40).grid(row=row+1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 2
        
        # Date of Birth
        ttk.Label(self.main_frame, text="Date of Birth (DD/MM/YYYY)").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        self.date_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.date_var, width=40).grid(row=row+1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 2
        
        # Gender
        ttk.Label(self.main_frame, text="Gender").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        self.gender_var = tk.StringVar(value="M")
        gender_frame = ttk.Frame(self.main_frame)
        gender_frame.grid(row=row+1, column=0, sticky=tk.W, pady=(0, 10))
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="M").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="F").pack(side=tk.LEFT)
        row += 2
        
        # Municipality Code
        ttk.Label(self.main_frame, text="Municipality Code (e.g., A123)").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        self.municipality_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.municipality_var, width=40).grid(row=row+1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        row += 2
        
        # Generate Button
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=15)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            button_frame,
            text="Generate Fiscal Code",
            command=self.generate_code,
            style='Accent.TButton'
        ).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_form
        ).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        row += 1
        
        # Result Frame
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Result", padding="15")
        self.result_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(10, 0), padx=0)
        self.result_frame.columnconfigure(0, weight=1)
        
        # Fiscal Code Display with Copy Button
        code_frame = ttk.Frame(self.result_frame)
        code_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        code_frame.columnconfigure(0, weight=1)
        
        self.fiscal_code_label = ttk.Label(
            code_frame,
            text="",
            font=('Courier New', 16, 'bold'),
            foreground="#27ae60"
        )
        self.fiscal_code_label.grid(row=0, column=0, sticky=tk.W)
        
        self.copy_button = ttk.Button(
            code_frame,
            text="Copy",
            command=self.copy_to_clipboard,
            width=10
        )
        self.copy_button.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        self.copy_button.config(state=tk.DISABLED)
        
        # Breakdown
        self.breakdown_text = tk.Text(
            self.result_frame,
            height=6,
            width=40,
            font=('Courier New', 9),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor='#bdc3c7'
        )
        self.breakdown_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0)
        self.breakdown_text.config(state=tk.DISABLED)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.breakdown_text.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), padx=(5, 0))
        self.breakdown_text.config(yscrollcommand=scrollbar.set)
    
    def generate_code(self):
        """Generate the fiscal code based on input."""
        try:
            # Get values
            surname = self.surname_var.get().strip()
            name = self.name_var.get().strip()
            date_str = self.date_var.get().strip()
            gender = self.gender_var.get()
            municipality = self.municipality_var.get().strip()
            
            # Validate
            if not surname or not name:
                messagebox.showerror("Error", "Please enter surname and first name")
                return
            
            if not date_str:
                messagebox.showerror("Error", "Please enter date of birth")
                return
            
            if not municipality:
                messagebox.showerror("Error", "Please enter municipality code")
                return
            
            # Parse date
            try:
                birth_date = parse_date(date_str)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            
            # Generate code
            fiscal_code = FiscalCodeGenerator.generate(
                surname, name, birth_date, gender, municipality
            )
            
            # Display result
            self.fiscal_code_label.config(text=f"✓ {fiscal_code}")
            self.copy_button.config(state=tk.NORMAL)
            
            # Display breakdown
            breakdown = (
                f"Surname Code:       {fiscal_code[0:3]}\n"
                f"Name Code:          {fiscal_code[3:6]}\n"
                f"Year of Birth:      {fiscal_code[6:8]}\n"
                f"Month:              {fiscal_code[8]}\n"
                f"Day (+ 40 if F):    {fiscal_code[9:11]}\n"
                f"Municipality:       {fiscal_code[11:15]}\n"
                f"Check Digit:        {fiscal_code[15]}"
            )
            
            self.breakdown_text.config(state=tk.NORMAL)
            self.breakdown_text.delete(1.0, tk.END)
            self.breakdown_text.insert(1.0, breakdown)
            self.breakdown_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy the fiscal code to clipboard."""
        code_text = self.fiscal_code_label.cget("text").replace("✓ ", "").strip()
        if code_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(code_text)
            self.root.update()
            messagebox.showinfo("Success", f"Copied to clipboard: {code_text}")
    
    def reset_form(self):
        """Reset the form to clear all inputs and results."""
        # Clear input fields
        self.surname_var.set("")
        self.name_var.set("")
        self.date_var.set("")
        self.gender_var.set("M")
        self.municipality_var.set("")
        
        # Clear result display
        self.fiscal_code_label.config(text="")
        self.copy_button.config(state=tk.DISABLED)
        
        # Clear breakdown
        self.breakdown_text.config(state=tk.NORMAL)
        self.breakdown_text.delete(1.0, tk.END)
        self.breakdown_text.config(state=tk.DISABLED)


def main():
    """Run the application."""
    root = tk.Tk()
    app = FiscalCodeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
