# Data Directory

This directory contains the source documents for The Unofficial NYC Student Guide RAG system.

All files are plain text (.txt) manually compiled from Reddit, student forums, university
student services websites, and MTA/NYC government resources.

| File | Topic |
|------|-------|
| nyc_subway_guide.txt | NYC Subway system: OMNY, MetroCard, express vs local, apps |
| nyc_cheap_eats.txt | Budget food: dollar pizza, halal carts, Trader Joe's, meal prep |
| nyc_housing_guide.txt | Apartments: roommates, no-fee listings, lease basics, tenant rights |
| nyc_student_budget.txt | Money: monthly budget, banking, credit cards, textbooks, taxes |
| nyc_free_activities.txt | Free things: museums, parks, nightlife, study spots |
| nyc_health_wellness.txt | Health: clinics, mental health, fitness, dental, reproductive health |
| nyc_safety_navigation.txt | Safety: scam awareness, street navigation, weather, emergency contacts |
| nyc_academic_campus_life.txt | Academics: office hours, library resources, career services |
| nyc_transportation_guide.txt | Transit: buses, Citi Bike, Uber/Lyft, Staten Island Ferry |
| nyc_international_students.txt | International: F-1 visa, CPT/OPT, banking, cultural adjustment |

## Adding New Documents

1. Save your document as a `.txt` file in this directory.
2. Re-run `python build_database.py` to ingest and embed the new document.
