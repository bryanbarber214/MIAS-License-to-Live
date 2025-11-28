"""
AAMVA Driver's License Barcode Parser - Python Version
License to Live: MIAS
Parses AAMVA standard 2D barcodes from US driver's licenses
"""

import re
from datetime import datetime
from typing import Dict, Optional, Tuple

class AAMVAParser:
    """Parser for AAMVA standard driver's license barcodes"""
    
    # Field code mappings
    FIELD_CODES = {
        'DAC': 'first_name',
        'DAD': 'middle_name',
        'DCS': 'last_name',
        'DAQ': 'license_number',
        'DBB': 'date_of_birth',
        'DBD': 'issue_date',
        'DBA': 'expiration_date',
        'DAG': 'address_street',
        'DAI': 'address_city',
        'DAJ': 'address_state',
        'DAK': 'address_zip',
        'DBC': 'sex',
        'DAU': 'height_inches',
        'DAW': 'weight_lbs',
        'DAY': 'eye_color',
        'DAZ': 'hair_color',
        'DCG': 'country',
        'DCF': 'document_discriminator'
    }
    
    # Decode mappings
    SEX_MAP = {'1': 'Male', '2': 'Female', 'M': 'Male', 'F': 'Female'}
    
    EYE_COLOR_MAP = {
        'BLK': 'Black', 'BLU': 'Blue', 'BRO': 'Brown',
        'GRY': 'Gray', 'GRN': 'Green', 'HAZ': 'Hazel',
        'MAR': 'Maroon', 'PNK': 'Pink', 'DIC': 'Dichromatic'
    }
    
    HAIR_COLOR_MAP = {
        'BAL': 'Bald', 'BLK': 'Black', 'BLN': 'Blond',
        'BRO': 'Brown', 'GRY': 'Gray', 'RED': 'Red/Auburn',
        'SDY': 'Sandy', 'WHI': 'White'
    }
    
    def __init__(self):
        self.raw_data = None
        self.parsed = False
        self.error = None
        self.fields = {}
    
    def parse(self, barcode_data: str) -> Tuple[bool, Dict, Optional[str]]:
        """
        Parse AAMVA barcode data
        
        Args:
            barcode_data: Raw string from barcode scanner
            
        Returns:
            Tuple of (success, fields_dict, error_message)
        """
        self.raw_data = barcode_data
        self.parsed = False
        self.error = None
        self.fields = {}
        
        try:
            # Clean Eyoyo scanner output
            # Remove leading @ symbol
            cleaned_data = re.sub(r'^@\s*', '', barcode_data)
            
            # DON'T remove line breaks - use them to identify field boundaries!
            # Each AAMVA field starts on a new line
            
            # Remove leading/trailing whitespace from each line but keep line structure
            lines = cleaned_data.strip().split('\n')
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            cleaned_data = '\n'.join(cleaned_lines)
            
            # Verify it starts with ANSI (AAMVA standard)
            if not cleaned_data.startswith('ANSI'):
                raise ValueError("Invalid barcode format - must start with ANSI")
            
            # Extract all fields
            for code, field_name in self.FIELD_CODES.items():
                value = self._extract_field(cleaned_data, code)
                
                # Special processing for certain fields
                if field_name in ['date_of_birth', 'issue_date', 'expiration_date']:
                    value = self._parse_date(value)
                elif field_name == 'sex':
                    value = self._decode_sex(value)
                elif field_name == 'eye_color':
                    value = self._decode_eye_color(value)
                elif field_name == 'hair_color':
                    value = self._decode_hair_color(value)
                
                self.fields[field_name] = value
            
            self.parsed = True
            return True, self.fields, None
            
        except Exception as e:
            self.error = f"Parse error: {str(e)}"
            self.parsed = False
            return False, {}, self.error
    
    def _extract_field(self, data: str, code: str) -> Optional[str]:
        """Extract a specific field from AAMVA data"""
        # Pattern: Find the field code at the start of a line, capture everything after it on that line
        # Each field is on its own line in the original format
        pattern = rf'^{code}(.*)$'
        match = re.search(pattern, data, re.MULTILINE)
        
        if match:
            value = match.group(1).strip()
            return value if value else None
        return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """Parse AAMVA date format (MMDDYYYY) to YYYY-MM-DD"""
        if not date_str or len(date_str) != 8:
            return None
        
        try:
            month = date_str[0:2]
            day = date_str[2:4]
            year = date_str[4:8]
            
            # Validate date
            date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None
    
    def _decode_sex(self, code: Optional[str]) -> Optional[str]:
        """Decode sex code"""
        if not code:
            return None
        return self.SEX_MAP.get(code.upper(), code)
    
    def _decode_eye_color(self, code: Optional[str]) -> Optional[str]:
        """Decode eye color code"""
        if not code:
            return None
        return self.EYE_COLOR_MAP.get(code.upper(), code)
    
    def _decode_hair_color(self, code: Optional[str]) -> Optional[str]:
        """Decode hair color code"""
        if not code:
            return None
        return self.HAIR_COLOR_MAP.get(code.upper(), code)
    
    def prepare_for_database(self) -> Dict:
        """Prepare parsed data for database insertion"""
        if not self.parsed:
            raise ValueError("Data not parsed yet")
        
        return {
            'license_number': self.fields.get('license_number'),
            'first_name': self.fields.get('first_name'),
            'last_name': self.fields.get('last_name'),
            'date_of_birth': self.fields.get('date_of_birth'),
            'address': self.fields.get('address_street'),
            'city': self.fields.get('address_city'),
            'state': self.fields.get('address_state'),
            'zip_code': self.fields.get('address_zip'),
            'phone': None,  # Not in barcode
            'email': None,  # Not in barcode
            'blood_type': None  # Not in barcode
        }
    
    def format_display(self) -> str:
        """Format parsed data for display"""
        if not self.parsed:
            return f"Error: {self.error}"
        
        output = "=== PARSED DRIVER'S LICENSE DATA ===\n\n"
        
        # Personal Information
        output += "PERSONAL INFORMATION:\n"
        name_parts = [self.fields.get('first_name')]
        if self.fields.get('middle_name'):
            name_parts.append(self.fields.get('middle_name'))
        name_parts.append(self.fields.get('last_name'))
        output += f"  Name: {' '.join(filter(None, name_parts))}\n"
        
        if self.fields.get('date_of_birth'):
            dob = datetime.strptime(self.fields['date_of_birth'], "%Y-%m-%d")
            output += f"  Date of Birth: {dob.strftime('%B %d, %Y')}\n"
        
        if self.fields.get('sex'):
            output += f"  Sex: {self.fields['sex']}\n"
        
        # License Information
        output += "\nLICENSE INFORMATION:\n"
        output += f"  License Number: {self.fields.get('license_number')}\n"
        output += f"  State: {self.fields.get('address_state')}\n"
        
        if self.fields.get('issue_date'):
            issue = datetime.strptime(self.fields['issue_date'], "%Y-%m-%d")
            output += f"  Issue Date: {issue.strftime('%B %d, %Y')}\n"
        
        if self.fields.get('expiration_date'):
            exp = datetime.strptime(self.fields['expiration_date'], "%Y-%m-%d")
            output += f"  Expiration Date: {exp.strftime('%B %d, %Y')}\n"
        
        # Address
        output += "\nADDRESS:\n"
        output += f"  Street: {self.fields.get('address_street')}\n"
        output += f"  City: {self.fields.get('address_city')}\n"
        output += f"  State: {self.fields.get('address_state')}\n"
        output += f"  ZIP Code: {self.fields.get('address_zip')}\n"
        
        # Physical Description
        output += "\nPHYSICAL DESCRIPTION:\n"
        if self.fields.get('height_inches'):
            output += f"  Height: {self.fields['height_inches']} inches\n"
        if self.fields.get('weight_lbs'):
            output += f"  Weight: {self.fields['weight_lbs']} lbs\n"
        if self.fields.get('eye_color'):
            output += f"  Eye Color: {self.fields['eye_color']}\n"
        if self.fields.get('hair_color'):
            output += f"  Hair Color: {self.fields['hair_color']}\n"
        
        return output


