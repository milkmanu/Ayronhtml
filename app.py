from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
from database import db
from config import FLASK_HOST, FLASK_PORT, WEBAPP_URL
import json

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════
def verify_telegram_user(data):
    """Verify Telegram WebApp data"""
    # In production, verify the hash
    # For now, just check if user_id exists
    return data.get('user', {}).get('id')

# ═══════════════════════════════════════════
# DATA ENDPOINTS
# ═══════════════════════════════════════════
@app.route('/api/data', methods=['GET'])
def get_all_data():
    """Get all data for WebApp"""
    return jsonify(db.get_all())

@app.route('/api/user-role/<int:user_id>', methods=['GET'])
def get_user_role(user_id):
    """Get user role (ega, hisobchi, ishchi)"""
    role = db.get_user_role(user_id)
    return jsonify({'role': role})

# ═══════════════════════════════════════════
# SOTUV (SALES)
# ═══════════════════════════════════════════
@app.route('/api/sotuv', methods=['POST'])
def add_sotuv():
    """Add new sale"""
    data = request.json
    data['sana'] = datetime.now().isoformat()
    
    # Add to database
    sotuv = db.add_sotuv(data)
    
    return jsonify({'success': True, 'data': sotuv}), 201

@app.route('/api/sotuv', methods=['GET'])
def get_sotuvlar():
    """Get all sales"""
    sotuvlar = db.data['sotuvlar']
    return jsonify(sotuvlar)

# ═══════════════════════════════════════════
# RASXOD (EXPENSES)
# ═══════════════════════════════════════════
@app.route('/api/rasxod', methods=['POST'])
def add_rasxod():
    """Add new expense"""
    data = request.json
    data['sana'] = datetime.now().isoformat()
    
    rasxod = db.add_rasxod(data)
    
    return jsonify({'success': True, 'data': rasxod}), 201

@app.route('/api/rasxod', methods=['GET'])
def get_rasxodlar():
    """Get all expenses"""
    rasxodlar = db.data['rasxodlar']
    return jsonify(rasxodlar)

# ═══════════════════════════════════════════
# ISHCHILAR (WORKERS)
# ═══════════════════════════════════════════
@app.route('/api/ishchilar', methods=['GET'])
def get_ishchilar():
    """Get all workers"""
    return jsonify(db.data['ishchilar'])

@app.route('/api/ishchilar', methods=['POST'])
def add_ishchi():
    """Add new worker"""
    data = request.json
    user_id = data.get('id')
    ism = data.get('ism')
    
    if not user_id or not ism:
        return jsonify({'error': 'ID va ism kerak'}), 400
    
    worker = db.add_ishchi(user_id, ism)
    return jsonify({'success': True, 'data': worker}), 201

# ═══════════════════════════════════════════
# MAHSULOTLAR (PRODUCTS)
# ═══════════════════════════════════════════
@app.route('/api/mahsulotlar', methods=['GET'])
def get_mahsulotlar():
    """Get all products"""
    return jsonify(db.data['mahsulotlar'])

@app.route('/api/mahsulotlar', methods=['POST'])
def add_mahsulot():
    """Add new product"""
    data = request.json
    prod_id = data.get('id')
    
    if not prod_id:
        return jsonify({'error': 'ID kerak'}), 400
    
    db.data['mahsulotlar'][prod_id] = {
        'name': data.get('name'),
        'price': data.get('price'),
        'emoji': data.get('emoji')
    }
    db.save()
    
    return jsonify({'success': True}), 201

# ═══════════════════════════════════════════
# QOLDIQ (INVENTORY)
# ═══════════════════════════════════════════
@app.route('/api/qoldiq', methods=['GET'])
def get_qoldiq():
    """Get inventory"""
    return jsonify(db.data['qoldiq'])

@app.route('/api/qoldiq/<prod_id>', methods=['PUT'])
def update_qoldiq(prod_id):
    """Update product quantity"""
    data = request.json
    miqdor = data.get('miqdor', 0)
    
    db.data['qoldiq'][prod_id] = miqdor
    db.save()
    
    return jsonify({'success': True})

# ═══════════════════════════════════════════
# HISOBOT (REPORTS)
# ═══════════════════════════════════════════
@app.route('/api/hisobot/bugun', methods=['GET'])
def hisobot_bugun():
    """Get today's report"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    sotuvlar = [s for s in db.data['sotuvlar'] if s['sana'].startswith(today)]
    rasxodlar = [r for r in db.data['rasxodlar'] if r['sana'].startswith(today)]
    
    total_sotuv = sum(s.get('summa', 0) for s in sotuvlar)
    total_rasxod = sum(r.get('summa', 0) for r in rasxodlar)
    foyda = total_sotuv - total_rasxod
    
    return jsonify({
        'date': today,
        'sotuvlar': sotuvlar,
        'rasxodlar': rasxodlar,
        'total_sotuv': total_sotuv,
        'total_rasxod': total_rasxod,
        'foyda': foyda
    })

# ═══════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# ═══════════════════════════════════════════
# STATIC FILES
# ═══════════════════════════════════════════
@app.route('/', methods=['GET'])
def serve_webapp():
    """Serve WebApp HTML"""
    return send_file('ayron_premium.html')

# ═══════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"🚀 Backend running on {FLASK_HOST}:{FLASK_PORT}")
    print(f"📱 WebApp: {WEBAPP_URL}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
