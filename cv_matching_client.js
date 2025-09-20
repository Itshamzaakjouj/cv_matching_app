class CVMatchingClient {
    constructor() {
        this.analysisTime = 10; // Temps d'analyse en secondes
        this.remainingTime = this.analysisTime;
        this.timer = null;
    }

    async startAnalysis() {
        const loadingDiv = document.getElementById('analysisLoading');
        const resultsDiv = document.getElementById('analysisResults');
        const timerDiv = document.createElement('div');
        timerDiv.id = 'analysisTimer';
        timerDiv.className = 'mt-4 text-lg font-semibold text-blue-600';
        loadingDiv.appendChild(timerDiv);

        // Afficher le chargement et cacher les résultats
        loadingDiv.style.display = 'block';
        resultsDiv.style.display = 'none';

        // Démarrer le compte à rebours
        this.remainingTime = this.analysisTime;
        this.updateTimer();
        this.timer = setInterval(() => this.updateTimer(), 1000);

        try {
            // Récupérer les données de l'offre
            const jobData = {
                title: document.getElementById('jobTitle').value,
                department: document.getElementById('department').value,
                description: document.getElementById('jobDescription').value,
                skills: Array.from(document.querySelectorAll('.skill-tag')).map(tag => tag.textContent.trim()),
                experience: document.getElementById('experience').value
            };

            // Récupérer les CVs
            const cvFiles = Array.from(document.getElementById('fileList').children).map(file => ({
                name: file.querySelector('.filename').textContent,
                content: file.getAttribute('data-content') || 'Contenu du CV simulé'
            }));

            // Simuler l'envoi au serveur et l'analyse
            await new Promise(resolve => setTimeout(resolve, this.analysisTime * 1000));

            // Simuler les résultats
            const results = this.generateSimulatedResults(jobData, cvFiles);

            // Sauvegarder et afficher les résultats
            window.analysisStorage.saveAnalysis({
                jobData: jobData,
                results: results
            });
            
            // Afficher les résultats
            this.displayResults(results);
        } catch (error) {
            console.error('Erreur lors de l\'analyse:', error);
            loadingDiv.innerHTML = `
                <div class="text-red-600">
                    <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                    <p class="text-lg">Une erreur est survenue lors de l'analyse</p>
                    <p class="text-sm mt-2">${error.message}</p>
                </div>
            `;
        } finally {
            // Arrêter le timer
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        }
    }

    updateTimer() {
        const timerDiv = document.getElementById('analysisTimer');
        if (this.remainingTime > 0) {
            timerDiv.innerHTML = `
                <div class="flex items-center justify-center space-x-2">
                    <i class="fas fa-clock"></i>
                    <span>Temps restant : ${this.remainingTime} seconde${this.remainingTime > 1 ? 's' : ''}</span>
                </div>
            `;
            this.remainingTime--;
        } else {
            timerDiv.innerHTML = `
                <div class="flex items-center justify-center space-x-2 text-green-600">
                    <i class="fas fa-check-circle"></i>
                    <span>Analyse terminée !</span>
                </div>
            `;
        }
    }

    generateSimulatedResults(jobData, cvFiles) {
        return {
            globalMetrics: {
                averageScore: 75.5,
                bestScore: 92.3
            },
            candidates: cvFiles.map((cv, index) => ({
                name: cv.name,
                score: 90 - (index * 5),
                matchingDetails: {
                    competencies: 85 - (index * 3),
                    experience: 80 - (index * 2),
                    education: 95 - (index * 4),
                    softSkills: 88 - (index * 3)
                }
            })),
            skillsData: {
                required: jobData.skills.length,
                found: jobData.skills.length - 1
            }
        };
    }

    displayResults(results) {
        const loadingDiv = document.getElementById('analysisLoading');
        const resultsDiv = document.getElementById('analysisResults');

        // Mettre à jour les métriques globales
        document.querySelector('#globalMetrics .text-blue-700').textContent = 
            `${results.globalMetrics.averageScore.toFixed(1)}%`;
        document.querySelector('#globalMetrics .text-green-700').textContent = 
            `${results.globalMetrics.bestScore.toFixed(1)}%`;

        // Afficher le classement des candidats
        const rankingDiv = document.getElementById('candidateRanking');
        rankingDiv.innerHTML = results.candidates.map((candidate, index) => `
            <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <span class="flex items-center justify-center w-8 h-8 rounded-full ${
                            index === 0 ? 'bg-yellow-100 text-yellow-700' :
                            index === 1 ? 'bg-gray-100 text-gray-700' :
                            index === 2 ? 'bg-orange-100 text-orange-700' :
                            'bg-blue-100 text-blue-700'
                        }">
                            ${index + 1}
                        </span>
                        <div>
                            <h4 class="font-medium text-gray-800">${candidate.name}</h4>
                            <p class="text-sm text-gray-500">Score global: ${candidate.score.toFixed(1)}%</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-sm space-y-1">
                            <p class="text-blue-600">Compétences: ${candidate.matchingDetails.competencies}%</p>
                            <p class="text-green-600">Expérience: ${candidate.matchingDetails.experience}%</p>
                            <p class="text-purple-600">Formation: ${candidate.matchingDetails.education}%</p>
                            <p class="text-indigo-600">Soft Skills: ${candidate.matchingDetails.softSkills}%</p>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        // Initialiser les graphiques
        this.initializeCharts(results);

        // Afficher les résultats
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
    }

    initializeCharts(results) {
        // Distribution des scores
        const scoreCtx = document.getElementById('scoreDistribution').getContext('2d');
        new Chart(scoreCtx, {
            type: 'bar',
            data: {
                labels: results.candidates.map(c => c.name),
                datasets: [{
                    label: 'Score global',
                    data: results.candidates.map(c => c.score),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        // Compétences requises vs trouvées
        const skillsCtx = document.getElementById('skillsComparison').getContext('2d');
        new Chart(skillsCtx, {
            type: 'doughnut',
            data: {
                labels: ['Compétences trouvées', 'Compétences manquantes'],
                datasets: [{
                    data: [results.skillsData.found, results.skillsData.required - results.skillsData.found],
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.5)',
                        'rgba(239, 68, 68, 0.5)'
                    ],
                    borderColor: [
                        'rgb(34, 197, 94)',
                        'rgb(239, 68, 68)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.cvMatchingClient = new CVMatchingClient();
});