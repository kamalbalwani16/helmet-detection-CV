# 🚦 Helmet Detection System for Traffic Safety

A computer vision-based system that detects whether riders are wearing helmets using **YOLOv8**. The project includes a **Flask backend** and an interactive **web interface** for real-time image-based detection and compliance analysis.

---

## 📌 Overview

This project aims to improve road safety by automating helmet detection in traffic images. It identifies riders with and without helmets and provides visual results along with safety statistics.

---

## ✨ Features

- 🔍 Helmet / No-Helmet detection using YOLOv8  
- 📸 Image upload with drag-and-drop support  
- 📊 Detection statistics (total people, helmet count, compliance %)  
- 🖼️ Annotated output with bounding boxes  
- 📥 Downloadable result images  
- ⚡ Fast inference with lightweight model  

---

## 🧠 Model Details

- Model: **YOLOv8 (Nano variant)**  
- Trained on a custom helmet detection dataset  
- Input size: 640 × 640  
- Epochs: 50  

### 📊 Performance

- **Precision:** 0.82  
- **Recall:** 0.82  
- **mAP@50:** 0.866  
- **mAP@50-95:** 0.552  

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask  
- **Model:** YOLOv8 (Ultralytics)  
- **Frontend:** HTML, CSS, JavaScript  
- **Libraries:** OpenCV, NumPy  

---

**📂 Project Structure**

helmet-detection/
│
├── app.py
├── requirements.txt
├── model/
│ └── best.pt
│
├── templates/
│ └── index.html
│
├── static/
│ ├── css/
│ │ └── style.css
│ ├── js/
│ │ └── script.js
│ ├── uploads/
│ └── results/


---

## ⚙️ Setup & Run Locally

1 Clone the repository

```bash
git clone https://github.com/your-username/Helmet-Detection-using-CV.git
cd Helmet-Detection-using-CV

2 Install dependencies
pip install -r requirements.txt

If pip doesn’t work:
python -m pip install -r requirements.txt

3. Run the application
python app.py

4. Open in browser
http://127.0.0.1:5000

---

**## Future Improvements**
🎥 Video detection support
📡 Real-time CCTV integration
🚗 Number plate recognition
💰 Automated traffic violation system
☁️ Cloud deployment

## 📂 Project Structure
.
