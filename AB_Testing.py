import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, mannwhitneyu
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Set page title and configuration
st.set_page_config(page_title="A/B Testing Analysis: Promotion Effectiveness", layout="wide")

st.title("A/B Testing Fast Food Marketing Campaigns")
st.write("This analysis compares two different promotion types and their impact on sales.")

# Data loading
@st.cache_data
def load_data():
    df = pd.read_csv('Dataset.csv')
    age_bins = [0, 5, 10, 15, float('inf')]
    age_labels = ['0-5 years', '6-10 years', '11-15 years', '16+ years']
    df['AgeGroup'] = pd.cut(df['AgeOfStore'], bins=age_bins, labels=age_labels)
    if 'Unnamed: 0' in df.columns:
        df.drop(axis=1, columns='Unnamed: 0', inplace=True)
    return df

df = load_data()

# Add sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Exploratory Analysis", "Statistical Testing", "Conclusion"])

if page == "Overview":
    st.header("Overview")
    st.markdown(""" A fast-food chain plans to add a new item to its menu. However, they are still undecided between two possible marketing campaigns for promoting the new product. In order to determine which promotion has the greatest effect on sales, the new item is introduced at locations in several randomly selected markets. A different promotion is used at each location, and the weekly sales of the new item are recorded for the first four weeks. """)
    st.subheader("Problem Statement")
    st.markdown(""" Which of the two marketing promotions (Promotion 1 or Promotion 2) generates higher sales for our new menu item, as measured by weekly sales in thousands of dollars, across our store locations over a four-week test period?""")
    st.subheader("Primary Success Metric")
    st.write(" Average sales of new menu item in thousands of dollars")
    st.subheader('Experiment Design')
    st.markdown("""
    * Both promotions will be tested simultaneously across multiple store locations
    * Stores assigned Promotion 1 will be considered as Control Group. Stroes assigned Promotion 2 will be considered Treatment Group
    * Stores have been randomly assigned to Control group and Treamtment group based on factors such as Market Size and Age of Store 
    * Sales will be tracked over a four-week period
    * Each location will implement only one promotion type throughout the test period            
    """)
    st.subheader("Hypothesis")
    st.markdown("""
    * Null Hypothesis (H₀): There is no significant difference in average sales (SalesInThousands) between Control group and Treatment group.
    * Alternative Hypothesis (H₁): There is a significant difference in average sales (SalesInThousands) between Control group and Treatment group.
    """)
    st.subheader("Decision Criteria")
    st.markdown("""
    1) Statistical significance will be evaluated at the 95% confidence level (α = 0.05)
    2) If a statistically significant difference exists, the promotion with higher mean sales will be selected
    3) Segmentation analysis will be conducted to determine if the Treatment group's promotion effectiveness varies by market size or store age
    """)

    

