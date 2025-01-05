# NMT Tool - Flutter Development CLI

NMT Tool is a command-line utility designed to simplify Flutter app development. It provides commands for creating Flutter projects, managing features, generating entities from CSV, and setting up responsive layouts.

---

## **Installation and Setup**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <repository_directory>
```

### **2. Create a Python Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Usage**

### **1. Check Tool Version**
To confirm the tool is installed correctly, check its version:
```bash
python my_tool.py version
```

---

### **2. Create a New Flutter Project**
Generate a new Flutter project with a predefined directory structure:
```bash
python my_tool.py create <project_name>
```
Example:
```bash
python my_tool.py create MyFlutterApp
```

#### **Directory Structure:**
```
MyFlutterApp/
  ├── lib/
  │   ├── core/
  │   │   └── entities/
  │   ├── features/
  │   ├── shared/
  │   └── config/
```

---

### **3. Generate an Equatable Entity from CSV**
Create a Dart entity based on the headers and data types in a CSV file:
```bash
python my_tool.py generate_entity <csv_path> <entity_name>
```
Example:
```bash
python my_tool.py generate_entity ./entities.csv User
```
- **CSV Example:**
  ```csv
  id,name,age,isActive
  1,John,25,true
  2,Jane,30,false
  ```

#### **Output:**
A Dart file will be created in `lib/core/entities/<entity_name>.dart`.

---

### **4. Generate a Responsive Flutter Layout**
Add a predefined responsive layout template to your Flutter project:
```bash
python my_tool.py flutter_layout <project_name>
```
Example:
```bash
python my_tool.py flutter_layout MyFlutterApp
```

#### **Output:**
The file `responsive_layout.dart` will be created in the `lib/` directory.

---

### **5. Change Flutter Project Package Name**
Update the package name for both Android and iOS in your Flutter project:
```bash
python my_tool.py change_package_name <new_package_name>
```
Example:
```bash
python my_tool.py change_package_name com.example.mynewapp
```

---

### **6. Initialize NMT Configuration**
Set up the default NMT configuration for a Flutter project:
```bash
python my_tool.py init
```

#### **Output:**
A file `nmt.json` will be created with basic project configuration.

---

## **Dependencies**
- Python 3.7+
- Click library for building CLI tools
- Flutter installed and added to the PATH

---

## **Development**
Feel free to contribute to the project by submitting issues or pull requests on GitHub.

---

By following this guide, you can easily set up and use the NMT Tool to streamline your Flutter development workflow! 🎉




Check the Version of the Tool
# python my_tool.py version

Create a New Flutter Project
# python my_tool.py create <project_name>


Generate an Equatable Entity from a CSV File
# python my_tool.py generate_entity <csv_path> <entity_name>


Generate a Responsive Flutter Layout Template
# python my_tool.py flutter_layout


Change the Package Name of a Flutter Project
# python my_tool.py change_package_name <new_package_name>
