# Phase 3: Deep Learning

> **Duration:** 8–10 weeks  
> **Prerequisite:** Phase 2 complete  
> **Goal:** Build, train, and deploy neural networks for vision and text problems using PyTorch

---

## Why Deep Learning Is Different

Classical ML: You engineer features → feed into algorithm → get prediction  
Deep Learning: You feed raw data → network learns its own features → prediction

Deep learning wins when:
- Data is unstructured (images, text, audio, video)
- You have large amounts of data (10k+ examples)
- The relevant patterns are too complex to hand-engineer

---

## Module 3.1 — Neural Networks From First Principles

### The Neuron: Building Block of Everything

```
Input → Weighted Sum → Activation Function → Output
```

A single neuron computes: `output = activation(w₁x₁ + w₂x₂ + ... + wₙxₙ + bias)`

```python
import numpy as np

class Neuron:
    def __init__(self, n_inputs):
        self.weights = np.random.randn(n_inputs) * 0.01
        self.bias = 0.0
    
    def forward(self, x):
        z = np.dot(self.weights, x) + self.bias  # Linear combination
        return self.relu(z)                        # Apply activation
    
    def relu(self, z):
        return np.maximum(0, z)                    # ReLU: max(0, z)

# A single neuron
neuron = Neuron(n_inputs=3)
x = np.array([0.5, -0.3, 1.2])
output = neuron.forward(x)
print(f"Neuron output: {output:.4f}")
```

### A Neural Network Layer

```python
class DenseLayer:
    def __init__(self, n_inputs, n_neurons):
        # Weight matrix: each neuron has its own set of weights
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.01
        self.biases = np.zeros(n_neurons)
    
    def forward(self, X):
        # X: (batch_size, n_inputs)
        # W: (n_inputs, n_neurons)
        # output: (batch_size, n_neurons)
        return np.dot(X, self.weights) + self.biases

# Stacking layers = deep network
layer1 = DenseLayer(n_inputs=784, n_neurons=256)  # 784 pixel inputs → 256 neurons
layer2 = DenseLayer(n_inputs=256, n_neurons=128)
layer3 = DenseLayer(n_inputs=128, n_neurons=10)   # 10 class outputs
```

### Backpropagation — How Networks Learn

**Intuition:** Forward pass computes predictions. Backward pass computes "how much did each weight contribute to the error?" Then update weights to reduce error.

The chain rule of calculus makes this possible:
```
∂Loss/∂w₁ = ∂Loss/∂output × ∂output/∂layer2 × ∂layer2/∂layer1 × ∂layer1/∂w₁
```

In PyTorch, you never implement this manually — autograd handles it.

---

## Module 3.2 — PyTorch Fundamentals

PyTorch is the industry standard for research and production deep learning.

### Why PyTorch Over TensorFlow?

- More Pythonic, easier to debug
- Dynamic computation graphs (define-by-run) — easier to understand
- Dominates research (most papers use PyTorch)
- PyTorch → ONNX → TensorFlow Lite / CoreML (for mobile deployment)

### Tensors

```python
import torch
import torch.nn as nn

# Creating tensors
x = torch.tensor([1.0, 2.0, 3.0])
W = torch.randn(3, 4)
zeros = torch.zeros(2, 3)
ones = torch.ones(5)

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)

# Shape operations
print(x.shape)           # torch.Size([3])
x_reshaped = x.view(-1, 1)  # (3,) → (3,1)
x_unsqueezed = x.unsqueeze(0)  # (3,) → (1,3)

# Autograd — automatic differentiation
x = torch.tensor([2.0], requires_grad=True)
y = x**2 + 3*x + 1
y.backward()             # Compute gradients
print(x.grad)            # dy/dx = 2x + 3 = 7.0 at x=2
```

### Building a Network with nn.Module

```python
import torch
import torch.nn as nn
import torch.optim as optim

class ChurnPredictor(nn.Module):
    def __init__(self, input_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),                      # Dropout for regularization
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()                          # Binary classification output
        )
    
    def forward(self, x):
        return self.network(x)

# Instantiate
model = ChurnPredictor(input_dim=20).to(device)
print(model)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total_params:,}")
```

### The Training Loop

