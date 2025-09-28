# FitAI - AI-Powered Fitness & Diet Management System

![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.12.6-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

FitAI is a comprehensive AI-powered web application that provides personalized fitness and diet recommendations using machine learning algorithms. The system helps users achieve their health goals through intelligent meal planning, workout suggestions, and health predictions.

---

## 🎯 Inspiration

In today's fast-paced world, maintaining a healthy lifestyle is challenging. With the rise of sedentary jobs, processed foods, and limited time for exercise, many people struggle to achieve their fitness goals. We were inspired by the need for accessible, personalized health guidance that leverages cutting-edge AI technology to make healthy living achievable for everyone.

The global obesity epidemic and increasing lifestyle diseases motivated us to create an intelligent system that combines nutrition science, exercise physiology, and machine learning to provide data-driven health recommendations.

---

## 🚀 What it does

FitAI revolutionizes personal health management by offering:

- **AI-Powered Weight Prediction**: Uses machine learning to predict weight changes based on caloric intake, activity levels, and user parameters
- **Smart Food Recognition**: Upload food photos to instantly get nutritional analysis using computer vision AI
- **Personalized Diet Plans**: Rule-based and ML-driven meal planning tailored to individual goals
- **Health Risk Assessment**: Predict heart and lung disease risks using medical data analysis
- **Intelligent Workout Generation**: AI-generated exercise plans based on user profiles and goals
- **Comprehensive User Dashboard**: Track progress, save results, and manage health journey
- **Social Authentication**: Seamless Google OAuth integration for easy access

---

## 🛠️ How we built it

The project was built using a modern web development stack with AI/ML integration:

### Backend Architecture
- **Django Framework**: Robust web framework for rapid development
- **Machine Learning Pipeline**: Scikit-learn models for predictions
- **Computer Vision**: Hugging Face Transformers for food recognition
- **Database Design**: SQLite with Django ORM for data management

### AI/ML Implementation
- **Weight Change Model**: Multi-output regression using nutritional and activity data
- **Health Prediction Models**: Classification algorithms for disease risk assessment
- **Food Recognition**: Pre-trained vision models fine-tuned for nutritional analysis
- **Recommendation Engine**: Rule-based systems combined with ML predictions

### Frontend Development
- **Responsive Design**: Tailwind CSS for modern, mobile-first UI
- **Interactive Forms**: Dynamic user inputs with real-time validation
- **Progressive Web App**: Optimized for performance and user experience

---

## 💪 Challenges we ran into

### Technical Challenges
- **Model Accuracy**: Training ML models with limited healthcare datasets while ensuring realistic predictions
- **API Integration**: Handling rate limits and data consistency with external APIs (USDA FoodData)
- **Scalability**: Optimizing AI models for web deployment without compromising performance
- **Data Privacy**: Implementing secure user data handling and OAuth authentication

### Development Challenges
- **Complex Workflows**: Managing multi-step user onboarding and personalized recommendations
- **Real-time Processing**: Balancing AI computation time with user experience
- **Cross-browser Compatibility**: Ensuring consistent experience across different devices
- **Error Handling**: Robust error management for API failures and invalid inputs

---

## 🏆 Accomplishments that we're proud of

- **Accurate AI Predictions**: Developed ML models that provide realistic health predictions
- **Comprehensive Feature Set**: Built a complete health management platform in limited time
- **User-Centric Design**: Created an intuitive interface that simplifies complex health data
- **Security Implementation**: Properly secured sensitive API keys and user data
- **Scalable Architecture**: Designed a modular system that can easily accommodate new features
- **Real-world Impact**: Created a tool that can genuinely help people improve their health

---

## 📚 What we learned

### Technical Skills
- **Advanced Django**: Mastered complex Django patterns, authentication, and API integration
- **Machine Learning**: Gained expertise in training, deploying, and optimizing ML models
- **Computer Vision**: Learned to implement and fine-tune vision AI models
- **API Development**: Experience with REST APIs, OAuth, and third-party integrations

### Project Management
- **Agile Development**: Adapted to changing requirements and tight deadlines
- **Code Quality**: Importance of testing, documentation, and security practices
- **User Experience**: Understanding user needs and designing intuitive interfaces
- **Problem Solving**: Creative solutions to complex technical challenges

---

## 🔮 What's next for FitAI – Smart Health & Fitness Assistant

### Immediate Roadmap
- **Mobile App Development**: Native iOS/Android apps for better accessibility
- **Wearable Integration**: Connect with fitness trackers and smart devices
- **Advanced Analytics**: Detailed progress tracking with data visualization
- **Social Features**: Community challenges and peer motivation

### Long-term Vision
- **Telemedicine Integration**: Connect with healthcare providers
- **IoT Integration**: Smart home devices for automated health monitoring
- **Advanced AI**: Deep learning models for more accurate predictions
- **Global Expansion**: Multi-language support and cultural adaptation
- **Research Partnerships**: Collaborate with medical institutions for data validation

---

## 🏗️ Built with

### Backend & Framework
- **Django 5.2.6** - High-level Python web framework
- **Python 3.12.6** - Programming language
- **SQLite** - Database management system

### AI & Machine Learning
- **Scikit-learn 1.6.0** - Machine learning library
- **NumPy 1.26.4** - Numerical computing
- **Pandas 2.2.3** - Data manipulation and analysis
- **Joblib 1.4.2** - Model serialization
- **Hugging Face Transformers 4.45.2** - AI models for NLP and vision
- **PyTorch 2.5.1** - Deep learning framework

### Web Technologies
- **HTML5** - Markup language
- **CSS3** - Styling
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - Client-side scripting

### APIs & Integrations
- **USDA FoodData Central API** - Nutritional database
- **Google OAuth 2.0** - Social authentication
- **Django Allauth** - Authentication framework

### Deployment & DevOps
- **Gunicorn 23.0.0** - WSGI HTTP Server
- **WhiteNoise 6.7.0** - Static file serving
- **python-dotenv 1.0.0** - Environment variable management
- **Heroku** - Cloud deployment platform

### Development Tools
- **Git** - Version control
- **VS Code** - Code editor
- **Pip** - Package installer
- **Virtualenv** - Environment management

## 🌟 Features

### 🤖 AI-Powered Features
- **Weight Change Prediction**: Predict weight changes based on caloric intake and activity levels
- **Food Recognition**: Upload food images to identify nutritional content
- **Heart Disease Risk Assessment**: ML-based heart disease prediction
- **Lung Disease Risk Assessment**: AI-powered lung health evaluation
- **Calorie Burn Prediction**: Estimate calories burned during workouts

### 🍎 Diet Management
- **Personalized Meal Plans**: Custom diet plans based on goals (weight loss/gain/maintenance)
- **Meal Customization**: Swap and customize meals according to preferences
- **Nutritional Analysis**: Detailed nutritional breakdown of foods
- **USDA Food Database Integration**: Real-time nutritional data

### 💪 Fitness & Workout
- **Workout Plan Generation**: AI-generated workout plans based on user profile
- **Exercise Recommendations**: Personalized exercise suggestions
- **Progress Tracking**: Monitor fitness journey over time

### 👤 User Management
- **User Authentication**: Secure login/registration system
- **Google OAuth Integration**: Social login support
- **Profile Management**: Comprehensive user profiles with goals and preferences
- **Onboarding Flow**: Guided setup process for new users

## 🛠️ Tech Stack

### Backend
- **Django 5.2.6** - Web framework
- **Python 3.12.6** - Programming language
- **SQLite** - Database (development)

### Frontend
- **HTML5/CSS3** - Markup and styling
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - Client-side scripting

### AI/ML
- **Scikit-learn** - Machine learning algorithms
- **Joblib** - Model serialization
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **Hugging Face Transformers** - Food recognition AI
- **PyTorch** - Deep learning framework

### Authentication & APIs
- **Django Allauth** - Social authentication
- **Google OAuth 2.0** - Social login
- **USDA FoodData Central API** - Nutritional data

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.12.6** or higher
- **pip** (Python package installer)
- **Git** (version control)
- **Virtualenv** (recommended for environment management)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shahwaiz19/FitAI_web_pro.git
cd FitAI_web_pro/fitness_diet
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root directory (`fitness_diet/`) with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite is used by default, no additional config needed)

