import pandas as pd
from typing import Dict, Any, List

class CSVExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(self.file_path)
            # Fill NaN values with empty string or None to handle them gracefully
            df = df.fillna('')
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []
