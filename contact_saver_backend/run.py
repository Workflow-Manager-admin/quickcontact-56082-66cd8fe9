from app import app

if __name__ == "__main__":
    # Run with debug=True to get detailed logging of all actions (including error traces and prints above)
    app.run(host="0.0.0.0", port=3001, debug=True)
