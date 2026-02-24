# Quick Start Guide 🚀

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd FiscalCode
```

### 2. Install Dependencies (Optional)

For the web version, install Flask:
```bash
pip install -r requirements.txt
```

## Running the Application

### Command Line Version ⌨️
Simple CLI with interactive prompts:
```bash
python fiscalcode.py
```

**Example:**
```
Surname (Cognome): Rossi
First Name (Nome): Mario
Date of Birth (DD/MM/YYYY): 01/01/1980
Gender (M/F): M
Municipality Code (e.g., A123): H501
```

### Desktop GUI Version 🖥️
Modern desktop application with tkinter:
```bash
python gui.py
```
- No additional dependencies needed (tkinter is built-in)
- Clean, modern interface
- Real-time validation

### Web Version 🌐
Modern web application (requires Flask):
```bash
python app.py
```
Then open: **http://localhost:5000**

Features:
- Beautiful responsive design
- Works on all devices
- Instant feedback
- Copy to clipboard

## How to Use

1. **Enter your information:**
   - Surname (Cognome)
   - First Name (Nome)
   - Date of Birth (DD/MM/YYYY)
   - Gender (M/F - affects day calculation)
   - Municipality Code (4-character code)

2. **Generate:**
   - Click "Generate" button
   - Your fiscal code will be displayed

3. **Understand the code:**
   - See the breakdown of each component
   - Copy to clipboard easily

## Understanding the Output

Example: `RSSMRA80A01H501C`

| Part | Value | Meaning |
|------|-------|---------|
| Characters 1-3 | RSS | Surname consonants |
| Characters 4-6 | MRA | Name consonants |
| Characters 7-8 | 80 | Birth year (1980) |
| Character 9 | A | Birth month (January) |
| Characters 10-11 | 01 | Day of birth (+40 if female) |
| Characters 12-15 | H501 | Municipality code |
| Character 16 | C | Check digit |

## Municipality Codes

The municipality code is a 4-character code assigned to Italian cities. Examples:
- **H501** - Roma (Rome)
- **A123** - Milano (Milan)
- **B456** - Napoli (Naples)

## Tips

✅ Use real Italian municipality codes for valid fiscal codes  
✅ Females: Day automatically adds 40 (day 12 becomes 52)  
✅ The check digit validates the code correctness  
✅ Works for all combinations of names and dates  

## Troubleshooting

### Common Issues

**"Module not found: flask"**
```bash
pip install flask
```

**"Invalid date format"**
- Use format: DD/MM/YYYY
- Example: 25/12/1985

**"Municipality code must be 4 characters"**
- Municipality code must be exactly 4 characters
- Example: H501, not H50

## Project Structure

```
FiscalCode/
├── fiscalcode.py        # Core library
├── gui.py               # Desktop GUI (tkinter)
├── app.py               # Web app (Flask)
├── templates/
│   └── index.html       # Web interface
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Interactive features
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Verify your input format
3. Ensure Python 3.7+ is installed
4. For web version, ensure Flask is installed

## License

MIT License - Feel free to use and modify!

---

**Happy coding! 💻**
