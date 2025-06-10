from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, euclidean_distances
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    username='root',
    password='James@0405',
    database='london_properties'
)

cursor = db.cursor(dictionary=True)

query = "SELECT * FROM properties"
df_properties = pd.read_sql(query, db)

# Save original values before scaling
original_prices = df_properties['price']
original_bedrooms = df_properties['bedrooms']

# Apply scaling to 'price' and 'bedrooms' for similarity calculation
scaler = StandardScaler()
df_properties[['price', 'bedrooms']] = scaler.fit_transform(df_properties[['price', 'bedrooms']])

# Create tfidfvectorizer
tfidf = TfidfVectorizer(stop_words='english', max_features=15)
tfidf_matrix = tfidf.fit_transform(df_properties['description'])

# Calculate cosine similarity with itself
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Calculate euclidean distance for price and bedrooms
price_bedrooms_matrix = df_properties[['price', 'bedrooms']].values
price_bedrooms_similarity = euclidean_distances(price_bedrooms_matrix)
price_bedrooms_similarity = 1 / (1 + price_bedrooms_similarity)

# Create indices variable
indices = pd.Series(df_properties.index, index=df_properties['property_id']).drop_duplicates()

def combined_sim_score(idx):
    text_sim = cosine_sim[idx]
    price_bedrooms_sim = price_bedrooms_similarity[idx]

    combined_sim = 0.5 * text_sim + 0.5 * price_bedrooms_sim
    return combined_sim

# Recommendation function
def recommendation_system(property_id, cosine_sim=cosine_sim, num_recommended=5):
    if property_id not in indices:
        print(f"Property ID {property_id} not found in indices")  # Debugging line
        return []

    idx = indices[property_id]  # Get index of property
    sim_scores = list(enumerate(combined_sim_score(idx)))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_sim = sim_scores[1:num_recommended+1]  # Exclude first (it's the same property)
    property_indices = [i[0] for i in top_sim]

    recommended_properties =  df_properties.iloc[property_indices].copy()

    # Apply inverse transform to both 'price' and 'bedrooms'
    recommended_properties[['price', 'bedrooms']] = scaler.inverse_transform(recommended_properties[['price', 'bedrooms']])

    return recommended_properties[['property_id', 'address', 'price', 'bedrooms', 'description']].to_dict(orient="records")


@app.route("/recommendations", methods=['POST'])
def recommend_properties():
    data = request.json
    property_id = data.get('property_id')

    if property_id is None:
        return jsonify("Property_id is required"), 400
    
    recommendations = recommendation_system(property_id)

    if not recommendations:
        return jsonify(f'No properties closely related to {property_id}')
    
    return jsonify(recommendations)


@app.route("/search", methods=['POST'])
def search_properties():
    user_prefs = request.json

    query = """
    SELECT p.*, t.distance as tube_distance, c.crime_count as crime_count, a.gym, a.park, a.shop 
    FROM properties p 
    JOIN tubes t ON p.property_id = t.property_id
    JOIN crime c ON p.property_id = c.property_id
    JOIN amenities a ON p.property_id = a.property_id
    WHERE 1=1
    """
    params = []

    if user_prefs['min_rooms']:
        query += " AND p.bedrooms >= %s"
        params.append(user_prefs['min_rooms'])
    
    if user_prefs['max_rooms']:
        query += " AND p.bedrooms <= %s"
        params.append(user_prefs['max_rooms'])

    if user_prefs['min_price']:
        query += " AND p.price >= %s"
        params.append(user_prefs['min_price'])

    if user_prefs['max_price']:
        query += " AND p.price <= %s"
        params.append(user_prefs['max_price'])
    
    if user_prefs['tube_distance']:
        query += " AND t.distance <= %s"
        params.append(user_prefs['tube_distance'])

    cursor.execute(query, params)
    results = cursor.fetchall()

    return jsonify(results)

@app.route("/", methods=['GET'])
def home():
    return "Flask is working!", 200

if __name__ == "__main__":
    app.run(debug=True)
