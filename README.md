# 🌸 MLflow Integrated MLOps Pipeline for Iris Classification  

This repository demonstrates a **modern Machine Learning Operations (MLOps) pipeline** integrating **MLflow** for:

- Experiment tracking  
- Model registry management  
- Continuous Integration (CI) quality gating  

It fulfills the assignment requirements of:  
✅ Introducing **hyperparameter tuning**  
✅ Logging **artifacts and metrics** with MLflow  
✅ Utilizing the **MLflow Model Registry** for deployment  
✅ Removing legacy model management (like **DVC**)  

---

## 🧱 Project Structure  

The repository is organized into four core files, each playing a specific role in the MLOps pipeline.  

| File | Description |
|------|--------------|
| **notebook_week5.ipynb** | Development and training notebook integrating MLflow for tracking and registry. |
| **ci_sanity_check.py** | CI quality gate script to validate model performance before deployment. |
| **ci.yml** | GitHub Actions workflow orchestrating CI pipeline automation. |
| **requirements.txt** | Dependency list ensuring reproducible environments for both local and CI runs. |

---

## 📘 1. notebook_week5.ipynb  

**Purpose:** Primary development, training, and testing environment for the Iris classification model.  

### 🔹 Components & Objectives  

| Component | Utility | Assignment Objective Fulfilled |
|------------|----------|--------------------------------|
| **Data Handling** | Loads the `iris.csv` dataset directly from the configured **Google Cloud Storage (GCS)** path. | Explaining input files/data |
| **HPO Demonstration** | Defines two sets of hyperparameters (one commented out) to train a `DecisionTreeClassifier`. | Introduce hyperparameter tuning as part of training loop |
| **MLflow Tracking** | Starts an MLflow run, logs hyperparameters (`max_depth`, `criterion`), evaluation metrics (accuracy), and sets experiment tags. | Log experiment parameters, evaluation metrics |
| **MLflow Model Registry** | Uses `mlflow.sklearn.log_model(registered_model_name="iris-classifier-dt")` to serialize, save, and register the model to the remote MLflow registry. | Log models via MLflow; remove legacy DVC model logging |
| **Evaluation Pipeline** | Fetches model from MLflow Registry using stage-aware URI `models:/iris-classifier-dt/Production`, ensuring evaluation on the deployed model version. | Modify evaluation pipeline to fetch the latest/best model from MLflow |

---

## ⚙️ 2. ci_sanity_check.py  

**Purpose:** Core CI quality gate script validating the deployed model before passing CI.  

### 🔹 Components & Objectives  

| Component | Utility | Assignment Objective Fulfilled |
|------------|----------|--------------------------------|
| **MLflow Connection** | Connects to the remote MLflow Tracking Server via `MLFLOW_TRACKING_URI`. | CI to fetch and utilize the latest/best model from MLflow Model Registry |
| **Dynamic Loading** | Loads the **Production** model using MLflow stage URI `models:/iris-classifier-dt/Production`. | CI to fetch and utilize latest/best model |
| **Sanity Test** | Defines a small static test dataset (`sanity_df`) to evaluate model performance. | Run sanity checks |
| **Quality Gate** | Compares model accuracy against `MIN_ACCEPTABLE_ACCURACY = 0.90`. Returns exit code `0` (PASS) or `1` (FAIL) to control CI pipeline outcome. | Run quality gating in CI |

---

## 🔁 3. ci.yml  

**Purpose:** GitHub Actions workflow defining and automating the CI process.  

### 🔹 Components & Objectives  

| Component | Utility | Assignment Objective Fulfilled |
|------------|----------|--------------------------------|
| **Triggers** | Executes workflow on push to `main`, `dev`, or `master` branches. | CI to fetch and utilize latest/best model from MLflow Registry |
| **Dependency Setup** | Installs Python 3.11 and dependencies from `requirements.txt`. | CI orchestration |
| **GCP Authentication** | Uses `google-github-actions/auth@v2` with secret `${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}` to authenticate with GCS. | Working demo in GCP environment |
| **Execute Sanity Check** | Runs `ci_sanity_check.py`. Workflow passes/fails based on script exit code. | CI to fetch and utilize latest/best model |

---

## 📦 4. requirements.txt  

**Purpose:** Ensures consistent dependency management across development and CI environments.  

### 🔹 Dependencies & Purpose  

| Package | Purpose | Assignment Objective Fulfilled |
|----------|----------|--------------------------------|
| **mlflow** | Core library for experiment tracking, model logging, and registry management. | Log experiments, metrics, and models via MLflow |
| **scikit-learn** | Used for `DecisionTreeClassifier` training and evaluation metrics. | Model training & evaluation |
| **pandas** | Data loading and manipulation for both training and CI. | Input data processing |
| **google-cloud-storage** | Enables MLflow to manage artifacts in a GCS bucket. | Cloud artifact storage |
| **numpy** | Essential scientific computing library, required by scikit-learn/pandas. | Data processing |

---

## ☁️ Cloud Integration  

This pipeline leverages **Google Cloud Storage (GCS)** as the remote artifact store for MLflow, ensuring centralized model versioning and reproducible experiment management.  

---

## 🚀 CI/CD Flow Summary  

1. **Developer trains model** via `notebook_week5.ipynb` → MLflow logs experiment, metrics, and registers the model.  
2. **Model promoted to “Production”** stage in MLflow.  
3. **GitHub Actions CI** triggers on push → authenticates to GCP → fetches Production model.  
4. **`ci_sanity_check.py`** runs → validates model accuracy against threshold.  
5. **CI pass/fail** dictates deployment readiness.  

---

## 🧩 Key Highlights  

- 🔁 **Automated MLflow model registry integration**  
- 🧠 **Decision Tree hyperparameter tuning**  
- 🧪 **Continuous Integration quality gating**  
- ☁️ **Seamless GCP artifact storage**  
- 🧰 **Fully reproducible pipeline setup**

---

