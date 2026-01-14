<template>
  <div class="access-page">
    <div class="container">
      <div class="card">
        <div class="card-header">
          <div class="lock-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2>Secure Document Access</h2>
          <p class="subtitle">Enter the passcode to unlock and view the document</p>
        </div>

        <form @submit.prevent="handleAccess" class="access-form" v-if="!accessGranted">
          <div class="form-group">
            <label for="passcode" class="label">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Passcode
            </label>
            <input 
              type="password" 
              id="passcode"
              v-model="passcode"
              placeholder="Enter the passcode"
              class="input"
              :class="{ 'input-error': error }"
              required
              autofocus
              @input="clearError"
            />
            <p v-if="error" class="error-text">{{ error }}</p>
            <p v-else class="input-hint">The passcode was provided by the document owner</p>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="!passcode || loading"
          >
            <span v-if="!loading">Unlock Document</span>
            <span v-else class="loading">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-dasharray="32" stroke-dashoffset="32">
                  <animate attributeName="stroke-dasharray" dur="2s" values="0 32;16 16;0 32;0 32" repeatCount="indefinite"/>
                  <animate attributeName="stroke-dashoffset" dur="2s" values="0;-16;-32;-32" repeatCount="indefinite"/>
                </circle>
              </svg>
              Verifying...
            </span>
          </button>
        </form>

        <div v-if="accessGranted" class="success-container">
          <div class="success-icon">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2>Access Granted!</h2>
          <p class="success-message">{{ accessMessage }}</p>
          <div v-if="documentInfo" class="document-info">
            <div class="info-item">
              <span class="info-label">Filename:</span>
              <span class="info-value">{{ documentInfo.filename }}</span>
            </div>
            <div class="info-item" v-if="documentInfo.file_size">
              <span class="info-label">Size:</span>
              <span class="info-value">{{ formatFileSize(documentInfo.file_size) }}</span>
            </div>
          </div>
          <div class="action-buttons">
            <button 
              @click="downloadFile" 
              class="btn btn-primary"
              :disabled="downloading"
            >
              <span v-if="!downloading">Download Document</span>
              <span v-else class="loading">
                <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-dasharray="32" stroke-dashoffset="32">
                    <animate attributeName="stroke-dasharray" dur="2s" values="0 32;16 16;0 32;0 32" repeatCount="indefinite"/>
                    <animate attributeName="stroke-dashoffset" dur="2s" values="0;-16;-32;-32" repeatCount="indefinite"/>
                  </circle>
                </svg>
                Downloading...
              </span>
            </button>
            <button @click="goHome" class="btn btn-secondary">Upload New Document</button>
          </div>
        </div>

        <div v-if="expired" class="expired-container">
          <div class="expired-icon">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2>Document Expired</h2>
          <p class="expired-message">This document link has expired. Documents are only available for 24 hours.</p>
          <button @click="goHome" class="btn btn-primary">Upload New Document</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { accessDocument, downloadDocument } from '../services/api'

export default {
  name: 'Access',
  data() {
    return {
      passcode: '',
      loading: false,
      error: null,
      accessGranted: false,
      accessMessage: '',
      expired: false,
      documentInfo: null,
      downloading: false
    }
  },
  computed: {
    docId() {
      return this.$route.params.id
    }
  },
  methods: {
    clearError() {
      this.error = null
    },
    async handleAccess() {
      if (!this.passcode) return

      this.loading = true
      this.error = null

      try {
        const response = await accessDocument(this.docId, this.passcode)
        this.accessGranted = true
        this.documentInfo = response
        this.accessMessage = response.message || 'You now have access to the document.'
      } catch (err) {
        const errorMessage = err.message || 'Failed to access document'
        
        if (errorMessage.includes('404') || errorMessage.includes('not found')) {
          this.error = 'Document not found. Please check the link.'
        } else if (errorMessage.includes('410') || errorMessage.includes('Expired')) {
          this.expired = true
        } else if (errorMessage.includes('403') || errorMessage.includes('Invalid')) {
          this.error = 'Incorrect passcode. Please try again.'
        } else {
          this.error = errorMessage
        }
      } finally {
        this.loading = false
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    },
    goHome() {
      this.$router.push('/')
    },
    async downloadFile() {
      if (!this.passcode || !this.documentInfo) return
      
      this.downloading = true
      try {
        await downloadDocument(this.docId, this.passcode, this.documentInfo.filename)
      } catch (err) {
        this.error = err.message || 'Failed to download file'
      } finally {
        this.downloading = false
      }
    }
  },
  async mounted() {
    // Check if document exists and is expired on mount
    try {
      // We'll check this when user tries to access, but for now just show the form
    } catch (err) {
      if (err.message.includes('410') || err.message.includes('Expired')) {
        this.expired = true
      }
    }
  }
}
</script>

<style scoped>
.access-page {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow-xl);
  padding: 2.5rem;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.lock-icon {
  color: var(--primary-color);
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.card-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

.access-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.label svg {
  color: var(--primary-color);
}

.input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 1rem;
  transition: all 0.2s;
  background: var(--card-bg);
  color: var(--text-primary);
}

.input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.input-error {
  border-color: var(--error-color);
}

.input-error:focus {
  border-color: var(--error-color);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.error-text {
  font-size: 0.875rem;
  color: var(--error-color);
  font-weight: 500;
  margin-top: 0.25rem;
}

.btn {
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--text-secondary);
  color: white;
}

.btn-secondary:hover {
  background: #475569;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.success-container {
  text-align: center;
  padding: 1rem 0;
}

.success-icon {
  color: var(--success-color);
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.success-container h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--success-color);
  margin-bottom: 0.75rem;
}

.success-message {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.document-info {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid var(--success-color);
  border-radius: var(--radius-sm);
  padding: 1rem;
  margin-bottom: 1.5rem;
  text-align: left;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.info-value {
  color: var(--text-secondary);
  font-size: 0.875rem;
  word-break: break-all;
  margin-left: 1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.expired-container {
  text-align: center;
  padding: 1rem 0;
}

.expired-icon {
  color: var(--warning-color);
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.expired-container h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--warning-color);
  margin-bottom: 0.75rem;
}

.expired-message {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .card {
    padding: 1.5rem;
    margin: 0 1rem;
  }

  .card-header h2 {
    font-size: 1.5rem;
  }

  .lock-icon svg {
    width: 56px;
    height: 56px;
  }

  .success-icon svg,
  .expired-icon svg {
    width: 64px;
    height: 64px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .card {
    padding: 1.25rem;
  }

  .card-header h2 {
    font-size: 1.25rem;
  }

  .lock-icon svg {
    width: 48px;
    height: 48px;
  }

  .success-icon svg,
  .expired-icon svg {
    width: 56px;
    height: 56px;
  }
}
</style>
