from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'turkz_secret_key_123'

# Барлық брондар мен хабарламалар сақталатын тізімдер
bookings_list = []
contacts_list = []

# Админ құпиясөзі
ADMIN_PASSWORD = "admin123"

# Барлық елдер мен турлардың тізімі
tours = [
    {
        "id": 1,
        "hotel": "JUSTINIANO DELUXE RESORT 5*",
        "country": "Түркия",
        "city": "Аланья",
        "lat": 36.6289,
        "lon": 31.7514,
        "dates": "22 ноя - 29 ноя",
        "days": "8 күн / 7 түн",
        "stars": "★★★★★",
        "prices": {
            "Астана": {"price": "888 516 ₸", "old_price": "1 068 828 ₸"},
            "Алматы": {"price": "850 000 ₸", "old_price": "1 020 000 ₸"},
            "Шымкент": {"price": "910 000 ₸", "old_price": "1 100 000 ₸"},
            "Қарағанды": {"price": "870 000 ₸", "old_price": "1 050 000 ₸"},
            "Ақтау": {"price": "830 000 ₸", "old_price": "1 000 000 ₸"}
        },
        "discount": "-180 312 ₸ акция",
        "discount_reason": "Бұл скидка мен акция қонақүйдің маусымаралық арнайы субсидиясы және 'Ерте брондау' бағдарламасы аясында беріледі.",
        "desc": "Аланьяның ең көрікті жағалауында орналасқан. Жерорта теңізінің таңғажайып көрінісі, жағажай, ашық бассейн және All Inclusive жүйесі қарастырылған.",
        "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&auto=format&fit=crop&q=80",
        "gallery": [
            {
                "url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&auto=format&fit=crop&q=60",
                "title": "🌴 Жеке жағажай және демалыс аймағы",
                "desc": "Алтын құмды жағажай, жайлы шезлонгтар мен қолшатырлар. Теңіз суы мөлдір әрі балалармен шомылуға өте қауіпсіз."
            },
            {
                "url": "https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&auto=format&fit=crop&q=60",
                "title": "🏊‍♂️ Панорамалық ашық бассейн және СПА",
                "desc": "Кең ашық бассейн, су сырғанақтары және кешкі уақыттағы әсем жарықтандыру. Демалушыларға арналған тегін салқын сусындар бар."
            }
        ],
        "reviews": [
            {"name": "Әділхан", "text": "Өте керемет қонақүй! Отбасымен демалуға таптырмас орын."},
            {"name": "Мадина", "text": "Тамағы өте дәмді, жағажайы таза. Менеджерлерге үлкен рақмет!"}
        ]
    },
    {
        "id": 2,
        "hotel": "RIXOS SUNGATE 5*",
        "country": "Түркия",
        "city": "Анталия",
        "lat": 36.6715,
        "lon": 30.5516,
        "dates": "15 ноя - 22 ноя",
        "days": "7 күн / 6 түн",
        "stars": "★★★★★",
        "prices": {
            "Астана": {"price": "750 000 ₸", "old_price": "950 000 ₸"},
            "Алматы": {"price": "720 000 ₸", "old_price": "920 000 ₸"},
            "Шымкент": {"price": "770 000 ₸", "old_price": "970 000 ₸"},
            "Қарағанды": {"price": "740 000 ₸", "old_price": "940 000 ₸"},
            "Ақтау": {"price": "700 000 ₸", "old_price": "900 000 ₸"}
        },
        "discount": "-200 000 ₸ супер жеңілдік",
        "discount_reason": "Авиакомпаниямен жасалған тікелей келісім-шарт және топтық чартерлік рейстердің арқасында орын алған үнемдеу.",
        "desc": "Тау мен теңіз аясындағы сәнді демалыс орны. Аквапарк, әлемдік деңгейдегі мейрамханалар және кешкі шоулар сізді күтеді.",
        "img": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1200&auto=format&fit=crop&q=80",
        "gallery": [
            {
                "url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop&q=60",
                "title": "🏰 Сәнді виллалар мен жасыл аумақ",
                "desc": "Тау етегіндегі таза ауа мен заманауи сәулет өнері үйлескен демалыс корпустары."
            }
        ],
        "reviews": [
            {"name": "Нұрсұлтан", "text": "Шоулар мен аквапарк өте ұнады. Керемет демалыс болды!"}
        ]
    },
    {
        "id": 3,
        "hotel": "SUNRISE ARABIAN BEACH 5*",
        "country": "Египет",
        "city": "Шарм-эль-Шейх",
        "lat": 27.9158,
        "lon": 34.3300,
        "dates": "10 ноя - 17 ноя",
        "days": "7 күн / 6 түн",
        "stars": "★★★★★",
        "prices": {
            "Астана": {"price": "490 000 ₸", "old_price": "600 000 ₸"},
            "Алматы": {"price": "470 000 ₸", "old_price": "580 000 ₸"},
            "Шымкент": {"price": "510 000 ₸", "old_price": "620 000 ₸"},
            "Қарағанды": {"price": "485 000 ₸", "old_price": "595 000 ₸"},
            "Ақтау": {"price": "460 000 ₸", "old_price": "570 000 ₸"}
        },
        "discount": "-110 000 ₸ акция",
        "discount_reason": "Қызыл теңіз курорттарына маусымдық арнайы ұшу бағдарламасы бойынша берілген жеңілдік.",
        "desc": "Қызыл теңіздің маржан рифтерімен танымал керемет курорт. Дайвинг және жағажайдағы ұмытылмас демалыс.",
        "img": "https://images.unsplash.com/photo-1568322445074-8eb1203b12d2?w=1200&auto=format&fit=crop&q=80",
        "gallery": [
            {
                "url": "https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&auto=format&fit=crop&q=60",
                "title": "🐠 Маржан рифтері мен дайвинг орталығы",
                "desc": "Қызыл теңіздің түрлі-түсті балықтары мен маржандарын тамашалауға арналған арнайы понтон."
            }
        ],
        "reviews": [
            {"name": "Жанар", "text": "Су асты әлемі өте әдемі екен, рифтерді көріп таңқалдым."}
        ]
    },
    {
        "id": 4,
        "hotel": "SUN SIYAM IRU FUSHI 5*",
        "country": "Мальдивы",
        "city": "Мале",
        "lat": 2.7878,
        "lon": 73.4070,
        "dates": "05 жел - 13 жел",
        "days": "8 күн / 7 түн",
        "stars": "★★★★★",
        "prices": {
            "Астана": {"price": "1 150 000 ₸", "old_price": "1 350 000 ₸"},
            "Алматы": {"price": "1 120 000 ₸", "old_price": "1 320 000 ₸"},
            "Шымкент": {"price": "1 180 000 ₸", "old_price": "1 380 000 ₸"},
            "Қарағанды": {"price": "1 140 000 ₸", "old_price": "1 340 000 ₸"},
            "Ақтау": {"price": "1 100 000 ₸", "old_price": "1 300 000 ₸"}
        },
        "discount": "-200 000 ₸ акция",
        "discount_reason": "Мұхит үстіндегі виллалар мен элиталық демалысқа арналған маусымдық жеңілдік.",
        "desc": "Мұхит үстіндегі виллалар, мөлдір су және тропикалық табиғат аясындағы жұмақ демалыс.",
        "img": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1200&auto=format&fit=crop&q=80",
        "gallery": [
            {
                "url": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&auto=format&fit=crop&q=60",
                "title": "🌊 Су үстіндегі жеке бунгалолар",
                "desc": "Тікелей мұхитқа түсетін баспалдағы бар жеке виллалар."
            }
        ],
        "reviews": [
            {"name": "Арай", "text": "Өмірімдегі ең әдемі демалыс болды!"}
        ]
    }
]


