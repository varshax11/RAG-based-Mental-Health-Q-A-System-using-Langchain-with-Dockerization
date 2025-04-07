# RAG-based Mental Health Q&A System using LangChain with Dockerization 

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer medical questions using **LangChain** and large language models. It leverages external knowledge bases to provide context-aware and accurate responses for medical queries.

---

## Features

- Uses LangChain to manage LLM-based chains
- Designed for medical question answering
- Retrieval-Augmented Generation (RAG) architecture
- Dockerized for portability and easy deployment
- Ready for deployment to cloud platforms (AWS EC2, etc.)

---

## Project Structure

```bash

mental_health_rag_project/
├── Dockerfile                       # Instructions to build the Docker image
├── README.md                        # Project documentation and usage guide
├── requirements.txt                 # Python dependencies
├── app.py                           # Entry point to run the web application or backend
├── query.py                         # Script to handle user query input and processing
├── rag.py                           # Core Retrieval-Augmented Generation (RAG) pipeline
├── mental_health_documents/        # Folder containing the document dataset
│   └── mental_health_documents/    # Subfolder with text documents related to mental health

```



---

## Requirements

You need to have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

---

## Docker Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/varshax11/RAG-based-Medical-Q-A-System-using-Langchain.git
cd RAG-based-Medical-Q-A-System-using-Langchain
```

### Step 2: Build the Docker image
```bash
docker build -t rag-medical-qa .
```
This creates a Docker image named rag-medical-qa.



### Step 3: Run the Docker container
```bash

docker run -it --rm rag-medical-qa

```
The app should now start inside the container.

### Local (Non-Docker) Setup
If you prefer running the app directly:

Step 1: Create a virtual environment
```bash

python3 -m venv venv
source venv/bin/activate

```
Step 2: Install dependencies
```bash

pip install -r requirements.txt

```

Step 3: Run the application
```bash

python main.py

```

Make sure main.py is your entry point. Adjust if your project structure is different.

### Optional: Save/Share Docker Image
To save and compress the image:

``` bash

docker save rag-medical-qa | gzip > rag-medical-qa.tar.gz

```

To load it on another machine:

``` bash

gunzip -c rag-medical-qa.tar.gz | docker load

```

### Deployment to Cloud (EC2 / Cloud Run / Render)

Once Dockerized, you can deploy the container to:

AWS EC2: Launch an instance, install Docker, and run the container.

Render / Railway / Fly.io: Push the image or project, and set up the runtime environment.

GitHub Actions: Automate deployment by pushing the image to Docker Hub or ECR.

### Contributing
Pull requests are welcome. For major changes, please open an issue to discuss what you'd like to change.

### License
This project is licensed under the MIT License
