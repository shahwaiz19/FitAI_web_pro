from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import joblib
import numpy as np
from django.conf import settings
from .models import HealthAssessment

# Heart Disease Prediction View
@csrf_exempt
def heart_disease_prediction(request):
    if request.method == 'POST':
        try:
            # Get form data
            data = json.loads(request.body)

            # Extract features according to your model
            age = float(data.get('age', 50))
            sex = int(data.get('sex', 1))  # 0 = female, 1 = male
            chest_pain_type = data.get('chest_pain_type', 'ASY')  # ASY, ATA, NAP, TA
            resting_bp = float(data.get('resting_bp', 120))
            cholesterol = float(data.get('cholesterol', 200))
            fasting_bs = int(data.get('fasting_bs', 0))  # 0 or 1
            resting_ecg = data.get('resting_ecg', 'Normal')  # Normal, LVH, ST
            max_hr = float(data.get('max_hr', 150))
            exercise_angina = int(data.get('exercise_angina', 0))  # 0 or 1
            oldpeak = float(data.get('oldpeak', 1.0))
            st_slope = data.get('st_slope', 'Flat')  # Flat, Up, Down

            # Convert categorical variables to one-hot encoding
            sex_features = {
                'Sex_F': 1 if sex == 0 else 0,  # 0 = Female
                'Sex_M': 1 if sex == 1 else 0,  # 1 = Male
            }

            chest_pain_features = {
                'ChestPainType_ASY': 1 if chest_pain_type == 'ASY' else 0,
                'ChestPainType_ATA': 1 if chest_pain_type == 'ATA' else 0,
                'ChestPainType_NAP': 1 if chest_pain_type == 'NAP' else 0,
                'ChestPainType_TA': 1 if chest_pain_type == 'TA' else 0,
            }

            resting_ecg_features = {
                'RestingECG_Normal': 1 if resting_ecg == 'Normal' else 0,
                'RestingECG_LVH': 1 if resting_ecg == 'LVH' else 0,
                'RestingECG_ST': 1 if resting_ecg == 'ST' else 0,
            }

            exercise_angina_features = {
                'ExerciseAngina_N': 1 if exercise_angina == 0 else 0,  # 0 = No
                'ExerciseAngina_Y': 1 if exercise_angina == 1 else 0,  # 1 = Yes
            }

            st_slope_features = {
                'ST_Slope_Flat': 1 if st_slope == 'Flat' else 0,
                'ST_Slope_Up': 1 if st_slope == 'Up' else 0,
                'ST_Slope_Down': 1 if st_slope == 'Down' else 0,
            }

            # Prepare features dictionary in correct order
            features_dict = {
                'Age': age,
                'RestingBP': resting_bp,
                'Cholesterol': cholesterol,
                'FastingBS': fasting_bs,
                'MaxHR': max_hr,
                'Oldpeak': oldpeak,
                'Sex_F': sex_features['Sex_F'],
                'Sex_M': sex_features['Sex_M'],
                'ChestPainType_ASY': chest_pain_features['ChestPainType_ASY'],
                'ChestPainType_ATA': chest_pain_features['ChestPainType_ATA'],
                'ChestPainType_NAP': chest_pain_features['ChestPainType_NAP'],
                'ChestPainType_TA': chest_pain_features['ChestPainType_TA'],
                'RestingECG_LVH': resting_ecg_features['RestingECG_LVH'],
                'RestingECG_Normal': resting_ecg_features['RestingECG_Normal'],
                'RestingECG_ST': resting_ecg_features['RestingECG_ST'],
                'ExerciseAngina_N': exercise_angina_features['ExerciseAngina_N'],
                'ExerciseAngina_Y': exercise_angina_features['ExerciseAngina_Y'],
                'ST_Slope_Down': st_slope_features['ST_Slope_Down'],
                'ST_Slope_Flat': st_slope_features['ST_Slope_Flat'],
                'ST_Slope_Up': st_slope_features['ST_Slope_Up'],
            }

            # Load model and features
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'heart_disease', 'heart_model.pkl')
            features_path = os.path.join(settings.BASE_DIR, 'ml_models', 'heart_disease', 'model_features.pkl')

            if os.path.exists(model_path) and os.path.exists(features_path):
                model = joblib.load(model_path)
                feature_names = joblib.load(features_path)

                # Create feature array in correct order
                features = np.array([[features_dict[feature] for feature in feature_names]])

                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1] * 100

                risk_level = 'High' if prediction == 1 else 'Low'
                recommendations = "Consult a cardiologist immediately. Monitor blood pressure, cholesterol, and maintain a heart-healthy diet." if prediction == 1 else "Continue regular health check-ups and maintain a healthy lifestyle."

                # Save the health assessment to database
                try:
                    HealthAssessment.objects.create(
                        assessment_type='heart_disease',
                        risk_level=risk_level,
                        probability=round(probability, 2),
                        recommendations=recommendations
                    )
                except Exception as e:
                    print(f"Error saving heart disease assessment: {e}")

                result = {
                    'prediction': int(prediction),
                    'probability': round(probability, 2),
                    'risk_level': risk_level,
                    'message': 'Heart disease detected' if prediction == 1 else 'No heart disease detected'
                }
            else:
                # Mock prediction for demonstration
                result = {
                    'prediction': 0,
                    'probability': 15.5,
                    'risk_level': 'Low',
                    'message': 'Model not found - using mock prediction'
                }

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'heart_disease_prediction.html')

