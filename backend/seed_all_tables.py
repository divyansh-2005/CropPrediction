import os
import pandas as pd
from app import app, db
from app.module.models import crop_details, crop_name_info, msp_details, rain_info

# Path to your CSV file
csv_path = os.path.join('static', 'csvfile')
df = pd.read_csv(csv_path)

with app.app_context():
    # Seed crop_details
    crop_features = df.groupby('crop').agg({
        'n': 'mean',
        'p': 'mean',
        'k': 'mean',
        'temperature': 'mean',
        'humidity': 'mean',
        'ph': 'mean',
        'rainfall': 'mean'
    }).reset_index()
    for _, row in crop_features.iterrows():
        crop = row['crop'].lower()
        exists = crop_details.query.filter_by(crop=crop).first()
        if not exists:
            entry = crop_details(
                crop=crop,
                n=row['n'],
                p=row['p'],
                k=row['k'],
                temperature=row['temperature'],
                humidity=row['humidity'],
                ph=row['ph'],
                rainfall=row['rainfall']
            )
            db.session.add(entry)
    db.session.commit()
    print('crop_details table populated.')

    # Seed crop_name_info
    for crop in df['crop'].unique():
        crop = crop.lower()
        exists = crop_name_info.query.filter_by(recommendation_name=crop).first()
        if not exists:
            entry = crop_name_info(
                recommendation_name=crop,
                production_name=crop
            )
            db.session.add(entry)
    db.session.commit()
    print('crop_name_info table populated.')

    # Seed msp_details (dummy data)
    for crop in df['crop'].unique():
        crop = crop.lower()
        exists = msp_details.query.filter_by(crop=crop).first()
        if not exists:
            entry = msp_details(
                crop=crop,
                year2010=1000,
                year2011=1100,
                year2012=1200,
                year2013=1300,
                year2014=1400,
                year2015=1500,
                year2016=1600,
                year2017=1700,
                year2018=1800,
                year2019=1900,
                year2020=2000,
                year2021=2100
            )
            db.session.add(entry)
    db.session.commit()
    print('msp_details table populated.')

    # Seed rain_info (dummy data for one state)
    exists = rain_info.query.filter_by(state='gujarat').first()
    if not exists:
        entry = rain_info(
            state='gujarat',
            january=10, february=10, march=10, april=10, may=10, june=10,
            july=10, august=10, september=10, october=10, november=10, december=10
        )
        db.session.add(entry)
        db.session.commit()
        print('rain_info table populated.')

print('All tables seeded.')
