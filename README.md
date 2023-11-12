# Phishing Email Filtering
## Paper Coming Soon!
I use Flask as the user interface, and allow users to upload their email as a .eml file and see:

1.What are the features extracted?
2.Whether it's a phishing email or not based on model prediction?

Throughout my research, the models I trained are able to achieve more than 80% accuracy. I will continue to work on this and make sure it works perfectly fine.
## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/downloads/) (version X.X or higher)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Clone the Repository

Open your terminal or command prompt and run the following command to clone the repository:

```bash
git clone [link to repo]
```

### Activate venv
```bash
cd [repo]
conda create --name venv python=3.11
conda activate venv
```
### Install Requirements
```bash
pip install -r requirements.txt
```
### Run Flask APP
```bash
python main.py
```
