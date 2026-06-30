from pathlib import Path

file_path = Path("pages/file_manager.html")

# Read HTML content
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Existing refresh button
old_button = '<button class="btn btn-outline" id="refreshFiles">Refresh</button>'

# New buttons
new_buttons = '''
<button class="btn btn-outline" onclick="window.location.href=\'recycle_bin.html\'">
    🗑️ Recycle Bin
</button>

<button class="btn btn-outline" id="refreshFiles">
    Refresh
</button>
'''

# Replace button safely
if old_button in content:
    content = content.replace(old_button, new_buttons)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Recycle Bin button added successfully!")

else:
    print("❌ Refresh button not found.")

