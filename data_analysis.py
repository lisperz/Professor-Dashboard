import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pymongo import MongoClient, errors

# ---------------------------
# 1. Data Loading from MongoDB
# ---------------------------
try:
    client = MongoClient("mongodb://127.0.0.1:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # Check connection
    db = client["professor_dashboard"]  # Database name
    collection = db["professors"]         # Collection name
    print("Connected to MongoDB successfully.")
except errors.ServerSelectionTimeoutError as err:
    print("Failed to connect to MongoDB:", err)
    raise err

# Fetch data from the 'professors' collection, excluding the '_id' field
data = list(collection.find({}, {"_id": 0}))
if not data:
    print("No data found in MongoDB.")
else:
    print("Data loaded successfully from MongoDB:")
    print(data)

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(data)
print("\nDataFrame head:")
print(df.head())

# ---------------------------
# 2. Data Exploration and Analysis
# ---------------------------

# Example analysis: count the number of professors per department
dept_counts = df['department'].value_counts()
print("\nProfessor count by department:")
print(dept_counts)

# Compute additional statistics, such as the length of professor names (for example only)
df['name_length'] = df['name'].apply(len)
name_stats = df['name_length'].describe()
print("\nName length statistics:")
print(name_stats)

# ---------------------------
# 3. Data Visualization
# ---------------------------

# Plot a bar chart for professor count by department
plt.figure(figsize=(8, 6))
dept_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Professors by Department')
plt.xlabel('Department')
plt.ylabel('Count')
plt.tight_layout()
# Save the chart as an image file
bar_chart_path = 'department_counts.png'
plt.savefig(bar_chart_path)
plt.close()

# Plot a histogram for the distribution of professor name lengths
plt.figure(figsize=(8, 6))
df['name_length'].plot(kind='hist', bins=10, color='lightgreen')
plt.title('Distribution of Professor Name Lengths')
plt.xlabel('Name Length')
plt.ylabel('Frequency')
plt.tight_layout()
hist_chart_path = 'name_length_distribution.png'
plt.savefig(hist_chart_path)
plt.close()

print("\nCharts saved:", bar_chart_path, hist_chart_path)

# ---------------------------
# 4. Generate PDF Report
# ---------------------------

def generate_pdf_report(output_path, dept_counts, name_stats, bar_chart, hist_chart):
    """
    :param output_path: The output PDF file path
    :param dept_counts: A pd.Series-like object (department statistics)
    :param name_stats: A pd.Series-like object (name length statistics)
    :param bar_chart:   The file path of the department bar chart
    :param hist_chart:  The file path of the name length histogram
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Set margins and line spacing
    margin_left = 50
    margin_top = 50
    line_spacing = 16  # Line spacing
    
    # Calculate the initial text coordinate
    current_y = height - margin_top

    # -------------------------
    # 1. Report Title
    # -------------------------
    c.setFont("Helvetica-Bold", 18)
    title = "Professor Data Analysis Report"
    c.drawCentredString(width / 2, current_y, title)
    current_y -= 2 * line_spacing  # Move down a bit

    # -------------------------
    # 2. Department Statistics
    # -------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, current_y, "Department Counts:")
    current_y -= line_spacing

    c.setFont("Helvetica", 12)
    for dept, count in dept_counts.items():
        line_text = f"  {dept}: {count}"
        c.drawString(margin_left, current_y, line_text)
        current_y -= line_spacing

    current_y -= line_spacing  # Blank line

    # -------------------------
    # 3. Name Length Statistics
    # -------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, current_y, "Name Length Statistics:")
    current_y -= line_spacing

    c.setFont("Helvetica", 12)
    for stat in name_stats.index:
        val = name_stats[stat]
        # Display only two decimal places
        line_text = f"  {stat}: {val:.2f}"
        c.drawString(margin_left, current_y, line_text)
        current_y -= line_spacing

    current_y -= 2 * line_spacing  # Additional space before charts

    # -------------------------
    # 4. Insert Charts (side by side)
    # -------------------------
    # Set the size for each chart
    chart_width = 2.5 * inch   # Approximately 180 px
    chart_height = 2.0 * inch  # Approximately 144 px

    # Place the first chart (bar_chart) on the left
    c.drawImage(
        bar_chart,
        margin_left,
        current_y - chart_height,  # y-coordinate for the bottom left of the image
        width=chart_width,
        height=chart_height,
        preserveAspectRatio=True
    )
    # Label under the image
    c.setFont("Helvetica", 10)
    c.drawString(margin_left, current_y - chart_height - line_spacing,
                 "Figure 1: Professors by Department")

    # Place the second chart (hist_chart) on the right
    x_for_second_chart = margin_left + chart_width + inch  # 1 inch gap
    c.drawImage(
        hist_chart,
        x_for_second_chart,
        current_y - chart_height,
        width=chart_width,
        height=chart_height,
        preserveAspectRatio=True
    )
    c.drawString(x_for_second_chart, current_y - chart_height - line_spacing,
                 "Figure 2: Name Length Distribution")

    # Adjust current_y for the next content (if needed)
    current_y -= (chart_height + 2 * line_spacing)

    # -------------------------
    # 5. Finish and Save
    # -------------------------
    c.showPage()
    c.save()
    print(f"PDF report generated: {output_path}")

# Generate PDF report
pdf_report_path = "Professor_Data_Analysis_Report.pdf"
generate_pdf_report(
    pdf_report_path,
    dept_counts,    # pd.Series
    name_stats,     # pd.Series
    bar_chart_path, # Path of bar chart
    hist_chart_path # Path of histogram
)
