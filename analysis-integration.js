// ============================================================================
// INTÉGRATION DE L'HISTORIQUE DANS LE PROCESSUS D'ANALYSE - TalentScope
// ============================================================================

class AnalysisIntegration {
    constructor() {
        this.historyService = null;
        this.analysisStartTime = null;
        this.init();
    }

    init() {
        // Attendre que le service d'historique soit disponible
        this.waitForHistoryService();
    }

    waitForHistoryService() {
        const checkService = () => {
            if (window.analysisHistoryService) {
                this.historyService = window.analysisHistoryService;
                this.setupAnalysisHooks();
                console.log('Intégration de l\'historique initialisée');
            } else {
                setTimeout(checkService, 100);
            }
        };
        checkService();
    }

    setupAnalysisHooks() {
        // Intercepter les fonctions d'analyse existantes
        this.hookAnalysisFunctions();
        
        // Ajouter des boutons d'historique à l'interface
        this.addHistoryButtons();
        
        // Écouter les événements d'analyse
        this.setupEventListeners();
    }

    hookAnalysisFunctions() {
        // Sauvegarder les fonctions originales
        const originalAnalyze = window.analyzeCV;
        const originalProcessAnalysis = window.processAnalysis;
        const originalShowResults = window.showResults;

        // Remplacer la fonction d'analyse
        window.analyzeCV = async (...args) => {
            this.analysisStartTime = Date.now();
            console.log('Début de l\'analyse - sauvegarde dans l\'historique');
            
            try {
                const result = await originalAnalyze.apply(this, args);
                return result;
            } catch (error) {
                console.error('Erreur lors de l\'analyse:', error);
                throw error;
            }
        };

        // Remplacer la fonction de traitement
        window.processAnalysis = async (...args) => {
            try {
                const result = await originalProcessAnalysis.apply(this, args);
                return result;
            } catch (error) {
                console.error('Erreur lors du traitement:', error);
                throw error;
            }
        };

        // Remplacer la fonction d'affichage des résultats
        window.showResults = (...args) => {
            const result = originalShowResults.apply(this, args);
            
            // Sauvegarder dans l'historique après l'affichage des résultats
            setTimeout(() => {
                this.saveAnalysisToHistory();
            }, 1000);
            
            return result;
        };
    }

    addHistoryButtons() {
        // Ajouter un bouton pour voir l'historique
        this.addHistoryButton();
        
        // Ajouter un lien vers l'historique dans la navigation
        this.addHistoryNavigationLink();
    }

    addHistoryButton() {
        // Chercher la zone des résultats ou des contrôles
        const resultsContainer = document.querySelector('.results-container') || 
                                document.querySelector('.analysis-results') ||
                                document.querySelector('.main-content');

        if (resultsContainer) {
            const historyButton = document.createElement('div');
            historyButton.className = 'history-integration';
            historyButton.innerHTML = `
                <div class="history-actions">
                    <button class="btn btn-secondary" onclick="window.open('analysis-history.html', '_blank')">
                        <i class="fas fa-history"></i> Voir l'historique
                    </button>
                    <button class="btn btn-primary" onclick="this.exportCurrentAnalysis()">
                        <i class="fas fa-download"></i> Exporter cette analyse
                    </button>
                </div>
            `;

            // Ajouter les styles
            const styles = `
                <style>
                    .history-integration {
                        margin: 20px 0;
                        padding: 20px;
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 12px;
                        border: 1px solid rgba(255, 255, 255, 0.2);
                    }

                    .history-actions {
                        display: flex;
                        gap: 15px;
                        justify-content: center;
                        flex-wrap: wrap;
                    }

                    .history-actions .btn {
                        padding: 12px 20px;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    }

                    .history-actions .btn-primary {
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        color: white;
                    }

                    .history-actions .btn-primary:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }

                    .history-actions .btn-secondary {
                        background: rgba(255, 255, 255, 0.9);
                        color: #667eea;
                        border: 1px solid #667eea;
                    }

                    .history-actions .btn-secondary:hover {
                        background: rgba(102, 126, 234, 0.1);
                    }
                </style>
            `;

            document.head.insertAdjacentHTML('beforeend', styles);
            resultsContainer.appendChild(historyButton);
        }
    }

    addHistoryNavigationLink() {
        // Ajouter un lien dans la sidebar si elle existe
        const sidebar = document.querySelector('.sidebar .nav-section');
        if (sidebar) {
            const historyLink = document.createElement('div');
            historyLink.className = 'nav-item';
            historyLink.innerHTML = `
                <a href="analysis-history.html" class="nav-link">
                    <i class="fas fa-history"></i>
                    <span>Historique</span>
                </a>
            `;
            sidebar.appendChild(historyLink);
        }
    }

