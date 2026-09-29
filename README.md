# 🛍️ Veylora — Modern Full-Stack E-Commerce Platform

A production-structured, high-performance E-Commerce Web Application engineered with **Python**, **Django 5.x**, **HTML5**, **Modern CSS3**, and **Vanilla JavaScript**.

Designed with a heavy focus on **Backend Concurrency**, **ACID Transactional Integrity**, **Automated Test Coverage**, and **Mobile-First Responsive Design**.

---

## ✨ Key Features

- 🛒 **Session-Based Cart Engine**: Client-agnostic cart with live stock validation and server-side dynamic calculations.
- 🔒 **ACID-Compliant Atomic Checkout**: Powered by Django's `@transaction.atomic` and `select_for_update()` row locking to eliminate race conditions during high-concurrency purchase spikes.
- 📦 **Immutable Snapshot Persistence**: Stores historical price and product name snapshots at the `OrderItem` level for auditable records.
- 📱 **Modern Responsive UI**: Mobile off-canvas drawer, floating bottom navigation bar, 2-column mobile cards, and desktop layouts.
- 🛠️ **Fulfillment Dashboard**: Custom Django Admin suite for real-time inventory management and order status workflows (`Pending` → `Processing` → `Shipped` → `Delivered`).
- 🧪 **100% Passing Test Suite**: 18+ comprehensive unit and integration tests covering cart mutations, stock bounds, and authentication boundaries.

---

## 🏗️ Project Structure

```text
veylora-store/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── config/                  # Global project settings and URLs
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/                   # Core store application
│   ├── migrations/
│   ├── templates/store/     # HTML5 templates
│   ├── static/store/        # CSS3 & JavaScript assets
│   ├── admin.py             # Admin configurations
│   ├── cart.py              # Cart business logic
│   ├── forms.py             # User & Checkout forms
│   ├── models.py            # Category, Product, Order, OrderItem
│   ├── tests.py             # Automated unit & integration tests
│   ├── urls.py
│   └── views.py
└── media/                   # Product catalog images
    └── products/
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/veylora-store.git
cd veylora-store
```

### 2. Set Up Virtual Environment
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```

### 5. Apply Database Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Automated Tests
```bash
python manage.py test
```

### 8. Start Development Server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
Admin portal: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, Django 5.x
- **Database**: SQLite (Development) / PostgreSQL-ready (Production)
- **Frontend**: HTML5, Modern Vanilla CSS, Vanilla JavaScript (ES6+)
- **Testing**: Django Test Suite / PyTest

---

## 📄 License
MIT License. Free for learning and commercial extension.
