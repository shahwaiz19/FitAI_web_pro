# ML Models Setup Guide

This guide explains how to integrate your trained machine learning models for heart disease and lung disease prediction into the FitAI application.

## Directory Structure

Your trained models should be placed in the following directory structure:

```
fitness_diet/
├── ml_models/
│   ├── heart_disease/
│   │   ├── heart_disease_model.pkl          # Your trained heart disease model
│   │   └── scaler.pkl                       # (Optional) Your fitted scaler
│   └── lung_disease/
│       ├── lung_disease_model.pkl           # Your trained lung disease model
│       └── scaler.pkl                       # (Optional) Your fitted scaler
```

## Model Requirements

### Heart Disease Model
- **File**: `heart_disease_model.pkl`
- **Input Features** (13 features in this order):
  1. `age` - Age in years
  2. `sex` - Gender (0 = female, 1 = male)
  3. `cp` - Chest pain type (0-3)
  4. `trestbps` - Resting blood pressure (mm Hg)
  5. `chol` - Serum cholesterol (mg/dl)
  6. `fbs` - Fasting blood sugar > 120 mg/dl (0 = false, 1 = true)
  7. `restecg` - Resting electrocardiographic results (0-2)
  8. `thalach` - Maximum heart rate achieved
  9. `exang` - Exercise induced angina (0 = no, 1 = yes)
  10. `oldpeak` - ST depression induced by exercise
  11. `slope` - Slope of the peak exercise ST segment (0-2)
  12. `ca` - Number of major vessels colored by fluoroscopy (0-3)
  13. `thal` - Thalassemia (1-3)

- **Output**: Binary classification (0 = No heart disease, 1 = Heart disease)
- **Expected Methods**: `predict()`, `predict_proba()`

### Lung Disease Model
- **File**: `lung_disease_model.pkl`
- **Input Features** (15 features in this order):
  1. `age` - Age in years
  2. `gender` - Gender (0 = female, 1 = male)
  3. `smoking` - Smoking habit (0 = no, 1 = yes)
  4. `yellow_fingers` - Yellow fingers (0 = no, 1 = yes)
  5. `anxiety` - Anxiety level (0 = no, 1 = yes)
  6. `peer_pressure` - Peer pressure (0 = no, 1 = yes)
  7. `chronic_disease` - Chronic disease (0 = no, 1 = yes)
  8. `fatigue` - Fatigue (0 = no, 1 = yes)
  9. `allergy` - Allergy (0 = no, 1 = yes)
  10. `wheezing` - Wheezing (0 = no, 1 = yes)
  11. `alcohol` - Alcohol consumption (0 = no, 1 = yes)
  12. `coughing` - Coughing (0 = no, 1 = yes)
  13. `shortness_of_breath` - Shortness of breath (0 = no, 1 = yes)
  14. `swallowing_difficulty` - Swallowing difficulty (0 = no, 1 = yes)
  15. `chest_pain` - Chest pain (0 = no, 1 = yes)

- **Output**: Binary classification (0 = No lung disease, 1 = Lung disease)
- **Expected Methods**: `predict()`, `predict_proba()`

## Model Training Requirements

### Supported Libraries
- scikit-learn (recommended)
- Any library that can be saved with joblib

### Model Format
- Models must be saved using `joblib.dump(model, 'model_name.pkl')`
- Example:
  ```python
  import joblib
  from sklearn.ensemble import RandomForestClassifier

  # Your trained model
  model = RandomForestClassifier()
  # ... training code ...

  # Save the model
  joblib.dump(model, 'heart_disease_model.pkl')
  ```

### Scaler (Optional)
If your model requires feature scaling, save the fitted scaler as well:
```python
from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler()
scaler.fit(X_train)
joblib.dump(scaler, 'scaler.pkl')
```

## Testing Your Models

### Heart Disease Model Test
```python
import joblib
import numpy as np

# Load model
model = joblib.load('ml_models/heart_disease/heart_disease_model.pkl')

# Test with sample data
sample_data = np.array([[45, 1, 2, 130, 250, 0, 1, 150, 0, 1.2, 1, 0, 2]])
prediction = model.predict(sample_data)
probability = model.predict_proba(sample_data)

print(f"Prediction: {prediction[0]}")
print(f"Probability: {probability[0][1] * 100:.2f}%")
```

### Lung Disease Model Test
```python
import joblib
import numpy as np

# Load model
model = joblib.load('ml_models/lung_disease/lung_disease_model.pkl')

# Test with sample data
sample_data = np.array([[35, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0]])
prediction = model.predict(sample_data)
probability = model.predict_proba(sample_data)

print(f"Prediction: {prediction[0]}")
print(f"Probability: {probability[0][1] * 100:.2f}%")
```

## Integration Steps

1. **Place your models** in the appropriate directories as shown above
2. **Test the models** using the provided test code
3. **Start the Django server**:
   ```bash
   cd fitness_diet
   python manage.py runserver
   ```
4. **Access the features**:
   - Heart Disease Prediction: `http://127.0.0.1:8000/heart-disease/`
   - Lung Disease Prediction: `http://127.0.0.1:8000/lung-disease/`

## Troubleshooting

### Model Not Found Error
- Ensure models are placed in the correct directories
- Check file names match exactly
- Verify file permissions

### Prediction Errors
- Check that input features match the expected format
- Ensure model was trained with the correct feature order
- Verify model compatibility with joblib

### Performance Issues
- Models should be lightweight for web deployment
- Consider using model compression if file sizes are large
- Test model loading time

## Security Notes

- Models are loaded from the local filesystem
- In production, consider using a model registry service
- Validate input data before passing to models
- Monitor model performance and update as needed

## Support

If you encounter any issues with model integration, please check:
1. Model file formats and compatibility
2. Feature order and data types
3. File paths and permissions
4. Django server logs for detailed error messages
