install:
	pip install -r requirements.txt

api:
	uvicorn app.main:app --reload

ui:
	streamlit run frontend/streamlit_app.py

test:
	pytest -q
