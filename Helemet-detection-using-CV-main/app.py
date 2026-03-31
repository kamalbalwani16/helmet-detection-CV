from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
MODEL_PATH = "model/best.pt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

model = YOLO(MODEL_PATH)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PNG, JPG, and JPEG files are allowed"}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    result_path = os.path.join(app.config["RESULT_FOLDER"], filename)

    file.save(upload_path)

    results = model(upload_path)

    helmet_count = 0
    no_helmet_count = 0

    names = model.names

    annotated_img = results[0].plot()

    for box in results[0].boxes:
        cls_id = int(box.cls[0].item())
        class_name = names[cls_id]

        if class_name == "helmet":
            helmet_count += 1
        elif class_name == "no_helmet":
            no_helmet_count += 1

    total = helmet_count + no_helmet_count
    compliance = round((helmet_count / total) * 100, 2) if total > 0 else 0

    cv2.imwrite(result_path, annotated_img)

    return jsonify({
        "result_image": f"/static/results/{filename}",
        "helmet_count": helmet_count,
        "no_helmet_count": no_helmet_count,
        "total": total,
        "compliance": compliance
    })

if __name__ == "__main__":
    app.run(debug=True)