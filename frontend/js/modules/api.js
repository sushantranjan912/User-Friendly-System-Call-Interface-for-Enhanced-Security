// API Communication Module
const API_BASE_URL = window.API_BASE_URL || `${window.location.origin}/api`;
const REQUEST_TIMEOUT_MS = 10000;

function createApiError(message, status = 0, data = null) {
    const error = new Error(message);
    error.status = status;
    if (data) {
        error.data = data;
    }
    return error;
}

function getFriendlyErrorMessage(status, serverMessage) {
    switch (status) {
        case 400:
            return serverMessage || 'Invalid request. Please check your input.';
        case 401:
            return serverMessage || 'Unauthorized. Please login again.';
        case 403:
            return serverMessage || 'Forbidden. You do not have permission to access this resource.';
        case 404:
            return serverMessage || 'Server unavailable or endpoint not found.';
        case 409:
            return serverMessage || 'Resource conflict. Please review your request.';
        case 500:
            return serverMessage || 'Unexpected server error. Please try again later.';
        default:
            return serverMessage || 'Request failed. Please try again.';
    }
}

function normalizeFetchError(error) {
    if (error.name === 'AbortError') {
        return createApiError('Request timed out. Please try again.', 0);
    }

    if (error instanceof TypeError) {
        return createApiError('Network connection failed. Please check your internet connection or server status.', 0);
    }

    return error.status ? error : createApiError(error.message || 'Unexpected network error.', 0);
}

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        },
        signal: controller.signal
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const contentType = response.headers.get('content-type') || '';
        const data = contentType.includes('application/json') ? await response.json() : null;

        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }

            const message = (data && data.error) ? data.error : getFriendlyErrorMessage(response.status, response.statusText);
            throw createApiError(message, response.status, data);
        }

        return data;
    } catch (error) {
        throw normalizeFetchError(error);
    } finally {
        clearTimeout(timeoutId);
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

    async login(email, password) {
        return apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
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
