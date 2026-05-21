import csv
import re
import glob
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Month lookup table used by the site's header element
MONTH_LOOKUP = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def detect_cycle_month(soup):
    """Finds the active billing month text from the page header element."""
    selected_month = soup.select_one('h6[class*="1bcwr2w"]')
    if selected_month:
        label = selected_month.get_text(strip=True)
        return MONTH_LOOKUP.get(label, datetime.now().month)
    return datetime.now().month

def detect_year(all_p):
    """Scans paragraph elements for a full date format to capture the year."""
    current_year = datetime.now().year
    for tag in all_p:
        found = re.search(r'\d{1,2}/\d{1,2}/(\d{4})', tag.get_text())
        if found:
            return int(found.group(1))
    return current_year

def process_file(file_path):
    """Processes a single file anchoring data forward from the detected 17th cycle start."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. Get Total Usage
    total_gb = 459.0
    all_p = soup.find_all('p')
    for i, p in enumerate(all_p):
        if 'Total Data Usage' in p.text:
            try:
                total_gb = float(all_p[i + 1].text.replace('GB', '').strip())
                break
            except: 
                pass

    # 2. Get Bar Heights
    bars = soup.find_all('rect', class_='MuiBarElement-series-y_0')
    heights = []
    for rect in bars:
        try:
            heights.append(float(rect.get('height', 0)))
        except:
            heights.append(0.0)
    
    if not heights or sum(heights) == 0: 
        return None, None
        
    gb_per_pixel = total_gb / sum(heights)

    # 3. Dynamic Month & Year detection from the working sample
    month_number = detect_cycle_month(soup)
    detected_year = detect_year(all_p)
    
    # Anchor cycle start specifically to the 17th day of the scraped cycle month
    start_date = datetime(detected_year, month_number, 17)
    print(f"   -> Anchoring cycle start to: {start_date.strftime('%B %d, %Y')}")

    # 4. Map rows forward from start date
    data_rows = []
    for i, h in enumerate(heights):
        date_obj = start_date + timedelta(days=i)
        data_rows.append({
            'Date': date_obj.strftime('%m/%d/%Y'), 
            'GB': round(h * gb_per_pixel, 2)
        })
    
    return total_gb, data_rows

def auto_scrape_starlink():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(os.path.join(script_dir, "*.html"))
    
    if not files:
        print(f"Error: No .html files found in {script_dir}")
        return

    print("Found files:")
    for i, f in enumerate(files): 
        print(f"  [{i + 1}] {os.path.basename(f)}")
    print("  [0] Process Everything")

    selection = input("\nSelect a option to scrape: ").strip()
    
    if selection == '0':
        chosen_files = files
    else:
        try:
            chosen_files = [files[int(selection) - 1]]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

    combined_usage = {}
    total_consumption = 0.0

    for file_path in chosen_files:
        print(f"\nProcessing: {os.path.basename(file_path)}")
        total, rows = process_file(file_path)
        
        if not rows:
            print("   -> Error: Could not extract data from file.")
            continue

        total_consumption += total
        for row in rows:
            date_key = row['Date']
            # Accumulate and merge duplicate dates safely across multiple files
            combined_usage[date_key] = combined_usage.get(date_key, 0.0) + row['GB']

    if not combined_usage:
        print("\nNo rows generated to export.")
        return

    # Export to CSV with chronological sorting
    try:
        csv_dest = os.path.join(script_dir, 'data_usage.csv')
        with open(csv_dest, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Data Usage (GB)'])
            
            ordered_dates = sorted(
                combined_usage.keys(),
                key=lambda x: datetime.strptime(x, '%m/%d/%Y')
            )
            
            for entry_date in ordered_dates:
                writer.writerow([entry_date, round(combined_usage[entry_date], 2)])
            
            writer.writerow([])
            writer.writerow(['Total Usage', round(total_consumption, 2)])
            
        print(f"\nSuccess! Exported to 'data_usage.csv'.")
        print(f"Total Combined Usage: {round(total_consumption, 2)} GB")
        
    except PermissionError:
        print("\nError: Could not save 'data_usage.csv'. Please close the file if it is open in Excel.")

if __name__ == '__main__':
    auto_scrape_starlink()
