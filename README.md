Introduction:
-------------
This project is my attempt to combine two things I enjoy: exploring data and understanding the trends of real-world decisions. Starbucks is something we all love and start our day with, I was curious of why we love it so much? what is increasing their sales, etc. hence wanted to dive into its data and uncover insights. Therefore, this project - "The Starbucks Analytics Dashboard" is an interactive tool built to analyze customer behaviors, menu offerings, and store locations. 

Why This Project?
-----------------
As someone exploring the field of data analytics, I wanted to challenge myself with a project that’s both insightful and practical. Starbucks provides a wealth of publicly available data (Kaggle) on its menu, store locations, and customer offers, making it a great use case to:
1. Understand customer preferences and behaviors.
2. Analyze menu trends to suggest improvements.
3. Explore global store locations and identify expansion opportunities.
This isn’t just a project; it’s my story of learning, experimenting, and growing as a budding data analyst.

Tools Used:
-----------
1. Python: For data cleaning, transformation, and analysis.
2. Dash and Plotly: To create interactive visualizations.
3. Pandas: For data handling and preprocessing.
4. Render: For deployment to make the dashboard accessible online.
   
WorkFlow:
---------
1. Data Collection -
   I worked with three datasets:
      - Portfolio Dataset: Customer offers and segmentation.
      - Menu Dataset: Nutritional information for Starbucks menu items.
      - Directory Dataset: Global store locations.
        
2. Data Cleaning & Transformation -
   - Filled missing values.
   - Ensured consistency in columns like latitude and longitude.
   - Prepped the data for visualizations.
   - Problems Faced :
     ---------------
      - Missing columns in datasets (e.g., latitude and longitude).
      - Duplicate column names (Latitude vs latitude, etc.).
      - Data type mismatches causing preprocessing errors.
   - Solution:
     ---------
   Added a robust preprocessing pipeline to:
      - Handle missing columns and provide default values.
      - Convert data types (e.g., latitude and longitude) to numeric.
      - Deduplicate and validate column names.
      - Fill missing values with mean or default values.
     
4. Exploratory Data Analysis (EDA) -
   - Performed EDA to identify trends and insights.
   - Created visualizations for calorie distributions, customer clusters, and global heatmaps.

5. Dashboard Development
   - Tabs in the Dashboard:

      Customer Segmentation:
     ------------------------
      - Built an interactive scatter plot to analyze customer behavior based on clusters.
      - Users can filter data by clusters using a dropdown.
        
      Menu Optimization:
      ------------------
      - Created a histogram to show calorie distribution across menu items.
      - Added a range slider to filter calorie levels dynamically.
     
      Store Location Optimization:
      ----------------------------
      - Developed a global heatmap using Plotly Density Mapbox to visualize store density worldwide.
      - Interactive updates with a button for heatmap refresh.

   - Deployed the project on Render for live access [ https://dashboard.render.com/web/srv-ctjopt1opnds73fqj23 ---> https://starbucksanalysis-9.onrender.com/ ]

How to Explore the Dashboard:
----------------------------
1. Live Dashboard
   Visit the live dashboard here: [ https://dashboard.render.com/web/srv-ctjopt1opnds73fqj23 ---> https://starbucksanalysis-9.onrender.com/ ]
   
2. Run Locally
   - Clone the repository:
      git clone https://github.com/your-username/StarbucksAnalyticsDashboard.git
      cd StarbucksAnalyticsDashboard
   - Install dependencies:
      pip install -r requirements.txt
     
4. Run the app:
   - python app_py.py

Key Findings:
-------------
- Customer Insights:
   - Cluster-based segmentation highlighted differences in customer reward preferences, task difficulty, and engagement duration.
   - Reward-oriented customers showed higher engagement with challenging offers.
- Menu Optimization:
   - Majority of menu items are clustered in the lower calorie range, with peaks around 100–150 calories.
   - Opportunities exist to introduce mid-range calorie beverages for balance.
- Store Location Optimization:
   - Heatmap revealed store density in North America, Europe, and East Asia.
   - Sparse store presence in regions like Africa and South America indicates potential for expansion.

Live: https://starbucksanalysis-9.onrender.com 

Conclusion:
-----------
The dashboard is now live and serves as:
   - A decision-making tool for analyzing customer preferences, menu optimization strategies, and global store distributions.
   - A showcase of interactive data visualization and analytical skills.
 
