# 🧠 NeuroSim CDS System

**NeuroSim** is a modular, memory-aware Clinical Decision Support (CDS) system inspired by human cognitive processes. It integrates seamlessly with existing EHR systems using FHIR APIs and simulates encoding, decay, contextual retrieval, and reinforcement of clinical data in real time.

---

## 🔧 Features
- **FHIR-based EHR Integration**
- **Memory Encoding & Strength Decay**
- **Contextual Retrieval via Cosine Similarity**
- **Reinforcement-Based Learning**
- **Real-time Memory Visualization Dashboard**

---

## 🏥 Use Case
Designed for hospital neurology departments to reduce clinician cognitive load, prevent diagnostic errors, and surface relevant patient data at the point of care.

---

## 📁 Project Structure
```bash
neurosim/
├── main.py                     # Application entry point
├── engine/
│   ├── memory_engine.py        # Memory encoding & decay
│   ├── reinforcement.py        # Reinforcement logic
│   └── similarity.py           # Contextual recall scoring
├── ehr/
│   └── fhir_adapter.py         # FHIR API integration
├── db/
│   └── orm.py                  # SQLite memory storage
├── ui/
│   └── dashboard.py            # Real-time memory visualization
```

---

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone https://github.com/your-org/neurosim-cds.git
cd neurosim-cds
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure EHR Endpoint
Edit `fhir_adapter.py`:
```python
FHIRAdapter(base_url="https://ehr.example.org/fhir")
```

### 4. Run NeuroSim
```bash
python main.py
```

---

## 🧪 Demo Functions
- Pulls FHIR Observations for a test patient
- Encodes data with timestamp and type
- Applies memory decay and reinforcement logic
- Contextually retrieves relevant memory traces
- Visualizes memory strength timeline in Matplotlib

---

## 🔐 Requirements
- Python 3.8+
- Internet access (for FHIR calls)
- Optional: SQLite3 installed locally

---

## 🌍 African Health Support
- Compatible with OpenMRS, Care2X, and other open EHRs
- Offline-first design options
- Customizable for multilingual voice/CLI interfaces

---

## 📄 License
MIT License

---

## 🤝 Contributing
PRs and issue reports welcome! Join us in building AI that thinks with memory.
