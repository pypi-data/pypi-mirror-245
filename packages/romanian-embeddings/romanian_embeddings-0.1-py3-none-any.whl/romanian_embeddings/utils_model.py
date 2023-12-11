import os
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from transformers.convert_graph_to_onnx import convert
import numpy as np

import onnxruntime as ort
from transformers import AutoTokenizer

import multiprocessing
from queue import Empty


def convert_model_to_onnx(model_name: str, output_dir: str = './') -> Path:
    model_path = Path(output_dir) / f"{model_name}.onnx"
    if not model_path.exists():
        model = AutoModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        convert(framework="pt", model=model, tokenizer=tokenizer, output=model_path, opset=11)
    return model_path


class ONNXModelWorker:
    def __init__(self, model_path: str, model_name: str, normalize: bool=True):
        self.model_path = model_path
        self.model_name = model_name
        self.model = ort.InferenceSession(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.normalize = normalize

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings

        # Use np.expand_dims to expand the dimensions and broadcasting for expansion
        input_mask_expanded = np.expand_dims(attention_mask, -1)

        # Perform element-wise multiplication and sum
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)

        # Use np.clip to avoid division by zero
        sum_mask = np.clip(np.sum(input_mask_expanded, axis=1), a_min=1e-9, a_max=None)

        return sum_embeddings / sum_mask
    
    def process(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="np", padding=True, truncation=True, max_length=512)
        outputs = self.model.run(None, dict(inputs))
        embeddings = self.mean_pooling(outputs, inputs["attention_mask"])
        if self.normalize:
            # Calculate the L2 norm of each vector (axis=1)
            l2_norms = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
            # Normalize each vector by its L2 norm
            embeddings = embeddings / l2_norms

        return embeddings  # Assuming the output is the embedding


class ParallelWorkerPool:
    def __init__(self, num_workers, worker_class, model_path, model_name):
        self.num_workers = num_workers
        self.worker_class = worker_class
        self.model_path = model_path
        self.model_name = model_name
        self.input_queue = multiprocessing.Queue()
        self.output_queue = multiprocessing.Queue()

    def worker_function(self):
        worker = self.worker_class(self.model_path, self.model_name)
        while True:
            try:
                text = self.input_queue.get(timeout=10)
                if text is None:
                    break
                embedding = worker.process(text)
                self.output_queue.put(embedding)
            except Empty:
                continue

    def start(self):
        self.processes = [multiprocessing.Process(target=self.worker_function) for _ in range(self.num_workers)]
        for p in self.processes:
            p.start()

    def stop(self):
        for _ in range(self.num_workers):
            self.input_queue.put(None)
        for p in self.processes:
            p.join()

    def get_embedding(self, text):
        self.input_queue.put(text)
        return self.output_queue.get()


if __name__ == "__main__":
    model_name = "bert-base-uncased"
    output_dir = "./models"
    model_path = convert_model_to_onnx(model_name, output_dir)

    pool = ParallelWorkerPool(num_workers=2, worker_class=ONNXModelWorker, model_path=str(model_path), model_name=model_name)
    pool.start()

    # Example usage
    texts = ["Hello, world!", "The quick brown fox jumps over the lazy dog"]
    for text in texts:
        embedding = pool.get_embedding(text)
        print(f"Embedding for '{text}': {embedding}")

    pool.stop()

