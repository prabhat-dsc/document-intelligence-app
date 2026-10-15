from fastapi import FastAPI
from app.api.router import api_router 
from app.core.logging_config import setup_logging
from fastapi.openapi.utils import get_openapi



setup_logging() 

app = FastAPI(
    title="Document Intelligence RAG API",
    version="1.0.0",
    description="OCR + Hybrid Retrieval + Reranking + RAG API",

)

app.include_router(api_router, prefix="/api/v1")

######################### Code for upolad option in swagger

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schemas = schema.get("components", {}).get("schemas", {})

    for component in schemas.values():
        for prop in component.get("properties", {}).values():
            # Handle list[UploadFile]
            if prop.get("type") == "array":
                items = prop.get("items", {})

                if items.get("contentMediaType") == "application/octet-stream":
                    items.pop("contentMediaType", None)
                    items["format"] = "binary"

            # Handle a single UploadFile
            elif (
                prop.get("type") == "string"
                and prop.get("contentMediaType") == "application/octet-stream"
            ):
                prop.pop("contentMediaType", None)
                prop["format"] = "binary"

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi



###########################

@app.get("/")
def root():
    return {"service": "document-intelligence-rag", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}






