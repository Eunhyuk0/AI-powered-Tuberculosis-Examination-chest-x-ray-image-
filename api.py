import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()

#저장된 모델 사용
model = tf.keras.models.load_model("model.h5")

#AImodel.py 와 같은 이미지 사이즈
IMG_SIZE = (224, 224)
CLASS_NAMES = ["Normal", "Tuberculosis"]
UPLOAD_DIR = "uploaded_images"

@app.post("/process")
async def process_image(file: UploadFile = File(...)): #async
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PNG or JPG images are allowed")

    try:
        #이미지 준비
        image = Image.open(file.file).convert("RGB")
        image = image.resize(IMG_SIZE)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        #model.predict 수행, 변환
        predictions = model.predict(image_array)
        prob = float(predictions[0][0])
        is_positive = prob > 0.5
        confidence = prob if is_positive else 1 - prob

        if confidence < 0.3: #분류가 애매한 경우
            return JSONResponse(content={"result": "Sorry, too low confidence"})

        predicted_label = CLASS_NAMES[1] if is_positive else CLASS_NAMES[0]

        #거의 확실한 경우 -> class 에 맞게 저장 (파일이름 : 시간)
        if confidence > 0.7:
            save_folder = os.path.join(UPLOAD_DIR, predicted_label)
            os.makedirs(save_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(save_folder, f"{timestamp}.jpg")
            image.save(save_path)

        return JSONResponse(content={
            "result": f"{predicted_label}  {int(confidence*100)}%" #confidence 값 대신 %로 표시
        })
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed: Unknown Error!") #기타 에러 케이스
