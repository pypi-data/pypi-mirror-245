import bentoml
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained('jhgan/ko-sbert-multitask')
model = AutoModel.from_pretrained('jhgan/ko-sbert-multitask')

bentoml.transformers.save_model("sentence_bert_tokenizer", tokenizer)
bentoml.transformers.save_model("sentence_bert_model", model, signatures={"__call__": {"batchable": True}})