import requests
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import torch

API_KEY = "nhBUZbSkmWY38fTowunb16U3tFrKqlOGIEDqYGNI"

@csrf_exempt
def food_calorie_predictor(request):
    if request.method == "POST" and request.FILES.get("food_image"):
        try:
            uploaded_file = request.FILES["food_image"]
            image = Image.open(uploaded_file)

            # Load model with GPU if available
            device = 0 if torch.cuda.is_available() else -1
            classifier = pipeline("image-classification", model="nateraw/food", device=device)

            preds = classifier(image, top_k=1)
            food_label = preds[0]["label"]

            # Fetch calories from USDA API
            url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_label}&api_key={API_KEY}"
            response = requests.get(url)
            data = response.json()

            calories = "Not found"
            if "foods" in data and len(data["foods"]) > 0:
                food = data["foods"][0]
                for n in food.get("foodNutrients", []):
                    if "Energy" in n.get("nutrientName", ""):
                        calories = f"{n['value']} {n['unitName']}"
                        break

            return JsonResponse({
                "food_name": food_label,
                "calories": calories,
                "confidence": f"{preds[0]['score']:.2%}"
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})