def test_parser():
    """Test the parser with sample Texas license data"""
    # Sample barcode from Eyoyo scanner (with @ and line breaks)
    test_data = """@
ANSI 636015090002DL00410280ZT03210007DLDCACM
DCBNONE
DCDNONE
DBA05252029
DCSBARBER
DDEN
DACBRYAN
DDFN
DADEDWARD
DDGN
DBD06132025
DBB05251977
DBC1
DAYHAZ
DAU072 in
DAG2802 LAKESIDE LN
DAICARROLLTON
DAJTX
DAK75006-4725
DAQ10896644
DCF20629580167103805092
DCGUSA
DAZBRO
DCK10032767923
DCLW
DDAF
DDB07162021
DAW180
DDK1
ZTZTAN"""
    
    print("Testing AAMVA Parser with Texas Driver's License...")
    print("(includes @ symbol and line breaks)\n")
    
    parser = AAMVAParser()
    success, fields, error = parser.parse(test_data)
    
    if success:
        print(parser.format_display())
        print("\n=== DATABASE-READY FORMAT ===")
        db_data = parser.prepare_for_database()
        for key, value in db_data.items():
            print(f"{key}: {value}")
        print("\n✅ Parser test successful!")
    else:
        print(f"❌ Parser test failed: {error}")
    
    return success


if __name__ == "__main__":
    # Run test if script is executed directly
    test_parser()
