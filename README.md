# 📝 Project Report: QuizMaster

- **Name**: Gautham Krishna S
- **Roll No**: 23F2000466

---

## 🚀 Project Title:
**QuizMaster: Your Exam Preparation Hub**

---

## 📚 Frameworks and Libraries Used:
- **Python**: 3.11.9 🐍
- **SQLite**: 3.46.1 💾
- **Flask**: 3.0.2 🌐
- **Flask-SQLAlchemy**: 3.1.1 🛠️
- **Bootstrap**: 5.3.3 🎨
- **Jinja2**: 3.1.3 🔗
- **datetime**: Python’s Inbuilt Library ⏰
- **HTML, CSS, JavaScript**: Used for creating the frontend. 🖼️
- **Frontend Validation**: Added validation on forms to ensure proper data input before submission. ✅

---

# 🚀 Getting Started

Follow the instructions below to set up and run the Flask application locally.

## Prerequisites
- Python 3.x installed on your system.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/23f2000466/Quiz-Master
   cd Quiz-Master/QuizMaster
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   flask run
   ```

2. Access the application:  
   Open your browser and visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📝 Abstract:
This project is a multi-user application designed for **Admin** and **Users**, acting as an exam preparation platform for multiple courses. The development was structured in phases:

1. **Database Initialization**: Created tables for users, quizzes, and results with SQLite3, incorporating password hashing with bcrypt.
2. **Coding Environment Setup**: Modularized code and implemented Bootstrap for UI and Jinja2 for templates.
3. **Frontend Development**: Leveraged HTML, CSS, and JavaScript to create an intuitive and responsive user interface, including **frontend validation on forms** for better user experience and data integrity.
4. **Controllers Development**: Handled different user roles using Flask and Flask-SQLAlchemy.
5. **Testing**: Utilized dummy data to verify the backend and frontend functionality.

---

## 🌟 Core Functionalities:

### 👨‍💼 Admin:
1. Manage users and quizzes (Create, Edit, Delete).
2. Cascade delete quiz-related records upon quiz deletion.
3. Monitor all quiz attempts and scores.
4. Search and manage users with restricted access.
5. Summarize quiz statistics and user performance.

### 🧍 User:
1. Register, log in, and manage profile.
2. Select subjects and attempt quizzes.
3. View past quiz performance and track progress.
4. Rate quizzes and provide feedback.

---

## 📊 Database Schema:
![Schema image](https://github.com/user-attachments/assets/8a328953-ce72-49b0-8801-4d611382f4f9)

---

## 🌐 API Endpoints (Controller):
The API endpoints, defined in `controllers.py`, facilitate CRUD operations. Key endpoints include:
- User Management: Register, Login, and Profile Management.
- Quiz Management: Create, Update, and Delete Quizzes.
- Question Handling: Add and Retrieve Questions.
- Score Tracking: Fetch User Scores and Quiz Performance.

---

## 📽️ Video Demo:
[Watch Here](https://drive.google.com/file/d/1Ugx-WuqCiKHpBV9PR4rEtNDhB-rKgHD9/view?usp=drive_link)

---

