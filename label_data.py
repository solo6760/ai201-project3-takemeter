import csv

def map_category_to_label(title, category):
    title_upper = title.upper()
    
    # Check for ANALYSIS indicators
    if "[OC]" in title_upper or "SERIOUS NEXT DAY THREAD" in title_upper or "ANALYSIS" in title_upper:
        return "ANALYSIS", ""
        
    # Check for NEWS indicators
    if "[HIGHLIGHT]" in title_upper or "POST GAME THREAD" in title_upper or "[WOJNAROWSKI]" in title_upper:
        return "NEWS", ""
        
    # Check specific ambiguous cases from the CSV
    if "CAN SOMEONE EXPLAIN TRADES TO ME?" in title_upper or "CAN SOMEONE EXPLAIN THE “SIGN & TRADE” RULES" in title_upper:
        return "HOT_TAKE", "Questions/explainer requests on rules fall under discussion/opinion rather than news or deep OC analysis."
        
    if "ADRIAN WOJNAROWSKI ALSO LEAKED MVP WINNERS" in title_upper:
        return "HOT_TAKE", "Opinion/meta-discussion criticizing media double standards."
        
    if "GREATEST R/NBA COMMENTS AND COPYPASTAS OF ALL-TIME" in title_upper or "WRITE AN R/NBA HEADLINE" in title_upper:
        return "HOT_TAKE", "Fun meta-discussions/memes are community narrative."
        
    if "THE GUARDIAN" in title_upper and "15 THINGS WE LEARNED" in title_upper:
        return "HOT_TAKE", "Journalistic opinion roundups are editorialized narrative."
        
    if "DAILY DISCUSSION THREAD" in title_upper:
        return "NEWS", "General directory and index threads are administrative/news."

    # General mappings based on Category
    if category == "Deep Analysis":
        return "ANALYSIS", ""
    elif category == "Hot Take":
        return "HOT_TAKE", ""
    elif category == "Highlights & Play" or category == "Game & Match Discussion":
        return "NEWS", ""
    elif category == "Trade & Speculation":
        # Woj/Shams announcements are news, general salary discussion is hot_take
        if any(insider in title_upper for insider in ["WOJ", "SHAMS", "SOURCES", "REPORTS"]):
            return "NEWS", ""
        return "HOT_TAKE", "General contract/cap speculation without official announcement."
        
    return "HOT_TAKE", "Fallback default classification"

def main():
    labeled_rows = []
    counts = {"ANALYSIS": 0, "HOT_TAKE": 0, "NEWS": 0}
    
    with open("r_nba_discourse_links.csv", mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            title = row["Title"]
            orig_cat = row["Category"]
            
            label, note = map_category_to_label(title, orig_cat)
            counts[label] += 1
            
            labeled_rows.append({
                "text": title,
                "label": label,
                "notes": note,
                "is_prelabeled": "True",
                "prelabeled_by": "Gemini-3.5-Flash"
            })
            
    with open("labeled_data.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["text", "label", "notes", "is_prelabeled", "prelabeled_by"])
        writer.writeheader()
        writer.writerows(labeled_rows)
        
    print("Class distribution:")
    total = len(labeled_rows)
    for lbl, count in counts.items():
        prop = count / total
        print(f"  {lbl}: {count} ({prop:.2%})")
        
    print("\nSuccessfully saved labeled_data.csv!")

if __name__ == "__main__":
    main()
