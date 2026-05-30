const searchForm = document.getElementById('search-form');
const keywordInput = document.getElementById('keyword-input');
const loadingContainer = document.getElementById('loading-container');
const resultsContainer = document.getElementById('results-container');
const resultsCount = document.getElementById('results-count');
const jobsList = document.getElementById('jobs-list');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const keyword = keywordInput.value.trim();
    if (!keyword) return;

    // Reset UI
    showLoading();
    hideResults();
    hideError();

    try {
        const data = await fetchJobs(keyword);
        
        if (data.error) {
            throw new Error(data.error);
        }

        displayJobs(data.jobs);
        resultsCount.textContent = `${data.count} ${data.count === 1 ? 'Job' : 'Jobs'} Found for "${keyword}"`;
        
        hideLoading();
        showResults();
    } catch (error) {
        console.error(error);
        errorMessage.textContent = `Error: ${error.message || 'Could not fetch jobs. Please try again later.'}`;
        hideLoading();
        showError();
    }
});

async function fetchJobs(keyword) {
    const response = await fetch(`/api/jobs?keyword=${encodeURIComponent(keyword)}`);
    if (!response.ok) {
        throw new Error('Failed to fetch jobs from server.');
    }
    return response.json();
}

function displayJobs(jobs) {
    jobsList.innerHTML = '';
    
    if (jobs.length === 0) {
        jobsList.innerHTML = '<p class="no-jobs">No jobs found matching your criteria.</p>';
        return;
    }

    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        jobCard.innerHTML = `
            <h3 class="job-title">${job.Title}</h3>
            <p class="job-company">${job.Company}</p>
            <p class="job-category">${job.Category}</p>
            <a href="${job['Apply Link']}" target="_blank" class="apply-btn">View Details / Apply</a>
        `;
        jobsList.appendChild(jobCard);
    });
}

function showLoading() {
    loadingContainer.classList.remove('hidden');
}

function hideLoading() {
    loadingContainer.classList.add('hidden');
}

function showResults() {
    resultsContainer.classList.remove('hidden');
}

function hideResults() {
    resultsContainer.classList.add('hidden');
}

function showError() {
    errorContainer.classList.remove('hidden');
}

function hideError() {
    errorContainer.classList.add('hidden');
}