    setupEventListeners() {
        // Écouter les événements de fin d'analyse
        document.addEventListener('analysisCompleted', (event) => {
            this.saveAnalysisToHistory(event.detail);
        });

        // Écouter les mises à jour de l'historique
        window.addEventListener('analysisHistoryUpdated', () => {
            this.updateHistoryIndicators();
        });
    }

    saveAnalysisToHistory(analysisData = null) {
        if (!this.historyService) {
            console.warn('Service d\'historique non disponible');
            return;
        }

        try {
            // Collecter les données d'analyse depuis l'interface
            const data = analysisData || this.collectAnalysisData();
            
            if (data) {
                const historyItem = this.historyService.addAnalysis(data);
                console.log('Analyse sauvegardée dans l\'historique:', historyItem.id);
                
                // Afficher une notification de succès
                this.showSaveNotification(historyItem);
                
                // Mettre à jour les indicateurs
                this.updateHistoryIndicators();
            }
        } catch (error) {
            console.error('Erreur lors de la sauvegarde dans l\'historique:', error);
        }
    }

    collectAnalysisData() {
        const data = {
            cvName: this.getCVName(),
            cvContent: this.getCVContent(),
            jobDescription: this.getJobDescription(),
            position: this.getPosition(),
            department: this.getDepartment(),
            score: this.getAnalysisScore(),
            status: 'completed',
            duration: this.getAnalysisDuration(),
            algorithm: 'default',
            compatibilityScore: this.getCompatibilityScore(),
            skillsMatch: this.getSkillsMatch(),
            experienceMatch: this.getExperienceMatch(),
            recommendations: this.getRecommendations(),
            strengths: this.getStrengths(),
            weaknesses: this.getWeaknesses(),
            missingSkills: this.getMissingSkills(),
            additionalNotes: this.getAdditionalNotes(),
            fileSize: this.getFileSize(),
            fileType: this.getFileType(),
            processingTime: this.getProcessingTime()
        };

        return data;
    }

    // Méthodes pour extraire les données de l'interface
    getCVName() {
        const cvNameInput = document.querySelector('input[name="cvName"]') ||
                           document.querySelector('#cv-name') ||
                           document.querySelector('.cv-name');
        return cvNameInput ? cvNameInput.value : 'CV analysé';
    }

    getCVContent() {
        const cvContent = document.querySelector('#cv-content') ||
                         document.querySelector('.cv-content') ||
                         document.querySelector('[data-cv-content]');
        return cvContent ? cvContent.textContent.substring(0, 1000) : '';
    }

    getJobDescription() {
        const jobDesc = document.querySelector('textarea[name="jobDescription"]') ||
                       document.querySelector('#job-description') ||
                       document.querySelector('.job-description');
        return jobDesc ? jobDesc.value : '';
    }

    getPosition() {
        const position = document.querySelector('input[name="position"]') ||
                        document.querySelector('#position') ||
                        document.querySelector('.position');
        return position ? position.value : 'Poste non spécifié';
    }

    getDepartment() {
        const dept = document.querySelector('select[name="department"]') ||
                    document.querySelector('#department') ||
                    document.querySelector('.department');
        return dept ? dept.value : 'Département non spécifié';
    }

    getAnalysisScore() {
        const scoreElement = document.querySelector('.score-value') ||
                            document.querySelector('#analysis-score') ||
                            document.querySelector('[data-score]');
        if (scoreElement) {
            const scoreText = scoreElement.textContent;
            const match = scoreText.match(/(\d+)%/);
            return match ? parseInt(match[1]) : 0;
        }
        return 0;
    }

    getAnalysisDuration() {
        if (this.analysisStartTime) {
            return Math.round((Date.now() - this.analysisStartTime) / 1000);
        }
        return 0;
    }

    getCompatibilityScore() {
        const compatScore = document.querySelector('.compatibility-score') ||
                           document.querySelector('#compatibility-score');
        if (compatScore) {
            const scoreText = compatScore.textContent;
            const match = scoreText.match(/(\d+)%/);
            return match ? parseInt(match[1]) : 0;
        }
        return this.getAnalysisScore();
    }

    getSkillsMatch() {
        const skillsElement = document.querySelector('.skills-match') ||
                             document.querySelector('#skills-match');
        if (skillsElement) {
            return {
                matched: this.extractSkillsList(skillsElement, '.matched-skill'),
                missing: this.extractSkillsList(skillsElement, '.missing-skill')
            };
        }
        return { matched: [], missing: [] };
    }

