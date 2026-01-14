const API_BASE_URL = '/api'

export const uploadDocument = async (file, passcode) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('passcode', passcode)

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      let errorMessage = 'Upload failed'
      try {
        const error = await response.json()
        errorMessage = error.detail || error.message || `Server error: ${response.status}`
      } catch (e) {
        // If response is not JSON, use status text
        errorMessage = `Server error: ${response.status} ${response.statusText}`
      }
      throw new Error(errorMessage)
    }

    return await response.json()
  } catch (err) {
    // Handle network errors
    if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
      throw new Error('Cannot connect to server. Please check if the backend is running.')
    }
    throw err
  }
}

export const accessDocument = async (docId, passcode) => {
  const response = await fetch(`${API_BASE_URL}/access/${docId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ passcode })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Access denied')
  }

  return await response.json()
}

export const downloadDocument = async (docId, passcode, filename) => {
  const response = await fetch(`${API_BASE_URL}/download/${docId}?passcode=${encodeURIComponent(passcode)}`, {
    method: 'GET'
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Download failed')
  }

  // Get the blob from response
  const blob = await response.blob()
  
  // Create download link
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename || 'document'
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
  
  return { success: true }
}
