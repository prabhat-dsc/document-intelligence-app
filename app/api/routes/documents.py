from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException
from app.core.config import settings 
from app.services.document_service import (
                  create_document_record, 
                  list_documents,
                  get_document,
                  delete_document)

from app.services.ingestion_service import ingest_document


router = APIRouter()

@router.post("/upload")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
):
    # check files is uploaded or not
    if not files:
        raise HTTPException(status_code= 404, detail="No files supplied.")

    results = []
    settings.upload_dir.mkdir(parents=True,exist_ok=True)

    for upload in files:
        if not upload.filename or not upload.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=404,
                                 detail=f"Only PDF files are supported: {upload.filename}",
                                 )
        data = await upload.read()

        if len(data)> settings.max_upload_size_mb *1024 *1024:
                raise HTTPException(
                status_code=413,
                detail=f"{upload.filename} exceeds the upload size limit.",
            )

        record = create_document_record( filename= upload.filename ,data= data )
        file_path = settings.upload_dir / f"{record['document_id']}.pdf"
        file_path.write_bytes(data)

        background_tasks.add_task(
             ingest_document,
             record["document_id"],
             str(file_path)
        )

        results.append(record) 
        
     
    return {"documents": results}    

@router.get("")
def documents():
     return {"documents": list_documents()}


@router.get("/{document_id}")
def get_document(document_id: str):
     item = get_document(document_id)

     if not item:
          raise HTTPException(status_code=404, detail="Document not found")
     return item

@router.delete("/{document_id}")
def remove_document(document_id:str):
    if not get_document(document_id):
          raise HTTPException(status_code=404, detail="Document not found.")

    delete_document(document_id)
    return {"deleted": True, "document_id": document_id}

     

    






