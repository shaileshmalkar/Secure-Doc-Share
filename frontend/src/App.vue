<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1 class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 13H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 17H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M10 9H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Secure Doc Share
        </h1>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 Secure Document Sharing. Your files are protected.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #6366f1;
  --primary-dark: #4f46e5;
  --primary-light: #818cf8;
  --success-color: #10b981;
  --error-color: #ef4444;
  --warning-color: #f59e0b;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --radius: 12px;
  --radius-sm: 8px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

.header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 0;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.logo svg {
  width: 32px;
  height: 32px;
}

.main {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background: var(--card-bg);
  border-top: 1px solid var(--border-color);
  padding: 1.5rem 0;
  margin-top: auto;
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }

  .logo {
    font-size: 1.25rem;
  }

  .logo svg {
    width: 28px;
    height: 28px;
  }

  .main {
    padding: 1.5rem 0;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.125rem;
  }

  .main {
    padding: 1rem 0;
  }
}
</style>
