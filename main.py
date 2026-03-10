from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image
import io
import uvicorn
from collections import Counter


app = FastAPI(title="lt-iscan API")


model_path = r"C:\Users\hp\Desktop\Training Folder\lt-iscan_model\runs\detect\train\weights\best.pt"
model = YOLO(model_path)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/lt_iscan_predict")
async def predict(
   
    file: UploadFile = File(..., description="Image file to run detection on"),
):
   
    if not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid file type '{file.content_type}'. Please upload an image."}
        )

   
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    
    results = model.predict(
        source=image,
        
        verbose=False
    )

    detections = []
    class_names = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf_score = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

           
            class_names.append(cls_name)

    product_counts = dict(Counter(class_names))

    return JSONResponse(content={
        "status": "success",
        "image": file.filename,
      
        "total_detections": len(detections),
        "product_summary": [
            {"product_name": name, "count": count}
            for name, count in sorted(product_counts.items())
        ],
        "detections": detections
    })




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)