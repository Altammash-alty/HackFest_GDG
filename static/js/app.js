// MedMitra - Voice Assistant Web Client

class MedMitraClient {
    constructor() {
        this.socket = null;
        this.recognition = null;
        this.isListening = false;
        this.synthesis = window.speechSynthesis;
        this.currentUtterance = null;
        this.currentReminderMedication = null;
        this.waitingForMedicationResponse = false;
        
        this.initializeSocket();
        this.initializeVoiceRecognition();
        this.initializeUI();
    }

    initializeSocket() {
        // Connect to Flask-SocketIO server
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to MedMitra server');
            this.updateStatus('connected', 'Connected');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.updateStatus('disconnected', 'Disconnected');
        });
        
        this.socket.on('connected', (data) => {
            console.log('Server message:', data.message);
        });
        
        this.socket.on('medication_reminder', (data) => {
            this.waitingForMedicationResponse = true;
            this.handleReminder(data);
            // Show browser notification if app is in background
            this.showBrowserNotification(data);
        });
        
        this.socket.on('medmitra_response', (data) => {
            this.handleResponse(data);
        });
        
        // Request notification permission
        this.requestNotificationPermission();
        
        // Keep connection alive
        setInterval(() => {
            if (this.socket && this.socket.connected) {
                this.socket.emit('ping');
            }
        }, 30000); // Ping every 30 seconds
    }
    
    async requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            try {
                await Notification.requestPermission();
            } catch (error) {
                console.log('Notification permission request failed:', error);
            }
        }
    }
    
    showBrowserNotification(data) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const medication = data.medication;
            const notification = new Notification('🔔 Medication Reminder', {
                body: `${medication.name} ${medication.dosage} - Time to take your medication!`,
                icon: '/static/icon-192.png',
                badge: '/static/icon-192.png',
                tag: 'medication-reminder',
                requireInteraction: true,
                vibrate: [200, 100, 200]
            });
            
            notification.onclick = () => {
                window.focus();
                notification.close();
            };
            
            // Auto-close after 10 seconds
            setTimeout(() => notification.close(), 10000);
        }
    }

    initializeVoiceRecognition() {
        // Check if browser supports Web Speech API
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            try {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                this.recognition = new SpeechRecognition();
                
                this.recognition.continuous = false;
                this.recognition.interimResults = false;
                
                // Mobile-friendly language settings
                // Try to detect device language, fallback to Hindi/English
                const userLang = navigator.language || navigator.userLanguage || 'en-IN';
                if (userLang.startsWith('hi') || userLang.includes('IN')) {
                    this.recognition.lang = 'hi-IN';
                } else {
                    this.recognition.lang = 'en-IN,hi-IN'; // Try English first, then Hindi
                }
                
                // Mobile-specific settings
                if (this.isMobileDevice()) {
                    this.recognition.continuous = false; // Single utterance on mobile
                    this.recognition.maxAlternatives = 1;
                }
                
                this.recognition.onstart = () => {
                    this.isListening = true;
                    this.updateVoiceUI(true);
                    console.log('Voice recognition started');
                };
                
                this.recognition.onresult = (event) => {
                    if (event.results.length > 0 && event.results[0].length > 0) {
                        const transcript = event.results[0][0].transcript;
                        const confidence = event.results[0][0].confidence;
                        console.log('Voice input:', transcript, 'Confidence:', confidence);
                        
                        // If we're waiting for medication response, handle it immediately
                        if (this.waitingForMedicationResponse) {
                            this.handleMedicationResponse(transcript);
                        } else {
                            this.sendMessage(transcript);
                        }
                    }
                    
                    this.updateVoiceUI(false);
                };
                
                this.recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error, event);
                    this.isListening = false;
                    this.updateVoiceUI(false);
                    this.handleVoiceError(event.error);
                };
                
                this.recognition.onend = () => {
                    this.isListening = false;
                    this.updateVoiceUI(false);
                    console.log('Voice recognition ended');
                };
                
                // Test if recognition can be initialized
                console.log('Voice recognition initialized successfully');
            } catch (error) {
                console.error('Failed to initialize voice recognition:', error);
                this.showVoiceError('Voice recognition initialization failed. Please use text input.');
                this.hideVoiceButton();
            }
        } else {
            console.warn('Speech recognition not supported in this browser');
            this.showVoiceError('Voice recognition not supported. Please use text input.');
            this.hideVoiceButton();
        }
    }
    
    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    handleVoiceError(errorCode) {
        let errorMessage = '';
        let suggestion = '';
        
        switch(errorCode) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                suggestion = 'Speak clearly into the microphone.';
                break;
            case 'aborted':
                errorMessage = 'Voice recognition was stopped.';
                suggestion = 'Tap the microphone button to try again.';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone not found or not accessible.';
                suggestion = 'Please check microphone permissions in browser settings.';
                break;
            case 'network':
                errorMessage = 'Network error occurred.';
                suggestion = 'Please check your internet connection.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied.';
                suggestion = 'Please allow microphone access in browser settings and reload the page.';
                break;
            case 'service-not-allowed':
                errorMessage = 'Speech recognition service not allowed.';
                suggestion = 'This may require HTTPS connection. Please use text input.';
                break;
            case 'bad-grammar':
                errorMessage = 'Grammar error.';
                suggestion = 'Please try speaking again.';
                break;
            case 'language-not-supported':
                errorMessage = 'Language not supported.';
                suggestion = 'Trying English instead.';
                // Fallback to English
                if (this.recognition) {
                    this.recognition.lang = 'en-US';
                }
                break;
            default:
                errorMessage = `Voice recognition error: ${errorCode}`;
                suggestion = 'Please use text input as fallback.';
        }
        
        this.showError(`🎤 ${errorMessage} ${suggestion}`);
        
        // For permission errors, show special message
        if (errorCode === 'not-allowed' || errorCode === 'audio-capture') {
            this.showPermissionHelp();
        }
    }
    
    showPermissionHelp() {
        const helpMessage = 'To enable voice: 1) Tap browser menu → Settings → Site Settings → Microphone → Allow, 2) Reload page';
        this.addMessage(helpMessage, 'medmitra');
    }
    
    hideVoiceButton() {
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.style.display = 'none';
        }
    }
    
    showVoiceError(message) {
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.style.opacity = '0.5';
            voiceButton.title = message;
        }
        this.showError(message);
    }

    initializeUI() {
        // Voice button
        const voiceButton = document.getElementById('voiceButton');
        voiceButton.addEventListener('click', () => {
            this.toggleVoiceInput();
        });
        
        // Text input
        const textInput = document.getElementById('textInput');
        const sendButton = document.getElementById('sendButton');
        
        sendButton.addEventListener('click', () => {
            this.sendTextMessage();
        });
        
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendTextMessage();
            }
        });
        
        // Check for current reminder on load
        this.checkCurrentReminder();
    }

    toggleVoiceInput() {
        if (!this.recognition) {
            this.showError('Voice recognition not available. Please use text input.');
            return;
        }
        
        if (this.isListening) {
            try {
                this.recognition.stop();
                this.updateVoiceUI(false);
            } catch (error) {
                console.error('Error stopping recognition:', error);
                this.isListening = false;
                this.updateVoiceUI(false);
            }
        } else {
            try {
                // Check if already started
                if (this.isListening) {
                    return;
                }
                
                // Request microphone permission first (mobile)
                if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                    navigator.mediaDevices.getUserMedia({ audio: true })
                        .then(() => {
                            // Permission granted, start recognition
                            this.recognition.start();
                        })
                        .catch((err) => {
                            console.error('Microphone permission denied:', err);
                            this.handleVoiceError('not-allowed');
                        });
                } else {
                    // Fallback for browsers without getUserMedia
                    this.recognition.start();
                }
            } catch (error) {
                console.error('Error starting recognition:', error);
                this.updateVoiceUI(false);
                
                // Provide helpful error message
                if (error.name === 'InvalidStateError') {
                    this.showError('Voice recognition is already running. Please wait.');
                } else if (error.name === 'NotAllowedError' || error.message.includes('permission')) {
                    this.handleVoiceError('not-allowed');
                } else {
                    this.showError('Failed to start voice recognition. Please use text input.');
                }
            }
        }
    }

    updateVoiceUI(listening) {
        const voiceButton = document.getElementById('voiceButton');
        const voiceStatus = document.getElementById('voiceStatus');
        const voiceText = voiceButton.querySelector('.voice-text');
        
        if (listening) {
            voiceButton.classList.add('listening');
            voiceText.textContent = 'Listening...';
            voiceStatus.style.display = 'flex';
        } else {
            voiceButton.classList.remove('listening');
            voiceText.textContent = 'Tap to Speak';
            voiceStatus.style.display = 'none';
        }
    }

    sendTextMessage() {
        const textInput = document.getElementById('textInput');
        const message = textInput.value.trim();
        
        if (message) {
            this.sendMessage(message);
            textInput.value = '';
        }
    }

    sendMessage(text) {
        // Add user message to chat
        this.addMessage(text, 'user');
        
        // Send to server via WebSocket
        if (this.socket && this.socket.connected) {
            this.socket.emit('user_message', { text: text });
        } else {
            // Fallback to REST API
            this.sendMessageViaAPI(text);
        }
    }

    async sendMessageViaAPI(text) {
        try {
            const response = await fetch('/api/user/response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            this.handleResponse(data);
        } catch (error) {
            console.error('Error sending message:', error);
            this.showError('Failed to send message. Please try again.');
        }
    }

    handleResponse(data) {
        const response = data.response;
        this.addMessage(response, 'medmitra');
        this.speak(response);
        
        // Check if medication was taken
        if (data.medication_taken) {
            this.waitingForMedicationResponse = false;
            this.currentReminderMedication = null;
            
            // Show success message
            this.addMessage('✅ Medication recorded successfully!', 'medmitra');
            
            // Hide reminder card after a delay
            setTimeout(() => {
                const reminderCard = document.getElementById('reminderCard');
                reminderCard.style.display = 'none';
            }, 3000);
        } else if (this.currentReminderMedication && response.includes('yaad kara dunga')) {
            // User said "Nahi" - will remind again, keep listening
            this.waitingForMedicationResponse = true;
            setTimeout(() => {
                if (this.recognition && !this.isListening) {
                    this.toggleVoiceInput();
                }
            }, 2000);
        } else if (this.currentReminderMedication) {
            // Still waiting for medication response - auto-start listening again
            this.waitingForMedicationResponse = true;
            setTimeout(() => {
                if (this.recognition && !this.isListening) {
                    this.toggleVoiceInput();
                }
            }, 2000);
        }
        
        // Show caregiver alert if present
        if (data.caregiver_alert) {
            this.showCaregiverAlert(data.caregiver_alert);
        }
    }
    
    handleMedicationResponse(transcript) {
        // Send response immediately
        this.sendMessage(transcript);
        
        // Check if it's a clear yes/no response
        const transcriptLower = transcript.toLowerCase();
        if (transcriptLower.includes('haan') || transcriptLower.includes('yes') || 
            transcriptLower.includes('le li') || transcriptLower.includes('ho gaya')) {
            this.waitingForMedicationResponse = false;
        } else if (transcriptLower.includes('nahi') || transcriptLower.includes('no') || 
                   transcriptLower.includes('abhi nahi')) {
            // Will remind again
            this.waitingForMedicationResponse = true;
        }
    }

    handleReminder(data) {
        // Show reminder card
        const reminderCard = document.getElementById('reminderCard');
        const reminderContent = document.getElementById('reminderContent');
        const explanationDiv = document.getElementById('medicationExplanation');
        const explanationText = document.getElementById('explanationText');
        
        // Format the reminder message - extract explanation separately
        const messageParts = data.message.split('\n\n');
        let formattedMessage = '';
        let explanation = '';
        
        // Look for explanation pattern (usually contains "Yeh dawa" or similar)
        for (let i = 0; i < messageParts.length; i++) {
            const part = messageParts[i].trim();
            // Check if this part is the explanation
            if (part.includes('Yeh dawa') || part.includes('control') || 
                part.includes('blood') || part.includes('pressure') || 
                part.includes('sugar') || part.includes('cholesterol') ||
                part.includes('thyroid') || part.includes('acid')) {
                explanation = part;
            } else if (part && !part.includes('Kya aapne') && !part.includes('Kripya')) {
                // Include other parts except the question at the end
                formattedMessage += part + '\n\n';
            }
        }
        
        // If no explanation found, try to get it from medication data
        if (!explanation && data.medication) {
            // We'll fetch it from the API if needed
            this.fetchMedicationExplanation(data.medication.name).then(exp => {
                if (exp) {
                    explanationText.textContent = exp;
                    explanationDiv.style.display = 'block';
                }
            });
        }
        
        reminderContent.textContent = formattedMessage.trim() || data.message;
        reminderCard.style.display = 'block';
        
        // Show explanation if available
        if (explanation) {
            explanationText.textContent = explanation;
            explanationDiv.style.display = 'block';
        } else {
            explanationDiv.style.display = 'none';
        }
        
        // Store current reminder medication
        this.currentReminderMedication = data.medication;
        
        // Speak the reminder (only if page is visible)
        if (!document.hidden) {
            this.speak(data.message);
        }
        
        // Auto-start voice listening after reminder is spoken
        setTimeout(() => {
            if (this.recognition && !this.isListening && !document.hidden) {
                this.toggleVoiceInput();
            }
        }, 3000); // Wait 3 seconds after speaking to start listening
        
        // Scroll to reminder
        reminderCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Add reminder to chat
        this.addMessage(data.message, 'medmitra');
        
        // Vibrate device if supported
        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 200, 100, 200]);
        }
    }
    
    async fetchMedicationExplanation(medicationName) {
        // This would fetch from an API endpoint if we add one
        // For now, return null as explanation is already in the message
        return null;
    }

    async checkCurrentReminder() {
        try {
            const response = await fetch('/api/reminder/current');
            const data = await response.json();
            
            if (data.has_reminder) {
                this.handleReminder({
                    message: data.reminder_text,
                    medication: data.medication
                });
            }
        } catch (error) {
            console.error('Error checking reminder:', error);
        }
    }

    addMessage(text, type) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const p = document.createElement('p');
        p.textContent = text;
        contentDiv.appendChild(p);
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    speak(text) {
        // Stop any current speech
        if (this.currentUtterance) {
            this.synthesis.cancel();
        }
        
        // Create new utterance
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'hi-IN'; // Hindi (India)
        utterance.rate = 0.9; // Slightly slower for clarity
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Try to find Hindi voice, fallback to default
        const voices = this.synthesis.getVoices();
        const hindiVoice = voices.find(voice => 
            voice.lang.includes('hi') || voice.lang.includes('HI')
        );
        
        if (hindiVoice) {
            utterance.voice = hindiVoice;
        }
        
        utterance.onend = () => {
            this.currentUtterance = null;
        };
        
        utterance.onerror = (error) => {
            console.error('Speech synthesis error:', error);
        };
        
        this.currentUtterance = utterance;
        this.synthesis.speak(utterance);
    }

    updateStatus(status, text) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusDot = statusIndicator.querySelector('.status-dot');
        const statusText = statusIndicator.querySelector('.status-text');
        
        statusDot.className = `status-dot ${status}`;
        statusText.textContent = text;
    }

    showCaregiverAlert(message) {
        const alertDiv = document.getElementById('caregiverAlert');
        const alertMessage = document.getElementById('alertMessage');
        
        alertMessage.textContent = message;
        alertDiv.style.display = 'block';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            alertDiv.style.display = 'none';
        }, 10000);
    }

    showError(message) {
        this.addMessage(`⚠️ ${message}`, 'medmitra');
        // Also show in console for debugging
        console.warn('MedMitra Error:', message);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Load voices for speech synthesis
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = () => {
            console.log('Voices loaded');
        };
    }
    
    // Initialize MedMitra client
    window.medmitra = new MedMitraClient();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Pause speech when page is hidden
        if (window.medmitra && window.medmitra.synthesis) {
            window.medmitra.synthesis.pause();
        }
    }
});

