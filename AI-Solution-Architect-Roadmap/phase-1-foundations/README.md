# Phase 1: Foundations
### Math, Python, and Data Literacy

> **Duration:** 6–8 weeks  
> **Prerequisite:** Your existing engineering background  
> **Goal:** Be able to read AI papers, write data manipulation code, and understand the math behind ML algorithms without fear

---

## Why This Phase Matters

Every AI/ML algorithm is built on three foundations:
1. **Linear Algebra** — how data is represented (vectors, matrices, tensors)
2. **Calculus** — how models learn (gradients, optimization)
3. **Probability & Statistics** — how models reason under uncertainty

You don't need to become a mathematician. You need enough to:
- Understand *why* an algorithm behaves the way it does
- Debug a model that isn't learning
- Read research papers without getting stuck on notation
- Make architectural decisions grounded in mathematical reality

---

## Module 1.1 — Python for AI Engineers

### Why Python (Even If You Know Other Languages)

Python is the language of AI. Not because it's the fastest (it isn't), but because:
- NumPy, PyTorch, TensorFlow are Python-first
- The entire research ecosystem publishes in Python
- Most cloud AI SDKs have Python as the primary interface

Your mobile experience with Swift/Kotlin/Java/Dart gives you a head start on OOP and type thinking. Python will feel loose at first — embrace the ecosystem.

### Learning Path

**Week 1–2: Python Fundamentals (fast-track for experienced engineers)**

