// File Manager JavaScript - Updated with AppLock

let currentSort = { field: 'date', order: 'desc' };

function toggleSortMenu() {
    const menu = document.getElementById('sortMenu');
    if (menu) {
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
}

function sortFiles(field) {
    if (currentSort.field === field) {
        currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.field = field;
        currentSort.order = field === 'date' ? 'desc' : 'asc';
    }

    // Update button text to show arrow
    const btn = document.querySelector('button[onclick="toggleSortMenu()"]');
    if (btn) {
        const arrow = currentSort.order === 'asc' ? '⬆️' : '⬇️';
        const label = field.charAt(0).toUpperCase() + field.slice(1);
        btn.textContent = `Sort: ${label} ${arrow}`;
    }

    const menu = document.getElementById('sortMenu');
    if (menu) menu.style.display = 'none';

    loadFileList();
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    const menu = document.getElementById('sortMenu');
    const btn = document.querySelector('button[onclick="toggleSortMenu()"]');
    if (menu && btn && !menu.contains(e.target) && !btn.contains(e.target)) {
        menu.style.display = 'none';
    }
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadFileList();

    // Create File Form
    const createFileForm = document.getElementById('createFileForm');
    if (createFileForm) {
        createFileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const filename = document.getElementById('newFilename').value;
            const content = document.getElementById('newFileContent').value;

            try {
                await fileManagerAPI.createFile(filename, content);
                showToast('File created successfully', 'success');
                closeModal('createFileModal');
                createFileForm.reset();
                loadFileList();
            } catch (error) {
                showToast(error.message, 'error');
            }
        });
    }

    // Upload File Form
    const uploadFileForm = document.getElementById('uploadFileForm');
    const encryptionOption = document.getElementById('encryptionOption');
    const passcodeGroup = document.getElementById('passcodeGroup');
    const appLockOption = document.getElementById('appLockOption');
    const appLockPasscodeGroup = document.getElementById('appLockPasscodeGroup');

    if (encryptionOption) {
        encryptionOption.addEventListener('change', () => {
            passcodeGroup.style.display = encryptionOption.value === 'encrypt' ? 'block' : 'none';
        });
    }

    if (appLockOption) {
        appLockOption.addEventListener('change', () => {
            appLockPasscodeGroup.style.display = appLockOption.checked ? 'block' : 'none';
        });
    }

    if (uploadFileForm) {
        uploadFileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('uploadFileInput');
            const file = fileInput.files[0];
            const encrypt = document.getElementById('encryptionOption').value === 'encrypt';
            const passcode = document.getElementById('encryptionPasscode').value;

            const applock = document.getElementById('appLockOption').checked;
            const applockPasscode = document.getElementById('appLockPasscode').value;

            // Get permissions
            const permissions = {
                view: document.getElementById('permView').checked,
                download: document.getElementById('permDownload').checked,
                edit: document.getElementById('permEdit').checked,
                delete: document.getElementById('permDelete').checked
            };

            if (!file) return;

            if (encrypt && !passcode) {
                showToast('Please enter a passcode for encryption', 'error');
                return;
            }

            if (applock && !applockPasscode) {
                showToast('Please enter a passcode for AppLock', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);
            formData.append('encrypt', encrypt);
            formData.append('permissions', JSON.stringify(permissions));
            if (encrypt) {
                formData.append('passcode', passcode);
            }

            formData.append('applock', applock);
            if (applock) {
                formData.append('applock_passcode', applockPasscode);
            }

            try {
                const result = await fileManagerAPI.uploadFile(formData);
                if (result.success) {
                    let msg = 'File uploaded successfully';
                    if (result.data.encrypted) msg = `File encrypted and uploaded as ${result.data.filename}`;
                    if (result.data.locked) msg += ' (Locked)';

                    showToast(msg, 'success');
                    closeModal('uploadFileModal');
                    uploadFileForm.reset();
                    passcodeGroup.style.display = 'none';
                    appLockPasscodeGroup.style.display = 'none';
                    loadFileList();
                } else {
                    throw new Error(result.error);
                }
            } catch (error) {
                showToast(error.message, 'error');
            }
        });
    }

    // Refresh Button
    const refreshBtn = document.getElementById('refreshFiles');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadFileList);
    }
});

