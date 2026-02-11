import csv
import os
import json

# Configuration
CSV_FILE = r'e:\AI Course\Project\KIET\Feedback-portal\KIET First Year Engineering Bootcamp Feedback (Feb 7th & 8th, 2026) (Responses).csv'
OUTPUT_FILE = r'e:\AI Course\Project\KIET\Feedback-portal\docs\bootcamp\kiet\feedback.html'
IMAGES_DIR = r'e:\AI Course\Project\KIET\Feedback-portal\docs\bootcamp\kiet\assets\student_images'
REL_IMG_PATH = 'assets/student_images'

def generate_feedback_page():
    # Read CSV
    feedbacks = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            
            for row in reader:
                if len(row) < 7: continue
                
                name = row[2].strip()
                roll_no = row[3].strip()
                feedback = row[6].strip()
                
                if not feedback or not name: continue
                
                # Extract additional fields
                timestamp = row[0].strip()
                email = row[1].strip()
                branch = row[4].strip()
                # Ensure rating is a float for filtering, handle potential errors
                try:
                    rating = float(row[5].strip())
                except ValueError:
                    rating = 0.0
                
                suggestions = row[7].strip() if len(row) > 7 else ""

                # Check for image
                img_filename = f"AIK{roll_no}.jpg"
                img_path = os.path.join(IMAGES_DIR, img_filename)
                
                final_img_url = ""
                
                if os.path.exists(img_path):
                    final_img_url = f"{REL_IMG_PATH}/{img_filename}"
                else: 
                     img_filename_png = f"AIK{roll_no}.png"
                     img_path_png = os.path.join(IMAGES_DIR, img_filename_png)
                     if os.path.exists(img_path_png):
                        final_img_url = f"{REL_IMG_PATH}/{img_filename_png}"
                
                if final_img_url:
                    feedbacks.append({
                        'timestamp': timestamp,
                        'email': email,
                        'name': name,
                        'roll_no': roll_no,
                        'branch': branch,
                        'rating': rating,
                        'feedback': feedback,
                        'suggestions': suggestions,
                        'img_url': final_img_url
                    })

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Found {len(feedbacks)} students with both feedback and photos.")
    
    # Serialize data for JavaScript
    json_data = json.dumps(feedbacks, indent=None)

    # Generate HTML with Enhanced Aesthetics & Interactivity
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Feedback | AI Karyashala Bootcamp</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Animate.css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {{
            --primary-color: #2563eb;
            --primary-dark: #1e40af;
            --secondary-color: #64748b;
            --accent-color: #f59e0b;
            --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: 1px solid rgba(255, 255, 255, 0.6);
            --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
            --text-main: #1e293b;
            --text-muted: #64748b;
            --transition-speed: 0.3s;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            margin: 0;
            padding: 40px 20px;
            color: var(--text-main);
            overflow-x: hidden;
            background-attachment: fixed;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}

        /* Header Styling */
        .header {{
            text-align: center;
            margin-bottom: 40px;
            position: relative;
            padding: 40px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            border: var(--card-border);
            box-shadow: var(--glass-shadow);
        }}

        .header h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2563eb 0%, #9333ea 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 10px 0;
            letter-spacing: -1.5px;
        }}

        .header p {{
            font-size: 1.25rem;
            color: var(--secondary-color);
            margin: 0;
            font-weight: 400;
        }}

        /* Search & Filter Bar */
        .controls-wrapper {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 50px;
            padding: 15px 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            border: var(--card-border);
        }}

        .search-box {{
            flex-grow: 1;
            position: relative;
            min-width: 300px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 20px 12px 45px;
            border-radius: 30px;
            border: 1px solid rgba(0,0,0,0.1);
            background: rgba(255,255,255,0.8);
            font-family: inherit;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        .search-box input:focus {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
            border-color: var(--primary-color);
        }}

        .search-box i {{
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #94a3b8;
        }}

        .filters {{
            display: flex;
            gap: 15px;
        }}

        .filter-select {{
            padding: 10px 20px;
            border-radius: 30px;
            border: 1px solid rgba(0,0,0,0.1);
            background: white;
            font-family: inherit;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s ease;
            color: var(--text-main);
        }}

        .filter-select:hover, .filter-select:focus {{
            border-color: var(--primary-color);
        }}

        /* Pagination Styling */
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin: 40px 0;
        }}

        .btn {{
            padding: 12px 28px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .btn:disabled {{
            background: #cbd5e1;
            box-shadow: none;
            cursor: not-allowed;
            transform: none !important;
        }}

        .btn:hover:not(:disabled) {{
            background: var(--primary-dark);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        }}

        #page-info {{
            font-weight: 700;
            color: var(--text-main);
            background: white;
            padding: 8px 20px;
            border-radius: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        /* Gallery Grid */
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 30px;
            perspective: 1000px;
        }}

        /* Card Styling */
        .card {{
            background: var(--card-bg);
            border-radius: 24px;
            box-shadow: var(--glass-shadow);
            border: var(--card-border);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
            transform-style: preserve-3d;
            transform: translateZ(0); /* Hardware acceleration */
            cursor: pointer;
        }}

        /* 3D Tilt Effect handled by JS library, remove CSS hover transform to avoid conflict */
        
        .card-img-wrapper {{
            position: relative;
            height: 280px;
            overflow: hidden;
        }}

        .card-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s ease;
        }}

        .card:hover .card-img {{
            transform: scale(1.1);
        }}

        .card-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
            padding: 20px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .card:hover .card-overlay {{
            opacity: 1;
        }}
        
        .overlay-text {{
            color: white;
            font-weight: 600;
            font-size: 0.9rem;
            text-align: center;
        }}

        .card-body {{
            padding: 25px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            background: rgba(255,255,255,0.4);
        }}

        .student-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }}

        .student-info h3 {{
            margin: 0;
            color: var(--text-main);
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.3;
        }}

        .student-details {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 6px;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        
        .badge {{
             background: rgba(37, 99, 235, 0.1);
             color: var(--primary-color);
             padding: 3px 10px;
             border-radius: 6px;
             font-weight: 600;
             font-size: 0.75rem;
        }}

        .rating {{
            background: linear-gradient(135deg, #fbbf24, #d97706);
            color: white;
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            box-shadow: 0 4px 6px rgba(217, 119, 6, 0.2);
            display: flex;
            align-items: center;
            gap: 4px;
            white-space: nowrap;
        }}

        .feedback-preview {{
            margin-top: 15px;
            font-style: italic;
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            position: relative;
        }}

        .read-more-hint {{
            color: var(--primary-color);
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
            opacity: 0.8;
        }}
        
        .card:hover .read-more-hint {{
            opacity: 1;
            transform: translateX(5px);
            transition: transform 0.3s ease;
        }}

        /* Modal Styling */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(8px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .modal-overlay.active {{
            display: flex;
            opacity: 1;
        }}

        .modal-content {{
            background: white;
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative;
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }}

        @media(min-width: 768px) {{
            .modal-content {{
                flex-direction: row;
                overflow: hidden; /* Desktop keeps it constrained */
            }}
            .modal-image-side {{
                width: 40%;
                background: #f1f5f9;
            }}
            .modal-text-side {{
                width: 60%;
                overflow-y: auto;
            }}
        }}

        .modal-overlay.active .modal-content {{
            transform: scale(1);
        }}

        .modal-image-side img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            min-height: 300px;
        }}

        .modal-text-side {{
            padding: 40px;
            position: relative;
        }}

        .close-modal {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.05);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2rem;
            color: var(--text-muted);
            transition: all 0.2s;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .close-modal:hover {{
            background: #cbd5e1;
            color: var(--text-main);
            transform: rotate(90deg);
        }}

        .modal-details h2 {{
            margin: 0 0 5px 0;
            color: var(--primary-dark);
            font-size: 1.8rem;
        }}

        .modal-meta {{
            color: var(--text-muted);
            margin-bottom: 25px;
            font-size: 0.95rem;
            display: flex;
            gap: 15px;
            align-items: center;
        }}

        .full-feedback {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #334155;
            margin-bottom: 30px;
            position: relative;
        }}
        
        .full-feedback::before {{
            content: "❝";
            font-size: 3rem;
            color: #e2e8f0;
            position: absolute;
            left: -20px;
            top: -20px;
            z-index: -1;
        }}

        .suggestion-box {{
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .suggestion-box h4 {{
            margin: 0 0 10px 0;
            color: #92400e;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2.2rem; }}
            .controls-wrapper {{ flex-direction: column; align-items: stretch; border-radius: 30px; }}
            .filters {{ flex-direction: column; }}
            .modal-content {{ flex-direction: column; }}
            .modal-image-side {{ height: 250px; }}
        }}

        /* Background Animation */
        .bg-shape {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            z-index: 0;
            opacity: 0.6;
            animation: float 20s infinite ease-in-out;
        }}
        .shape-1 {{ width: 400px; height: 400px; background: rgba(37, 99, 235, 0.15); top: -100px; left: -100px; }}
        .shape-2 {{ width: 300px; height: 300px; background: rgba(147, 51, 234, 0.15); bottom: 10%; right: -50px; animation-delay: -5s; }}
        .shape-3 {{ width: 200px; height: 200px; background: rgba(245, 158, 11, 0.15); top: 40%; left: 30%; animation-delay: -10s; }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(30px, -50px); }}
        }}
    </style>
