# IvyIntel

## Overview

IvyIntel is an AI-powered real-time opportunity intelligence and student competency network designed to help students discover academic and professional opportunities from Ivy League universities in a centralized platform.

The system automatically monitors Ivy League university websites, extracts opportunities such as research programs, workshops, internships, and conferences, and categorizes them using artificial intelligence. It provides a personalized dashboard where students can view, filter, and explore opportunities efficiently.

In addition, IvyIntel introduces an intelligent ranking system called **InCoScore (Intelligent Competency Score)**, which evaluates student engagement and interaction with academic opportunities to measure competency and participation.

This project addresses the problem of fragmented opportunity information and lack of intelligent student performance tracking.

---

## Key Features

### Real-Time Opportunity Monitoring
- Automatically extracts opportunities from Ivy League university platforms using web scraping.

### AI-Based Opportunity Classification
- Classifies opportunities into domains such as:
  - Artificial Intelligence
  - Engineering
  - Law
  - Biomedical Sciences

### Student Authentication System
- Secure login and signup system using password hashing.

### Personalized Dashboard
- Provides filtered and categorized opportunity views based on university and academic domain.

### Opportunity Detail Page
- Displays full opportunity information and provides direct links to official university pages.

### Intelligent Recommendation System
- Recommends opportunities based on student interest.

### InCoScore Competency Ranking Engine
- Assigns intelligent competency scores based on user engagement such as:
  - Login activity
  - Viewing opportunities
  - Fetching new data

### Modern User Interface
- Professional dashboard with sidebar navigation, filtering system, and responsive design.

---

## System Architecture

```text
User
 │
 ▼
Flask Web Application
 │
 ├── Authentication System
 ├── Opportunity Scraper
 ├── AI Classification Module
 ├── InCoScore Ranking Engine
 │
 ▼
SQLite Database
 │
 ▼
Dashboard Interface



# IvyIntel  
An Intelligent Opportunity Discovery & Student Engagement Platform

---

## Installation Guide

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/ivyintel.git
cd ivyintel
```

---

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install flask requests beautifulsoup4 werkzeug
```

---

### Step 4: Initialize Database

```bash
python database.py
```

---

### Step 5: Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

# Usage

## Register or Login

Create a new account or log in using existing credentials.

---

## Dashboard Features

Users can:

- View opportunities  
- Filter by university  
- Filter by category  
- View opportunity details  
- Fetch real-time opportunity data  
- See personalized recommendations  
- View their InCoScore

---

## Opportunity Interaction

Users can:

- Open opportunity detail page  
- Visit official university pages  
- Improve their InCoScore through engagement  

---

# Project Structure

```
ivyintel/
│
├── app.py
├── database.py
├── scraper.py
├── classifier.py
│
├── database/
│   └── ivyintel.db
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── opportunity_detail.html
│
├── static/
│   ├── css/
│   ├── icons/
│   ├── logos/
│
├── venv/
└── README.md
```

---

# Technologies Used

## Backend
- Python  
- Flask  

## Frontend
- HTML  
- CSS  
- Jinja2  

## Database
- SQLite  

## Libraries
- Requests  
- BeautifulSoup  
- Werkzeug  

## Development Tools
- Visual Studio Code  
- Git  
- Python Virtual Environment  

---

# InCoScore Ranking System

The InCoScore engine measures student competency based on platform engagement.

| Activity              | Score |
|-----------------------|-------|
| Login                 | +2    |
| View Opportunity      | +5    |
| Fetch Opportunities   | +10   |

This enables intelligent student performance evaluation.

---

# Future Improvements

- Leaderboard system  
- Bookmark and save opportunities  
- Admin control panel  
- Advanced AI recommendation engine  
- Background automated scraping  
- Application tracking system  

---

# Contributing

Contributions are welcome.

## Steps:

1. Fork repository  

2. Create new branch:
```bash
git checkout -b feature-name
```

3. Commit changes:
```bash
git commit -m "Add new feature"
```

4. Push branch:
```bash
git push origin feature-name
```

5. Create Pull Request  

---

# License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this project.

---

# Author

Anurag Patel  
Artificial Intelligence Student  
Developer of IvyIntel  

---

