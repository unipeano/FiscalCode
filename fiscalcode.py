"""
Italian Fiscal Code Generator (Codice Fiscale Italiano)
A modern app to calculate Italian fiscal codes with validation.
"""

import re
from datetime import datetime
from typing import Tuple, Optional


class FiscalCodeGenerator:
    """Generator for Italian fiscal codes (Codice Fiscale)."""
    
    # Month mapping
    MONTH_MAP = {
        1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'H',
        7: 'L', 8: 'M', 9: 'P', 10: 'R', 11: 'S', 12: 'T'
    }
    
    # Check character conversion tables
    ODD_MAP = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13,
        '6': 15, '7': 17, '8': 19, '9': 21, 'A': 1, 'B': 0,
        'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17,
        'I': 19, 'J': 21, 'K': 2, 'L': 4, 'M': 18, 'N': 20,
        'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
        'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }
    
    EVEN_MAP = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9, 'A': 0, 'B': 1,
        'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13,
        'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
        'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }
    
    REMAINDER_MAP = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
        6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
        12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
        18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
        24: 'Y', 25: 'Z'
    }
    
    @staticmethod
    def extract_consonants(text: str) -> str:
        """Extract consonants from text, preserving vowels if needed."""
        consonants = ''.join(c.upper() for c in text if c.upper() in 'BCDFGHJKLMNPQRSTVWXYZ')
        vowels = ''.join(c.upper() for c in text if c.upper() in 'AEIOU')
        return consonants, vowels
    
    @staticmethod
    def get_surname_code(surname: str) -> str:
        """Extract 3-character code from surname."""
        consonants, vowels = FiscalCodeGenerator.extract_consonants(surname)
        code = (consonants + vowels)[:3]
        return code.ljust(3, 'X')  # Pad with X if less than 3 chars
    
    @staticmethod
    def get_name_code(name: str) -> str:
        """Extract 3-character code from first name."""
        consonants, vowels = FiscalCodeGenerator.extract_consonants(name)
        
        # If 4+ consonants, use 1st, 3rd, 4th; else use first 3 available
        if len(consonants) >= 4:
            code = consonants[0] + consonants[2] + consonants[3]
        else:
            code = (consonants + vowels)[:3]
        
        return code.ljust(3, 'X')  # Pad with X if less than 3 chars
    
    @staticmethod
    def get_birth_date_code(birth_date: datetime, gender: str) -> str:
        """Generate date portion of fiscal code."""
        year_code = f"{birth_date.year % 100:02d}"
        month_code = FiscalCodeGenerator.MONTH_MAP[birth_date.month]
        day = birth_date.day
        
        # Add 40 if female
        if gender.upper() == 'F':
            day += 40
        
        day_code = f"{day:02d}"
        return year_code + month_code + day_code
    
    @staticmethod
    def calculate_check_digit(code: str) -> str:
        """Calculate the check digit for the fiscal code."""
        total = 0
        for i, char in enumerate(code):
            if (i + 1) % 2 == 1:  # Odd positions (1-indexed)
                total += FiscalCodeGenerator.ODD_MAP.get(char, 0)
            else:  # Even positions
                total += FiscalCodeGenerator.EVEN_MAP.get(char, 0)
        
        remainder = total % 26
        return FiscalCodeGenerator.REMAINDER_MAP[remainder]
    
    @classmethod
    def generate(
        cls,
        surname: str,
        name: str,
        birth_date: datetime,
        gender: str,
        municipality_code: str
    ) -> str:
        """
        Generate Italian fiscal code.
        
        Args:
            surname: Family name
            name: First name
            birth_date: Date of birth
            gender: 'M' for male, 'F' for female
            municipality_code: 4-character municipality code (e.g., 'A123')
            
        Returns:
            16-character fiscal code
        """
        # Validate inputs
        if not surname or not name:
            raise ValueError("Surname and name are required")
        if not isinstance(birth_date, datetime):
            raise ValueError("Birth date must be a datetime object")
        if gender.upper() not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        if len(municipality_code) != 4:
            raise ValueError("Municipality code must be 4 characters")
        
        # Build the code
        code = (
            cls.get_surname_code(surname) +
            cls.get_name_code(name) +
            cls.get_birth_date_code(birth_date, gender) +
            municipality_code.upper()
        )
        
        # Add check digit
        check_digit = cls.calculate_check_digit(code)
        fiscal_code = code + check_digit
        
        return fiscal_code


def parse_date(date_str: str) -> datetime:
    """Parse date string in DD/MM/YYYY format."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        raise ValueError(f"Invalid date format. Use DD/MM/YYYY")


def print_header():
    """Print application header."""
    print("\n" + "=" * 50)
    print("  ITALIAN FISCAL CODE CALCULATOR")
    print("  Calcolatore Codice Fiscale Italiano")
    print("=" * 50 + "\n")


def print_separator():
    """Print visual separator."""
    print("-" * 50)


def get_user_input() -> Tuple[str, str, datetime, str, str]:
    """Collect user input for fiscal code generation."""
    print("Enter your information:")
    print_separator()
    
    surname = input("Surname (Cognome): ").strip()
    name = input("First Name (Nome): ").strip()
    
    while True:
        date_str = input("Date of Birth (DD/MM/YYYY): ").strip()
        try:
            birth_date = parse_date(date_str)
            break
        except ValueError as e:
            print(f"❌ {e}")
    
    while True:
        gender = input("Gender (M/F): ").strip().upper()
        if gender in ['M', 'F']:
            break
        print("❌ Please enter 'M' or 'F'")
    
    municipality_code = input("Municipality Code (e.g., A123): ").strip()
    
    return surname, name, birth_date, gender, municipality_code


def main():
    """Main application loop."""
    print_header()
    
    try:
        surname, name, birth_date, gender, municipality_code = get_user_input()
        
        print_separator()
        print("Generating fiscal code...")
        print_separator()
        
        fiscal_code = FiscalCodeGenerator.generate(
            surname, name, birth_date, gender, municipality_code
        )
        
        print("\n✓ Fiscal Code Generated:\n")
        print(f"  {fiscal_code}\n")
        
        # Display breakdown
        print("Code Breakdown:")
        print(f"  Surname Code:       {fiscal_code[0:3]}")
        print(f"  Name Code:          {fiscal_code[3:6]}")
        print(f"  Year of Birth:      {fiscal_code[6:8]}")
        print(f"  Month:              {fiscal_code[8]}")
        print(f"  Day (+ 40 if F):    {fiscal_code[9:11]}")
        print(f"  Municipality:       {fiscal_code[11:15]}")
        print(f"  Check Digit:        {fiscal_code[15]}")
        print()
        
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        return 1
    except KeyboardInterrupt:
        print("\n\nExiting...")
        return 0
    
    return 0


if __name__ == "__main__":
    exit(main())