# Lung Disease Prediction View
@csrf_exempt
def lung_disease_prediction(request):
    if request.method == 'POST':
        try:
            # Get form data
            data = json.loads(request.body)

            # Extract features according to your model
            age = float(data.get('age', 50))
            gender = int(data.get('gender', 1))  # 0 = Male, 1 = Female
            air_pollution = int(data.get('air_pollution', 2))  # 0-8 scale
            alcohol_use = int(data.get('alcohol_use', 1))  # 0-8 scale
            dust_allergy = int(data.get('dust_allergy', 2))  # 0-8 scale
            occupational_hazards = int(data.get('occupational_hazards', 1))  # 0-8 scale
            genetic_risk = int(data.get('genetic_risk', 1))  # 0-7 scale
            chronic_lung_disease = int(data.get('chronic_lung_disease', 0))  # 0-7 scale
            balanced_diet = int(data.get('balanced_diet', 1))  # 0-8 scale
            obesity = int(data.get('obesity', 0))  # 0-8 scale
            smoking = int(data.get('smoking', 1))  # 0-8 scale
            passive_smoker = int(data.get('passive_smoker', 0))  # 0-8 scale
            chest_pain = int(data.get('chest_pain', 1))  # 0-8 scale
            coughing_blood = int(data.get('coughing_blood', 0))  # 0-8 scale
            fatigue = int(data.get('fatigue', 1))  # 0-8 scale
            weight_loss = int(data.get('weight_loss', 0))  # 0-8 scale
            shortness_breath = int(data.get('shortness_breath', 1))  # 0-8 scale
            wheezing = int(data.get('wheezing', 0))  # 0-8 scale
            swallowing_diff = int(data.get('swallowing_diff', 1))  # 0-8 scale
            clubbing_nails = int(data.get('clubbing_nails', 0))  # 0-8 scale
            frequent_cold = int(data.get('frequent_cold', 1))  # 0-8 scale
            dry_cough = int(data.get('dry_cough', 1))  # 0-8 scale
            snoring = int(data.get('snoring', 0))  # 0-8 scale

            # Prepare features array in correct order
            features = np.array([[age, gender, air_pollution, alcohol_use, dust_allergy,
                                occupational_hazards, genetic_risk, chronic_lung_disease,
                                balanced_diet, obesity, smoking, passive_smoker,
                                chest_pain, coughing_blood, fatigue, weight_loss,
                                shortness_breath, wheezing, swallowing_diff,
                                clubbing_nails, frequent_cold, dry_cough, snoring]])

            # Load model and features
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'lung_disease', 'lungs_model.pkl')
            features_path = os.path.join(settings.BASE_DIR, 'ml_models', 'lung_disease', 'lungs_model_features.pkl')

            if os.path.exists(model_path) and os.path.exists(features_path):
                model = joblib.load(model_path)
                feature_names = joblib.load(features_path)

                # Create feature array in correct order
                features = np.array([[age, gender, air_pollution, alcohol_use, dust_allergy,
                                    occupational_hazards, genetic_risk, chronic_lung_disease,
                                    balanced_diet, obesity, smoking, passive_smoker,
                                    chest_pain, coughing_blood, fatigue, weight_loss,
                                    shortness_breath, wheezing, swallowing_diff,
                                    clubbing_nails, frequent_cold, dry_cough, snoring]])

                prediction = model.predict(features)[0]

                # Handle multi-class prediction (Low, Medium, High)
                risk_levels = ['Low', 'Medium', 'High']
                risk_level = risk_levels[prediction] if prediction < len(risk_levels) else 'Unknown'

                # Calculate probability for high risk (assuming class 2 is high risk)
                try:
                    probabilities = model.predict_proba(features)[0]
                    high_risk_probability = probabilities[2] * 100 if len(probabilities) > 2 else probabilities[-1] * 100
                except:
                    high_risk_probability = 50.0  # Default if predict_proba not available

                recommendations = "Quit smoking, avoid pollutants, consult a pulmonologist, and practice breathing exercises." if risk_level == 'High' else "Maintain good air quality, avoid smoking, and have regular check-ups."

                # Save the health assessment to database
                try:
                    HealthAssessment.objects.create(
                        assessment_type='lung_disease',
                        risk_level=risk_level,
                        probability=round(high_risk_probability, 2),
                        recommendations=recommendations
                    )
                except Exception as e:
                    print(f"Error saving lung disease assessment: {e}")

                result = {
                    'prediction': int(prediction),
                    'probability': round(high_risk_probability, 2),
                    'risk_level': risk_level,
                    'message': f'Lung disease risk level: {risk_level}'
                }
            else:
                # Mock prediction for demonstration
                result = {
                    'prediction': 0,
                    'probability': 12.3,
                    'risk_level': 'Low',
                    'message': 'Model not found - using mock prediction'
                }

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'lung_disease_prediction.html')

# Heart Disease Prediction Page
def heart_disease_page(request):
    return render(request, 'heart_disease_prediction.html')

# Lung Disease Prediction Page
def lung_disease_page(request):
    return render(request, 'lung_disease_prediction.html')
