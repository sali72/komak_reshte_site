## Komak Reshte: A University Application Assistant

**Introduction**

Komak Reshte is a hands-on Django project aimed at aiding university applicants. It helps students find available fields of study, create and modify lists, reorder them, and export data—all without the tedious task of finding unique codes for each field of study. The application supports both English and Persian languages and utilizes a simple SQLite database for data storage.


Students can import data via CSV or through the Django admin panel. The data should come from Iran's Sanjesh guidebook for Konkoor and must include the following columns: Order, Unique Code, Field of Study, Exam Group, University, Requires Exam, Tuition Type, First Half Acceptances, Second Half Acceptances, Women, Men, and Extra Information. Once imported, users can manage their lists with ease.

**Data Import**

To effectively use Komak Reshte, you'll need to import data from Iran's Sanjesh guidebook for Konkoor. The imported CSV file should contain the following columns:

* **Order**
* **Unique Code**
* **Field of Study**
* **Exam Group**
* **University**
* **Requires Exam**
* **Tuition Type**
* **First Half Acceptances**
* **Second Half Acceptances**
* **Women**
* **Men**
* **Extra Information**

**Usage**

1. **Access the App:** Navigate to the Komak Reshte application URL.
2. **Select Language:** Choose your preferred language (English or Persian) using the provided buttons.
3. **Import Data:** Load your CSV data from the Sanjesh guidebook into the application. You can also use the Django admin panel for data entry.
4. **Manage Lists:** Create, edit, and reorder your lists of fields of study to suit your preferences.
5. **Export Data:** Easily export your data in a format that's convenient for you.

**Vision**

Komak Reshte may to become a comprehensive resource for students navigating the university application process. We welcome contributions and suggestions to further enhance its features and capabilities.
