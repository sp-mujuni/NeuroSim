from engine.memory_engine import MemoryEngine
from ehr.fhir_adapter import FHIRAdapter
from engine.similarity import SimilarityScorer
from engine.reinforcement import ReinforcementEngine

# Initialize core components
memory_engine = MemoryEngine()
fhir_adapter = FHIRAdapter()
similarity_scorer = SimilarityScorer()
reinforcement = ReinforcementEngine()

# Ingest FHIR data
print("Fetching patient data from FHIR server...")
observations = fhir_adapter.get_patient_observations("patient-001")
memory_engine.encode_observations(observations)

# Optional: Trigger visualization/dashboard in another process
from ui.dashboard import launch_dashboard
launch_dashboard(memory_engine)
