

import sqlite3
import hashlib
import uuid
from datetime import datetime
from app.core.config import settings 


def _connect():
    settings.sqlite_db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_db)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            status TEXT NOT NULL,
            pages INTEGER DEFAULT 0,
            chunks INTEGER DEFAULT 0,
            error TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def create_document_record(filename: str, data: bytes):
    digest= hashlib.sha256(data).hexdigest()

    with _connect() as conn:
        existing = conn.execute(
            "SELECT * FROM documents WHERE sha256 = ? ",
              (digest,),   
                     ).fetchone()
        if existing :
            return dict(existing)
        
        document_id = str(uuid.uuid4())
        record = (
            document_id,
            filename,
            digest,
            "UPLOADED",
            0,
            0,
            None,
            datetime.utcnow().isoformat(),
        )
        conn.execute(
            """ INSERT INTO 
               documents (document_id, filename, sha256, status, pages, chunks, error,created_at )
               values(?, ?, ?, ?, ?, ?, ?, ?)  """ ,
               record,
        )
        conn.commit()

    return dict(zip(
        ["document_id", "filename", "sha256", "status", "pages", 
         "chunks", "error",'created_at'],
         record 
         ) )   
 
def update_document(document_id , **fields):
    allowed = {"status", "pages", "chunks", "error" }

    fields = {k:v for k,v in fields.items() if k in allowed}
    if not fields :
        return 

    clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [document_id]

    with _connect() as conn:
        conn.execute(
            f"UPDATE documents SET {clause} WHERE document_id =? ",
            (values),
        )
        conn.commit()


def get_document(document_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE document_id=?",
            (document_id,),
        ).fetchone()
    return dict(row) if row else None    

def list_documents():
    with _connect() as conn:
        rows = conn.execute(
            " SELECT * FROM documents ORDER BY created_at DESC"
        ).fetchall()

        return [dict(row) for row in rows]  

def delete_document(document_id):
    with _connect() as conn:
        conn.execute(
            "DELETE FROM documents WHERE document_id =?",
            (document_id,),
        )
        conn.commit()



                       





        
        
    


