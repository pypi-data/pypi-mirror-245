import bentoml
import torch
from bentoml.io import JSON, NumpyNdarray

tokenizer = bentoml.transformers.get("sentence_bert_tokenizer")
_TokenizerRunnable = tokenizer.to_runnable()

model = bentoml.transformers.get("sentence_bert_model")
_ModelRunnable = model.to_runnable()


class ModelRunnable(_ModelRunnable):
    def __init__(self):
        super().__init__()
        self.tokenizer = _TokenizerRunnable()
    @bentoml.Runnable.method(batchable=True)
    def __call__(self, keywords):
        encoded_input = self.tokenizer(keywords, padding=True, truncation=True, return_tensors='pt')
        model_output = super().__call__(**encoded_input)
        sentence_embedding = self._mean_pooling(model_output, encoded_input["attention_mask"])
        return sentence_embedding
    
    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# Build the runner from the runnable manually, instead of calling model.to_runner() method
model_runner = bentoml.Runner(ModelRunnable)
svc = bentoml.Service(name="sentence_bert", runners=[model_runner], models=[model, tokenizer])

@svc.api(input=JSON(), output=NumpyNdarray())
async def get_embedding(inp):
    keywords = inp["keywords"]
    with torch.no_grad():
        sentence_embedding = await model_runner.async_run(keywords)
    return sentence_embedding.detach().numpy()