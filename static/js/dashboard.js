// Caregiver Dashboard JavaScript

class Dashboard {
    constructor() {
        this.socket = null;
        this.currentTab = 'medications';
        this.medications = [];
        this.history = [];
        
        this.initializeSocket();
        this.initializeUI();
        this.loadMedications();
        this.loadHistory();
    }

    initializeSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to MedMitra server');
        });
        
        this.socket.on('medication_reminder', (data) => {
            // Update history when reminder is sent
            this.loadHistory();
        });
        
        this.socket.on('medication_taken', (data) => {
            // Update history when medication is taken
            this.loadHistory();
        });
        
        this.socket.on('medication_added', (data) => {
            // Reload medications when new one is added
            this.loadMedications();
        });
        
        this.socket.on('medication_deleted', (data) => {
            // Reload medications when one is deleted
            this.loadMedications();
        });
    }

    initializeUI() {
        // Tab switching
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });

        // Add medication button
        document.getElementById('addMedicationBtn').addEventListener('click', () => {
            this.openMedicationModal();
        });

        // Modal controls
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeMedicationModal();
        });

        document.getElementById('cancelBtn').addEventListener('click', () => {
            this.closeMedicationModal();
        });

        // Medication form
        document.getElementById('medicationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addMedication();
        });

        // History filter
        document.getElementById('historyFilter').addEventListener('change', (e) => {
            this.filterHistory(e.target.value);
        });

        // Copy patient link
        document.getElementById('copyLinkBtn').addEventListener('click', () => {
            this.copyPatientLink();
        });

        // Show instructions button
        const showInstructionsBtn = document.getElementById('showInstructionsBtn');
        if (showInstructionsBtn) {
            showInstructionsBtn.addEventListener('click', () => {
                // Show instructions in an alert or modal
                const instructions = `
📱 PATIENT MOBILE SETUP INSTRUCTIONS

1. Make sure patient's phone is on the SAME Wi-Fi network as this computer

2. Share the patient app link (shown above) via:
   - WhatsApp
   - SMS
   - Email
   - Or show on screen for patient to type

3. Patient opens link in mobile browser:
   - Chrome (Android) or Safari (iOS)
   - Type or paste the link
   - Press Go

4. Patient installs app:
   - Android: Menu (3 dots) → Add to Home Screen
   - iPhone: Share button → Add to Home Screen

5. Patient grants microphone permission when asked

💡 TIP: Generate a QR code for easier access!
   Use any online QR code generator with the link above.

For detailed instructions, see: PATIENT_MOBILE_SETUP.md
                `;
                alert(instructions);
            });
        }

        // Set patient link
        const patientLink = window.location.origin + '/';
        document.getElementById('patientLink').value = patientLink;

        // Close modal on outside click
        document.getElementById('medicationModal').addEventListener('click', (e) => {
            if (e.target.id === 'medicationModal') {
                this.closeMedicationModal();
            }
        });
    }

    switchTab(tabName) {
        this.currentTab = tabName;
        
        // Update tab buttons
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    async loadMedications() {
        try {
            const response = await fetch('/api/medications');
            const data = await response.json();
            this.medications = data.medications;
            this.renderMedications();
        } catch (error) {
            console.error('Error loading medications:', error);
        }
    }

    renderMedications() {
        const grid = document.getElementById('medicationsGrid');
        
        if (this.medications.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">No medications scheduled</p>
                    <p>Click "Add Medication" to create a schedule</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.medications.map(med => `
            <div class="medication-card">
                <div class="medication-header">
                    <div>
                        <h3 class="medication-name">${this.escapeHtml(med.name)}</h3>
                        <p class="medication-dosage">${this.escapeHtml(med.dosage)}</p>
                    </div>
                    <div class="medication-time">
                        <span>🕐</span>
                        <span>${med.time_slot}</span>
                    </div>
                </div>
                <div class="medication-info">
                    <div class="info-item">
                        <span class="info-label">Patient:</span>
                        <span class="info-value">${this.escapeHtml(med.user_name)}</span>
                    </div>
                    ${med.doctor_instructions ? `
                        <div class="info-item">
                            <span class="info-label">Instructions:</span>
                            <span class="info-value">${this.escapeHtml(med.doctor_instructions)}</span>
                        </div>
                    ` : ''}
                </div>
                <button class="delete-btn" onclick="dashboard.deleteMedication('${med.name}')">
                    Delete Medication
                </button>
            </div>
        `).join('');
    }

    async addMedication() {
        const formData = {
            name: document.getElementById('medName').value,
            dosage: document.getElementById('medDosage').value,
            time_slot: document.getElementById('medTimeSlot').value,
            doctor_instructions: document.getElementById('medInstructions').value,
            user_name: document.getElementById('medUserName').value
        };

        try {
            const response = await fetch('/api/medications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (data.success) {
                this.closeMedicationModal();
                this.loadMedications();
                // Reset form
                document.getElementById('medicationForm').reset();
            } else {
                alert('Error: ' + (data.error || 'Failed to add medication'));
            }
        } catch (error) {
            console.error('Error adding medication:', error);
            alert('Failed to add medication. Please try again.');
        }
    }

    async deleteMedication(medName) {
        if (!confirm(`Are you sure you want to delete ${medName}?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/medications/${encodeURIComponent(medName)}`, {
                method: 'DELETE'
            });

            const data = await response.json();
            
            if (data.success) {
                this.loadMedications();
            } else {
                alert('Error: ' + (data.error || 'Failed to delete medication'));
            }
        } catch (error) {
            console.error('Error deleting medication:', error);
            alert('Failed to delete medication. Please try again.');
        }
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            this.history = data.history || [];
            this.renderHistory();
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    renderHistory() {
        const list = document.getElementById('historyList');
        
        if (this.history.length === 0) {
            list.innerHTML = `
                <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <p style="font-size: 1.1rem;">No medication history yet</p>
                </div>
            `;
            return;
        }

        list.innerHTML = this.history.map(record => {
            const date = new Date(record.scheduled_time);
            const status = record.taken ? 'taken' : (record.missed ? 'missed' : 'pending');
            const statusText = record.taken ? 'Taken' : (record.missed ? 'Missed' : 'Pending');
            
            return `
                <div class="history-item">
                    <div class="history-info">
                        <h3 class="history-medication">${this.escapeHtml(record.medication_name)} - ${this.escapeHtml(record.dosage)}</h3>
                        <p class="history-time">
                            Scheduled: ${date.toLocaleString()}
                            ${record.taken_time ? ` | Taken: ${new Date(record.taken_time).toLocaleString()}` : ''}
                        </p>
                    </div>
                    <div class="history-status status-${status}">
                        ${statusText}
                    </div>
                </div>
            `;
        }).join('');
    }

    filterHistory(filter) {
        // This would filter the history based on the filter value
        // For now, we'll just reload all history
        this.loadHistory();
    }

    openMedicationModal() {
        document.getElementById('medicationModal').classList.add('active');
    }

    closeMedicationModal() {
        document.getElementById('medicationModal').classList.remove('active');
    }

    copyPatientLink() {
        const linkInput = document.getElementById('patientLink');
        linkInput.select();
        linkInput.setSelectionRange(0, 99999); // For mobile devices
        
        try {
            document.execCommand('copy');
            const btn = document.getElementById('copyLinkBtn');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        } catch (err) {
            alert('Failed to copy link. Please copy manually.');
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new Dashboard();
});

