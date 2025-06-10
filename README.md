<h1 align="center" style="color:#FFFFFF; font-family: 'Arial', sans-serif;">London poperties recommendation system</h1> <p align="left" style="color:#FFFFFF; font-family: 'Verdana', sans-serif;"> <b>Overview: This project involved building a comprehensive dataset by combining property listings from Rightmove with external data sources such as crime statistics, tube station proximity, and local amenities (via various APIs). I used SQL to perform exploratory data analysis and developed a scoring system to identify properties offering affordable rent alongside strong local amenities. The insights were visualised using Power BI, and I built a content-based recommendation system in Python to suggest similar properties based on user preferences.</b>

### Table of contents
- [Business Problem](#business-problem)
- [Introduction](#introduction)
- [Dataset](#dataset)
- [EDA](#eda)
- [Visulisations](#visulisations)
- [Recommendation system](#recommendation-system)
- [Limitations](#limitations)

### Business Problem
Like many young professionals, my friends and I have found it increasingly difficult to find reasonably priced rental properties in London. With rent prices continuing to rise, there's a growing need for smarter tools to assist in the property search. This project aims to help users identify semi-affordable places to live by factoring in not just price, but also proximity to tube stations, local crime rates, and nearby amenities such as gyms and shops.

### Introduction
Finding affordable and livable rental properties in London is a challenge for many young professionals. This project tackles that issue by building a recommendation system that combines Rightmove listings with external data on crime rates, tube proximity, and local amenities.

After performing exploratory data analysis in SQL and creating a scoring system to rank properties by affordability and convenience, I visualised the insights using Power BI. A content-based filtering system in Python then recommends properties based on user preferences, helping renters make smarter, data-informed decisions.

### Dataset
This dataset was primarily built by scraping Rightmove for London property listings. Using Google’s APIs, I retrieved postcodes for many of the properties, which enabled integration with additional data sources. The UK Police API provided local crime statistics, the Transport for London API identified the nearest tube stations, and another Google API was used to locate nearby amenities such as gyms and shops.

### EDA
Using SQL, I developed a custom scoring system to evaluate each property based on key factors that impact livability. By applying weighted values to features such as price per room, proximity to the nearest tube station, and local crime rates, the system generates a composite score for every listing. This allowed for a more balanced comparison of properties, helping identify those that offer the best value in both cost and convenience.

### Visulisations
In Power BI, I created a heatmap to visually highlight the most and least affordable areas to live in London, offering an at-a-glance view of rental price distribution across the city. Additional visualisations were developed to explore how rental prices vary with proximity to tube stations and how they are influenced by local crime rates, providing deeper insights into the factors that affect housing costs.

### Recomendation system
To help users discover similar properties based on their preferences, I developed a content-based recommendation system using Flask and Python. The system combines text similarity from property descriptions (using TF-IDF and cosine similarity) with numerical similarity based on price and number of bedrooms (using scaled Euclidean distance). A weighted score blends these two components to generate personalized property recommendations. Users can receive suggestions by submitting a property_id, and the API returns a list of similar listings with key details such as address, price, and description. Additionally, a search endpoint allows filtering based on user-defined criteria like price range, number of bedrooms, distance to tube stations, and nearby amenities.

### Limitations
While the recommendation system provides useful insights, there are several limitations to consider:

Data Accuracy & Completeness: The dataset relies on property listings scraped from Rightmove and external APIs. Some entries may have missing or outdated information, which could impact the quality of recommendations.

Static Data: The data snapshot is not updated in real time. Property availability, prices, and crime rates may change frequently, so the recommendations may not reflect the latest market conditions.

Limited Feature Scope: The scoring and similarity model currently use only a subset of available features—price, bedrooms, description text, and proximity to tube stations. Other important factors like property condition, lease terms, or energy efficiency are not included.

Basic Weighting System: The weights used to combine textual and numerical similarity are fixed and not user-adjustable. This may not accurately reflect all users’ preferences or priorities.

Scalability: The recommendation system processes everything in-memory, which may not scale efficiently with very large datasets or high traffic without further optimization.
