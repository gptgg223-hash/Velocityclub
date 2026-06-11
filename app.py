from flask import Flask, request
import requests
import os

app = Flask(__name__)


# ==================== HOME PAGE ====================
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velocity Club</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a0033, #2d004d);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 60px;
        }
        .logo {
            font-size: 28px;
            font-weight: 700;
            color: #c026d3;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            font-weight: 500;
        }
        .hero {
            text-align: center;
            max-width: 700px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.8rem;
            background: linear-gradient(to right, #c026d3, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }
        .subtitle {
            font-size: 1.25rem;
            opacity: 0.9;
            margin-bottom: 50px;
        }
        .search-form {
            display: flex;
            max-width: 680px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 9999px;
            padding: 8px;
            backdrop-filter: blur(12px);
        }
        input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: white;
            font-size: 1.1rem;
            padding: 18px 24px;
        }
        button {
            background: linear-gradient(to right, #8b5cf6, #c026d3);
            color: white;
            border: none;
            padding: 0 42px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
        }
        footer {
            text-align: center;
            margin-top: 80px;
            opacity: 0.7;
            font-size: 0.95rem;
        }
        @media (max-width: 600px) {
            h1 { font-size: 2.3rem; }
            .search-form { flex-direction: column; border-radius: 20px; padding: 6px; }
            button { padding: 16px; border-radius: 9999px; margin-top: 8px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">♫ Velocity Club</div>
        <nav>
            <a href="#">Home</a>
            <a href="#">Contact</a>
            <a href="#">About</a>
            <a href="#">Developer</a>
        </nav>
    </header>

    <div class="hero">
        <h1>Find Your Favorite Songs</h1>
        <p class="subtitle">Search any song, artist, or album and listen instantly</p>
        
        <form action="/search" method="POST" class="search-form">
            <input type="text" name="song" placeholder="Search songs, artists..." required>
            <button type="submit">Search</button>
            <button type="button"
            onclick="startVoice()">🎤</button>
        </form>
<div style="margin-top:40px;text-align:center;">
<h2>Trending Songs</h2>

<form action="/search" method="POST">
<button name="song" value="Believer">Believer</button>
<button name="song" value="Shape of You">Shape of You</button>
<button name="song" value="Kesariya">Kesariya</button>
<button name="song" value="Levitating">Levitating</button>
</form>
</div>

    </div>
<p>Developed by XDevelopers with JioSaavn</p>
<p>© 2026 Velocity Club</p>

<script>
function startVoice() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Voice search not supported on this browser.");
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;

        document.querySelector('input[name="song"]').value = text;

        document.querySelector('.search-form').submit();
    };

    recognition.onerror = function(event) {
        alert("Voice search error: " + event.error);
    };

    recognition.start();
}
</script>

</body>
</html>
"""

# ==================== SEARCH RESULTS PAGE ====================
@app.route('/')
def home():
    return HOME_PAGE


@app.route('/search', methods=['POST'])
def search():
    song = request.form.get("song", "").strip()

    if not song:
        return "<h1 style='color:white;background:#121212;padding:100px;'>Please enter a song name!</h1>"

    response = requests.get(
        "https://jiosavanapiryden.vercel.app/api/search/songs",
        params={"query": song}
    )

    try:
        data = response.json()
        results = data.get("data", {}).get("results", [])[:12]
    except:
        results = []

    songs_html = ""
    for result in results:
        title = result.get("name", "Unknown")
        artist = result.get("artists", {}).get("primary", [{}])[0].get("name", "Unknown")
        album = result.get("album", {}).get("name", "Unknown")
        duration = result.get("duration", 0)
        image = result.get("image", [{}])[-1].get("url", "")
        song_url = result.get("url", "#")

        songs_html += f"""
        <div class="song-card">
            <img src="{image}" alt="{title}">
            <div class="song-info">
                <h3>{title}</h3>
                <p>🎤 {artist}</p>
                <p>💿 {album}</p>
                <p>⏱️ {duration} sec</p>
            </div>
            <div class="song-actions">
                <a href="{song_url}" target="_blank"><button class="play-btn">🎵 Open Song</button></a>
                <a href="{song_url}" target="_blank"><button class="jio-btn">View on JioSaavn ↗</button></a>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Results - Velocity Club</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{
                margin: 0;
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0a0a0a, #1a0033, #2d004d);
                color: white;
                padding: 20px;
            }}
            header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }}
            .logo {{ font-size: 28px; font-weight: 700; color: #c026d3; }}
            .new-search {{
                background: #6b21a8;
                color: white;
                padding: 12px 24px;
                border-radius: 9999px;
                text-decoration: none;
                font-weight: 600;
            }}
            h2 {{ text-align: center; margin: 20px 0 8px; font-size: 2rem; }}
            .subtitle {{ text-align: center; opacity: 0.8; margin-bottom: 30px; }}
            
            .song-card {{
                background: rgba(30, 20, 50, 0.85);
                border-radius: 20px;
                padding: 16px;
                margin: 16px auto;
                max-width: 780px;
                display: flex;
                align-items: center;
                gap: 18px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            }}
            .song-card img {{
                width: 100px;
                height: 100px;
                border-radius: 14px;
                object-fit: cover;
            }}
            .song-info {{ flex: 1; text-align: left; }}
            .song-info h3 {{ margin-bottom: 6px; font-size: 1.3rem; }}
            .song-info p {{ margin: 3px 0; opacity: 0.9; }}
            
            .song-actions {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                min-width: 150px;
            }}
            button {{
                padding: 13px 22px;
                border: none;
                border-radius: 9999px;
                font-weight: 600;
                cursor: pointer;
            }}
            .play-btn {{
                background: linear-gradient(to right, #8b5cf6, #c026d3);
                color: white;
            }}
            .jio-btn {{
                background: transparent;
                color: white;
                border: 2px solid #a855f7;
            }}
            @media (max-width: 600px) {{
                .song-card {{ flex-direction: column; text-align: center; }}
                .song-actions {{ flex-direction: row; justify-content: center; min-width: auto; }}
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="logo">♫ Velocity Club</div>
            <a href="/" class="new-search">← New Search</a>
        </header>
        
        <h2>Search Results for "{song}"</h2>
        <p class="subtitle">Showing top results</p>
        
        {songs_html}
        
        <a href="/" style="display:block; text-align:center; margin:40px auto; color:#c026d3; text-decoration:none; font-weight:600;">← Search Again</a>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
    
