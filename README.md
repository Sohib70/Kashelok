# 💰 Kashelok (Kirim / Chiqim Hisoblash Tizimi)

**Kashelok** — bu foydalanuvchilar uchun shaxsiy **kirim va chiqimlarni boshqarish** tizimi.  
Har bir foydalanuvchi **o‘zining kategoriyalari, kirimlari va chiqimlarini** alohida yuritadi.  
Admin yoki boshqa foydalanuvchilar **boshqalarning ma’lumotlarini ko‘ra olmaydi**.  

---

## 🚀 Funksiyalar
- 🔑 Ro‘yxatdan o‘tish va login
- 👤 Profilni yangilash
- ➕ Yangi kategoriya qo‘shish (faqat foydalanuvchining o‘ziga tegishli)
- 💵 Kirim qo‘shish (summa, kategoriya, izoh, to‘lov turi)
- 🛒 Chiqim qo‘shish (summa, kategoriya, izoh, to‘lov turi)
- 📊 Kategoriyalar bo‘yicha jami summalarni ko‘rish
- 🌐 To‘lov turini tanlash: Naqd, Karta, Dollar
- ⏱ Har bir kirim/chiqim uchun sana saqlanadi
- 🔒 Har bir foydalanuvchi faqat o‘zining ma’lumotlarini ko‘radi

---

## 🛠 Texnologiyalar
- **Backend:** Python 3.x, Django 5.x
- **Database:** SQLite (standart), lekin PostgreSQL yoki MySQL ulash mumkin
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Autentifikatsiya:** Django Auth (login, logout, parolni tiklash)

---

## ⚙️ O‘rnatish bo‘yicha qo‘llanma

### 1. Loyihani clone qilish
```bash
git clone https://github.com/username/kashelok.git
cd kashelok
2. Virtual environment yaratish va ishga tushirish
Windows:

bash
Copy code
python -m venv .venv
.venv\Scripts\activate
Linux/Mac:

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
3. Kutubxonalarni o‘rnatish
bash
Copy code
pip install -r requirements.txt
4. Migratsiyalarni bajarish
bash
Copy code
python manage.py migrate
5. Superuser yaratish
bash
Copy code
python manage.py createsuperuser
6. Loyihani ishga tushirish
bash
Copy code
python manage.py runserver
Keyin brauzerda http://127.0.0.1:8000 manziliga o‘ting.

📂 Loyiha tuzilishi
bash
Copy code
Kashelok/
│── finance/              # Kirim/Chiqim uchun app
│   ├── models.py         # Income va Expense modellari
│   ├── views.py          # Kirim/chiqim logikasi
│   ├── urls.py           # Yo‘llar
│   ├── templates/        # HTML shablonlari
│
│── users/                # Foydalanuvchilar app
│   ├── models.py         # User modeli (agar kengaytirilgan bo‘lsa)
│   ├── forms.py          # Ro‘yxatdan o‘tish, login, parol tiklash
│   ├── views.py          # Login, register, profile
│   ├── templates/        # Login/register HTML
│
│── static/               # CSS/JS fayllar
│── templates/            # Umumiy shablonlar (base.html va boshqalar)
│── manage.py
│── requirements.txt
│── README.md
🔐 Xavfsizlik
Har bir foydalanuvchi faqat o‘zining kategoriyalari va tranzaksiyalarini ko‘radi.

Admin ham boshqa foydalanuvchilarning kirim/chiqimlarini ko‘ra olmaydi.

Login qilmagan foydalanuvchilar tizimdan foydalana olmaydi.

👨‍💻 Muallif
Sohib Xolbo‘riyev
Toshkent davlat iqtisodiyot universiteti talabasi

📜 Litsenziya
Bu loyiha o‘quv maqsadida yozilgan va erkin foydalanish mumkin.