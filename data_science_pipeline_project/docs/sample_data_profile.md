# Sample Data Profile

Date: 2026-06-18
Project: data_science_pipeline_project
Source file: data/stylesense_reviews.csv

## Purpose

This document tracks the current sample dataset used by the StyleSense pipeline and provides a reproducible refresh process.

## Refresh Command

```bash
cd data_science_pipeline_project
python -c "from pathlib import Path; from data_generation import generate_stylesense_dataset, save_dataset; df=generate_stylesense_dataset(n_samples=1000, random_state=42); save_dataset(df, Path('data/stylesense_reviews.csv'))"
```

## Current Dataset Snapshot

- Rows: 1000
- Columns: age, category, price_range, rating, review_text, recommend
- Missing values (total): 0
- Recommendation rate: 0.534

### Category Distribution

- Pants: 180
- Shoes: 174
- Dresses: 170
- Tops: 166
- Accessories: 166
- Outerwear: 144

### Price Range Distribution

- Mid-Range: 270
- Luxury: 254
- Budget: 247
- Premium: 229

### Rating Distribution

- 1: 199
- 2: 176
- 3: 204
- 4: 212
- 5: 209

## Notes

- The sample data is synthetic and deterministic when using `random_state=42`.
- The dataset schema aligns with preprocessing and model training code in this project.
