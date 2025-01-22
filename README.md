
## Installation

### Prerequisites

1. Python 3.10 or higher must be installed.
   * On Ubuntu/Debian:
     ```
     sudo apt update && sudo apt install python3 python3-venv python3-pip
     ```
   * On Windows: Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) and add it to your PATH.
2. Make sure `git` is installed.

---

### Steps

1. Clone the repository:

   ```
   git clone https://github.com/HugoSeverino/Datanovate_site.git
   cd Datanovate_site
   ```
2. Set up the virtual environment:
   On Linux/MacOS:

   ```
           python3 -m venv venv_datanovate
   	source venv_datanovate/bin/activate
   ```

   On Windows:

   ```
   	python -m venv venv_datanovate
   	venv_datanovate\Scripts\activate
   ```
3. Install Python dependencies:

   ```
   pip install -r requirements.txt
   ```

---

### **Running the Application**

1. Start the server:

   ```
   python app.py
   ```
   or

   ```
   flask run
   ```
2. Open your browser and navigate to:

   * [http://127.0.0.1:5000](http://127.0.0.1:5000)
