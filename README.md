# Content-Based Image Retrieval (CBIR) System

A sophisticated Content-Based Image Retrieval system that uses deep learning features to find visually similar images in a multimedia database. Built with Flask, PostgreSQL, and powered by ResNet50 for feature extraction.

## 🌟 Features

- **Deep Learning-Powered Search**: Uses ResNet50 pre-trained model for robust feature extraction
- **Cosine Similarity Matching**: Advanced similarity computation for accurate image retrieval
- **Web Interface**: Clean, responsive web interface for image upload and search
- **PostgreSQL Integration**: Efficient database storage with binary feature vectors
- **Duplicate Prevention**: Automatic detection and prevention of duplicate image entries
- **Previous Uploads**: Browse and manage previously uploaded images
- **REST API**: JSON API endpoints for programmatic access

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Machine Learning**: TensorFlow/Keras, ResNet50
- **Image Processing**: PIL, NumPy
- **Similarity Computation**: Scikit-learn (Cosine Similarity)
- **Frontend**: HTML5, CSS3, JavaScript
- **CORS**: Flask-CORS for cross-origin requests

## 📁 Project Structure

```
CBIR-Multimedia-Database/
├── app.py                    # Flask web application
├── models.py                 # Database models and ML functions
├── insert.py                 # Batch image insertion script
├── templates/
│   ├── index.html           # Main upload interface
│   ├── results.html         # Search results display
│   └── previous_uploads.html # Previous uploads management
└── static/uploads/          # Directory for uploaded images
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7+
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Krathor2212/CBIR-Multimedia-Database.git
cd CBIR-Multimedia-Database
```

### 2. Install Dependencies

```bash
pip install flask flask-cors psycopg2-binary tensorflow scikit-learn pillow numpy
```

### 3. Database Setup

Create a PostgreSQL database and update the connection details in `models.py`:

```sql
CREATE DATABASE adbpro;

-- Create the images table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(500) NOT NULL,
    features BYTEA NOT NULL,
    caption TEXT
);
```

Update database credentials in `models.py`:
```python
def get_db_connection():
    conn = psycopg2.connect(
        dbname="adbpro", 
        user="your_username", 
        password="your_password",  
        host="localhost", 
        port="5432"
    )
    return conn
```

### 4. Create Upload Directory

```bash
mkdir -p static/uploads
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📊 Dataset Integration

The system supports the Flickr8k dataset for bulk image insertion:

**Dataset**: [Flickr8k on Kaggle](https://www.kaggle.com/datasets/adityajn105/flickr8k)

To use the bulk insertion script:

1. Download and extract the Flickr8k dataset
2. Organize files as:
   ```
   flickr_8k/
   ├── images/          # Image files
   └── captions.txt     # Image captions
   ```
3. Run the insertion script:
   ```bash
   python insert.py
   ```

## 🔧 API Endpoints

### Web Interface
- `GET /` - Main upload page
- `POST /search` - Upload and search for similar images
- `GET /previous-uploads` - View previous uploads

### REST API
- `GET /api/previous-uploads` - Get list of uploaded files (JSON)

## 🧠 How It Works

1. **Feature Extraction**: Images are processed through ResNet50 (pre-trained on ImageNet) to extract 2048-dimensional feature vectors
2. **Database Storage**: Features are stored as binary data in PostgreSQL for efficient retrieval
3. **Similarity Search**: When a query image is uploaded, its features are compared against all stored features using cosine similarity
4. **Result Ranking**: Images are ranked by similarity score and top 80 results are returned

## 📸 Usage

### Web Interface

1. Navigate to `http://localhost:5000`
2. Upload an image using the file picker
3. Click "Search" to find similar images
4. View results with similarity scores
5. Browse previous uploads in the dedicated section

### Programmatic Usage

```python
from models import search_similar_images, add_image_to_db

# Add image to database
add_image_to_db("example.jpg", "/path/to/image.jpg", "Description")

# Search for similar images
results = search_similar_images("/path/to/query/image.jpg")
```

## 🎯 Performance Considerations

- **Feature Extraction**: ResNet50 processing takes ~1-2 seconds per image
- **Search Speed**: Similarity computation is O(n) where n is the number of images in database
- **Memory Usage**: Feature vectors require ~8KB per image in memory
- **Scalability**: For large datasets (>100k images), consider implementing approximate nearest neighbor search


## 🙏 Acknowledgments

- ResNet50 model from TensorFlow/Keras
- Flickr8k dataset contributors
- PostgreSQL community
- Flask framework developers


## 🖼️ Screenshots

### Main Interface
![Main Interface](https://github.com/user-attachments/assets/1ba3e4ee-2a49-47fb-a210-95eb4a45ced4)

### Search Results
![Search Results](https://github.com/user-attachments/assets/a8979132-8ceb-4a12-b537-b7bdbe4b08f6)
