// Gestionnaire d'analyse des CVs
class CVAnalyzer {
    constructor() {
        this.currentStep = 1;
        this.uploadedFiles = [];
        this.jobData = {};
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Gestionnaire du formulaire d'offre d'emploi
        const jobForm = document.getElementById('job-form');
        if (jobForm) {
            jobForm.addEventListener('submit', (e) => this.handleJobSubmit(e));
        }

        // Zone de dépôt des CVs
        const dropZone = document.getElementById('file-upload-area');
        if (dropZone) {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, this.preventDefaults);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => this.highlight(dropZone));
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => this.unhighlight(dropZone));
            });

            dropZone.addEventListener('drop', (e) => this.handleDrop(e));
        }

        // Boutons de navigation
        document.querySelectorAll('.step-nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const direction = e.target.dataset.direction;
                if (direction === 'next') {
                    this.nextStep();
                } else {
                    this.prevStep();
                }
            });
        });
    }

    // Gestion des étapes
    async nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep === 3) {
                await this.startAnalysis();
            }
            this.showStep(++this.currentStep);
            this.updateProgress();
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.showStep(--this.currentStep);
            this.updateProgress();
        }
    }

    showStep(step) {
        document.querySelectorAll('.step-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`step${step}`).classList.add('active');
    }

    updateProgress() {
        document.querySelectorAll('.progress-step').forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('completed', 'active');
            
            if (stepNum < this.currentStep) {
                step.classList.add('completed');
            } else if (stepNum === this.currentStep) {
                step.classList.add('active');
            }
        });
    }

    // Gestion du formulaire d'offre d'emploi
    handleJobSubmit(e) {
        e.preventDefault();
        this.jobData = {
            title: document.getElementById('job-title').value,
            description: document.getElementById('job-description').value,
            skills: document.getElementById('job-skills').value.split(',').map(s => s.trim()),
            experience: document.getElementById('job-experience').value
        };
        this.nextStep();
    }

    // Gestion des fichiers
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlight(el) {
        el.classList.add('dragover');
    }

    unhighlight(el) {
        el.classList.remove('dragover');
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        this.handleFiles(files);
    }

    handleFiles(files) {
        const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        
        [...files].forEach(file => {
            if (allowedTypes.includes(file.type)) {
                this.uploadedFiles.push(file);
                this.updateFileList(file);
            }
        });
    }

    updateFileList(file) {
        const fileList = document.getElementById('file-list');
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-icon">📄</div>
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${this.formatFileSize(file.size)}</div>
            </div>
            <button class="file-remove" onclick="cvAnalyzer.removeFile('${file.name}')">
                Supprimer
            </button>
        `;
        fileList.appendChild(fileItem);
    }

    removeFile(fileName) {
        this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== fileName);
        this.updateFileList();
    }

    // Analyse des CVs
    async startAnalysis() {
        const analysisStatus = document.getElementById('analysis-status');
        analysisStatus.textContent = 'Analyse en cours...';

        try {
            // Simuler l'analyse
            await this.simulateAnalysis();

            // Afficher les résultats
            this.displayResults();
            
            analysisStatus.textContent = 'Analyse terminée !';
            return true;
        } catch (error) {
            analysisStatus.textContent = 'Erreur lors de l\'analyse';
            console.error(error);
            return false;
        }
    }

    async simulateAnalysis() {
        // Simuler le temps de traitement
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Générer des résultats simulés
        this.results = this.uploadedFiles.map(file => ({
            fileName: file.name,
            score: Math.random() * 30 + 70, // Score entre 70 et 100
            skills: this.jobData.skills.filter(() => Math.random() > 0.3),
            experience: Math.floor(Math.random() * 10) + 1,
            education: ['Master', 'Licence', 'Doctorat'][Math.floor(Math.random() * 3)]
        }));

        // Trier par score
        this.results.sort((a, b) => b.score - a.score);
    }

    displayResults() {
        const resultsGrid = document.getElementById('results-grid');
        resultsGrid.innerHTML = '';

        this.results.forEach((result, index) => {
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <div class="result-header">
                    <div class="result-score ${this.getScoreClass(result.score)}">
                        ${Math.round(result.score)}%
                    </div>
                    <div class="result-name">${result.fileName}</div>
                </div>
                <div class="result-details">
                    <div class="detail-item">
                        <span class="detail-label">Expérience:</span>
                        <span class="detail-value">${result.experience} ans</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Formation:</span>
                        <span class="detail-value">${result.education}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Compétences:</span>
                        <div class="skill-tags">
                            ${result.skills.map(skill => `
                                <span class="skill-tag">${skill}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
            resultsGrid.appendChild(resultCard);
        });
    }

    // Utilitaires
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    getScoreClass(score) {
        if (score >= 85) return 'excellent';
        if (score >= 70) return 'good';
        return 'average';
    }

    validateCurrentStep() {
        switch (this.currentStep) {
            case 1:
                return this.validateJobForm();
            case 2:
                return this.validateFileUpload();
            case 3:
                return this.validateAnalysisPrep();
            default:
                return true;
        }
    }

    validateJobForm() {
        const title = document.getElementById('job-title').value;
        const description = document.getElementById('job-description').value;
        if (!title || !description) {
            alert('Veuillez remplir tous les champs obligatoires');
            return false;
        }
        return true;
    }

    validateFileUpload() {
        if (this.uploadedFiles.length === 0) {
            alert('Veuillez importer au moins un CV');
            return false;
        }
        return true;
    }

    validateAnalysisPrep() {
        return true; // Validation supplémentaire si nécessaire
    }
}

// Initialiser l'analyseur au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.cvAnalyzer = new CVAnalyzer();
});

