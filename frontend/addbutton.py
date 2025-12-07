with open('pages/file_manager.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add recycle bin button
old_btn = '<button class="btn btn-outline" id="refreshFiles">Refresh</button>'
new_btns = '''<button class="btn btn-outline" onclick="window.location.href='recycle_bin.html'">🗑️ Recycle Bin</button>
                    <button class="btn btn-outline" id="refreshFiles">Refresh</button>'''

content = content.replace(old_btn, new_btns)

with open('pages/file_manager.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added recycle bin button')
