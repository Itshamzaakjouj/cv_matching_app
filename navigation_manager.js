class NavigationManager {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.jobData = null;
        this.cvFiles = [];
        
        // Éléments DOM
        this.steps = Array.from({length: this.totalSteps}, (_, i) => document.getElementById(`step${i+1}`));
        this.contents = Array.from({length: this.totalSteps}, (_, i) => document.getElementById(`step${i+1}-content`));
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        
        // Initialisation
        this.initializeEventListeners();
        this.updateStepVisuals();
    }

    initializeEventListeners() {
        // Navigation
        this.prevBtn.addEventListener('click', () => this.goToPreviousStep());
        this.nextBtn.addEventListener('click', () => this.goToNextStep());

        // Boutons de modification
        document.addEventListener('click', (e) => {
            if (e.target.matches('[onclick*="editJobOffer"]')) {
                this.editJobOffer();
            } else if (e.target.matches('[onclick*="editCVs"]')) {
                this.editCVs();
            }
        });
    }

    collectJobData() {
        return {
            title: document.getElementById('jobTitle').value,
            department: document.getElementById('department').value,
            description: document.getElementById('jobDescription').value,
            skills: Array.from(document.querySelectorAll('.skill-tag')).map(tag => tag.textContent.trim()),
            experience: document.getElementById('experience').value
        };
    }

    collectCVData() {
        return Array.from(document.getElementById('fileList').children).map(file => ({
            name: file.querySelector('.filename').textContent.trim(),
            size: file.querySelector('.text-gray-500').textContent.trim()
        }));
    }

    updateVerificationView() {
        // Récupérer les données actuelles
        this.jobData = this.collectJobData();
        this.cvFiles = this.collectCVData();

        // Mettre à jour le résumé de l'offre
        const jobSummary = document.getElementById('jobSummary');
        jobSummary.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="text-lg font-semibold text-gray-800">${this.jobData.title}</h4>
                    <p class="text-gray-600">${this.jobData.department}</p>
                </div>
                <div>
                    <h5 class="font-medium text-gray-700">Description</h5>
                    <p class="text-gray-600">${this.jobData.description}</p>
                </div>
                <div>
                    <h5 class="font-medium text-gray-700">Compétences requises</h5>
                    <div class="flex flex-wrap gap-2 mt-2">
                        ${this.jobData.skills.map(skill => `
                            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                                ${skill}
                            </span>
                        `).join('')}
                    </div>
                </div>
                <div>
                    <h5 class="font-medium text-gray-700">Expérience</h5>
                    <p class="text-gray-600">${this.getExperienceText(this.jobData.experience)}</p>
                </div>
            </div>
        `;

        // Mettre à jour la liste des CVs
        const cvSummary = document.getElementById('cvSummary');
        if (this.cvFiles.length === 0) {
            cvSummary.innerHTML = `
                <div class="text-center py-4">
                    <p class="text-gray-500">Aucun CV importé</p>
                </div>
            `;
        } else {
            cvSummary.innerHTML = `
                <div class="space-y-3">
                    ${this.cvFiles.map((file, index) => `
                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div class="flex items-center space-x-3">
                                <span class="flex items-center justify-center w-8 h-8 rounded-full bg-green-100 text-green-700">
                                    ${index + 1}
                                </span>
                                <div>
                                    <span class="text-gray-700">${file.name}</span>
                                    <span class="text-gray-500 text-sm ml-2">${file.size}</span>
                                </div>
                            </div>
                            <button onclick="window.cvUploadHandler.previewFile('${file.name}')" 
                                    class="text-blue-600 hover:text-blue-800 transition-colors">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }

    getExperienceText(experience) {
        const experienceMap = {
            '0': '0-2 ans (Junior)',
            '2': '2-5 ans (Intermédiaire)',
            '5': '5+ ans (Senior)'
        };
        return experienceMap[experience] || 'Non spécifié';
    }

    editJobOffer() {
        this.currentStep = 1;
        this.updateStepVisuals();
    }

    editCVs() {
        this.currentStep = 2;
        this.updateStepVisuals();
    }

    updateStepVisuals() {
        // Mise à jour des indicateurs d'étape
        this.steps.forEach((step, index) => {
            if (index + 1 === this.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else if (index + 1 < this.currentStep) {
                step.classList.remove('active');
                step.classList.add('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        // Mise à jour du contenu
        this.contents.forEach((content, index) => {
            if (index + 1 === this.currentStep) {
                content.classList.add('active');
                content.classList.remove('hidden');
                // Si on est à l'étape de vérification, mettre à jour la vue
                if (index + 1 === 3) {
                    this.updateVerificationView();
                }
            } else {
                content.classList.remove('active');
                content.classList.add('hidden');
            }
        });

        // Mise à jour des boutons
        this.prevBtn.style.display = this.currentStep > 1 ? 'flex' : 'none';
        this.nextBtn.innerHTML = this.currentStep === this.totalSteps ? 
            '<span>Terminer</span><i class="fas fa-check ml-2"></i>' : 
            '<span>Suivant</span><i class="fas fa-arrow-right ml-2"></i>';
    }

    async validateStep() {
        switch (this.currentStep) {
            case 1: // Offre d'emploi
                const title = document.getElementById('jobTitle').value.trim();
                const department = document.getElementById('department').value;
                const description = document.getElementById('jobDescription').value.trim();
                const skills = document.querySelectorAll('.skill-tag');

                if (!title) {
                    alert('Veuillez saisir le titre du poste');
                    document.getElementById('jobTitle').focus();
                    return false;
                }
                if (!department) {
                    alert('Veuillez sélectionner un département');
                    document.getElementById('department').focus();
                    return false;
                }
                if (!description) {
                    alert('Veuillez saisir une description du poste');
                    document.getElementById('jobDescription').focus();
                    return false;
                }
                if (skills.length === 0) {
                    alert('Veuillez ajouter au moins une compétence requise');
                    document.getElementById('skillInput').focus();
                    return false;
                }
                return true;

            case 2: // Import CVs
                const cvList = document.getElementById('fileList');
                if (!cvList || cvList.children.length === 0) {
                    alert('Veuillez importer au moins un CV avant de continuer');
                    return false;
                }
                return true;

            case 3: // Vérification
                return true;

            case 4: // Résultats
                return true;

            default:
                return false;
        }
    }

    async goToNextStep() {
        try {
            // Désactiver les boutons pendant la validation
            this.nextBtn.disabled = true;
            this.prevBtn.disabled = true;
            
            // Afficher l'animation de chargement sur le bouton
            this.nextBtn.innerHTML = `
                <div class="flex items-center">
                    <div class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    <span>Validation...</span>
                </div>
            `;

            // Valider l'étape actuelle
            if (await this.validateStep()) {
                // Animer la transition
                const currentContent = this.contents[this.currentStep - 1];
                currentContent.style.opacity = '0';
                
                await new Promise(resolve => setTimeout(resolve, 300));

                if (this.currentStep < this.totalSteps) {
                    this.currentStep++;
                    this.updateStepVisuals();
                    
                    // Afficher la nouvelle étape avec animation
                    const nextContent = this.contents[this.currentStep - 1];
                    nextContent.style.opacity = '0';
                    setTimeout(() => {
                        nextContent.style.opacity = '1';
                        // Si on passe à l'étape des résultats, lancer l'analyse
                        if (this.currentStep === 4) {
                            window.cvMatchingClient.startAnalysis();
                        }
                    }, 50);
                } else {
                    // Terminer l'analyse
                    window.location.href = '/dashboard';
                }
            }
        } catch (error) {
            console.error('Erreur lors de la navigation:', error);
            alert('Une erreur est survenue lors du changement d\'étape');
        } finally {
            // Réactiver les boutons
            this.nextBtn.disabled = false;
            this.prevBtn.disabled = false;
            
            // Restaurer l'apparence du bouton suivant
            this.nextBtn.innerHTML = this.currentStep === this.totalSteps ? 
                '<span>Terminer</span><i class="fas fa-check ml-2"></i>' : 
                '<span>Suivant</span><i class="fas fa-arrow-right ml-2"></i>';
        }
    }

    goToPreviousStep() {
        if (this.currentStep > 1) {
            const currentContent = this.contents[this.currentStep - 1];
            currentContent.style.opacity = '0';
            
            setTimeout(() => {
                this.currentStep--;
                this.updateStepVisuals();
                
                const prevContent = this.contents[this.currentStep - 1];
                prevContent.style.opacity = '0';
                setTimeout(() => {
                    prevContent.style.opacity = '1';
                }, 50);
            }, 300);
        }
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.navigationManager = new NavigationManager();
});