# API Keys
USDA_API_KEY=your-usda-api-key-here

# Google OAuth (Optional - for social login)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## 🔑 API Keys Setup

### USDA FoodData Central API
1. Visit [USDA FoodData Central](https://fdc.nal.usda.gov/)
2. Register for an API key
3. Add the key to your `.env` file as `USDA_API_KEY`

### Google OAuth (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Add credentials to `.env` file

## 📖 Usage Guide

### User Registration & Login
1. Visit the landing page
2. Click "Register" to create a new account
3. Complete the onboarding process
4. Set your fitness goals and preferences

### Main Features

#### Weight Change Prediction
- Navigate to `/predict-weight-change/`
- Enter your current weight, target weight, duration, and activity level
- Get AI-powered predictions for weight changes

#### Food Recognition
- Go to `/food-recognition/`
- Upload an image of your food
- Get nutritional analysis and calorie information

#### Diet Planning
- Access personalized diet plans based on your goals
- Customize meals and swap food items
- Track nutritional intake

#### Health Assessments
- Heart disease risk prediction
- Lung disease risk evaluation
- Get personalized health recommendations

#### Workout Planning
- AI-generated workout plans
- Exercise recommendations based on your profile
- Progress tracking and adjustments

## 🏗️ Project Structure

```
fitness_diet/
├── fitness_diet/              # Main Django app
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py              # URL configurations
│   ├── views.py             # View functions
│   ├── models.py            # Database models
│   ├── forms.py             # Django forms
│   └── templates/           # HTML templates
├── ml_models/               # Machine learning models
│   ├── weight_change/
│   ├── diet_plan/
│   ├── heart_disease/
│   └── lung_disease/
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── templates/               # Global templates
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version
├── manage.py               # Django management script
└── README.md              # This file
```

## 🔧 Development Commands

```bash
# Run development server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## 🌐 Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set USDA_API_KEY=your-api-key
   heroku config:set GOOGLE_CLIENT_ID=your-client-id
   heroku config:set GOOGLE_CLIENT_SECRET=your-client-secret
   ```
5. Deploy: `git push heroku main`

### Local Production Setup
```bash
# Set DEBUG=False in settings.py
# Configure ALLOWED_HOSTS
# Run collectstatic
python manage.py collectstatic
# Use gunicorn for production
gunicorn fitness_diet.wsgi:application
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Developer**: Shahwaiz
- **Project**: FitAI - AI Fitness & Diet Management System

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Happy Hacking! 🚀**

*Built with ❤️ using Django, AI/ML, and modern web technologies*