```python
from torch.utils.data import DataLoader, TensorDataset

# Prepare data
X_tensor = torch.FloatTensor(X_train.values).to(device)
y_tensor = torch.FloatTensor(y_train.values).unsqueeze(1).to(device)
dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Training setup
model = ChurnPredictor(input_dim=X_train.shape[1]).to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.BCELoss()

# Training loop
train_losses = []
for epoch in range(50):
    model.train()
    epoch_loss = 0
    
    for batch_X, batch_y in loader:
        optimizer.zero_grad()         # 1. Clear old gradients
        outputs = model(batch_X)      # 2. Forward pass
        loss = criterion(outputs, batch_y)  # 3. Compute loss
        loss.backward()               # 4. Backpropagation
        optimizer.step()              # 5. Update weights
        epoch_loss += loss.item()
    
    avg_loss = epoch_loss / len(loader)
    train_losses.append(avg_loss)
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch}: Loss = {avg_loss:.4f}")

# Evaluation
model.eval()
with torch.no_grad():                 # No gradients needed for inference
    X_test_tensor = torch.FloatTensor(X_test.values).to(device)
    predictions = model(X_test_tensor).cpu().numpy()
```

---

## Module 3.3 — Convolutional Neural Networks (CNNs) for Vision

**Use when:** Images, screenshots, video frames, medical imaging.

**Key insight for mobile engineers:** CNNs are what powers face unlock, photo categorization, document scanning, and AR filters in mobile apps.

### How CNNs Work

```
Input Image (H×W×C)
       ↓
Convolutional Layer — learns local patterns (edges, textures)
       ↓
Pooling Layer — downsample, reduce spatial dimensions
       ↓
More Conv + Pool blocks...
       ↓
Flatten
       ↓
Dense Layers — combine features
       ↓
Output (class probabilities)
```

### CNN Implementation

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# Transform: normalize images for training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),        # Data augmentation
    transforms.ColorJitter(brightness=0.2),   # Data augmentation
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])  # ImageNet normalization
])

# Load dataset
train_dataset = torchvision.datasets.ImageFolder('data/train/', transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

class MobileScreenshotClassifier(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),   # (3,224,224) → (32,224,224)
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),                           # → (32,112,112)
            
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # → (64,112,112)
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),                           # → (64,56,56)
            
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1), # → (128,56,56)
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),                           # → (128,28,28)
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),                 # → (128,1,1)
            nn.Flatten(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)
```

### Transfer Learning — The Practical Approach

**Don't train from scratch.** Use a pre-trained model (trained on millions of images) and fine-tune it for your task. This works with as few as 500-1000 images.

```python
import torchvision.models as models

# Load pre-trained ResNet50
backbone = models.resnet50(pretrained=True)

# Freeze all layers (don't update their weights)
for param in backbone.parameters():
    param.requires_grad = False

# Replace the final layer with your task-specific head
num_features = backbone.fc.in_features  # 2048 for ResNet50
backbone.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, num_classes)
)

# Only the new head gets trained
optimizer = optim.Adam(backbone.fc.parameters(), lr=0.001)

# Fine-tuning phase 2: unfreeze and train with small lr
for param in backbone.parameters():
    param.requires_grad = True
optimizer = optim.Adam(backbone.parameters(), lr=0.0001)
```

**Popular pre-trained models:**
| Model | Params | Speed | Accuracy | Mobile? |
|-------|--------|-------|----------|---------|
| ResNet50 | 25M | Medium | High | MobileNet is better |
| EfficientNetB0 | 5.3M | Fast | Very High | Yes |
| MobileNetV3 | 5.4M | Very Fast | Good | Yes (designed for mobile) |
| ViT-B/16 | 86M | Slow | Highest | No |

---

## Module 3.4 — Recurrent Networks & NLP

### Word Embeddings — Representing Text as Vectors

```python
# The fundamental idea: words with similar meanings → similar vectors
# king - man + woman ≈ queen (famous Word2Vec property)

from gensim.models import Word2Vec

sentences = [["the", "app", "crashed", "on", "startup"],
             ["great", "app", "very", "stable"],
             ["the", "ui", "is", "beautiful"]]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
print(model.wv['app'])          # 100-dim vector for 'app'
print(model.wv.most_similar('crash'))  # Words similar to 'crash'
```

### Text Classification with PyTorch

```python
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# Sentiment analysis on app reviews
class AppReviewClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_classes)
    
    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

# Modern approach: use pre-trained embeddings from Hugging Face (Phase 4)
```

### LSTM for Sequence Modeling

```python
class SessionPredictor(nn.Module):
    """Predict next user action given sequence of past actions"""
    
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers,
                            batch_first=True, dropout=0.3)
        self.classifier = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        embedded = self.embedding(x)              # (batch, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        last_hidden = hidden[-1]                  # Take last layer's hidden state
        return self.classifier(last_hidden)
