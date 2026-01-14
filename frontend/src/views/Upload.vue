<template>
  <div class="upload-page">
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h2>Upload Secure Document</h2>
          <p class="subtitle">Share your document securely with a passcode. It will expire in 24 hours.</p>
        </div>

        <form @submit.prevent="handleUpload" class="upload-form">
          <div class="file-upload-area" :class="{ 'dragover': isDragging, 'has-file': selectedFile }" 
               @dragover.prevent="isDragging = true"
               @dragleave.prevent="isDragging = false"
               @drop.prevent="handleDrop">
            <input 
              type="file" 
              ref="fileInput"
              @change="handleFileSelect"
              class="file-input"
              id="file-input"
              accept="*/*"
            />
            <div class="upload-content">
              <svg v-if="!selectedFile" class="upload-icon" width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div v-if="!selectedFile" class="upload-text">
                <p class="upload-title">Drag & drop your file here</p>
                <p class="upload-subtitle">or click to browse</p>
              </div>
              <div v-else class="file-info">
                <svg class="file-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div class="file-details">
                  <p class="file-name">{{ selectedFile.name }}</p>
                  <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
                </div>
                <button type="button" @click="removeFile" class="remove-btn" aria-label="Remove file">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

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
              placeholder="Enter a secure passcode"
              class="input"
              required
              minlength="4"
            />
            <p class="input-hint">Minimum 4 characters. Share this passcode with the recipient.</p>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="!selectedFile || !passcode || uploading"
          >
            <span v-if="!uploading">Upload & Generate Link</span>
            <span v-else class="loading">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-dasharray="32" stroke-dashoffset="32">
                  <animate attributeName="stroke-dasharray" dur="2s" values="0 32;16 16;0 32;0 32" repeatCount="indefinite"/>
                  <animate attributeName="stroke-dashoffset" dur="2s" values="0;-16;-32;-32" repeatCount="indefinite"/>
                </circle>
              </svg>
              Uploading...
            </span>
          </button>
        </form>

        <div v-if="uploadSuccess" class="success-message">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="success-content">
            <h3>Upload Successful!</h3>
            <p>Your document has been uploaded securely.</p>
            <div class="link-container">
              <input 
                type="text" 
                :value="shareLink" 
                readonly 
                class="link-input"
                ref="linkInput"
              />
              <button @click="copyLink" class="btn-copy">
                {{ linkCopied ? 'Copied!' : 'Copy' }}
              </button>
            </div>
          </div>
        </div>

        <div v-if="error" class="error-message">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <p>{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadDocument } from '../services/api'

export default {
  name: 'Upload',
  data() {
    return {
      selectedFile: null,
      passcode: '',
      isDragging: false,
      uploading: false,
      uploadSuccess: false,
      shareLink: '',
      error: null,
      linkCopied: false
    }
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.error = null
      }
    },
    handleDrop(event) {
      this.isDragging = false
      const file = event.dataTransfer.files[0]
      if (file) {
        this.selectedFile = file
        this.error = null
      }
    },
    removeFile() {
      this.selectedFile = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    },
    async handleUpload() {
      if (!this.selectedFile || !this.passcode) return

      this.uploading = true
      this.error = null
      this.uploadSuccess = false

      try {
        const response = await uploadDocument(this.selectedFile, this.passcode)
        const fullLink = `${window.location.origin}${response.link}`
        this.shareLink = fullLink
        this.uploadSuccess = true
        
        // Reset form
        this.selectedFile = null
        this.passcode = ''
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = ''
        }
      } catch (err) {
        this.error = err.message || 'Failed to upload document. Please try again.'
      } finally {
        this.uploading = false
      }
    },
    async copyLink() {
      try {
        await navigator.clipboard.writeText(this.shareLink)
        this.linkCopied = true
        setTimeout(() => {
          this.linkCopied = false
        }, 2000)
      } catch (err) {
        // Fallback for older browsers
        this.$refs.linkInput.select()
        document.execCommand('copy')
        this.linkCopied = true
        setTimeout(() => {
          this.linkCopied = false
        }, 2000)
      }
    }
  }
}
</script>

<style scoped>
.upload-page {
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
  max-width: 600px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
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

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.file-upload-area {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-sm);
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--bg-color);
  position: relative;
}

.file-upload-area:hover {
  border-color: var(--primary-color);
  background: rgba(99, 102, 241, 0.05);
}

.file-upload-area.dragover {
  border-color: var(--primary-color);
  background: rgba(99, 102, 241, 0.1);
  transform: scale(1.02);
}

.file-upload-area.has-file {
  border-color: var(--success-color);
  background: rgba(16, 185, 129, 0.05);
  padding: 1.5rem;
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.upload-content {
  pointer-events: none;
}

.upload-icon {
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.upload-text {
  color: var(--text-secondary);
}

.upload-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--text-primary);
}

.upload-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

.file-icon {
  color: var(--primary-color);
  flex-shrink: 0;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  word-break: break-all;
}

.file-size {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.remove-btn {
  background: var(--error-color);
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
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

.input-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
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

.success-message {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: rgba(16, 185, 129, 0.1);
  border: 2px solid var(--success-color);
  border-radius: var(--radius-sm);
  display: flex;
  gap: 1rem;
}

.success-message svg {
  color: var(--success-color);
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.success-content {
  flex: 1;
}

.success-content h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--success-color);
  margin-bottom: 0.5rem;
}

.success-content p {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.link-container {
  display: flex;
  gap: 0.5rem;
}

.link-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  color: var(--text-primary);
  font-size: 0.875rem;
}

.btn-copy {
  padding: 0.75rem 1.5rem;
  background: var(--success-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-copy:hover {
  background: #059669;
}

.error-message {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid var(--error-color);
  border-radius: var(--radius-sm);
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.error-message svg {
  color: var(--error-color);
  flex-shrink: 0;
}

.error-message p {
  color: var(--error-color);
  font-weight: 500;
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

  .file-upload-area {
    padding: 2rem 1rem;
  }

  .file-info {
    flex-direction: column;
    text-align: center;
  }

  .file-details {
    text-align: center;
  }

  .link-container {
    flex-direction: column;
  }

  .btn-copy {
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

  .file-upload-area {
    padding: 1.5rem 0.75rem;
  }

  .upload-icon {
    width: 48px;
    height: 48px;
  }
}
</style>
