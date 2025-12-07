// API Communication Module
const API_BASE_URL = 'http://localhost:5000/api';

// API Helper Function
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };

    const config = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/';
                return;
            }
            const error = new Error(data.error || 'Request failed');
            error.data = data;
            throw error;
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication API
const authAPI = {
    async register(username, email, password, role = 'user') {
        return apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, role })
        });
    },

    async login(username, password) {
        return apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    async logout() {
        return apiRequest('/auth/logout', {
            method: 'POST'
        });
    }
};

// System Calls API
const systemCallsAPI = {
    async execute(command) {
        return apiRequest('/system/execute', {
            method: 'POST',
            body: JSON.stringify({ command })
        });
    },

    async getHistory(limit = 50, offset = 0) {
        return apiRequest(`/system/history?limit=${limit}&offset=${offset}`);
    },

    async getAllowedCommands() {
        return apiRequest('/system/allowed-commands');
    },

    async getStats() {
        return apiRequest('/system/stats');
    }
};

// Logs API
const logsAPI = {
    async getLogs(limit = 100, offset = 0, actionType = null) {
        let url = `/logs?limit=${limit}&offset=${offset}`;
        if (actionType) {
            url += `&action_type=${actionType}`;
        }
        return apiRequest(url);
    },

    async getLogTypes() {
        return apiRequest('/logs/types');
    },

    async getLogStats() {
        return apiRequest('/logs/stats');
    }
};

// File Manager API
const fileManagerAPI = {
    async listFiles() {
        return apiRequest('/files/');
    },

    async createFile(filename, content) {
        return apiRequest('/files/', {
            method: 'POST',
            body: JSON.stringify({ filename, content })
        });
    },

    async readFile(filename, passcode = null) {
        const headers = {};
        if (passcode) headers['X-File-Passcode'] = passcode;
        return apiRequest(`/files/${encodeURIComponent(filename)}`, { headers });
    },

    async updateFile(filename, content, passcode = null) {
        const headers = {};
        if (passcode) headers['X-File-Passcode'] = passcode;
        return apiRequest(`/files/${encodeURIComponent(filename)}`, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify({ content })
        });
    },

    async deleteFile(filename, passcode = null) {
        const headers = {};
        if (passcode) headers['X-File-Passcode'] = passcode;
        return apiRequest(`/files/${encodeURIComponent(filename)}`, {
            method: 'DELETE',
            headers: headers
        });
    },

    async uploadFile(formData) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/files/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        return response.json();
    },

    async downloadFile(filename, passcode = null) {
        const token = localStorage.getItem('token');
        const headers = {
            'Authorization': `Bearer ${token}`
        };
        if (passcode) headers['X-File-Passcode'] = passcode;

        const response = await fetch(`${API_BASE_URL}/files/download/${encodeURIComponent(filename)}`, {
            headers: headers
        });

        if (!response.ok) {
            const data = await response.json();
            // Pass the error data object to handle specific error codes like 'locked'
            const error = new Error(data.error || 'Download failed');
            error.data = data;
            throw error;
        }

        return response.blob();
    }
};

// Recycle Bin API
const recycleBinAPI = {
    async list() {
        return apiRequest('/recycle-bin/');
    },

    async restore(filename) {
        return apiRequest(`/recycle-bin/restore/${encodeURIComponent(filename)}`, {
            method: 'POST'
        });
    },

    async permanentlyDelete(filename) {
        return apiRequest(`/recycle-bin/delete/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
    },

    async empty() {
        return apiRequest('/recycle-bin/empty', {
            method: 'POST'
        });
    }
};