async function loadFileList() {
    const container = document.getElementById('fileList');
    container.innerHTML = '<div class="text-center"><div class="spinner"></div><p>Loading files...</p></div>';

    try {
        const response = await fileManagerAPI.listFiles();
        let files = response.data.files;

        if (files.length === 0) {
            container.innerHTML = '<div class="text-center text-muted"><p>No files found.</p></div>';
            return;
        }

        // Sort files
        files.sort((a, b) => {
            let valA, valB;

            if (currentSort.field === 'name') {
                valA = a.name.toLowerCase();
                valB = b.name.toLowerCase();
            } else if (currentSort.field === 'size') {
                valA = a.size;
                valB = b.size;
            } else { // date
                valA = a.modified;
                valB = b.modified;
            }

            if (valA < valB) return currentSort.order === 'asc' ? -1 : 1;
            if (valA > valB) return currentSort.order === 'asc' ? 1 : -1;
            return 0;
        });

        container.innerHTML = '';

        // Check user role
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const isAdmin = user.role === 'admin';

        const fragment = document.createDocumentFragment();

        // SVG Icons
        const icons = {
            view: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`,
            edit: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>`,
            download: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>`,
            delete: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`,
            lock: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>`,
            file: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>`
        };

        files.forEach(file => {
            const date = new Date(file.modified * 1000).toLocaleString();
            const size = formatBytes(file.size);

            // Get permissions for this file
            const perms = file.permissions || {};

            // Determine if buttons should be shown
            const showEdit = isAdmin || perms.edit;
            const showDelete = isAdmin || perms.delete;
            const showDownload = isAdmin || perms.download !== false; // default true
            const showView = isAdmin || perms.view !== false; // default true

            const isLocked = perms.is_locked;

            const card = document.createElement('div');
            card.className = 'file-card';
            card.innerHTML = `
                <div class="file-icon">${isLocked ? icons.lock : icons.file}</div>
                <div class="file-info">
                    <div class="file-name">
                        ${file.name}
                        ${isLocked ? '<span class="badge badge-warning" style="font-size: 0.7em; margin-left: 5px;">LOCKED</span>' : ''}
                    </div>
                    <div class="file-meta">${size} • ${date}</div>
                    <div class="file-permissions-indicator">
                        <span class="perm-badge ${perms.view ? 'enabled' : 'disabled'}" title="View ${perms.view ? 'enabled' : 'disabled'}">${icons.view}</span>
                        <span class="perm-badge ${perms.download ? 'enabled' : 'disabled'}" title="Download ${perms.download ? 'enabled' : 'disabled'}">${icons.download}</span>
                        <span class="perm-badge ${perms.edit ? 'enabled' : 'disabled'}" title="Edit ${perms.edit ? 'enabled' : 'disabled'}">${icons.edit}</span>
                        <span class="perm-badge ${perms.delete ? 'enabled' : 'disabled'}" title="Delete ${perms.delete ? 'enabled' : 'disabled'}">${icons.delete}</span>
                    </div>
                </div>
                <div class="file-actions">
                    ${showView ? `<button class="btn btn-icon btn-outline" onclick="viewFile('${file.name}')" title="View">${icons.view}</button>` : ''}
                    ${showEdit ? `<button class="btn btn-icon btn-outline" onclick="editFile('${file.name}')" title="Edit">${icons.edit}</button>` : ''}
                    ${showDownload ? `<button class="btn btn-icon btn-outline" onclick="downloadFile('${file.name}')" title="Download">${icons.download}</button>` : ''}
                    ${showDelete ? `<button class="btn btn-icon btn-danger" onclick="deleteFile('${file.name}')" title="Delete">${icons.delete}</button>` : ''}
                </div>
            `;
            fragment.appendChild(card);
        });

        container.appendChild(fragment);

    } catch (error) {
        container.innerHTML = `<div class="text-center text-danger"><p>Error loading files: ${error.message}</p></div>`;
    }
}