    getExperienceMatch() {
        const expElement = document.querySelector('.experience-match') ||
                          document.querySelector('#experience-match');
        if (expElement) {
            return {
                years: this.extractExperienceYears(expElement),
                relevance: this.extractExperienceRelevance(expElement)
            };
        }
        return { years: 0, relevance: 0 };
    }

    getRecommendations() {
        const recElement = document.querySelector('.recommendations') ||
                          document.querySelector('#recommendations');
        if (recElement) {
            return this.extractRecommendationsList(recElement);
        }
        return [];
    }

    getStrengths() {
        const strengthsElement = document.querySelector('.strengths') ||
                                document.querySelector('#strengths');
        if (strengthsElement) {
            return this.extractListItems(strengthsElement);
        }
        return [];
    }

    getWeaknesses() {
        const weaknessesElement = document.querySelector('.weaknesses') ||
                                 document.querySelector('#weaknesses');
        if (weaknessesElement) {
            return this.extractListItems(weaknessesElement);
        }
        return [];
    }

    getMissingSkills() {
        const missingElement = document.querySelector('.missing-skills') ||
                              document.querySelector('#missing-skills');
        if (missingElement) {
            return this.extractListItems(missingElement);
        }
        return [];
    }

    getAdditionalNotes() {
        const notesElement = document.querySelector('.additional-notes') ||
                            document.querySelector('#additional-notes');
        return notesElement ? notesElement.textContent : '';
    }

    getFileSize() {
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput && fileInput.files.length > 0) {
            return fileInput.files[0].size;
        }
        return 0;
    }

    getFileType() {
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput && fileInput.files.length > 0) {
            return fileInput.files[0].type;
        }
        return 'unknown';
    }

    getProcessingTime() {
        return this.getAnalysisDuration();
    }

    // Méthodes utilitaires pour extraire les données
    extractSkillsList(element, selector) {
        const skills = element.querySelectorAll(selector);
        return Array.from(skills).map(skill => skill.textContent.trim());
    }

    extractExperienceYears(element) {
        const yearsText = element.textContent;
        const match = yearsText.match(/(\d+)\s*ans?/i);
        return match ? parseInt(match[1]) : 0;
    }

    extractExperienceRelevance(element) {
        const relevanceText = element.textContent;
        const match = relevanceText.match(/(\d+)%/);
        return match ? parseInt(match[1]) : 0;
    }

    extractRecommendationsList(element) {
        const recommendations = element.querySelectorAll('li, .recommendation-item');
        return Array.from(recommendations).map(rec => rec.textContent.trim());
    }

    extractListItems(element) {
        const items = element.querySelectorAll('li, .list-item');
        return Array.from(items).map(item => item.textContent.trim());
    }

    showSaveNotification(historyItem) {
        // Créer une notification de succès
        const notification = document.createElement('div');
        notification.className = 'save-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-check-circle"></i>
                <span>Analyse sauvegardée dans l'historique</span>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Ajouter les styles
        const styles = `
            <style>
                .save-notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #10B981;
                    color: white;
                    padding: 15px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                    z-index: 1000;
                    animation: slideIn 0.3s ease;
                }

                .notification-content {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }

                .notification-content button {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                    margin-left: 10px;
                }

                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            </style>
        `;

        if (!document.querySelector('.save-notification-styles')) {
            const styleElement = document.createElement('style');
            styleElement.className = 'save-notification-styles';
            styleElement.textContent = styles;
            document.head.appendChild(styleElement);
        }

        document.body.appendChild(notification);

        // Supprimer automatiquement après 5 secondes
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    updateHistoryIndicators() {
        // Mettre à jour les compteurs d'historique dans l'interface
        const historyCount = this.historyService ? this.historyService.getHistory().length : 0;
        
        // Mettre à jour les éléments d'interface qui affichent le nombre d'analyses
        const countElements = document.querySelectorAll('.history-count, .analyses-count');
        countElements.forEach(element => {
            element.textContent = historyCount;
        });
    }

    exportCurrentAnalysis() {
        // Exporter l'analyse actuelle
        const currentData = this.collectAnalysisData();
        if (currentData) {
            const data = JSON.stringify(currentData, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analyse_${currentData.cvName}_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
    }
}

// Initialiser l'intégration au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Attendre un peu pour que les autres scripts se chargent
    setTimeout(() => {
        new AnalysisIntegration();
    }, 500);
});

// Export pour utilisation dans d'autres modules
window.AnalysisIntegration = AnalysisIntegration;
