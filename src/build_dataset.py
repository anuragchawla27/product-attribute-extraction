"""
build_dataset.py
Generates data/dataset.csv — 55 labeled product descriptions.
Multi-label fields (Embellishment, Color) use "|" as separator within a cell.
Run: python src/build_dataset.py
"""
import csv
import os

rows = [
    # description, category, silhouette, fabric, neckline, sleeve, length, embellishment, color
    ("Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
     "Bridesmaid Dress", "Not Specified", "Chiffon", "V-neck", "Not Specified", "Floor Length", "Pleated", "Sage|Dusty Blue"),

    ("Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back",
     "Prom Gown", "Sheath", "Sequin", "Illusion", "Not Specified", "Not Specified", "Sequin", "Not Specified"),

    ("Off shoulder satin ball gown with corset bodice and sweep train in royal navy",
     "Wedding Dress", "Ball Gown", "Satin", "Off-shoulder", "One-shoulder Drape", "Sweep Train", "Corset Bodice", "Royal Navy"),

    ("Lace mermaid wedding dress with long sleeves and scalloped hem",
     "Wedding Dress", "Mermaid", "Lace", "Not Specified", "Long Sleeve", "Floor Length", "Lace Overlay|Scalloped Hem", "Ivory"),

    ("Short cocktail dress with feather trim and beaded waist detail",
     "Cocktail Dress", "Not Specified", "Not Specified", "Not Specified", "Not Specified", "Short/Mini", "Feather Trim|Beaded", "Not Specified"),

    ("Tulle A line evening gown with floral embroidery and cap sleeves",
     "Evening Gown", "A-line", "Tulle", "Not Specified", "Cap Sleeve", "Not Specified", "Embroidered", "Not Specified"),

    ("Stretch jersey sheath dress with ruched waist and side slit",
     "Formal Dress", "Sheath", "Jersey", "Not Specified", "Not Specified", "Not Specified", "Ruched", "Not Specified"),

    ("Strapless sweetheart neckline glitter gown with layered skirt",
     "Evening Gown", "Not Specified", "Sequin", "Sweetheart", "Strapless", "Not Specified", "Sequin|Layered Skirt", "Not Specified"),

    ("One shoulder draped chiffon dress with high slit and empire waist",
     "Cocktail Dress", "Empire", "Chiffon", "One-shoulder", "One-shoulder Drape", "Not Specified", "Draped", "Not Specified"),

    ("Velvet winter formal dress with square neckline and puff sleeves",
     "Formal Dress", "Not Specified", "Velvet", "Square", "Puff Sleeve", "Not Specified", "None", "Not Specified"),

    ("Elegant satin A line wedding gown with sweetheart neckline and chapel train in ivory",
     "Wedding Dress", "A-line", "Satin", "Sweetheart", "Sleeveless", "Chapel Train", "None", "Ivory"),

    ("Beaded tulle ball gown with off shoulder sleeves and floor length skirt in champagne",
     "Prom Gown", "Ball Gown", "Tulle", "Off-shoulder", "Short Sleeve", "Floor Length", "Beaded", "Champagne"),

    ("Fitted sequin mermaid gown with halter neckline and thigh high slit in black",
     "Evening Gown", "Mermaid", "Sequin", "Halter", "Sleeveless", "Floor Length", "Sequin", "Black"),

    ("Knee length lace cocktail dress with scoop neckline and short sleeves in burgundy",
     "Cocktail Dress", "Sheath", "Lace", "Scoop", "Short Sleeve", "Knee Length", "Lace Overlay", "Burgundy"),

    ("Organza ball gown with pleated skirt and strapless sweetheart bodice in blush",
     "Prom Gown", "Ball Gown", "Organza", "Sweetheart", "Strapless", "Floor Length", "Pleated", "Blush"),

    ("Long sleeve lace wedding gown with illusion neckline and chapel train",
     "Wedding Dress", "A-line", "Lace", "Illusion", "Long Sleeve", "Chapel Train", "Lace Overlay", "Ivory"),

    ("Crepe sheath dress with square neckline and cap sleeves in emerald",
     "Formal Dress", "Sheath", "Crepe", "Square", "Cap Sleeve", "Knee Length", "None", "Emerald"),

    ("Tea length tulle party dress with embroidered bodice and cap sleeves in gold",
     "Party Dress", "A-line", "Tulle", "Not Specified", "Cap Sleeve", "Tea Length", "Embroidered", "Gold"),

    ("Fit and flare satin cocktail dress with boat neck and short sleeves in red",
     "Cocktail Dress", "Fit and Flare", "Satin", "Boat Neck", "Short Sleeve", "Knee Length", "None", "Red"),

    ("Trumpet silhouette wedding dress in satin with off shoulder neckline and chapel train",
     "Wedding Dress", "Trumpet", "Satin", "Off-shoulder", "Short Sleeve", "Chapel Train", "None", "Ivory"),

    ("Sequin embellished column gown with one shoulder neckline in silver",
     "Evening Gown", "Column", "Sequin", "One-shoulder", "One-shoulder Drape", "Floor Length", "Sequin", "Silver"),

    ("Corset bodice ball gown with tulle skirt and sweetheart neckline in dusty blue",
     "Prom Gown", "Ball Gown", "Tulle", "Sweetheart", "Strapless", "Floor Length", "Corset Bodice", "Dusty Blue"),

    ("Short jersey party dress with ruched sides and scoop neckline in black",
     "Party Dress", "Sheath", "Jersey", "Scoop", "Sleeveless", "Short/Mini", "Ruched", "Black"),

    ("Feather trimmed mini dress with off shoulder sleeves in red",
     "Party Dress", "Not Specified", "Not Specified", "Off-shoulder", "Short Sleeve", "Short/Mini", "Feather Trim", "Red"),

    ("Empire waist chiffon gown with V neckline and long sleeves in sage",
     "Evening Gown", "Empire", "Chiffon", "V-neck", "Long Sleeve", "Floor Length", "None", "Sage"),

    ("Draped satin gown with high slit and halter neckline in emerald",
     "Evening Gown", "Column", "Satin", "Halter", "Sleeveless", "Floor Length", "Draped", "Emerald"),

    ("Homecoming dress in sequin fabric with short hemline and spaghetti straps",
     "Homecoming Dress", "Fit and Flare", "Sequin", "Not Specified", "Sleeveless", "Short/Mini", "Sequin", "Not Specified"),

    ("Scalloped lace wedding gown with illusion sleeves and sweetheart neckline",
     "Wedding Dress", "Mermaid", "Lace", "Sweetheart", "Long Sleeve", "Floor Length", "Lace Overlay|Scalloped Hem", "Ivory"),

    ("Bridesmaid gown in dusty blue chiffon with pleated skirt and halter neckline",
     "Bridesmaid Dress", "A-line", "Chiffon", "Halter", "Sleeveless", "Floor Length", "Pleated", "Dusty Blue"),

    ("Beaded evening gown with illusion neckline and long sleeves in gold",
     "Evening Gown", "Sheath", "Not Specified", "Illusion", "Long Sleeve", "Floor Length", "Beaded", "Gold"),

    ("Tweed formal dress with square neckline and short sleeves in burgundy",
     "Formal Dress", "Sheath", "Tweed", "Square", "Short Sleeve", "Knee Length", "None", "Burgundy"),

    ("Off the shoulder velvet gown with puff sleeves and floor length hem in emerald",
     "Evening Gown", "A-line", "Velvet", "Off-shoulder", "Puff Sleeve", "Floor Length", "None", "Emerald"),

    ("Sequin cocktail dress with one shoulder drape and thigh slit in silver",
     "Cocktail Dress", "Sheath", "Sequin", "One-shoulder", "One-shoulder Drape", "Short/Mini", "Sequin", "Silver"),

    ("Organza bridesmaid dress with sweetheart neckline and cap sleeves in champagne",
     "Bridesmaid Dress", "A-line", "Organza", "Sweetheart", "Cap Sleeve", "Floor Length", "None", "Champagne"),

    ("Ruched jersey gown with V neckline and long sleeves in black",
     "Evening Gown", "Sheath", "Jersey", "V-neck", "Long Sleeve", "Floor Length", "Ruched", "Black"),

    ("Prom dress in tulle with beaded bodice and off shoulder sleeves in blush",
     "Prom Gown", "Ball Gown", "Tulle", "Off-shoulder", "Short Sleeve", "Floor Length", "Beaded", "Blush"),

    ("Satin sheath dress with boat neckline and knee length hem in navy",
     "Cocktail Dress", "Sheath", "Satin", "Boat Neck", "Sleeveless", "Knee Length", "None", "Royal Navy"),

    ("Embroidered chiffon gown with empire waist and cap sleeves in ivory",
     "Evening Gown", "Empire", "Chiffon", "Not Specified", "Cap Sleeve", "Floor Length", "Embroidered", "Ivory"),

    ("Lace overlay cocktail dress with scoop neckline and short sleeves in emerald",
     "Cocktail Dress", "Fit and Flare", "Lace", "Scoop", "Short Sleeve", "Knee Length", "Lace Overlay", "Emerald"),

    ("Layered tulle skirt gown with sweetheart bodice and beaded waist in gold",
     "Prom Gown", "Ball Gown", "Tulle", "Sweetheart", "Strapless", "Floor Length", "Beaded|Layered Skirt", "Gold"),

    ("Column gown in crepe with halter neckline and side slit in black",
     "Evening Gown", "Column", "Crepe", "Halter", "Sleeveless", "Floor Length", "None", "Black"),

    ("Off shoulder lace wedding dress with long train and beaded bodice",
     "Wedding Dress", "A-line", "Lace", "Off-shoulder", "Short Sleeve", "Chapel Train", "Lace Overlay|Beaded", "Ivory"),

    ("Velvet cocktail dress with square neckline and long sleeves in burgundy",
     "Cocktail Dress", "Sheath", "Velvet", "Square", "Long Sleeve", "Knee Length", "None", "Burgundy"),

    ("Sequin homecoming dress with halter neckline and open back in silver",
     "Homecoming Dress", "Sheath", "Sequin", "Halter", "Sleeveless", "Short/Mini", "Sequin", "Silver"),

    ("Chiffon evening gown with one shoulder neckline and draped skirt in dusty blue",
     "Evening Gown", "Column", "Chiffon", "One-shoulder", "One-shoulder Drape", "Floor Length", "Draped", "Dusty Blue"),

    ("Puff sleeve satin party dress with square neckline in red",
     "Party Dress", "Fit and Flare", "Satin", "Square", "Puff Sleeve", "Knee Length", "None", "Red"),

    ("Tulle ball gown wedding dress with corset bodice and off shoulder sleeves",
     "Wedding Dress", "Ball Gown", "Tulle", "Off-shoulder", "Short Sleeve", "Floor Length", "Corset Bodice", "Ivory"),

    ("Embroidered organza gown with illusion neckline and cap sleeves in champagne",
     "Evening Gown", "A-line", "Organza", "Illusion", "Cap Sleeve", "Floor Length", "Embroidered", "Champagne"),

    ("Fitted jersey cocktail dress with V neckline and side slit in black",
     "Cocktail Dress", "Sheath", "Jersey", "V-neck", "Sleeveless", "Knee Length", "None", "Black"),

    ("Feather trim evening gown with sweetheart neckline and floor length hem in emerald",
     "Evening Gown", "Sheath", "Not Specified", "Sweetheart", "Sleeveless", "Floor Length", "Feather Trim", "Emerald"),

    ("Draped chiffon party dress with empire waist and short sleeves in gold",
     "Party Dress", "Empire", "Chiffon", "Not Specified", "Short Sleeve", "Knee Length", "Draped", "Gold"),

    ("Beaded lace bridesmaid dress with scoop neckline and cap sleeves in sage",
     "Bridesmaid Dress", "A-line", "Lace", "Scoop", "Cap Sleeve", "Floor Length", "Beaded|Lace Overlay", "Sage"),

    ("Mermaid prom gown in satin with sweetheart neckline and sweep train in red",
     "Prom Gown", "Mermaid", "Satin", "Sweetheart", "Sleeveless", "Sweep Train", "None", "Red"),

    ("Ruched velvet gown with off shoulder sleeves and floor length hem in burgundy",
     "Evening Gown", "Sheath", "Velvet", "Off-shoulder", "Short Sleeve", "Floor Length", "Ruched", "Burgundy"),

    ("Scalloped hem lace cocktail dress with illusion neckline and long sleeves in ivory",
     "Cocktail Dress", "Sheath", "Lace", "Illusion", "Long Sleeve", "Knee Length", "Lace Overlay|Scalloped Hem", "Ivory"),
]

columns = ["description", "category", "silhouette", "fabric", "neckline",
           "sleeve", "length", "embellishment", "color"]

os.makedirs("data", exist_ok=True)
out_path = os.path.join("data", "dataset.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Wrote {len(rows)} labeled rows to {out_path}")
