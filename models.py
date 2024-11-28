import os
import numpy as np
import psycopg2
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
import io

def get_db_connection():
    conn = psycopg2.connect(
        dbname="adbpro", 
        user="postgres", 
        password="1234",  
        host="localhost", 
        port="5432"
    )
    return conn

model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_features(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()

def add_image_to_db(image_name, image_path, caption):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM images WHERE name = %s AND path = %s", (image_name, image_path))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Image {image_name} already exists in the database")
    else:
        features = extract_features(image_path)
        try:
            cursor.execute("""
                INSERT INTO images (name, path, features, caption)
                VALUES (%s, %s, %s, %s)
            """, (image_name, image_path, psycopg2.Binary(features), caption))
            conn.commit()
            print(f"Inserted {image_name} into the database")
        except Exception as e:
            print(f"Error inserting {image_name}: {e}")
            conn.rollback()

    cursor.close()
    conn.close()

def load_images_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, path, features FROM images")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    image_data = []
    for row in rows:
        image_data.append({
            "id": row[0],
            "name": row[1],
            "path": row[2],
            "feature": np.frombuffer(row[3], dtype=np.float32),
        })
    return image_data

def search_similar_images(query_image_path):
    images = load_images_from_db()
    query_feature = extract_features(query_image_path)
    similarities = []
    for img in images:
        similarity = cosine_similarity([query_feature], [img['feature']])
        similarities.append((similarity[0][0], img))
    similarities.sort(key=lambda x: x[0], reverse=True)
    results = []
    print(len(similarities))
    for i in range(80):
        score, img = similarities[i]
        results.append({
            "name": img['name'],
            "path": img['path'],
            "score": score
        })
    return results