```

---

## Module 3.5 — Transformers and Attention

**This is the architecture behind GPT, BERT, and every modern LLM.** Understanding it conceptually is essential for Applied AI architecture.

### The Attention Mechanism

**Core idea:** Instead of processing sequence step-by-step (LSTM), look at ALL positions simultaneously and learn which positions are relevant to each other.

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q (Query): What am I looking for?
    K (Key): What do I contain?
    V (Value): What do I return if selected?
    
    Example: In "The app crashed because it ran out of memory",
    when processing "it", Q asks "what does 'it' refer to?"
    K of "app" answers "I am a noun that could be 'it'"
    V of "app" returns its information to enrich "it"
    """
    d_k = Q.size(-1)
    
    # Compute attention scores
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    # Apply mask (for causal/decoder attention)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # Softmax → attention weights (probabilities)
    attention_weights = F.softmax(scores, dim=-1)
    
    # Weighted sum of values
    output = torch.matmul(attention_weights, V)
    return output, attention_weights

# Multi-head attention: run attention h times in parallel
# Each head learns different types of relationships
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # Linear projections and split into heads
        Q = self.W_Q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_K(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_V(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Attention
        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)
        
        # Concatenate heads and project
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        return self.W_O(attn_output)
```

### Using Pre-trained Transformers (Hugging Face)

You won't train a transformer from scratch (that costs millions of dollars). You'll use pre-trained ones.

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Zero-shot — use a pre-trained model directly, no fine-tuning
classifier = pipeline("sentiment-analysis", 
                       model="distilbert-base-uncased-finetuned-sst-2-english")

reviews = [
    "This app is incredible! Best app I've ever used.",
    "The app keeps crashing. Terrible experience.",
    "Works fine but the UI could be better."
]

results = classifier(reviews)
for review, result in zip(reviews, results):
    print(f"Review: {review[:50]}...")
    print(f"Sentiment: {result['label']} ({result['score']:.3f})\n")

# Fine-tuning on your own data
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=5)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)
trainer.train()
```

---

## Module 3.6 — On-Device Deep Learning (Your Mobile Superpower)

This is where your mobile background creates enormous value. Most AI architects can't talk to this.

### Converting Models for Mobile

```python
import torch

# Step 1: Train your PyTorch model
model = MobileScreenshotClassifier(num_classes=5)
# ... training ...

# Step 2: Export to ONNX (universal format)
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "model.onnx",
                  export_params=True,
                  opset_version=12,
                  input_names=['input'],
                  output_names=['output'])

# Step 3a: Convert to TensorFlow Lite (Android)
# Use onnx2tf or TFLite converter
# tensorflow.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Step 3b: Convert to CoreML (iOS)
import coremltools as ct
model_coreml = ct.convert("model.onnx",
                           inputs=[ct.ImageType(name="input", shape=(1,3,224,224))])
model_coreml.save("ScreenshotClassifier.mlpackage")
```

### On-Device vs Cloud AI Decision Framework

| Factor | On-Device | Cloud API |
|--------|-----------|-----------|
| Latency | <50ms | 200ms–2s |
| Privacy | Data stays on device | Data leaves device |
| Offline | Works without internet | Requires internet |
| Model size | Must be <50MB typically | Unlimited |
| Accuracy | Lower (compressed model) | Higher (full model) |
| Cost at scale | Free (compute on user device) | Per-call pricing |
| Battery | Uses device GPU/NPU | Minimal |

**Architecture decision:** Use on-device for real-time features (face unlock, live filters, text recognition). Use cloud for complex reasoning (LLM chat, complex classification, recommendations).

---

## Phase 3 Capstone Project

**Project: Mobile UI Screenshot Classifier + App Review Sentiment**

**Part A — Vision Model:**
1. Collect/generate screenshots of different mobile app screen types (login, home, checkout, error, settings)
2. Train a CNN classifier (use transfer learning with MobileNetV3)
3. Achieve >85% classification accuracy
4. Export to CoreML and TFLite format
5. Write a `classify_screenshot(image_path) → screen_type` function

**Part B — NLP Model:**
1. Use the [Google Play Store Reviews dataset](https://www.kaggle.com/datasets/lava18/google-play-store-apps) from Kaggle
2. Fine-tune DistilBERT for 5-class sentiment (1-5 stars)
3. Build a FastAPI endpoint: `POST /analyze-review` → `{stars: 4, sentiment: "positive", confidence: 0.89}`
4. Compare against the simple Logistic Regression from Phase 2

---

## Phase 3 Completion Checklist

- [ ] Understand forward pass, backpropagation, gradient descent in neural networks
- [ ] Can build and train a neural network in PyTorch from scratch
- [ ] Understand CNNs — convolution, pooling, feature maps
- [ ] Applied transfer learning for image classification
- [ ] Understand attention mechanism and transformer architecture conceptually
- [ ] Used Hugging Face to run a pre-trained NLP model
- [ ] Know the trade-offs of on-device vs cloud inference
- [ ] Exported a model to CoreML or TFLite
- [ ] Completed both parts of the capstone project

**When all boxes are checked → move to [Phase 4](../phase-4-applied-ai-genai/README.md)**