elif page == "Exploratory Analysis":
    st.header("Exploratory Data Analysis")
    
    st.write("First few rows of the dataset:")
    st.dataframe(df.head())
    
    st.write("Data summary:")
    st.dataframe(df.describe())
    
    st.subheader("Promotion distribution:")
    fig, ax = plt.subplots(figsize=(10,6))
    df['Promotion'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Sales distribution by promotion
    st.subheader("Sales Distribution by Promotion Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='SalesInThousands', hue='Promotion', kde=True, ax=ax)
    st.pyplot(fig)
    
    # Bar chart of average sales by promotion
    st.subheader("Average Sales by Promotion Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Promotion', y='SalesInThousands', data=df, ax=ax)
    st.pyplot(fig)

    # Weekly sales trend by promotion
    st.subheader("Weekly Sales Trend by Promotion Type")
    fig,ax =plt.subplots(figsize=(10,6))
    Weekly_sales=pd.DataFrame(df.groupby(['week','Promotion'])['SalesInThousands'].sum())
    Weekly_sales=Weekly_sales.reset_index()
    for promo in Weekly_sales['Promotion'].unique():
        promo_data=Weekly_sales[Weekly_sales['Promotion']==promo]
        plt.plot(promo_data['week'],promo_data['SalesInThousands'],marker='o',label=f'Promotion {promo}')
    plt.xlabel('Week')
    plt.ylabel('Sales in Thousands')
    plt.legend()
    st.pyplot(fig)
    
    # Sales by market size and promotion
    st.subheader("Sales by Market Size and Promotion Type")
    df['Promotion_str'] = df['Promotion'].astype(str)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='MarketSize', y='SalesInThousands', hue='Promotion_str', data=df, ax=ax)
    st.pyplot(fig)

elif page == "Statistical Testing":
    st.header("Statistical Analysis")
    
    # Show test assumptions
    st.subheader("Testing for Normality Assumptions and Homogenity of Variance")
    
    # Calculate test assumptions
    promo1_data = df[df['Promotion'] == 1]
    promo2_data = df[df['Promotion'] == 2]
    
    s1 = shapiro(promo1_data['SalesInThousands'])
    s2 = shapiro(promo2_data['SalesInThousands'])
    levene_test = levene(promo1_data['SalesInThousands'], promo2_data['SalesInThousands'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Control Group Normality (p-value)", f"{s1[1]:.6f}", "Passes Normality Assumption" if s1[1] > 0.05 else "Fails Normality Assumption")
        st.metric("Treatment Group Normality (p-value)", f"{s2[1]:.6f}", "Passes Normality Assumption" if s2[1] > 0.05 else "Fails Normality Assumption")
    
    with col2:
        st.metric("Equal Variance (p-value)", f"{levene_test[1]:.6f}", "Passes Variance Assumtion" if levene_test[1] > 0.05 else "Fails Variance Assumption")
        both_normal = s1[1] > 0.05 and s2[1] > 0.05
        st.metric("Normality Condition", "Satisfied" if both_normal else "Not Satisfied")
    
    st.write("Since normality condition is not satisfied, we'll use non-parametric Mann-Whitney U test.")
    
    # Mann-Whitney U test
    test_stat, p_value = mannwhitneyu(promo1_data['SalesInThousands'], promo2_data['SalesInThousands'], alternative='two-sided')
    
    st.subheader("Mann-Whitney U Test Results")
    st.metric("Test Statistic", f"{test_stat:.2f}")
    st.metric("p-value", f"{p_value:.10f}", "Statistically Significant" if p_value < 0.05 else "Not Significant")
    
    if p_value < 0.05:
        st.success("The distribution of sales for Control Group and Treatment Group are significantly different.")
        
    # Effect size calculation
    n1 = len(promo1_data)
    n2 = len(promo2_data)
    mean_1, mean_2 = promo1_data['SalesInThousands'].mean(), promo2_data['SalesInThousands'].mean()
    var_1, var_2 = promo1_data['SalesInThousands'].var(), promo2_data['SalesInThousands'].var()
    pooled_sd = np.sqrt(((n1 - 1) * var_1 + (n2 - 1) * var_2) / (n1 + n2 - 2))
    effect_size = (mean_1 - mean_2) / pooled_sd
    
    st.subheader("Practical Significance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Control Group Mean Sales", f"{mean_1:.2f}")
        st.metric("Treatment Group Mean Sales", f"{mean_2:.2f}")
    
    with col2:
        st.metric("Mean Difference", f"{mean_1 - mean_2:.2f}")
        st.metric("Effect Size (Cohen's d)", f"{effect_size:.2f}", 
                  "Large" if effect_size > 0.8 else "Medium" if effect_size > 0.5 else "Small")

    st.subheader("Analysis by segement")
        
    # Aanalysis by Segemnt
    def analyze_by_segment(df, segment_column):
    
        # Group by segment and promotion
        grouped = df.groupby([segment_column, 'Promotion'])['SalesInThousands'].agg(['count', 'mean', 'std'])
        grouped = grouped.reset_index()
        
        # Reshape to have promotions as columns
        pivot_table = grouped.pivot_table(
            index=segment_column, 
            columns='Promotion', 
            values=['count', 'mean', 'std']
        )
        
        # Calculate the difference and percentage difference
        segemnt_results = pd.DataFrame()
        segemnt_results[segment_column] = pivot_table.index
        segemnt_results['Control_Group_count'] = pivot_table[('count', 1)].values
        segemnt_results['Treatment_Group_count'] = pivot_table[('count', 2)].values
        segemnt_results['Control_Group_mean'] = pivot_table[('mean', 1)].values
        segemnt_results['Treatment_Group_mean'] = pivot_table[('mean', 2)].values
        segemnt_results['difference'] = segemnt_results['Control_Group_mean'] - segemnt_results['Treatment_Group_mean']
        segemnt_results['percent_diff'] = (segemnt_results['difference'] / segemnt_results['Treatment_Group_mean']) * 100
        
        # Print segment results summary
        for _, row in segemnt_results.iterrows():
            segment = row[segment_column]
            diff = row['difference']
            pct = row['percent_diff']
            p1_mean = row['Control_Group_mean']
            p2_mean = row['Treatment_Group_mean']
            
            print(f"  {segment}: Control Group (${p1_mean:.2f}k) vs Treatment Group (${p2_mean:.2f}k) - Diff: ${diff:.2f}k ({pct:.2f}%)")
        
        st.dataframe(segemnt_results)
    
    st.markdown(""" * MarketSize Analysis""")
    analyze_by_segment(df,'MarketSize')

    st.markdown(""" * AgeGroup Analysis""")
    analyze_by_segment(df,'AgeGroup')

    # Interaction Effects
    
    st.subheader("Interaction Effects")
    def interaction_effects():
       
        # Promotion Model
        model1 = ols('SalesInThousands ~ C(Promotion)', data=df).fit()
        st.markdown(""" * Sales(in thousands) ~ Promotion""") 
        st.write(sm.stats.anova_lm(model1,typ=2))

        # 2. Promotion and MarketSize model
        model2 = ols('SalesInThousands ~ C(Promotion) + C(MarketSize)', data=df).fit()
        st.markdown(""" * Sales(in thousands) ~ Promotion + MarketSize""")
        st.write(sm.stats.anova_lm(model2,typ=2)) 

        # 3. Promotion, MarketSize and their interaction
        model3 = ols('SalesInThousands ~ C(Promotion) * C(MarketSize)', data=df).fit()
        st.markdown(""" * Sales(in thousands) ~ Promotion * MarketSize""")
        st.write(sm.stats.anova_lm(model3,typ=2)) 

        # 4. Promotion and AgeGroup model
        model4 = ols('SalesInThousands ~ C(Promotion) + C(AgeGroup)', data=df).fit()
        st.markdown(""" * Sales(in thousands) ~ Promotion + AgeGroup""")
        st.write(sm.stats.anova_lm(model4,typ=2)) 

        # 5. Promotion, AgeGroup and their interaction
        model5 = ols('SalesInThousands ~ C(Promotion) * C(AgeGroup)', data=df).fit()
        st.markdown(""" * Sales(in thousands) ~ Promotion * AgeGroup""")
        st.write(sm.stats.anova_lm(model5,typ=2)) 

    
    interaction_effects()



elif page == "Conclusion":
    st.header("Conclusion")
    
    st.write("""
    ### Key Findings:
    
    * Promotion 1 significantly outperforms Promotion 2 with a p-value < 0.005
    * Average sales for Control group (stores with Promotion 1) is $58.10k
    * Average sales for Treatment group (stores with Promotion 2) is $47.33k 
    * This represents a $10.77k absolute increase or 22.75% improvement with Promotion 1
    * The effect size (Cohen's d = 0.68) indicates a moderate to large practical significance
    * Promotion 1 outperformed Promotion 2 across all market sizes, the advantage was largest in Large markets (+$14.91k difference)
    * Promotion 1 outperformed Promotion 2 in most age groups, the largest advantage was in newer stores (0-5 years) with a $17.11k difference
    * Interestingly, for stores aged 11-15 years, Promotion 2 performed slightly better (-$1.88k difference)
    * Promotion 1 consistently outperformed Promotion 2 across all four weeks, the gap between promotions widened over time, with the largest difference in Week 4 ($12.16k)
    
    
    
    ### Recommendation:
    
    1) Implement Promotion 1 for the new menu item across most locations
    2) Prioritize Large markets where Promotion 1 showed the strongest advantage (+$14.91k)
    3) Focus especially on newer stores (0-5 years) where the impact was highest (+$17.11k)
    4) For stores in the 11-15 year age range, consider Promotion 2 as its performance was slightly better comapred to Promotion 1
    5) Monitor performance over time to ensure the promotion advantage remains consistent
    """)
    
    # Summary metrics
    promo1_data = df[df['Promotion'] == 1]
    promo2_data = df[df['Promotion'] == 2]
    mean_1, mean_2 = promo1_data['SalesInThousands'].mean(), promo2_data['SalesInThousands'].mean()
    
    st.subheader("Summary Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Promotion 1 Avg Sales", f"${mean_1:.2f}K")
    with col2:
        st.metric("Promotion 2 Avg Sales", f"${mean_2:.2f}K")
    with col3:
        st.metric("Sales Lift from Promotion 1", f"{((mean_1/mean_2)-1)*100:.1f}%", 
                  f"${mean_1-mean_2:.2f}K")
