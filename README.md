# IST105 - Assignment #9: Cisco DNA Center Network Automation

## Architecture Overview

* **WebServer-EC2**

  * OS: Amazon Linux 2023
  * Runs the Django application (`assignment9` project, `dna_center_cisco` app)
  * Connects to Cisco DNA Center sandbox via HTTPS (REST API)
  * Connects to MongoDB-EC2 for logging via port `27017`

* **MongoDB-EC2**

  * OS: Amazon Linux 2023
  * Runs `mongod` (MongoDB server)
  * Listens on port `27017`, open only to the WebServer-EC2 private IP
  * Stores logs in database `dnac_logs`, collection `interactions`

---

## Setup

### 1. MongoDB-EC2

1. Install MongoDB.

2. Start and enable the service:

   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

---

### 2. WebServer-EC2 (Django)

1. Clone the repository:

   ```bash
   git clone https://github.com/ezgna/IST105-Assignment9.git
   cd IST105-Assignment9
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply Django migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the Django development server:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```