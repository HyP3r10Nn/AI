from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
FILENAME = "brain_memory.json"

def load_memories():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_memories(memories):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    memories = load_memories()
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        tags = request.form.get("tags", "").lower().split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]

        if text and not any(mem["text"] == text for mem in memories):
            new_entry = {
                "text": text,
                "tags": tags,
                "timestamp": datetime.now().isoformat()
            }
            memories.append(new_entry)
            save_memories(memories)
            return redirect(url_for("index"))

    query = request.args.get("query", "").strip().lower()
    tagsearch = request.args.get("tag", "").strip().lower()

    if query:
        memories = [m for m in memories if query in m["text"].lower()]
    if tagsearch:
        memories = [m for m in memories if tagsearch in m["tags"]]

    return render_template("index.html", memories=memories, query=query, tagsearch=tagsearch)

@app.route("/delete/<int:index>")
def delete(index):
    memories = load_memories()
    if 0 <= index < len(memories):
        memories.pop(index)
        save_memories(memories)
    return redirect(url_for("index"))

@app.route("/clear")
def clear():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