Resources:
- [Python for Everybody (py4e.com)](https://www.py4e.com/) — free, beginner-friendly
- [Real Python](https://realpython.com/) — practitioner-grade tutorials

Topics to cover:
- [ ] Python syntax, types, control flow
- [ ] Functions, lambdas, decorators
- [ ] List comprehensions, generators, iterators
- [ ] Classes and OOP in Python
- [ ] File I/O, JSON handling
- [ ] Virtual environments (`venv`, `pip`)
- [ ] Type hints (Python 3.9+)

**Key differences from mobile languages to internalize:**
```python
# Duck typing — no explicit interface declaration needed
def process(data):          # data can be anything with .items()
    for k, v in data.items():
        print(k, v)

# List comprehension — very common in data work
squares = [x**2 for x in range(10)]

# Unpacking
a, b, *rest = [1, 2, 3, 4, 5]

# Generators — memory-efficient for large data
def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1
```

**Week 2–3: Scientific Python Stack**

| Library | Purpose | Priority |
|---------|---------|---------|
| NumPy | N-dimensional arrays, fast math | Critical |
| Pandas | Tabular data manipulation | Critical |
| Matplotlib | Plotting and visualization | Important |
| Seaborn | Statistical visualization | Important |

### NumPy Deep Dive (Critical)

NumPy is the backbone of all AI in Python. Spend dedicated time here.

```python
import numpy as np

# Arrays — the fundamental structure
a = np.array([1, 2, 3])           # 1D array (vector)
b = np.array([[1,2],[3,4]])       # 2D array (matrix)
c = np.zeros((3, 4))              # 3x4 matrix of zeros
d = np.random.randn(100, 10)      # 100 samples, 10 features

# Shape is everything
print(d.shape)   # (100, 10)
print(d.ndim)    # 2
print(d.dtype)   # float64

# Broadcasting — NumPy magic, learn this well
a = np.array([1, 2, 3])   # shape (3,)
b = 2                      # scalar
print(a * b)               # [2, 4, 6] — broadcasts b across a

# Matrix operations — this IS linear algebra in code
A = np.random.randn(3, 4)
B = np.random.randn(4, 5)
C = A @ B                  # Matrix multiplication: (3,5)

# Slicing
data = np.random.randn(100, 10)
first_50 = data[:50]            # First 50 rows
col_3 = data[:, 2]              # All rows, column index 2
subset = data[10:20, 3:7]       # Rows 10-20, cols 3-7
```

**Practice exercises:**
1. Implement mean normalization (zero mean, unit variance) using only NumPy
2. Implement dot product of two vectors manually, then compare with `np.dot()`
3. Reshape a 1D array of 1000 elements into (10, 10, 10) 3D tensor

### Pandas Deep Dive (Critical)

```python
import pandas as pd

# DataFrame — like a spreadsheet in code
df = pd.read_csv('data.csv')
print(df.head())
print(df.info())
print(df.describe())

# Selecting data
df['column']              # Series (single column)
df[['col1', 'col2']]      # DataFrame (multiple columns)
df.iloc[0:5]              # First 5 rows by position
df.loc[df['age'] > 25]    # Filter rows by condition

# Transformations
df['log_price'] = np.log(df['price'])   # New derived column
df.dropna()                              # Remove rows with null
df.fillna(df.mean())                    # Fill nulls with mean

# GroupBy — aggregation
df.groupby('category')['revenue'].mean()

# Merge — like SQL JOIN
merged = pd.merge(df1, df2, on='user_id', how='left')
```

---

## Module 1.2 — Mathematics for Machine Learning

> You don't need to derive every proof. You need **intuition** and **computational fluency**.

### 1.2.1 Linear Algebra

**The core mental model:** Data is vectors. Models transform vectors. Training finds the right transformation.

**Concepts to master:**

| Concept | What It Means in AI |
|---------|---------------------|
| Vector | A single data point (e.g., [age=25, salary=70000, churn=0]) |
| Matrix | A batch of data points or a layer's weights |
| Dot product | Similarity between two vectors; foundation of attention |
| Matrix multiplication | How data flows through neural network layers |
| Transpose | Reshaping data for computations |
| Eigenvalues/Eigenvectors | Used in PCA — finding the "important directions" in data |
| Norms (L1, L2) | Measuring how "big" a vector is; used in regularization |

**Resources:**
- [3Blue1Brown: Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — Watch ALL of this. Stunning visual intuition.
- [Khan Academy Linear Algebra](https://www.khanacademy.org/math/linear-algebra) — For practice problems

**Practical code:**
```python
import numpy as np

# Vectors
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# Dot product — measures similarity
dot = np.dot(v1, v2)           # 32

# L2 norm — "length" of a vector
norm = np.linalg.norm(v1)      # 3.74

# Cosine similarity — direction similarity (used in LLMs!)
cos_sim = dot / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Matrix multiplication — how NN layers work
W = np.random.randn(4, 3)   # Weight matrix (4 neurons, 3 inputs)
x = np.array([0.5, -0.2, 1.0])  # Input
output = W @ x               # Shape: (4,) — 4 neuron activations

# Eigendecomposition — for PCA
A = np.array([[3, 1], [1, 3]])
eigenvalues, eigenvectors = np.linalg.eig(A)
```

### 1.2.2 Calculus (Differentiation Focus)

**The core mental model:** Training a model means finding the minimum of a loss function. Calculus tells us which direction to step.

**Concepts to master:**

| Concept | What It Means in AI |
|---------|---------------------|
| Derivative | Rate of change — how much does the loss change if I adjust this weight? |
| Gradient | Derivative for multiple variables — points "uphill" in weight space |
| Chain rule | How backpropagation works — gradients flow backward through layers |
| Partial derivative | How loss changes w.r.t. one specific weight |
| Gradient descent | Iteratively step opposite to gradient to minimize loss |

**Resources:**
- [3Blue1Brown: Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)
- [Khan Academy Calculus](https://www.khanacademy.org/math/calculus-1)

**Gradient Descent — The Algorithm That Trains Everything:**
```python
import numpy as np
import matplotlib.pyplot as plt

# Problem: find x that minimizes f(x) = x^2 + 2x + 1
# True minimum: x = -1

def f(x):
    return x**2 + 2*x + 1

def df(x):  # Derivative: 2x + 2
    return 2*x + 2

# Gradient descent
x = 10.0          # Start far from minimum
lr = 0.1          # Learning rate
history = []

for step in range(50):
    grad = df(x)        # Compute gradient
    x = x - lr * grad   # Step opposite to gradient
    history.append((x, f(x)))
    if step % 10 == 0:
        print(f"Step {step}: x={x:.4f}, f(x)={f(x):.4f}")

# This same logic, scaled to millions of parameters, is how GPT-4 was trained
```

### 1.2.3 Probability & Statistics

**The core mental model:** Models don't output certainties — they output probability distributions. Understanding uncertainty is core to AI reasoning.

**Concepts to master:**

| Concept | What It Means in AI |
|---------|---------------------|
| Probability distribution | What values a variable is likely to take |
| Conditional probability P(A\|B) | Foundation of Naive Bayes; Bayesian reasoning |
| Bayes' theorem | How to update beliefs given evidence |
| Expected value | Average outcome — used in reward modeling, RL |
| Variance / Std deviation | How spread out predictions are |
| Normal/Gaussian distribution | Most natural phenomena; assumed in many models |
| Cross-entropy | The loss function for classification models |
| KL divergence | Measuring difference between two distributions; used in VAEs, RLHF |

**Resources:**
- [StatQuest with Josh Starmer](https://www.youtube.com/c/joshstarmer) — Best stats explanations on YouTube
- [Think Stats — free book](https://greenteapress.com/wp/think-stats-2e/)

**Practical code:**
```python
import numpy as np
from scipy import stats

# Normal distribution
mu, sigma = 0, 1
samples = np.random.normal(mu, sigma, 1000)
print(f"Mean: {samples.mean():.3f}, Std: {samples.std():.3f}")

# Probability — discrete
outcomes = ['cat', 'dog', 'bird']
probs = [0.6, 0.3, 0.1]

# Cross-entropy loss — measures how wrong a classifier is
def cross_entropy(y_true, y_pred):
    # y_true: [0, 1, 0] (one-hot encoded ground truth)
    # y_pred: [0.1, 0.8, 0.1] (model's predicted probabilities)
    return -np.sum(y_true * np.log(y_pred + 1e-9))

y_true = np.array([0, 1, 0])       # True class: dog
y_pred = np.array([0.1, 0.8, 0.1]) # Model says 80% dog
print(cross_entropy(y_true, y_pred))  # Low loss — model is right

y_pred_bad = np.array([0.5, 0.2, 0.3])
print(cross_entropy(y_true, y_pred_bad))  # Higher loss — model is wrong
```

---

## Module 1.3 — Data Fundamentals

### Understanding Data Types in AI

| Data Type | Examples | Models That Handle It |
|-----------|---------|----------------------|
| Tabular / Structured | CSV files, SQL tables, app events | Linear models, Tree models, XGBoost |
| Text / NLP | Reviews, logs, documents | BERT, GPT, Word2Vec |
| Image | Photos, screenshots, X-rays | CNN, ViT, CLIP |
| Time Series | Stock prices, sensor data, DAU metrics | LSTM, Transformers, Prophet |
| Graph | Social networks, knowledge graphs | GNN, Node2Vec |
| Audio | Speech, music | Whisper, Wav2Vec |
| Multimodal | Image + Text, Video + Audio | CLIP, Flamingo, GPT-4V |

### Data Lifecycle (Critical for Architects)

```
Raw Data Collection
       ↓
Data Ingestion & Storage (S3, GCS, data warehouse)
       ↓
Data Validation (schema checks, null detection, drift)
       ↓
Exploratory Data Analysis (EDA)
       ↓
Feature Engineering & Preprocessing
       ↓
Train/Validation/Test Split
       ↓
Model Training
       ↓
Model Evaluation
       ↓
Deployment
       ↓
Monitoring (data drift, model drift, business metrics)
```

### Jupyter Notebooks — Your Data Exploration Environment

```bash
# Install and launch
pip install jupyter notebook
jupyter notebook

# Or use Google Colab (free, no setup)
# https://colab.research.google.com
```

**Notebook best practices:**
- One notebook = one experiment or analysis
- Always restart and run all before sharing
- Use markdown cells to document your reasoning
- Keep data loading, transformation, and visualization in separate sections

---

## Module 1.4 — Setting Up Your AI Development Environment

```bash
# 1. Install Python 3.11
# https://www.python.org/downloads/

# 2. Create a virtual environment
python -m venv ai-env
source ai-env/bin/activate  # Mac/Linux
# ai-env\Scripts\activate   # Windows

# 3. Install core libraries
pip install numpy pandas matplotlib seaborn jupyter scikit-learn

# 4. Install deep learning (CPU mode to start)
pip install torch torchvision

# 5. Install GenAI tools
pip install openai langchain transformers

# 6. Verify
python -c "import numpy as np; import pandas as pd; import torch; print('All good!')"
```

**VS Code Setup for AI:**
- Install Python extension
- Install Jupyter extension
- Install GitHub Copilot (huge productivity boost)
- Configure pylint or ruff for linting

---

## Phase 1 Capstone Project

**Project: Mobile App Crash Log Analyzer**

Build a Python data pipeline that:
1. Loads crash log data from a CSV file (simulate with synthetic data)
2. Cleans and normalizes the data using Pandas
3. Performs exploratory data analysis
4. Produces visualizations: crash rate by OS version, by device, by app version
5. Computes statistics: mean time between crashes, p99 crash rate
6. Exports a summary report

**Why this project:** It directly uses your mobile domain knowledge, reinforces Python + Pandas + NumPy + Matplotlib, and produces something you can explain in an interview as "here's how I applied data skills to a real problem I knew well."

**Starter template:** See [`phase-1-foundations/project-crash-analyzer.ipynb`](./project-crash-analyzer.ipynb)

---

## Phase 1 Completion Checklist

- [ ] Python: Can write scripts, use comprehensions, handle files, use classes
- [ ] NumPy: Can create, slice, reshape, and perform operations on arrays
- [ ] Pandas: Can load, clean, filter, group, and merge DataFrames
- [ ] Math: Understand vector/matrix operations conceptually and in code
- [ ] Math: Understand gradient descent — can implement from scratch
- [ ] Math: Understand probability distributions and cross-entropy loss
- [ ] Completed the crash log analyzer capstone project
- [ ] Set up local development environment with Jupyter working

**When all boxes are checked → move to [Phase 2](../phase-2-data-science-ml/README.md)**
