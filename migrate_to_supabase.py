import csv
import os
import mimetypes
from supabase import create_client, Client

# ================= CONFIGURATION =================
# REPLACE THESE WITH YOUR ACTUAL VALUES FROM SUPABASE
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY" # CAUTION: Keep this secret!

# File Paths
CSV_FILE = r'e:\AI Course\Project\KIET\Feedback-portal\KIET First Year Engineering Bootcamp Feedback (Feb 7th & 8th, 2026) (Responses).csv'
IMAGES_DIR = r'e:\AI Course\Project\KIET\Feedback-portal\docs\bootcamp\kiet\assets\student_images'

# =================================================

def migrate_data():
    if "YOUR_SUPABASE" in SUPABASE_URL:
        print("Error: Please update SUPABASE_URL and SUPABASE_KEY in the script.")
        return

    print("Connecting to Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Reading CSV...")
    students_to_upload = []
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            
            for row in reader:
                if len(row) < 7: continue
                
                # Extract Data
                timestamp = row[0].strip()
                email = row[1].strip()
                name = row[2].strip()
                roll_no = row[3].strip()
                branch = row[4].strip()
                
                try:
                    rating = float(row[5].strip())
                except:
                    rating = 0.0
                    
                feedback_text = row[6].strip()
                suggestions = row[7].strip() if len(row) > 7 else ""
                
                if not feedback_text or not name: continue

                # Image Handling
                img_filename_jpg = f"AIK{roll_no}.jpg"
                img_filename_png = f"AIK{roll_no}.png"
                
                local_img_path = None
                upload_filename = None
                
                if os.path.exists(os.path.join(IMAGES_DIR, img_filename_jpg)):
                    local_img_path = os.path.join(IMAGES_DIR, img_filename_jpg)
                    upload_filename = img_filename_jpg
                elif os.path.exists(os.path.join(IMAGES_DIR, img_filename_png)):
                    local_img_path = os.path.join(IMAGES_DIR, img_filename_png)
                    upload_filename = img_filename_png
                
                public_url = ""
                
                if local_img_path:
                    # Upload Image
                    print(f"Uploading image for {name} ({roll_no})...")
                    try:
                        with open(local_img_path, 'rb') as f:
                            mime_type = mimetypes.guess_type(local_img_path)[0]
                            supabase.storage.from_("student-images").upload(
                                path=upload_filename,
                                file=f,
                                file_options={"content-type": mime_type, "upsert": "true"}
                            )
                        
                        # Get Public URL
                        public_url = supabase.storage.from_("student-images").get_public_url(upload_filename)
                    except Exception as e:
                        print(f"Failed to upload image for {roll_no}: {e}")

                # Prepare Data Record
                student_record = {
                    "timestamp": timestamp,
                    "email": email,
                    "name": name,
                    "roll_no": roll_no,
                    "branch": branch,
                    "rating": rating,
                    "feedback": feedback_text,
                    "suggestions": suggestions,
                    "img_url": public_url
                }
                
                students_to_upload.append(student_record)

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Found {len(students_to_upload)} students. Uploading data to database...")
    
    # Insert Data in Batches
    batch_size = 50
    for i in range(0, len(students_to_upload), batch_size):
        batch = students_to_upload[i:i+batch_size]
        try:
            data, count = supabase.table("feedback").insert(batch).execute()
            print(f"Uploaded batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error uploading batch: {e}")

    print("Migration Complete!")

if __name__ == "__main__":
    migrate_data()