</head>
<body>
    <!-- Background Shapes -->
    <div class="bg-shape shape-1"></div>
    <div class="bg-shape shape-2"></div>
    <div class="bg-shape shape-3"></div>

    <div class="container animate__animated animate__fadeIn">
        <div class="header">
            <h1>Student Voices</h1>
            <p>AI Karyashala Bootcamp • Authentic Feedback Gallery</p>
        </div>

        <!-- Search & Filters -->
        <div class="controls-wrapper">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search by name, roll number..." oninput="filterData()">
            </div>
            <div class="filters">
                <select id="branchFilter" class="filter-select" onchange="filterData()">
                    <option value="">All Branches</option>
                    <option value="CSM">CSM</option>
                    <option value="AID">AID</option>
                    <option value="CSC">CSC</option>
                    <option value="CAI">CAI</option>
                    <option value="CSD">CSD</option>
                </select>
                <select id="ratingFilter" class="filter-select" onchange="filterData()">
                    <option value="">All Ratings</option>
                    <option value="5">5 Stars</option>
                    <option value="4">4 Stars & Up</option>
                    <option value="3">3 Stars & Up</option>
                </select>
            </div>
        </div>

        <div class="pagination">
            <button id="prev-btn" class="btn" onclick="changePage(-1)"><i class="fas fa-arrow-left"></i> Previous</button>
            <span id="page-info">Page 1</span>
            <button id="next-btn" class="btn" onclick="changePage(1)">Next <i class="fas fa-arrow-right"></i></button>
        </div>

        <div id="gallery-container" class="gallery-grid">
            <!-- Content will be injected by JS -->
        </div>

        <div class="pagination">
            <button id="prev-btn-2" class="btn" onclick="changePage(-1)"><i class="fas fa-arrow-left"></i> Previous</button>
            <span id="page-info-2">Page 1</span>
            <button id="next-btn-2" class="btn" onclick="changePage(1)">Next <i class="fas fa-arrow-right"></i></button>
        </div>
        
        <div style="text-align: center; margin-top: 50px; color: #94a3b8; font-size: 0.9rem; position: relative;">
            Made with <i class="fas fa-heart" style="color: #ef4444;"></i> for AI Karyashala
        </div>
    </div>

    <!-- Modal Structure -->
    <div class="modal-overlay" id="feedbackModal">
        <div class="modal-content" onclick="event.stopPropagation()">
            <button class="close-modal" onclick="closeModal()"><i class="fas fa-times"></i></button>
            <div class="modal-image-side">
                <img id="modalImg" src="" alt="Student">
            </div>
            <div class="modal-text-side">
                <div class="modal-details">
                    <h2 id="modalName">Student Name</h2>
                    <div class="modal-meta">
                        <span class="badge" id="modalBranch">Branch</span>
                        <span class="badge" id="modalRoll">Roll No</span>
                    </div>
                </div>
                
                <div class="rating" id="modalRating" style="width: fit-content; margin-bottom: 20px;">
                    5.0
                </div>

                <div class="full-feedback" id="modalFeedback">
                    Feedback text...
                </div>

                <div id="modalSuggestionBox" class="suggestion-box" style="display: none;">
                    <h4><i class="fas fa-lightbulb"></i> Suggestion / Query</h4>
                    <p id="modalSuggestionText">Suggestion text...</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Vanilla Tilt JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.0/vanilla-tilt.min.js"></script>

    <script>
        // Embedded Data
        const ALL_DATA = {json_data};
        let FILTERED_DATA = [...ALL_DATA];
        const PAGE_SIZE = 20;
        let currentPage = 1;

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            renderPage(1);
        }});

        function filterData() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const branchFilter = document.getElementById('branchFilter').value;
            const ratingFilter = document.getElementById('ratingFilter').value;

            FILTERED_DATA = ALL_DATA.filter(student => {{
                // Search
                const matchesSearch = student.name.toLowerCase().includes(searchTerm) || 
                                      student.roll_no.toLowerCase().includes(searchTerm);
                
                // Branch (Partial match OK, e.g. 'CSM' matches 'CSM-H')
                const matchesBranch = branchFilter === "" || student.branch.toUpperCase().includes(branchFilter);
                
                // Rating (Greater than or equal)
                const matchesRating = ratingFilter === "" || student.rating >= parseFloat(ratingFilter);

                return matchesSearch && matchesBranch && matchesRating;
            }});

            currentPage = 1;
            renderPage(currentPage);
        }}

        function renderPage(page) {{
            const container = document.getElementById('gallery-container');
            container.innerHTML = '';
            
            if (FILTERED_DATA.length === 0) {{
                container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 50px; color: #64748b; font-size: 1.2rem;">No students found matching your criteria.</div>`;
                updatePaginationControls();
                return;
            }}

            const start = (page - 1) * PAGE_SIZE;
            const end = start + PAGE_SIZE;
            const pageData = FILTERED_DATA.slice(start, end);
            
            pageData.forEach((student, index) => {{
                // Create Card
                const card = document.createElement('div');
                card.className = 'card animate__animated animate__fadeInUp';
                card.style.animationDelay = `${{index * 0.05}}s`;
                card.onclick = () => openModal(student); // Open modal on click
                
                // Set tilt attributes
                card.setAttribute("data-tilt", "");
                card.setAttribute("data-tilt-max", "5");
                card.setAttribute("data-tilt-speed", "400");
                card.setAttribute("data-tilt-glare", "");
                card.setAttribute("data-tilt-max-glare", "0.2");

                card.innerHTML = `
                    <div class="card-img-wrapper">
                        <img src="${{student.img_url}}" alt="${{student.name}}" class="card-img" onerror="this.src='https://via.placeholder.com/400x350/e2e8f0/94a3b8?text=No+Photo';">
                        <div class="card-overlay">
                            <div class="overlay-text">Click to read full feedback</div>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="student-header">
                            <div class="student-info">
                                <h3>${{student.name}}</h3>
                                <div class="student-details">
                                    <span class="badge">${{student.branch}}</span>
                                    <span style="font-size: 0.75rem; color: #94a3b8;">${{student.roll_no}}</span>
                                </div>
                            </div>
                            <div class="rating">
                                ${{student.rating}}
                            </div>
                        </div>
                        
                        <div class="feedback-preview">
                            ${{student.feedback}}
                        </div>
                        
                        <div class="read-more-hint">
                            Read More <i class="fas fa-arrow-right" style="font-size: 0.8rem;"></i>
                        </div>
                    </div>
                `;
                
                container.appendChild(card);
            }});

            // Initialize Tilt for new elements
            VanillaTilt.init(document.querySelectorAll(".card"));

            updatePaginationControls();
            
            if(window.scrollY > 200) {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}

        function changePage(delta) {{
            const maxPage = Math.ceil(FILTERED_DATA.length / PAGE_SIZE);
            const newPage = currentPage + delta;
            
            if (newPage >= 1 && newPage <= maxPage) {{
                currentPage = newPage;
                renderPage(currentPage);
            }}
        }}

        function updatePaginationControls() {{
            const maxPage = Math.ceil(FILTERED_DATA.length / PAGE_SIZE) || 1;
            const prevBtns = [document.getElementById('prev-btn'), document.getElementById('prev-btn-2')];
            const nextBtns = [document.getElementById('next-btn'), document.getElementById('next-btn-2')];
            const infoSpans = [document.getElementById('page-info'), document.getElementById('page-info-2')];

            prevBtns.forEach(btn => btn.disabled = currentPage === 1);
            nextBtns.forEach(btn => btn.disabled = currentPage === maxPage);
            infoSpans.forEach(span => span.textContent = `Page ${{currentPage}} of ${{maxPage}} (${{FILTERED_DATA.length}} Results)`);
        }}

        // Modal Functions
        function openModal(student) {{
            const modal = document.getElementById('feedbackModal');
            document.getElementById('modalImg').src = student.img_url;
            document.getElementById('modalName').textContent = student.name;
            document.getElementById('modalBranch').textContent = student.branch;
            document.getElementById('modalRoll').textContent = student.roll_no;
            document.getElementById('modalRating').innerHTML = `${{student.rating}} <i class="fas fa-star" style="font-size:0.8em; margin-left:5px;"></i>`;
            document.getElementById('modalFeedback').textContent = student.feedback;

            // Handle Suggestions
            const suggestionBox = document.getElementById('modalSuggestionBox');
            if(student.suggestions && student.suggestions.length > 2 && student.suggestions.toLowerCase() !== 'no') {{
                document.getElementById('modalSuggestionText').textContent = student.suggestions;
                suggestionBox.style.display = 'block';
            }} else {{
                suggestionBox.style.display = 'none';
            }}

            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        }}

        function closeModal() {{
            const modal = document.getElementById('feedbackModal');
            modal.classList.remove('active');
            document.body.style.overflow = 'auto'; // Restore scrolling
        }}

        // Close modal when clicking outside
        document.getElementById('feedbackModal').addEventListener('click', (e) => {{
            if (e.target.id === 'feedbackModal') {{
                closeModal();
            }}
        }});
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeModal();
        }});
    </script>
</body>
</html>
"""

    # Write HTML
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated feedback page at: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing HTML: {e}")

if __name__ == "__main__":
    generate_feedback_page()
