// ===== TALENTSCOPE - ANALYSIS JAVASCRIPT =====

// Gestionnaire d'analyse
const AnalysisManager = {
    // Configuration
    config: {
        maxFileSize: 10 * 1024 * 1024, // 10MB
        allowedTypes: ['application/pdf'],
        analysisSteps: [
            '📄 Extraction du contenu des CVs...',
            '🔍 Analyse des compétences techniques...',
            '💼 Évaluation de l'expérience professionnelle...',
            '🎓 Vérification du niveau d\'éducation...',
            '🧠 Calcul des scores avec IA...',
            '📊 Génération des résultats...'
        ]
    },

    // État de l'analyse
    state: {
        currentStep: 1,
        jobDescription: '',
        uploadedFiles: [],
        analysisResults: null,
        isAnalyzing: false
    },

    // Initialisation
    init: () => {
        Utils.log('Initialisation de la page d\'analyse');
        
        // Vérifier l'authentification
        if (!AuthManager.isLoggedIn()) {
            Utils.log('Utilisateur non authentifié, redirection...');
            window.location.href = '/auth';
            return;
        }

        // Initialiser les composants
        AnalysisManager.initStepNavigation();
        AnalysisManager.initFileUpload();
        AnalysisManager.initFormValidation();
        AnalysisManager.initAnalysisProcess();
    },

    // Initialiser la navigation entre étapes
    initStepNavigation: () => {
        // Fonctions globales pour la navigation
        window.nextStep = (stepNumber) => {
            AnalysisManager.goToStep(stepNumber);
        };

        window.prevStep = (stepNumber) => {
            AnalysisManager.goToStep(stepNumber);
        };

        window.startAnalysis = () => {
            AnalysisManager.startAnalysis();
        };

        window.newAnalysis = () => {
            AnalysisManager.resetAnalysis();
        };
    },

    // Aller à une étape spécifique
    goToStep: (stepNumber) => {
        Utils.log(`Navigation vers l'étape ${stepNumber}`);
        
        // Valider l'étape actuelle avant de passer à la suivante
        if (stepNumber > AnalysisManager.state.currentStep) {
            if (!AnalysisManager.validateCurrentStep()) {
                return;
            }
        }

        // Mettre à jour l'état
        AnalysisManager.state.currentStep = stepNumber;

        // Mettre à jour l'interface
        AnalysisManager.updateStepDisplay();
        AnalysisManager.updateProgressSteps();
    },

    // Valider l'étape actuelle
    validateCurrentStep: () => {
        switch (AnalysisManager.state.currentStep) {
            case 1:
                return AnalysisManager.validateJobDescription();
            case 2:
                return AnalysisManager.validateFileUpload();
            case 3:
                return true; // La vérification est toujours valide
            default:
                return true;
        }
    },

    // Valider la description du poste
    validateJobDescription: () => {
        const jobDescription = document.getElementById('jobDescription').value.trim();
        
        if (!jobDescription) {
            Notifications.error('Veuillez saisir une description du poste');
            return false;
        }

        if (jobDescription.length < 50) {
            Notifications.error('La description du poste doit contenir au moins 50 caractères');
            return false;
        }

        AnalysisManager.state.jobDescription = jobDescription;
        return true;
    },

    // Valider l'upload de fichiers
    validateFileUpload: () => {
        if (AnalysisManager.state.uploadedFiles.length === 0) {
            Notifications.error('Veuillez sélectionner au moins un fichier CV');
            return false;
        }

        return true;
    },

    // Mettre à jour l'affichage des étapes
    updateStepDisplay: () => {
        // Masquer toutes les étapes
        const panels = document.querySelectorAll('.step-panel');
        panels.forEach(panel => panel.classList.remove('active'));

        // Afficher l'étape actuelle
        const currentPanel = document.getElementById(`step-${AnalysisManager.state.currentStep}`);
        if (currentPanel) {
            currentPanel.classList.add('active');
        }

        // Mettre à jour le contenu spécifique à chaque étape
        AnalysisManager.updateStepContent();
    },

    // Mettre à jour le contenu spécifique à chaque étape
    updateStepContent: () => {
        switch (AnalysisManager.state.currentStep) {
            case 3:
                AnalysisManager.updateVerificationContent();
                break;
            case 4:
                AnalysisManager.updateResultsContent();
                break;
        }
    },

    // Mettre à jour les indicateurs de progression
    updateProgressSteps: () => {
        const steps = document.querySelectorAll('.step');
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNumber < AnalysisManager.state.currentStep) {
                step.classList.add('completed');
            } else if (stepNumber === AnalysisManager.state.currentStep) {
                step.classList.add('active');
            }
        });
    },

    // Initialiser l'upload de fichiers
    initFileUpload: () => {
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('cvFiles');

        if (!uploadZone || !fileInput) return;

        // Clic sur la zone d'upload
        uploadZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag & Drop
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            AnalysisManager.handleFileSelection(files);
        });

        // Sélection de fichiers
        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            AnalysisManager.handleFileSelection(files);
        });
    },

    // Gérer la sélection de fichiers
    handleFileSelection: (files) => {
        Utils.log('Fichiers sélectionnés', files);

        // Valider les fichiers
        const validFiles = files.filter(file => AnalysisManager.validateFile(file));
        
        if (validFiles.length === 0) {
            return;
        }

        // Ajouter les fichiers à l'état
        AnalysisManager.state.uploadedFiles = [...AnalysisManager.state.uploadedFiles, ...validFiles];

        // Mettre à jour l'affichage
        AnalysisManager.updateFileDisplay();
        AnalysisManager.updateNextButton();
    },

    // Valider un fichier
    validateFile: (file) => {
        // Vérifier le type
        if (!AnalysisManager.config.allowedTypes.includes(file.type)) {
            Notifications.error(`Le fichier ${file.name} n'est pas un PDF valide`);
            return false;
        }

        // Vérifier la taille
        if (file.size > AnalysisManager.config.maxFileSize) {
            Notifications.error(`Le fichier ${file.name} est trop volumineux (max 10MB)`);
            return false;
        }

        return true;
    },

    // Mettre à jour l'affichage des fichiers
    updateFileDisplay: () => {
        const uploadedFilesDiv = document.getElementById('uploadedFiles');
        const fileListDiv = document.getElementById('fileList');

        if (!uploadedFilesDiv || !fileListDiv) return;

        if (AnalysisManager.state.uploadedFiles.length > 0) {
            uploadedFilesDiv.style.display = 'block';
            
            fileListDiv.innerHTML = AnalysisManager.state.uploadedFiles.map((file, index) => `
                <div class="file-item">
                    <i class="fas fa-file-pdf file-icon"></i>
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${AnalysisManager.formatFileSize(file.size)}</span>
                    <button class="file-remove" onclick="AnalysisManager.removeFile(${index})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `).join('');
        } else {
            uploadedFilesDiv.style.display = 'none';
        }
    },

    // Supprimer un fichier
    removeFile: (index) => {
        AnalysisManager.state.uploadedFiles.splice(index, 1);
        AnalysisManager.updateFileDisplay();
        AnalysisManager.updateNextButton();
    },

    // Mettre à jour le bouton suivant
    updateNextButton: () => {
        const nextButton = document.getElementById('nextStep2');
        if (nextButton) {
            nextButton.disabled = AnalysisManager.state.uploadedFiles.length === 0;
        }
    },

    // Formater la taille du fichier
    formatFileSize: (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Initialiser la validation des formulaires
    initFormValidation: () => {
        const jobDescription = document.getElementById('jobDescription');
        if (jobDescription) {
            jobDescription.addEventListener('input', () => {
                AnalysisManager.updateNextButton();
            });
        }
    },

    // Mettre à jour le contenu de vérification
    updateVerificationContent: () => {
        const jobPreview = document.getElementById('jobPreview');
        const cvsPreview = document.getElementById('cvsPreview');

        if (jobPreview) {
            jobPreview.innerHTML = `
                <div class="job-preview-content">
                    <p>${AnalysisManager.state.jobDescription}</p>
                </div>
            `;
        }

        if (cvsPreview) {
            cvsPreview.innerHTML = AnalysisManager.state.uploadedFiles.map((file, index) => `
                <div class="cv-preview-item">
                    <i class="fas fa-file-pdf"></i>
                    <span>${file.name}</span>
                </div>
            `).join('');
        }
    },

    // Initialiser le processus d'analyse
    initAnalysisProcess: () => {
        // Cette fonction sera appelée lors du lancement de l'analyse
    },

    // Démarrer l'analyse
    startAnalysis: async () => {
        if (AnalysisManager.state.isAnalyzing) {
            return;
        }

        Utils.log('Démarrage de l\'analyse');
        
        AnalysisManager.state.isAnalyzing = true;
        AnalysisManager.state.currentStep = 4;
        
        // Mettre à jour l'interface
        AnalysisManager.updateStepDisplay();
        AnalysisManager.updateProgressSteps();
        
        // Afficher la progression
        AnalysisManager.showAnalysisProgress();
        
        try {
            // Simuler l'analyse
            await AnalysisManager.simulateAnalysis();
            
            // Afficher les résultats
            AnalysisManager.showResults();
            
        } catch (error) {
            Utils.log('Erreur lors de l\'analyse', error);
            Notifications.error('Erreur lors de l\'analyse des CVs');
        } finally {
            AnalysisManager.state.isAnalyzing = false;
        }
    },

    // Afficher la progression de l'analyse
    showAnalysisProgress: () => {
        const progressContainer = document.getElementById('analysisProgress');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        if (!progressContainer || !progressFill || !progressText) return;

        progressContainer.style.display = 'block';

        let currentStep = 0;
        const totalSteps = AnalysisManager.config.analysisSteps.length;

        const updateProgress = () => {
            if (currentStep < totalSteps) {
                const progress = ((currentStep + 1) / totalSteps) * 100;
                progressFill.style.width = `${progress}%`;
                progressText.textContent = AnalysisManager.config.analysisSteps[currentStep];
                currentStep++;
                
                setTimeout(updateProgress, 2000);
            } else {
                progressText.textContent = '✅ Analyse terminée avec succès !';
            }
        };

        updateProgress();
    },

    // Simuler l'analyse
    simulateAnalysis: async () => {
        // Simulation d'un délai d'analyse
        await new Promise(resolve => setTimeout(resolve, 12000));

        // Générer des résultats simulés
        AnalysisManager.state.analysisResults = AnalysisManager.generateMockResults();
    },

    // Générer des résultats simulés
    generateMockResults: () => {
        const results = [];
        const names = ['cv_hamza.pdf', 'cv_sophia.pdf', 'cv_adam.pdf', 'cv_ali.pdf', 'cv_hafsa.pdf', 'cv_yassine.pdf'];
        const statuses = ['Excellent', 'Très bon', 'Bon', 'Moyen'];
        const colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800'];

        names.forEach((name, index) => {
            const score = 60 + Math.random() * 35; // Score entre 60 et 95
            const statusIndex = score >= 90 ? 0 : score >= 80 ? 1 : score >= 70 ? 2 : 3;
            
            results.push({
                name: name,
                score: Math.round(score * 10) / 10,
                status: statuses[statusIndex],
                color: colors[statusIndex],
                icon: score >= 90 ? '🥇' : score >= 80 ? '🥈' : '🥉',
                position: `Candidat ${index + 1}`,
                skills: ['Python', 'Machine Learning', 'Data Science'],
                date: new Date().toLocaleDateString('fr-FR')
            });
        });

        // Trier par score décroissant
        return results.sort((a, b) => b.score - a.score);
    },

    // Afficher les résultats
    showResults: () => {
        const resultsContainer = document.getElementById('resultsContainer');
        const resultsList = document.getElementById('resultsList');
        const analysisProgress = document.getElementById('analysisProgress');

        if (!resultsContainer || !resultsList || !analysisProgress) return;

        // Masquer la progression
        analysisProgress.style.display = 'none';

        // Afficher les résultats
        resultsContainer.style.display = 'block';

        // Mettre à jour les statistiques
        AnalysisManager.updateResultsStats();

        // Afficher la liste des résultats
        AnalysisManager.updateResultsList();
    },

    // Mettre à jour les statistiques des résultats
    updateResultsStats: () => {
        const results = AnalysisManager.state.analysisResults;
        if (!results) return;

        const totalAnalyzed = results.length;
        const averageScore = results.reduce((sum, r) => sum + r.score, 0) / totalAnalyzed;
        const bestScore = Math.max(...results.map(r => r.score));

        const totalAnalyzedEl = document.getElementById('totalAnalyzed');
        const averageScoreEl = document.getElementById('averageScore');
        const bestScoreEl = document.getElementById('bestScore');

        if (totalAnalyzedEl) totalAnalyzedEl.textContent = totalAnalyzed;
        if (averageScoreEl) averageScoreEl.textContent = Math.round(averageScore * 10) / 10 + '%';
        if (bestScoreEl) bestScoreEl.textContent = Math.round(bestScore * 10) / 10 + '%';
    },

    // Mettre à jour la liste des résultats
    updateResultsList: () => {
        const resultsList = document.getElementById('resultsList');
        if (!resultsList) return;

        const results = AnalysisManager.state.analysisResults;
        if (!results) return;

        resultsList.innerHTML = results.map((result, index) => `
            <div class="result-item">
                <div class="result-rank">${index + 1}</div>
                <div class="result-content">
                    <div class="result-name">${result.icon} ${result.name}</div>
                    <div class="result-status">${result.status} - ${result.position}</div>
                </div>
                <div class="result-score">
                    <div class="score-value" style="color: ${result.color}">${result.score}%</div>
                    <div class="score-label">Score de compatibilité</div>
                </div>
            </div>
        `).join('');
    },

    // Réinitialiser l'analyse
    resetAnalysis: () => {
        AnalysisManager.state = {
            currentStep: 1,
            jobDescription: '',
            uploadedFiles: [],
            analysisResults: null,
            isAnalyzing: false
        };

        // Réinitialiser l'interface
        document.getElementById('jobDescription').value = '';
        AnalysisManager.updateFileDisplay();
        AnalysisManager.updateStepDisplay();
        AnalysisManager.updateProgressSteps();

        // Masquer les résultats
        const resultsContainer = document.getElementById('resultsContainer');
        const analysisProgress = document.getElementById('analysisProgress');
        
        if (resultsContainer) resultsContainer.style.display = 'none';
        if (analysisProgress) analysisProgress.style.display = 'none';

        Notifications.info('Nouvelle analyse initialisée');
    }
};

// Fonctions globales
window.nextStep = (stepNumber) => AnalysisManager.goToStep(stepNumber);
window.prevStep = (stepNumber) => AnalysisManager.goToStep(stepNumber);
window.startAnalysis = () => AnalysisManager.startAnalysis();
window.newAnalysis = () => AnalysisManager.resetAnalysis();

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    Utils.log('Initialisation de la page d\'analyse');
    AnalysisManager.init();
});

// Export pour utilisation globale
window.AnalysisManager = AnalysisManager;
