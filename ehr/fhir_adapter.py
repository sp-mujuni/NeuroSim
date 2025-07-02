import requests

class FHIRAdapter:
    def __init__(self, base_url="https://ehr.example.org/fhir"):
        self.base_url = base_url
        self.headers = {"Accept": "application/fhir+json"}

    def get_patient_observations(self, patient_id):
        endpoint = f"{self.base_url}/Observation?patient={patient_id}"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            entries = response.json().get("entry", [])
            return entries
        except requests.RequestException as e:
            print(f"FHIR request failed: {e}")
            return []
