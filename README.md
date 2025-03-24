# A-B_Testing_Fast_Food_marketing_Campaign

## Overview
This project analyzes the effectiveness of two different marketing promotions for a new menu item at a fast-food chain. The analysis compares sales performance between two promotion types to determine which generates higher sales across multiple store locations.

## Problem Statement
Which of the two marketing promotions (Promotion 1 or Promotion 2) generates higher sales for a new menu item, as measured by weekly sales in thousands of dollars, across store locations over a four-week test period?

## Dataset
The dataset (Dataset.csv) contains the following information:
  * Promotion: Type of promotion (1 or 2)
  * MarketSize: Size of the market (Small, Medium, Large)
  * AgeOfStore: Age of the store in years
  * AgeGroup: Categorized age groups ('0-5 years', '6-10 years', '11-15 years', '16+ years')
  * SalesInThousands: Sales of the new menu item in thousands of dollars
  * week: Week of the promotion (1-4)

## Methodology
### Experiment Design

1) Stores were randomly assigned to two test groups:
  * Control Group: Stores implementing Promotion 1
  * Treatment Group: Stores implementing Promotion 2

2) Sales were tracked over a four-week period
3) Each location implemented only one promotion type throughout the test period


## Hypothesis Testing

* Null Hypothesis (H₀): No significant difference in average sales between Control and Treatment groups
* Alternative Hypothesis (H₁): Significant difference in average sales between Control and Treatment groups
* Significance Level: 95% confidence (α = 0.05)

## Statistical Analysis
The following statistical methods were employed:

1) Normality Testing: Shapiro-Wilk test to check if data follows normal distribution
2) Homogeneity of Variance: Levene's test to check if groups have equal variances
3) Non-parametric Testing: Mann-Whitney U test (since normality assumptions weren't met)
4) Effect Size Calculation: Cohen's d to measure practical significance
5) Segmentation Analysis: Sales comparison across different market sizes and store age groups
6) Interaction Effects: ANOVA to analyze interactions between promotion type and store characteristics


## Key Findings

* Promotion 1 significantly outperforms Promotion 2 (p-value < 0.005)
* Average sales for Control group (Promotion 1): $58.10k
* Average sales for Treatment group (Promotion 2): $47.33k
* Absolute difference: $10.77k (22.75% improvement with Promotion 1)
* Effect size (Cohen's d = 0.68): Moderate to large practical significance
* Promotion 1 outperformed Promotion 2 across all market sizes, with largest advantage in Large markets (+$14.91k)
* Promotion 1 outperformed Promotion 2 in most age groups, with largest advantage in newer stores (0-5 years, +$17.11k)
* For stores aged 11-15 years, Promotion 2 performed slightly better (-$1.88k)
* The sales gap between promotions widened over time, with largest difference in Week 4

## Recommendations

1) Implement Promotion 1 for the new menu item across most locations
2) Prioritize Large markets where Promotion 1 showed strongest advantage
3) Focus on newer stores (0-5 years) where impact was highest
4) Consider Promotion 2 for stores in the 11-15 year age range
5) Monitor performance over time to ensure consistent results