@app.route('/')
def home():
    selected_city = request.args.get('city_from', 'Астана')
    selected_country = request.args.get('country', 'Барлық елдер')

    filtered = tours
    if selected_country != 'Барлық елдер':
        filtered = [t for t in filtered if t['country'] == selected_country]

    html = f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>TurKz - Туристік агенттік</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background-color: #f0f3f7; color: #333; }}
            .top-bar {{ background: #0088cc; color: white; padding: 12px 40px; display: flex; align-items: center; justify-content: space-between; }}
            .logo {{ font-size: 24px; font-weight: bold; background: #ffcc00; color: #002b49; padding: 5px 15px; border-radius: 6px; }}
            .nav-links {{ display: flex; gap: 12px; align-items: center; }}
            .admin-link {{ color: white; background: #28a745; padding: 8px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }}
            .admin-link:hover {{ background: #218838; }}
            .my-bookings-link {{ color: white; background: #ff6600; padding: 8px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }}
            .my-bookings-link:hover {{ background: #e55c00; }}
            .contact-link {{ color: white; background: #17a2b8; padding: 8px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }}
            .contact-link:hover {{ background: #138496; }}

            .hero-header {{ background: linear-gradient(rgba(0,43,73,0.7), rgba(0,43,73,0.7)), url('https://images.unsplash.com/photo-1527838832706-5058004cdec3?w=1200&auto=format&fit=crop&q=60'); background-size: cover; color: white; text-align: center; padding: 40px 20px; }}
            .hero-header h1 {{ font-size: 30px; margin: 0 0 10px 0; }}

            .filter-container {{ max-width: 1000px; margin: -30px auto 30px auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); position: relative; z-index: 10; }}
            .search-form {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; }}
            .form-group {{ display: flex; flex-direction: column; }}
            .form-group label {{ font-size: 12px; color: #777; margin-bottom: 5px; text-transform: uppercase; font-weight: bold; }}
            .form-group select, .form-group input {{ padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }}
            .btn-search {{ background: #ff6600; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; align-self: flex-end; }}
            .btn-search:hover {{ background: #e55c00; }}

            .main-content {{ max-width: 1000px; margin: 30px auto; padding: 0 20px; }}
            .section-title {{ font-size: 22px; font-weight: bold; margin-bottom: 20px; color: #1a2b4c; }}

            .hot-card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); display: flex; margin-bottom: 25px; position: relative; }}
            .discount-tag {{ position: absolute; top: 15px; left: 15px; background: #28a745; color: white; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; z-index: 2; }}
            .card-img {{ width: 320px; height: 210px; object-fit: cover; }}
            .card-body {{ padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}
            .hotel-name {{ font-size: 20px; font-weight: bold; color: #1a2b4c; margin: 0; text-decoration: none; }}
            .hotel-name:hover {{ color: #0088cc; }}
            .stars {{ color: #ffcc00; margin: 5px 0; }}
            .location {{ color: #666; font-size: 14px; }}
            .dates {{ background: #eef2f7; display: inline-block; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 500; margin-top: 10px; }}
            .card-right {{ padding: 20px; border-left: 1px solid #eee; display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-end; min-width: 180px; }}
            .old-price {{ text-decoration: line-through; color: #999; font-size: 14px; }}
            .price {{ font-size: 24px; color: #d9534f; font-weight: bold; margin: 5px 0; }}
            .btn-select {{ background: #0088cc; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: bold; text-align: center; }}
            .btn-select:hover {{ background: #006699; }}
        </style>
    </head>
    <body>
        <div class="top-bar">
            <div class="logo">TurKz</div>
            <div class="nav-links">
                <a href="/contact" class="contact-link">📞 Байланысу</a>
                <a href="/my-bookings" class="my-bookings-link">🔍 Менің брондарым</a>
                <a href="/admin/dashboard" class="admin-link">📊 Брондар тізімі (Админ)</a>
                <span style="font-size: 14px;">8 (747) 000-00-00</span>
            </div>
        </div>
        <div class="hero-header">
            <h1>Қазақстанның кез келген қаласынан әлемнің түкпір-түкпіріне турлар</h1>
            <p>Ыңғайлы бағытты таңдап, акциямен саяхаттаңыз!</p>
        </div>

        <div class="filter-container">
            <form class="search-form" method="GET" action="/">
                <div class="form-group">
                    <label>Қай қаладан ұшу:</label>
                    <select name="city_from">
                        <option value="Астана" {"selected" if selected_city == "Астана" else ""}>Астанадан</option>
                        <option value="Алматы" {"selected" if selected_city == "Алматы" else ""}>Алматыдан</option>
                        <option value="Шымкент" {"selected" if selected_city == "Шымкент" else ""}>Шымкенттен</option>
                        <option value="Қарағанды" {"selected" if selected_city == "Қарағанды" else ""}>Қарағандыдан</option>
                        <option value="Ақтау" {"selected" if selected_city == "Ақтау" else ""}>Ақтаудан</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Бағыт (Ел):</label>
                    <select name="country">
                        <option value="Барлық елдер" {"selected" if selected_country == "Барлық елдер" else ""}>Барлық елдер</option>
                        <option value="Түркия" {"selected" if selected_country == "Түркия" else ""}>Түркия 🇹🇷</option>
                        <option value="Египет" {"selected" if selected_country == "Египет" else ""}>Египет 🇪🇬</option>
                        <option value="ОАЭ" {"selected" if selected_country == "ОАЭ" else ""}>ОАЭ 🇦🇪</option>
                        <option value="Мальдивы" {"selected" if selected_country == "Мальдивы" else ""}>Мальдивы 🇲🇻</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Ұшу күні:</label>
                    <input type="text" value="Алдағы күндері">
                </div>
                <button type="submit" class="btn-search">Тур іздеу</button>
            </form>
        </div>

        <div class="main-content">
            <div class="section-title">🔥 {selected_city} қаласынан ұшуға арналған ысық турлар</div>
    '''

    for tour in filtered:
        city_price_info = tour['prices'].get(selected_city, tour['prices']['Астана'])
        current_price = city_price_info['price']
        old_price = city_price_info['old_price']

        html += f'''
            <div class="hot-card">
                <div class="discount-tag">{tour['discount']}</div>
                <img src="{tour['img']}" class="card-img" alt="{tour['hotel']}">
                <div class="card-body">
                    <div>
                        <a href="/tour/{tour['id']}?city={selected_city}" class="hotel-name">{tour['hotel']}</a>
                        <div class="stars">{tour['stars']}</div>
                        <div class="location">📍 {tour['country']}, {tour['city']}</div>
                        <div class="dates">✈️ {selected_city} қаласынан | 📅 {tour['dates']} ({tour['days']})</div>
                    </div>
                </div>
                <div class="card-right">
                    <div class="old-price">{old_price}</div>
                    <div class="price">{current_price}</div>
                    <a href="/tour/{tour['id']}?city={selected_city}" class="btn-select">Толығырақ</a>
                </div>
            </div>
        '''

    html += '''
        </div>
    </body>
    </html>
    '''
    return html


# Әдемі градиентті Админ кіру беті
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error_msg = ""
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            error_msg = "Құпиясөз қате! Қайта көріңіз."

    return f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>Менеджер кіруі - TurKz</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            .login-box {{
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                width: 380px;
                text-align: center;
            }}
            h2 {{ color: #1a2b4c; margin-top: 0; font-size: 24px; }}
            input {{
                width: 100%;
                padding: 14px;
                margin: 15px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-sizing: border-box;
                font-size: 15px;
            }}
            input:focus {{
                border-color: #0088cc;
                outline: none;
                box-shadow: 0 0 5px rgba(0,136,204,0.3);
            }}
            button {{
                background: #0088cc;
                color: white;
                border: none;
                padding: 14px;
                width: 100%;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.2s;
            }}
            button:hover {{ background: #006699; }}
            .back-link {{ display: block; margin-top: 20px; color: #0088cc; text-decoration: none; font-size: 14px; font-weight: bold; }}
            .error {{ color: #d9534f; font-size: 14px; margin-bottom: 10px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔐 Менеджер кіруі</h2>
            <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Брондар тізімін көру үшін құпиясөзді енгізіңіз.</p>
            {f"<div class='error'>{error_msg}</div>" if error_msg else ""}
            <form method="POST">
                <input type="password" name="password" required placeholder="Құпиясөз (admin123)">
                <button type="submit">Кіру</button>
            </form>
            <a href="/" class="back-link">&larr; Басты бетке қайту</a>
        </div>
    </body>
    </html>
    '''


# Админ панель (WhatsApp-пен байланысу функциясы қосылған)
@app.route('/admin/dashboard')
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    rows_html = ""
    if not bookings_list:
        rows_html = '<tr><td colspan="7" style="text-align:center; padding: 20px; color: #777;">Әзірге брондау жоқ.</td></tr>'
    else:
        for idx, b in enumerate(bookings_list, 1):
            phone_clean = ''.join(filter(str.isdigit, b['phone']))
            rows_html += f'''
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{idx}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd; font-weight:bold;">{b['name']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                    <a href="https://wa.me/{phone_clean}" target="_blank" style="color: #28a745; text-decoration: none; font-weight: bold;" title="WhatsApp-қа жазу">💬 {b['phone']}</a>
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{b['hotel']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{b['city_from']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd; color:#d9534f; font-weight:bold;">{b['price']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd; font-size:12px; color:#666;">{b['time']}</td>
            </tr>
            '''

    contacts_html = ""
    if not contacts_list:
        contacts_html = '<tr><td colspan="5" style="text-align:center; padding: 20px; color: #777;">Әзірге байланыс сұраныстары жоқ.</td></tr>'
    else:
        for idx, c in enumerate(contacts_list, 1):
            phone_clean_c = ''.join(filter(str.isdigit, c['phone']))
            contacts_html += f'''
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{idx}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd; font-weight:bold;">{c['name']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                    <a href="https://wa.me/{phone_clean_c}" target="_blank" style="color: #28a745; text-decoration: none; font-weight: bold;" title="WhatsApp-қа жазу">💬 {c['phone']}</a>
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{c['message']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd; font-size:12px; color:#666;">{c['time']}</td>
            </tr>
            '''

    return f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head><meta charset="UTF-8"><title>Админ панель</title></head>
    <body style="font-family: Arial; background: #f0f3f7; margin:0;">
        <div style="background: #0088cc; color: white; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin:0;">TurKz - Админ панель</h2>
            <a href="/admin/logout" style="color:white; background:#d9534f; padding:8px 15px; text-decoration:none; border-radius:6px; font-weight:bold;">Шығу</a>
        </div>
        <div style="max-width: 1100px; margin: 30px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <a href="/" style="background: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 6px; font-weight: bold;">&larr; Сайтқа қайту</a>

            <h2>📋 Брондар тізімі</h2>
            <p style="font-size: 13px; color: #666;">Нөмірді басу арқылы клиентке тікелей WhatsApp-та жаза аласыз:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 30px;">
                <thead>
                    <tr style="background: #0088cc; color: white; text-align: left;">
                        <th style="padding: 10px;">№</th>
                        <th style="padding: 10px;">Аты</th>
                        <th style="padding: 10px;">Телефон (WhatsApp)</th>
                        <th style="padding: 10px;">Қонақүй</th>
                        <th style="padding: 10px;">Қаласы</th>
                        <th style="padding: 10px;">Бағасы</th>
                        <th style="padding: 10px;">Уақыты</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>

            <h2>📞 Байланысу сұраныстары</h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <thead>
                    <tr style="background: #17a2b8; color: white; text-align: left;">
                        <th style="padding: 10px;">№</th>
                        <th style="padding: 10px;">Аты</th>
                        <th style="padding: 10px;">Телефон (WhatsApp)</th>
                        <th style="padding: 10px;">Хабарлама</th>
                        <th style="padding: 10px;">Уақыты</th>
                    </tr>
                </thead>
                <tbody>{contacts_html}</tbody>
            </table>
        </div>
    </body>
    </html>
    '''


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))


# Байланысу беті
@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    success = False
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('message')
        time = datetime.now().strftime("%Y-%m-%d %H:%M")

        if name and phone:
            contacts_list.append({
                "name": name,
                "phone": phone,
                "message": message,
                "time": time
            })
            success = True

    return f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>Байланысу - TurKz</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ max-width: 600px; width: 100%; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
            h2 {{ color: #1a2b4c; margin-top: 0; }}
            input, textarea {{ width: 100%; padding: 14px; margin: 8px 0 20px 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; font-size: 15px; }}
            button {{ background: #17a2b8; color: white; border: none; padding: 14px; width: 100%; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; }}
            button:hover {{ background: #138496; }}
            .success-box {{ background: #e6f4ea; border-left: 4px solid #28a745; padding: 15px; border-radius: 6px; margin-bottom: 20px; color: #28a745; font-weight: bold; }}
            .back-link {{ display: inline-block; margin-top: 20px; color: #0088cc; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📞 Бізбен байланысу</h2>
            <p style="font-size: 14px; color: #666; margin-bottom: 20px;">Сұрақтарыңыз болса деректеріңізді қалдырыңыз, менеджерлер тез арада хабарласады.</p>
            {f"<div class='success-box'>🎉 Хабарламаңыз сәтті жіберілді!</div>" if success else ""}
            <form method="POST">
                <label style="font-size: 13px; font-weight: bold; color: #444;">Аты-жөніңіз:</label>
                <input type="text" name="name" required placeholder="Мысалы: Ернар">
                <label style="font-size: 13px; font-weight: bold; color: #444;">Телефон нөміріңіз:</label>
                <input type="text" name="phone" required placeholder="+7 (777) 000-00-00">
                <label style="font-size: 13px; font-weight: bold; color: #444;">Хабарлама / сұрағыңыз:</label>
                <textarea name="message" rows="4" placeholder="Сұрағыңызды жазыңыз..."></textarea>
                <button type="submit">Хабарлама жіберу</button>
            </form>
            <br><a href="/" class="back-link">&larr; Басты бетке қайту</a>
        </div>
    </body>
    </html>
    '''


# Менің брондарым беті
@app.route('/my-bookings', methods=['GET', 'POST'])
def my_bookings():
    search_query = request.form.get('query', '').strip()
    results = []

    if request.method == 'POST' and search_query:
        results = [b for b in bookings_list if
                   search_query.lower() in b['phone'].lower() or search_query.lower() in b['name'].lower()]

    results_html = ""
    if request.method == 'POST':
        if not results:
            results_html = '<p style="color: #d9534f; text-align: center; margin-top: 20px;">Бұл аты-жөні немесе телефон нөмірі бойынша ешқандай брондау табылмады.</p>'
        else:
            for b in results:
                results_html += f'''
                <div style="background: #eef2f7; padding: 20px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #28a745;">
                    <h3 style="margin: 0 0 10px 0; color: #1a2b4c;">🏨 {b['hotel']}</h3>
                    <p style="margin: 5px 0;">👤 <b>Аты-жөні:</b> {b['name']}</p>
                    <p style="margin: 5px 0;">📞 <b>Телефон:</b> {b['phone']}</p>
                    <p style="margin: 5px 0;">✈️ <b>Ұшу қаласы:</b> {b['city_from']}</p>
                    <p style="margin: 5px 0;">💰 <b>Бағасы:</b> <span style="color: #d9534f; font-weight: bold;">{b['price']}</span></p>
                    <p style="margin: 5px 0; font-size: 13px; color: #666;">⏰ <b>Брондалған уақыты:</b> {b['time']}</p>
                    <p style="margin: 10px 0 0 0; color: #28a745; font-weight: bold; font-size: 14px;">✅ Статус: Брондау расталды.</p>
                </div>
                '''

    return f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>Менің брондарым - TurKz</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ max-width: 600px; width: 100%; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
            h2 {{ color: #1a2b4c; margin-top: 0; }}
            input {{ width: 100%; padding: 14px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; font-size: 15px; }}
            button {{ background: #0088cc; color: white; border: none; padding: 14px; width: 100%; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; }}
            button:hover {{ background: #006699; }}
            .back-link {{ display: inline-block; margin-top: 20px; color: #0088cc; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔍 Менің брондарымды тексеру</h2>
            <form method="POST">
                <input type="text" name="query" required placeholder="Мысалы: +7 (777) 000-00-00" value="{search_query}">
                <button type="submit">Брондарымды табу</button>
            </form>
            {results_html}
            <br><a href="/" class="back-link">&larr; Басты бетке қайту</a>
        </div>
    </body>
    </html>
    '''


# Тур сипаттамасы (Карта, бағалар кестесі және пікірлермен)
@app.route('/tour/<int:tour_id>', methods=['GET', 'POST'])
def tour_detail(tour_id):
    tour = next((t for t in tours if t['id'] == tour_id), None)
    city_from = request.args.get('city', 'Астана')
    if not tour:
        return "Тур табылмады!", 404

    city_price_info = tour['prices'].get(city_from, tour['prices']['Астана'])
    current_price = city_price_info['price']
    old_price = city_price_info['old_price']

    if request.method == 'POST':
        user_name = request.form.get('author')
        user_text = request.form.get('review_text')
        if user_name and user_text:
            tour['reviews'].append({"name": user_name, "text": user_text})

    html = f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>{tour['hotel']} - TurKz</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background-color: #f0f3f7; color: #333; }}
            .top-bar {{ background: #0088cc; color: white; padding: 12px 40px; display: flex; align-items: center; justify-content: space-between; }}
            .logo {{ font-size: 24px; font-weight: bold; background: #ffcc00; color: #002b49; padding: 5px 15px; border-radius: 6px; }}
            .page-container {{ max-width: 1100px; margin: 30px auto; display: flex; gap: 30px; padding: 0 20px; }}
            .left-content {{ flex: 2; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .right-sidebar {{ flex: 1; display: flex; flex-direction: column; gap: 20px; }}
            .sidebar-box {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a2b4c; margin-top: 0; font-size: 24px; }}
            .main-img {{ width: 100%; height: 350px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; }}
            #map {{ width: 100%; height: 220px; border-radius: 8px; margin-top: 10px; }}
            .discount-box {{ background: #e6f4ea; border-left: 4px solid #28a745; padding: 12px; border-radius: 4px; margin: 15px 0; font-size: 14px; }}
            .price-tag {{ font-size: 26px; color: #d9534f; font-weight: bold; }}
            .old-price {{ text-decoration: line-through; color: #777; font-size: 15px; }}
            .discount-badge {{ background: #28a745; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; display: inline-block; margin-bottom: 10px; font-size: 13px; }}
            .btn-book {{ background: #ff6600; color: white; padding: 14px; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: bold; display: block; text-align: center; margin-top: 15px; }}
            .btn-book:hover {{ background: #e55c00; }}
            .back-link {{ display: inline-block; margin-bottom: 15px; color: #0088cc; text-decoration: none; font-weight: bold; }}
            .reviews-section {{ margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            .review-card {{ background: #f9f9f9; padding: 12px; border-radius: 6px; margin-bottom: 10px; border-left: 3px solid #0088cc; font-size: 14px; }}
            .review-form input, .review-form textarea {{ width: 100%; padding: 10px; margin: 6px 0 12px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
            .review-form button {{ background: #0088cc; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; }}
            .matrix-container {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 30px; overflow-x: auto; }}
            .price-matrix {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; }}
            .price-matrix th, .price-matrix td {{ border: 1px solid #e2e8f0; padding: 10px 8px; }}
            .price-matrix th {{ background: #f8fafc; color: #1a2b4c; font-weight: bold; }}
            .price-cell {{ background: #0088cc; color: white; border-radius: 4px; padding: 6px; font-weight: bold; text-decoration: none; display: block; }}
            .price-cell:hover {{ background: #006699; }}
            .empty-cell {{ color: #cbd5e1; }}
        </style>
    </head>
    <body>
        <div class="top-bar">
            <div class="logo">TurKz</div>
            <div>📞 8 (747) 000-00-00</div>
        </div>

        <div class="page-container">
            <div class="left-content">
                <a href="/?city_from={city_from}" class="back-link">&larr; Барлық турларға қайту</a>
                <div class="discount-badge">Арнайы акция: {tour['discount']}</div>
                <h1>{tour['hotel']}</h1>
                <div class="stars" style="color: #ffcc00; font-size: 18px; margin-bottom: 15px;">{tour['stars']} (📍 {tour['country']}, {tour['city']})</div>

                <img src="{tour['img']}" class="main-img" alt="{tour['hotel']}">

                <h3>🏖️ Қонақүй туралы сипаттама:</h3>
                <p style="font-size: 15px; line-height: 1.6; color: #555;">{tour['desc']}</p>

                <div class="discount-box">
                    <h4 style="margin: 0 0 5px 0; color: #28a745;">💡 Бұл акция не үшін беріледі?</h4>
                    <p style="margin: 0; color: #444;">{tour['discount_reason']}</p>
                </div>

                <div class="reviews-section">
                    <h3>💬 Туристердің пікірлері</h3>
    '''

    for rev in tour['reviews']:
        html += f'''
                    <div class="review-card">
                        <p style="margin: 0 0 4px 0; font-weight: bold; color: #0088cc;">{rev['name']}</p>
                        <p style="margin: 0; color: #555;">{rev['text']}</p>
                    </div>
        '''

    html += f'''
                    <h4 style="margin-top: 20px;">Өз пікіріңізді қалдырыңыз:</h4>
                    <form class="review-form" method="POST">
                        <label style="font-size: 13px; font-weight:bold;">Аты-жөніңіз:</label>
                        <input type="text" name="author" required placeholder="Мысалы: Айбек">

                        <label style="font-size: 13px; font-weight:bold;">Пікіріңіз:</label>
                        <textarea name="review_text" rows="3" required placeholder="Ойыңызбен бөлісіңіз..."></textarea>

                        <button type="submit">Пікір қалдыру</button>
                    </form>
                </div>
            </div>

            <div class="right-sidebar">
                <div class="sidebar-box">
                    <h3 style="margin-top: 0; font-size: 16px; color: #1a2b4c;">🗺️ Отель на карте</h3>
                    <div id="map"></div>
                </div>

                <div class="sidebar-box">
                    <div style="font-size: 13px; color: #666;">✈️ Ұшу қаласы: <b>{city_from}</b></div>
                    <div style="font-size: 13px; color: #666; margin: 4px 0 10px 0;">📅 {tour['dates']} ({tour['days']})</div>
                    <div class="old-price">Бұрынғы бағасы: {old_price}</div>
                    <div class="price">Бағасы: <span class="price-tag">{current_price}</span></div>

                    <a href="/book/{tour['id']}?city={city_from}" class="btn-book">Турды брондау</a>
                </div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            var lat = {tour['lat']};
            var lon = {tour['lon']};
            var map = L.map('map').setView([lat, lon], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
            L.marker([lat, lon]).addTo(map).bindPopup("<b>{tour['hotel']}</b>").openPopup();
        </script>
    </body>
    </html>
    '''
    return html


# Брондау беті
@app.route('/book/<int:tour_id>', methods=['GET', 'POST'])
def book_tour(tour_id):
    tour = next((t for t in tours if t['id'] == tour_id), None)
    city_from = request.args.get('city', 'Астана')
    if not tour:
        return "Тур табылмады!", 404

    city_price_info = tour['prices'].get(city_from, tour['prices']['Астана'])
    current_price = city_price_info['price']

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        bookings_list.append({
            "name": name,
            "phone": phone,
            "hotel": tour['hotel'],
            "city_from": city_from,
            "price": current_price,
            "time": current_time
        })

        return f'''
        <div style="font-family: Arial; text-align: center; padding: 60px; background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0;">
            <div style="max-width: 500px; width: 100%; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.3);">
                <h1 style="color: #28a745; margin-top: 0;">🎉 Өтініміңіз сәтті қабылданды!</h1>
                <p style="font-size: 16px; color: #333;">Құрметті <b>{name}</b>, сіздің <b>{city_from}</b> қаласынан <b>{tour['hotel']}</b> турына берген броныңыз тіркелді.</p>
                <br>
                <a href="/my-bookings" style="display: inline-block; padding: 12px 25px; background: #ff6600; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-right: 10px;">Менің брондарым</a>
                <a href="/" style="display: inline-block; padding: 12px 25px; background: #0088cc; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">Басты бет</a>
            </div>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html lang="kk">
    <head>
        <meta charset="UTF-8">
        <title>Брондау - TurKz</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }}
            .booking-card {{ background: white; width: 750px; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
            .booking-img-container {{ position: relative; width: 100%; height: 350px; }}
            .booking-img-container img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
            .img-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 25px 30px; }}
            .booking-form-body {{ padding: 35px 40px; }}
            input {{ width: 100%; padding: 14px; margin: 8px 0 20px 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; font-size: 15px; }}
            button {{ background: #ff6600; color: white; border: none; padding: 15px; width: 100%; font-size: 17px; font-weight: bold; border-radius: 8px; cursor: pointer; }}
            button:hover {{ background: #e55c00; }}
            .badge-sale {{ background: #28a745; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="booking-card">
            <div class="booking-img-container">
                <img src="{tour['img']}" alt="Тур суреті">
                <div class="img-overlay">
                    <span class="badge-sale">Акция: {tour['discount']}</span>
                    <h2 style="margin: 5px 0; font-size: 24px;">{tour['hotel']}</h2>
                    <p style="margin: 0; font-size: 14px; opacity: 0.9;">📍 {tour['country']}, {tour['city']} | ✈️ Ұшу қаласы: <b>{city_from}</b></p>
                    <div style="font-size: 22px; color: #ffcc00; font-weight: bold; margin-top: 6px;">Бағасы: {current_price}</div>
                </div>
            </div>

            <div class="booking-form-body">
                <h3 style="margin-top: 0; color: #1a2b4c; font-size: 22px;">Онлайн брондау</h3>
                <form method="POST">
                    <label style="font-size: 13px; font-weight: bold; color: #444;">Аты-жөніңіз:</label>
                    <input type="text" name="name" required placeholder="Мысалы: Нұрсейіт Нұрланұлы">

                    <label style="font-size: 13px; font-weight: bold; color: #444;">Телефон нөміріңіз:</label>
                    <input type="text" name="phone" required placeholder="+7 (777) 000-00-00">

                    <button type="submit">Брондауды растау</button>
                </form>
                <br><a href="/tour/{tour['id']}?city={city_from}" style="color: #0088cc; text-decoration: none; font-size: 14px; font-weight: bold;">&larr; Артқа қайту</a>
            </div>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)