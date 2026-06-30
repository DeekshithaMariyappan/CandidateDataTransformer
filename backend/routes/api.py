from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import json
import os
import shutil
from typing import Optional

from extractors.csv_extractor import CSVExtractor
from extractors.pdf_extractor import PDFExtractor
from extractors.llm_extractor import LLMExtractor
from merger.merge_engine import MergeEngine
from provenance.provenance_tracker import ProvenanceTracker
from confidence.confidence_engine import ConfidenceEngine
from projection.projector import Projector

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AppState:
    csv_path: Optional[str] = None
    pdf_path: Optional[str] = None
    config: Optional[dict] = None
    last_result: Optional[dict] = None

state = AppState()

@router.post("/upload")
async def upload_files(
    csv_file: Optional[UploadFile] = File(None),
    pdf_file: Optional[UploadFile] = File(None),
    config_file: Optional[UploadFile] = File(None)
):
    try:
        if csv_file:
            path = os.path.join(UPLOAD_DIR, csv_file.filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(csv_file.file, buffer)
            state.csv_path = path
            
        if pdf_file:
            path = os.path.join(UPLOAD_DIR, pdf_file.filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(pdf_file.file, buffer)
            state.pdf_path = path
            
        if config_file:
            content = await config_file.read()
            state.config = json.loads(content.decode("utf-8"))
            
        return {"message": "Files uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transform")
async def transform():
    if not state.csv_path or not state.pdf_path:
        raise HTTPException(status_code=400, detail="Missing CSV or PDF file")
        
    try:
        # 1. Extract CSV
        csv_extractor = CSVExtractor(state.csv_path)
        csv_data_list = csv_extractor.extract()
        csv_data = csv_data_list[0] if csv_data_list else {}
        
        # 2. Extract PDF
        pdf_extractor = PDFExtractor(state.pdf_path)
        raw_pdf_text = pdf_extractor.extract_text()
        
        # 3. LLM Extraction
        llm_extractor = LLMExtractor()
        llm_data = llm_extractor.extract_from_resume(raw_pdf_text)
        resume_extracted_json = llm_data
        print(resume_extracted_json)
        
        # 4 & 5 & 6. Normalization & Merging
        merge_engine = MergeEngine()
        profile = merge_engine.merge(csv_data, llm_data)
        
        # 7 & 8. Provenance & Confidence
        provenance_tracker = ProvenanceTracker()
        provenance_tracker.build_provenance(profile, csv_data, llm_data)
        
        confidence_engine = ConfidenceEngine()
        confidence_engine.calculate(profile)
        
        profile_dict = profile.dict()
        
        # 9. Config Projection
        if state.config:
            projector = Projector()
            final_profile = projector.project(profile_dict, state.config)
        else:
            # Default projection (everything except internal fields)
            final_profile = {k: v for k, v in profile_dict.items() if k not in ['provenance', 'conflicts', 'confidence_scores', 'overall_confidence']}
            
        result = {
            "profile": final_profile,
            "confidence": profile_dict.get("confidence_scores", {}),
            "overall_confidence": profile_dict.get("overall_confidence", 0.0),
            "provenance": [p for p in profile_dict.get("provenance", [])],
            "conflicts": profile_dict.get("conflicts", []),
            "llm_raw_data": llm_data # Sending back for preview
        }
        
        state.last_result = result
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download")
async def download():
    if not state.last_result:
        raise HTTPException(status_code=404, detail="No transformed data available")
    return JSONResponse(content=state.last_result.get("profile", {}))
