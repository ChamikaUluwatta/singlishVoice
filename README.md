# SinglishVoice: Code-mixed Romanized Sinhala Text-to-Speech System

## 📌 Overview
**SinglishVoice** is a research project and implementation of a Text-to-Speech (TTS) system designed to handle **code-mixed Romanized Sinhala (Singlish)**.  
Unlike traditional Sinhala TTS systems that require native Sinhala script, SinglishVoice processes Romanized input text — including informal spelling, shorthand, and code-mixed English — and produces natural Sinhala speech.

This project was developed as part of the **BEng in Software Engineering** dissertation at the **University of Westminster** in collaboration with the **Informatics Institute of Technology**.

---

## 🎯 Motivation
Sinhala speakers frequently use **Romanized Sinhala** on social media and digital platforms.  
However, existing TTS systems **do not support Romanized Sinhala input**, creating accessibility challenges for users.  

SinglishVoice bridges this gap by introducing an **end-to-end TTS pipeline**:
1. **Back-Transliteration**: Romanized Sinhala → Native Sinhala (using a fine-tuned NLLB model).  
2. **Speech Synthesis**: Native Sinhala → Natural Sinhala speech (using a VITS model).  

---

## ✨ Key Features
- Support for **code-mixed Romanized Sinhala (Singlish)**.  
- **Back-transliteration** using **fine-tuned NLLB**.  
- **High-quality speech synthesis** with **VITS** (Vocoder-free TTS).  
- **User-friendly GUI** for text input and speech generation.  
- Modular and scalable architecture.  

---

## 📊 Evaluation Results
- **NLLB Model (Transliteration)**  
  - Word Error Rate (WER): **21%**  
  - Character Error Rate (CER): **6%**  
  - BLEU Score: **58%**  

- **VITS Model (Text-to-Speech)**  
  - Male Speaker MOS: **3.8**  
  - Female Speaker MOS: **2.6**  

*Note*: Code-mixed sentences and female voice synthesis remain challenging.

---

## 🏗️ System Architecture
1. **Input**: Romanized Sinhala text (Singlish).  
2. **Back-Transliteration Module** (NLLB).  
3. **Speech Synthesis Module** (VITS).  
4. **Output**: Natural Sinhala speech.  

---

## ⚙️ Tech Stack
- **Languages**: Python  
- **Frameworks & Libraries**:  
  - PyTorch  
  - Hugging Face Transformers (NLLB)  
  - Coqui TTS (VITS)  
- **Datasets**:  
  - *Swa Bhasha* Dataset  
  - Dakshina Dataset  
  - PathNirvana (7.5 hrs audio)   

---

## 🚀 Installation & Usage
```bash
# Clone repository
git clone https://github.com/your-username/singlishvoice.git
cd singlishvoice

# Run Backend
cd Backend && pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8080

# Run Frontend
cd Frontend && pip install -r requirements.txt && streamlit run app.py
```

---

## 📌 Use Cases
- Accessibility support for **visually impaired users**.  
- **Social media content consumption** in Romanized Sinhala.  
- **Language learning & research** in Sinhala NLP.  
- Enabling **voice-enabled Sinhala applications**.  

---

## 🔮 Future Work
- Improve **female voice naturalness**.  
- Enhance handling of **complex code-mixed sentences**.  
- Optimize system for **real-time mobile applications**.  

---

## 👨‍💻 Author
**Chamika Uluwatta**  
BEng in Software Engineering, University of Westminster  
📅 April 2023  

Supervised by **Dr. Ruvan Weerasinghe**  

---

## 📚 References
For detailed methodology, evaluation, and academic references, please refer to the full [Thesis Document](./Thesis.pdf).  
