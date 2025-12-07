// Logs Module

// Load Logs
async function loadLogs() {
    const tableBody = document.getElementById('logsTableBody');
    if (!tableBody) return;

    const limit = document.getElementById('filterLimit')?.value || 100;
    const actionType = document.getElementById('filterActionType')?.value || null;

    showLoading('logsTableBody');

    try {
        const response = await logsAPI.getLogs(limit, 0, actionType);

        if (response.success && response.data.logs.length > 0) {
            tableBody.innerHTML = response.data.logs.map(log => `
                <tr>
                    <td>${formatDate(log.created_at)}</td>
                    <td>${log.username || 'System'}</td>
                    <td><span class="badge badge-primary">${log.action_type}</span></td>
                    <td>
                        <span class="badge badge-${getStatusColor(log.status)}">
                            ${log.status}
                        </span>
                    </td>
                    <td>${log.ip_address || 'N/A'}</td>
                    <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        ${log.details || 'N/A'}
                    </td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No logs found</td></tr>';
        }
    } catch (error) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Failed to load logs</td></tr>';
        console.error('Failed to load logs:', error);
    }
}

function getStatusColor(status) {
    if (status === 'success') return 'success';
    if (status === 'suspicious') return 'warning'; // Yellow
    return 'danger'; // Red for failure/error
}

// Load Log Types for Filter
async function loadLogTypes() {
    try {
        const response = await logsAPI.getLogTypes();

        if (response.success) {
            const filterSelect = document.getElementById('filterActionType');
            if (filterSelect) {
                const options = response.data.types.map(type =>
                    `<option value="${type}">${type}</option>`
                ).join('');
                filterSelect.innerHTML = '<option value="">All Actions</option>' + options;
            }
        }
    } catch (error) {
        console.error('Failed to load log types:', error);
    }
}

// Export Logs
function exportLogs() {
    const table = document.getElementById('logsTable');
    if (!table) return;

    // Get table data
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent);

    // Create CSV
    const csv = [
        headers.join(','),
        ...rows.map(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            return cells.map(cell => `"${cell.textContent.trim()}"`).join(',');
        })
    ].join('\n');

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit_logs_${new Date().toISOString()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);

    showToast('Logs exported successfully', 'success');
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Apply Filters
    const applyFiltersBtn = document.getElementById('applyFilters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', () => {
            loadLogs();
            showToast('Filters applied', 'info');
        });
    }

    // Refresh Logs
    const refreshLogsBtn = document.getElementById('refreshLogs');
    if (refreshLogsBtn) {
        refreshLogsBtn.addEventListener('click', () => {
            loadLogs();
            showToast('Logs refreshed', 'info');
        });
    }

    // Export Logs
    const exportLogsBtn = document.getElementById('exportLogs');
    if (exportLogsBtn) {
        exportLogsBtn.addEventListener('click', exportLogs);
    }
});
