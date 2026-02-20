<p align="center">
  <img src="frontend/static/images/SheGlam.png" alt="SheGlam Logo" width="150" height="auto">
</p>

# SheGlam - Instant Makeup Services

A premier marketplace connecting women with top-tier makeup artists for weddings, parties, and everyday glam.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0%2B-blueviolet)

---

## 📌 Overview

**SheGlam** is a comprehensive web platform designed to simplify the process of finding and booking professional makeup artists. It features separate portals for clients and artists, a robust booking management system, and secure authentication. The platform ensures a safe, high-quality experience with verified artist profiles and transparent reviews.

---

## ✨ Key Features

🔐 **Secure Authentication**: Role-based access control (User, Artist, Admin) using JWT.  
🎨 **Artist Discovery**: Search and filter verified artists by category (Bridal, Party, Hair, etc.).  
📅 **Booking System**: Streamlined booking flow with status tracking (Pending, Approved, Completed).  
⭐ **Reviews & Ratings**: Transparent feedback system ensuring service quality.  
📱 **Fully Responsive**: Optimized for mobile, tablet, and desktop devices.  
🛠️ **Admin Dashboard**: complete oversight of users, artists, and bookings.  
🖱️ **One-Click Launch**: Easily start the project with `run_sheglam.bat`.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.10+, Flask, Flask-JWT-Extended |
| **Database** | MongoDB (NoSQL) |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |
| **Styling** | Custom CSS Variables + Tailwind Utility Classes |
| **Security** | Bcrypt Hashing, Environment Variables (.env) |

---

## 📁 Project Structure

```bash
SheGlam/
├── 🖱️ run_sheglam.bat          # Double-click to launch (Windows)
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── backend/                    # Flask Backend Logic
│   ├── app.py                  # Application Entry Point
│   ├── config.py               # Configuration & Secrets
│   ├── database/               # DB Connection
│   └── routes/                 # API Endpoints (Auth, Artist, Booking)
└── frontend/                   # UI Code
    ├── static/                 # CSS, JS, Images, Uploads
    └── templates/              # HTML Templates (Jinja2)
```

---

## 🚀 Quick Start

### Option 1 — Double-click (Windows)
Simply double-click **`run_sheglam.bat`**.
This script will automatically:
1.  Check/Install Python dependencies.
2.  Set up the `.env` configuration.
3.  Launch the server and open your browser to `http://localhost:5000`.

### Option 2 — Manual Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/PawanSimha/SheGlam.git
    cd SheGlam
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Copy `.env.example` to `.env` and update `MONGODB_URI` if needed.
    ```bash
    cp .env.example .env
    ```

5.  **Run the App**
    ```bash
    python backend/app.py
    ```
    Open Browser: `http://localhost:5000`

---

## 🔑 Default Credentials (Admin)

For administrative access, you can use the default admin account (or create one via `.env`):

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@sheglam.com` | `admin123` |
| **User** | *(Register via Signup)* | *User Created* |
| **Artist** | *(Register via Signup)* | *User Created* |

---

## 📋 Requirements

-   **Python 3.10+**
-   **MongoDB** (Local or Atlas)
-   Dependencies listed in `requirements.txt`:
    -   Flask
    -   pymongo
    -   flask-jwt-extended
    -   bcrypt
    -   python-dotenv

Install all with:
```bash
pip install -r requirements.txt
```

---

## 👤 Author

**Pawan Simha**

-   **GitHub**: [@PawanSimha](https://github.com/PawanSimha)
-   **LinkedIn**: [linkedin.com/in/pawansimha](https://linkedin.com/in/pawansimha)

---

## 📄 License

This project is open-source and available under the MIT License.
