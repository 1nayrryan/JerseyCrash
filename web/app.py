from flask import Flask, render_template, jsonify, send_from_directory
import os
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'output', 'summaries')
CHARTS_DIR = os.path.join(ROOT, 'output', 'charts')


def list_csvs():
    if not os.path.isdir(DATA_DIR):
        return []
    return [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]


@app.route('/')
def index():
    files = list_csvs()
    return render_template('index.html', files=files)


@app.route('/table/<filename>')
def table(filename):
    if '..' in filename or filename.endswith('/'):
        return "Invalid filename", 400
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return "Not found", 404
    df = pd.read_csv(path)

    # Select only the three desired columns (title, year, crashes) if present.
    # Map common column names to canonical names.
    col_map = {}
    if 'Title' in df.columns:
        col_map['Title'] = 'Title'
    if 'County' in df.columns:
        col_map['County'] = 'Title'
    if 'Year' in df.columns:
        col_map['Year'] = 'Year'
    if 'Crashes' in df.columns:
        col_map['Crashes'] = 'Count of Crashes'
    if 'Count' in df.columns and 'Crashes' not in df.columns:
        col_map['Count'] = 'Count of Crashes'

    # Keep only columns that we mapped, in the order Title, Year, Count of Crashes
    desired = []
    for src, dst in [('Title', 'Title'), ('Year', 'Year'), ('Count of Crashes', 'Count of Crashes')]:
        # find source column name that maps to this destination
        found = None
        for k, v in col_map.items():
            if v == dst:
                found = k
                break
        if found:
            desired.append(found)

    if not desired:
        # fallback: show the full table if we couldn't find expected columns
        table_html = df.to_html(classes='table table-striped', index=False, border=0)
        return render_template('table.html', table_html=table_html, filename=filename)

    df_display = df.loc[:, desired].copy()

    # Normalize and format columns
    # Rename columns for display
    rename_map = {}
    if 'County' in df_display.columns or 'Title' in df_display.columns:
        # whichever exists, present as 'Title'
        src = 'County' if 'County' in df_display.columns else 'Title'
        rename_map[src] = 'Title'
    if 'Year' in df_display.columns:
        rename_map['Year'] = 'Year'
    # crashes column could be named 'Crashes' or 'Count'
    for c in ['Crashes', 'Count']:
        if c in df_display.columns:
            rename_map[c] = 'Count of Crashes'

    # Format Year as integer (where possible) and Crashes with thousands separator
    if 'Year' in df_display.columns:
        try:
            df_display['Year'] = df_display['Year'].astype('Int64')
        except Exception:
            pass

    for c in list(df_display.columns):
        if c in ('Crashes', 'Count'):
            # coerce to numeric then format
            df_display[c] = pd.to_numeric(df_display[c], errors='coerce')
            df_display[c] = df_display[c].apply(lambda v: f"{int(v):,}" if pd.notna(v) else '')

    df_display = df_display.rename(columns=rename_map)
    # Ensure column order: Title, Year, Count of Crashes
    final_cols = [c for c in ['Title', 'Year', 'Count of Crashes'] if c in df_display.columns]
    df_display = df_display.loc[:, final_cols]

    table_html = df_display.to_html(classes='table table-striped', index=False, border=0, escape=False)
    return render_template('table.html', table_html=table_html, filename=filename)


@app.route('/plots')
def plots_index():
    # List available matplotlib-generated PNGs from output/charts
    imgs = []
    if os.path.isdir(CHARTS_DIR):
        imgs = [f for f in os.listdir(CHARTS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        imgs.sort()
    return render_template('plots.html', images=imgs)


@app.route('/plots/image/<path:filename>')
def plots_image(filename):
    # Serve image files from the charts output folder
    if '..' in filename or filename.startswith('/'):
        return "Invalid filename", 400
    if not os.path.exists(os.path.join(CHARTS_DIR, filename)):
        return "Not found", 404
    return send_from_directory(CHARTS_DIR, filename)


@app.route('/data/<filename>')
def data(filename):
    if '..' in filename or filename.endswith('/'):
        return jsonify([]), 400
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return jsonify([]), 404
    df = pd.read_csv(path)
    return jsonify(df.to_dict(orient='records'))


@app.route('/chart/<filename>')
def chart(filename):
    if '..' in filename or filename.endswith('/'):
        return "Invalid filename", 400
    return render_template('chart.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
