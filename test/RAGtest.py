from app.core.rag.retriever import Retriever

ret = Retriever()
results = ret.retrieve("初中数学教什么？", top_k=2)
for r in results:
    print(r['content'], r['metadata'])
if not results:
    print("No results")