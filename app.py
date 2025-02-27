from flask import Flask, request, jsonify
from pygame import mixer
import os

app = Flask(__name__)
mixer.init()

music_dir = None

@app.route("/set-folder", methods=["POST"])
def set_folder():
    global music_dir
    data = request.json
    path = data.get("path")
    
    if not path or not os.path.exists(path):
        return jsonify({"error": "Invalid path"}), 400

    music_dir = path
    songs = [song for song in os.listdir(path) if song.endswith(".mp3")]
    return jsonify({"songs": songs})

@app.route("/play", methods=["POST"])
def play_song():
    if not music_dir:
        return jsonify({"error": "Music folder not set"}), 400

    data = request.json
    song_name = data.get("song")
    song_path = os.path.join(music_dir, song_name)

    if not os.path.exists(song_path):
        return jsonify({"error": "Song not found"}), 404

    mixer.music.load(song_path)
    mixer.music.play()
    return jsonify({"message": f"Playing {song_name}"})

@app.route("/stop", methods=["POST"])
def stop_song():
    mixer.music.stop()
    return jsonify({"message": "Music stopped"})

@app.route("/pause", methods=["POST"])
def pause_song():
    mixer.music.pause()
    return jsonify({"message": "Music paused"})

@app.route("/resume", methods=["POST"])
def resume_song():
    mixer.music.unpause()
    return jsonify({"message": "Music resumed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
