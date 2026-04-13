# ☕ Drink Detector: Matcha, Latte, & Black Coffee
**Group Task: Object Detection Pipeline with YOLOv8**

A specialized deep learning application designed to classify and detect three types of beverages in real-time. This project was developed as part of our Data Science & AI Camp training to demonstrate a full end-to-end computer vision pipeline.

---

🔗 Live Demo
Experience the Drink Detector in your browser here:

👉 [Launch App on Streamlit Cloud](https://drink-detector.streamlit.app/)

---

## 🎯 Learning Objectives
* **Pipeline Management:** Navigated the full object detection lifecycle (Collection → Annotation → Training → Deployment).
* **Roboflow Integration:** Managed dataset versioning and light augmentation.
* **YOLOv8 Optimization:** Trained a high-precision model using YOLOv8-Nano.
* **Streamlit UX:** Created a custom pastel-themed interface for user testing.

## 🛠️ Tech Stack
* **Model:** YOLOv8 (Ultralytics)
* **Dataset Management:** Roboflow
* **Deployment:** Streamlit
* **Image Processing:** Pillow, OpenCV, NumPy
* **Training Environment:** Google Colab (T4 GPU)

---

## 📸 Dataset & Augmentation
Our team collected a custom dataset of 30–60 images of various drinks. 
To improve model robustness, we applied the following **Augmentations**:
* **Horizontal Flip:** For perspective variety.
* **Brightness (+/- 25%):** To simulate different cafe lighting.
* **Blur (2px):** To account for mobile camera motion.
