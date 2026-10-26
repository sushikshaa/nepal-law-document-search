# Nepali Law Document Search (RAG retrieval)

Semantic search over public documents English, built with LangChain, FAISS and
multilingual Hugging Face embeddings. Returns cited passages (file + page) and says "not found"
when nothing is close enough.

## Run
pip install -r requirements.txt
# put 3-5 PDFs/.txt files into docs/
streamlit run app.py
python eval.py   # retrieval accuracy for different chunk sizes

## Results
(Fill in after running eval.py: top-1 / top-3 accuracy on N questions.)
