// System Calls Module

// Load Stats
async function loadStats() {
    try {
        const response = await systemCallsAPI.getStats();

        if (response.success) {
            const stats = response.data;

            document.getElementById('totalCommands').textContent = stats.total_commands;
            document.getElementById('successfulCommands').textContent = stats.successful;
            document.getElementById('failedCommands').textContent = stats.failed;
            document.getElementById('recentCommands').textContent = stats.recent_24h;
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Load Command History
async function loadHistory() {
    const container = document.getElementById('historyContainer');
    if (!container) return;

    try {
        const response = await systemCallsAPI.getHistory(20);

        if (response.success && response.data.history.length > 0) {
            container.innerHTML = response.data.history.map(cmd => `
                <div class="card mb-2" style="padding: var(--spacing-sm);">
                    <div class="flex-between">
                        <code style="flex: 1;">${cmd.command}</code>
                        <span class="badge badge-${cmd.status === 'success' ? 'success' : 'danger'}">
                            ${cmd.status}
                        </span>
                    </div>
                    <div class="text-muted" style="font-size: 0.85rem; margin-top: 0.5rem;">
                        ${timeAgo(cmd.executed_at)}
                    </div>
                    ${cmd.output ? `
                        <details style="margin-top: 0.5rem;">
                            <summary style="cursor: pointer; color: var(--primary);">View Output</summary>
                            <pre style="margin-top: 0.5rem; padding: 0.5rem; background: var(--bg-primary); border-radius: var(--radius-sm); font-size: 0.85rem; overflow-x: auto;">${cmd.output}</pre>
                        </details>
                    ` : ''}
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-center text-muted">No command history yet</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="text-center text-danger">Failed to load history</p>';
        console.error('Failed to load history:', error);
    }
}

// Load Allowed Commands
async function loadAllowedCommands() {
    try {
        const response = await systemCallsAPI.getAllowedCommands();

        if (response.success) {
            const commandsList = document.getElementById('allowedCommandsList');
            if (commandsList) {
                commandsList.innerHTML = response.data.commands.map(cmd => `
                    <div class="badge badge-primary" style="padding: var(--spacing-sm); font-size: 1rem;">
                        ${cmd}
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Failed to load allowed commands:', error);
    }
}

// Execute Command
async function executeCommand(command) {
    const executeBtn = document.getElementById('executeBtn');
    const outputDiv = document.getElementById('commandOutput');
    const outputContent = document.getElementById('outputContent');
    const outputStatus = document.getElementById('outputStatus');
    const outputTime = document.getElementById('outputTime');

    // Show loading state
    if (executeBtn) {
        executeBtn.classList.add('btn-loading');
        executeBtn.disabled = true;
    }

    try {
        const response = await systemCallsAPI.execute(command);

        if (response.success) {
            const result = response.data;

            // Show output
            if (outputDiv) outputDiv.classList.remove('hidden');
            if (outputContent) outputContent.textContent = result.output;
            if (outputStatus) {
                outputStatus.textContent = result.status;
                outputStatus.className = `badge badge-${result.status === 'success' ? 'success' : 'danger'}`;
            }
            if (outputTime) outputTime.textContent = 'Just now';

            showToast('Command executed successfully', 'success');

            // Reload stats and history
            loadStats();
            loadHistory();
        }
    } catch (error) {
        showToast(error.message || 'Command execution failed', 'error');
    } finally {
        if (executeBtn) {
            executeBtn.classList.remove('btn-loading');
            executeBtn.disabled = false;
        }
    }
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Command Form
    const commandForm = document.getElementById('commandForm');
    if (commandForm) {
        commandForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const commandInput = document.getElementById('commandInput');
            if (commandInput && commandInput.value.trim()) {
                await executeCommand(commandInput.value.trim());
            }
        });
    }

    // Show Allowed Commands
    const showAllowedBtn = document.getElementById('showAllowedCommands');
    if (showAllowedBtn) {
        showAllowedBtn.addEventListener('click', () => {
            openModal('allowedCommandsModal');
        });
    }

    // Close Allowed Commands Modal
    const closeAllowedBtn = document.getElementById('closeAllowedCommands');
    if (closeAllowedBtn) {
        closeAllowedBtn.addEventListener('click', () => {
            closeModal('allowedCommandsModal');
        });
    }

    // Refresh History
    const refreshHistoryBtn = document.getElementById('refreshHistory');
    if (refreshHistoryBtn) {
        refreshHistoryBtn.addEventListener('click', () => {
            loadHistory();
            showToast('History refreshed', 'info');
        });
    }
});
