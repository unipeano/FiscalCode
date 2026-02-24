# Italian Fiscal Code Calculator 🇮🇹

A modern, minimal web application to calculate Italian fiscal codes (*Codice Fiscale*).

## Features

✓ Modern, minimal design  
✓ Real-time validation  
✓ Detailed code breakdown  
✓ Responsive interface  
✓ Fast and lightweight  

## What is Codice Fiscale?

The Italian fiscal code is a 16-character alphanumeric code used to uniquely identify citizens for tax and administrative purposes. It's been in use since 1973.

## How It Works

The fiscal code is generated from:
- **Surname** → First 3 consonants (or consonants + vowels if fewer)
- **First Name** → 1st, 3rd, and 4th consonants (or first 3 available)
- **Birth Year** → Last 2 digits
- **Birth Month** → Letter (A-T mapping to Jan-Dec)
- **Birth Day** → Day number (+40 for females to distinguish gender)
- **Municipality Code** → 4-character code
- **Check Digit** → Calculated based on algorithm

## Installation & Usage

### Option 1: Command Line

```bash
python fiscalcode.py
```

Follow the prompts to enter your information.

### Option 2: Desktop GUI

```bash
python gui.py
```

A modern window will open with an easy-to-use form.

### Option 3: Web Interface

```bash
python app.py
```

Open your browser to `http://localhost:5000`

## Requirements

- Python 3.7+
- `flask` (for web version only - optional)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd FiscalCode

# Install optional dependencies (for web version)
pip install flask
```

## Example

**Input:**
- Surname: Rossi
- First Name: Mario
- Date of Birth: 01/01/1980
- Gender: M
- Municipality Code: H501

**Output:**
```
RSSMRA80A01H501C
```

**Breakdown:**
- RSS = Rossi (consonants)
- MRA = Mario (1st, 3rd, 4th consonant)
- 80 = 1980
- A = January
- 01 = Day 1
- H501 = Municipality code
- C = Check digit

## File Structure

```
FiscalCode/
├── fiscalcode.py    # Core fiscal code generator
├── gui.py           # Desktop GUI application
├── app.py           # Web application (Flask)
└── README.md        # This file
```

## Notes

- Municipality codes are 4-character alphanumeric codes specific to Italian cities
- For females, 40 is added to the day of birth (e.g., day 12 becomes 52 for females)
- The check digit is calculated using a specific algorithm with odd/even position mapping

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
