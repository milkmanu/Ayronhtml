# 🚀 Ayron Savdo v5 - Bot + WebApp

Telegram Bot va Web App integratsiyasi bilan **to'liq savdo management sistema**.

## 📋 Xususiyatlari

✅ **Telegram Bot** - /start, /sotuv, /hisobot commands  
✅ **Web App Dashboard** - Responsive, beautiful UI  
✅ **Backend API** - Flask with JSON database  
✅ **Real-time Sync** - Bot ↔ WebApp ↔ Database  
✅ **Role-based Access** - EGA, Hisobchi, Ishchi  
✅ **Complete Reports** - Bugun, Bu oy, Hamma

## 🏗️ Struktura

```
Ayronhtml/
├── ayron_premium.html      # WebApp Frontend
├── bot.py                  # Telegram Bot
├── app.py                  # Flask Backend
├── database.py             # JSON Database
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md              # This file
```

## 🔧 Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/milkmanu/Ayronhtml.git
cd Ayronhtml
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Create .env File
```bash
cp .env.example .env
```

**Edit .env:**
```env
BOT_TOKEN=8988862076:AAF7giS9WIpf9TZVKV-eogsxb4kTbt79Yio
WEBAPP_URL=http://localhost:5000
PORT=5000
EGA_ID=8168552332
```

### 4️⃣ Run Backend
```bash
python app.py
```

Output:
```
🚀 Backend running on 0.0.0.0:5000
📱 WebApp: http://localhost:5000
```

### 5️⃣ Run Bot (in another terminal)
```bash
python bot.py
```

Output:
```
🤖 Bot ishga tushdi...
```

## 🌐 Access

### Local Development
- **WebApp**: http://localhost:5000
- **Bot**: @ayron_savdo_bot (Telegram-da)

### Deployment

#### Heroku
```bash
git push heroku main
```

#### Railway
```bash
railway up
```

#### Vercel (Frontend only)
```bash
vercel --prod
```

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Main menu |
| `/sotuv` | Today's sales |
| `/hisobot` | Today's report |
| `/menu` | Show menu |

## 🔌 API Endpoints

### Data
- `GET /api/data` - Get all data
- `GET /api/user-role/<user_id>` - Get user role

### Sales (Sotuv)
- `POST /api/sotuv` - Add sale
- `GET /api/sotuv` - Get all sales

### Expenses (Rasxod)
- `POST /api/rasxod` - Add expense
- `GET /api/rasxod` - Get all expenses

### Workers (Ishchilar)
- `GET /api/ishchilar` - Get all workers
- `POST /api/ishchilar` - Add worker

### Products (Mahsulotlar)
- `GET /api/mahsulotlar` - Get all products
- `POST /api/mahsulotlar` - Add product

### Reports (Hisobot)
- `GET /api/hisobot/bugun` - Today's report

## 🗄️ Database Schema

```json
{
  "ishchilar": {
    "101": {"ism": "Sardor Karimov"},
    "102": {"ism": "Dilnoza Rahimova"}
  },
  "hisobchilar": {
    "201": {"ism": "Malika Yusupova"}
  },
  "mahsulotlar": {
    "ayron_1l": {
      "name": "Ayron 1L",
      "price": 15000,
      "emoji": "🥛"
    }
  },
  "sotuvlar": [
    {
      "sana": "2026-05-31T09:10:00",
      "ishchi_id": "101",
      "mahsulot_id": "ayron_1l",
      "miqdor": 5,
      "summa": 75000
    }
  ],
  "rasxodlar": [],
  "qoldiq": {},
  "filiallar": {},
  "kunlik_target": {},
  "ish_haqi": {}
}
```

## 👥 User Roles

### 🔴 EGA (Owner)
- ✅ Barcha dashboard ko'rish
- ✅ Hisobotlar
- ✅ Top ranking
- ✅ Ishchilar manage
- ✅ Mahsulotlar manage

### 🟡 Hisobchi (Accountant)
- ✅ Sotuv va rasxod
- ✅ Bugungi hisobot
- ❌ Other workers' data

### 🟢 Ishchi (Worker)
- ✅ O'z sotuvlarini ko'rish
- ✅ Target progress
- ❌ Boshqa ishchilar data

## 🛠️ Development

### Add New Feature
1. Update `database.py` for data model
2. Add endpoint in `app.py`
3. Update HTML/JS in `ayron_premium.html`
4. Test with API calls

### Example: Add New Endpoint
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    data = request.json
    # Process data
    db.save()
    return jsonify({'success': True})
```

## 📦 Deployment Checklist

- [ ] Bot token in .env
- [ ] WEBAPP_URL correct (production domain)
- [ ] Database backed up
- [ ] Requirements.txt updated
- [ ] .env.example updated
- [ ] Telegram bot webhook configured
- [ ] CORS enabled for WebApp domain

## 🐛 Troubleshooting

### Bot doesn't respond
```bash
# Check token
python -c "from config import BOT_TOKEN; print(BOT_TOKEN)"

# Restart
python bot.py
```

### WebApp shows blank page
- Check WEBAPP_URL in .env
- Browser console for errors
- Flask server running on port 5000

### Data not saving
- Check ayron_data.json permissions
- Flask server logs
- Database write access

## 📞 Support

Issues? Questions?
- GitHub Issues: [Create Issue](https://github.com/milkmanu/Ayronhtml/issues)
- Telegram: @milkmanu

## 📝 License

MIT License - use freely!

---

**Made with ❤️ for Ayron Savdo Team**