async function getPermissions(filename) {
    try {
        const response = await fetch(`${API_BASE_URL}/files/permissions/${encodeURIComponent(filename)}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const result = await response.json();
        if (result.success) {
            return result.data;
        }
        return {};
    } catch (error) {
        console.error('Permission check failed:', error);
        return {};
    }
}

async function handleLockedError(error, retryCallback) {
    if (error.data && error.data.locked) {
        const modal = document.getElementById('unlockFileModal');
        const input = document.getElementById('unlockPasscode');
        const btn = document.getElementById('unlockBtn');

        input.value = '';
        openModal('unlockFileModal');

        return new Promise((resolve, reject) => {
            // Remove any existing listeners to avoid duplicates
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);

            newBtn.onclick = async () => {
                const passcode = input.value;
                if (!passcode) {
                    showToast('Please enter a passcode', 'error');
                    return;
                }

                try {
                    closeModal('unlockFileModal');
                    await retryCallback(passcode);
                    resolve(true);
                } catch (retryError) {
                    if (retryError.data && retryError.data.locked) {
                        showToast('Incorrect passcode', 'error');
                        // Optionally reopen modal here if desired
                    } else {
                        showToast(retryError.message, 'error');
                    }
                    resolve(false);
                }
            };
        });
    }
    return false;
}

async function viewFile(filename) {
    const perms = await getPermissions(filename);
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    // Check view permission
    if (user.role !== 'admin' && perms.view === false) {
        showToast('🚫 Permission Denied: You do not have permission to view this file', 'error');
        return;
    }

    // Check lock
    if (perms.is_locked) {
        // Prompt for passcode
        const modal = document.getElementById('unlockFileModal');
        const input = document.getElementById('unlockPasscode');
        const btn = document.getElementById('unlockBtn');

        input.value = '';
        openModal('unlockFileModal');

        // Handle unlock
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.onclick = async () => {
            const passcode = input.value;
            if (!passcode) {
                showToast('Please enter a passcode', 'error');
                return;
            }

            // Verify passcode
            try {
                newBtn.disabled = true;
                newBtn.textContent = 'Verifying...';

                // We use readFile to verify. It will throw if passcode is wrong.
                await fileManagerAPI.readFile(filename, passcode);

                sessionStorage.setItem(`file_passcode_${filename}`, passcode);
                closeModal('unlockFileModal');

                const viewerUrl = `viewer.html?file=${encodeURIComponent(filename)}`;
                window.open(viewerUrl, '_blank');
            } catch (error) {
                showToast('Incorrect passcode', 'error');
            } finally {
                newBtn.disabled = false;
                newBtn.textContent = 'Unlock';
            }
        };
        return;
    }

    const viewerUrl = `viewer.html?file=${encodeURIComponent(filename)}`;
    window.open(viewerUrl, '_blank');
}

async function editFile(filename) {
    const perms = await getPermissions(filename);
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    // Check edit permission
    if (user.role !== 'admin' && perms.edit === false) {
        showToast('🚫 Permission Denied: You do not have permission to edit this file', 'error');
        return;
    }

    // Check lock
    if (perms.is_locked) {
        const modal = document.getElementById('unlockFileModal');
        const input = document.getElementById('unlockPasscode');
        const btn = document.getElementById('unlockBtn');

        input.value = '';
        openModal('unlockFileModal');

        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.onclick = async () => {
            const passcode = input.value;
            if (!passcode) {
                showToast('Please enter a passcode', 'error');
                return;
            }

            try {
                newBtn.disabled = true;
                newBtn.textContent = 'Verifying...';

                await fileManagerAPI.readFile(filename, passcode);

                sessionStorage.setItem(`file_passcode_${filename}`, passcode);
                closeModal('unlockFileModal');

                const editorUrl = `editor.html?file=${encodeURIComponent(filename)}`;
                window.open(editorUrl, '_blank');
            } catch (error) {
                showToast('Incorrect passcode', 'error');
            } finally {
                newBtn.disabled = false;
                newBtn.textContent = 'Unlock';
            }
        };
        return;
    }

    const editorUrl = `editor.html?file=${encodeURIComponent(filename)}`;
    window.open(editorUrl, '_blank');
}

async function deleteFile(filename) {
    const perms = await getPermissions(filename);
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (user.role !== 'admin' && perms.delete === false) {
        showToast('🚫 Permission Denied: You do not have permission to delete this file', 'error');
        return;
    }

    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;

    // Check lock
    if (perms.is_locked) {
        const modal = document.getElementById('unlockFileModal');
        const input = document.getElementById('unlockPasscode');
        const btn = document.getElementById('unlockBtn');

        input.value = '';
        openModal('unlockFileModal');

        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.onclick = async () => {
            const passcode = input.value;
            if (!passcode) {
                showToast('Please enter a passcode', 'error');
                return;
            }

            try {
                newBtn.disabled = true;
                newBtn.textContent = 'Verifying...';

                // Verify passcode by attempting delete
                await fileManagerAPI.deleteFile(filename, passcode);

                showToast('File deleted successfully', 'success');
                closeModal('unlockFileModal');
                loadFileList();
            } catch (error) {
                if (error.data && error.data.locked) {
                    showToast('Incorrect passcode', 'error');
                } else {
                    showToast(error.message, 'error');
                }
            } finally {
                newBtn.disabled = false;
                newBtn.textContent = 'Unlock';
            }
        };
        return;
    }

    // Not locked, proceed normally
    try {
        await fileManagerAPI.deleteFile(filename);
        showToast('File deleted successfully', 'success');
        loadFileList();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function downloadFile(filename) {
    const perms = await getPermissions(filename);
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (user.role !== 'admin' && perms.download === false) {
        showToast('🚫 Permission Denied: You do not have permission to download this file', 'error');
        return;
    }

    const performDownload = async (passcode = null) => {
        const blob = await fileManagerAPI.downloadFile(filename, passcode);
        const blobUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
        showToast('File downloaded successfully', 'success');
    };

    try {
        await performDownload();
    } catch (error) {
        const handled = await handleLockedError(error, performDownload);
        if (!handled && (!error.data || !error.data.locked)) {
            showToast('Download failed: ' + error.message, 'error');
        }
    }
}


function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}
