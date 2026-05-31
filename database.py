import json
import os
from datetime import datetime
from config import DB_FILE

class Database:
    def __init__(self):
        self.file = DB_FILE
        self.load()
    
    def load(self):
        """Load data from JSON"""
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'ishchilar': {
                    "101": {"ism": "Sardor Karimov"},
                    "102": {"ism": "Dilnoza Rahimova"},
                    "103": {"ism": "Jasur Toshmatov"}
                },
                'hisobchilar': {
                    "201": {"ism": "Malika Yusupova"}
                },
                'mahsulotlar': {
                    "ayron_1l": {"name": "Ayron 1L", "price": 15000, "emoji": "🥛"},
                    "ayron_05l": {"name": "Ayron 0.5L", "price": 10000, "emoji": "🥛"},
                    "urik_1l": {"name": "O'rik sharbat 1L", "price": 15000, "emoji": "🧃"},
                    "urik_05l": {"name": "O'rik sharbat 0.5L", "price": 10000, "emoji": "🧃"},
                    "somsa_1x": {"name": "Somsa 1x", "price": 3000, "emoji": "🥟"},
                    "somsa_3x": {"name": "Somsa 3x", "price": 10000, "emoji": "🥟"},
                    "ayron_katta": {"name": "Ayron stakan KATTA", "price": 8000, "emoji": "🥤"},
                    "ayron_kichik": {"name": "Ayron stakan KICHIK", "price": 5000, "emoji": "🥤"}
                },
                'sotuvlar': [],
                'rasxodlar': [],
                'qoldiq': {},
                'filiallar': {},
                'blok_list': [],
                'kunlik_target': {},
                'ish_haqi': {}
            }
            self.save()
    
    def save(self):
        """Save data to JSON"""
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_all(self):
        """Get all data"""
        return self.data
    
    def add_sotuv(self, sotuv_data):
        """Add new sale"""
        self.data['sotuvlar'].append(sotuv_data)
        self.save()
        return sotuv_data
    
    def add_rasxod(self, rasxod_data):
        """Add new expense"""
        self.data['rasxodlar'].append(rasxod_data)
        self.save()
        return rasxod_data
    
    def add_ishchi(self, id, ism):
        """Add new worker"""
        self.data['ishchilar'][str(id)] = {"ism": ism}
        self.save()
        return self.data['ishchilar'][str(id)]
    
    def get_user_role(self, user_id):
        """Get user role"""
        uid = str(user_id)
        if uid in self.data['ishchilar']:
            return 'ishchi'
        elif uid in self.data['hisobchilar']:
            return 'hisobchi'
        else:
            return 'ega'

# Create global instance
db = Database()
