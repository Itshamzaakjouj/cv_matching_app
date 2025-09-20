class HistoryManager {
    constructor() {
        this.initializeEventListeners();
        this.updateHistoryTable();
    }

    initializeEventListeners() {
        // Écouter les mises à jour des analyses
        window.addEventListener('analysisDataUpdated', () => this.updateHistoryTable());
        
        // Gestionnaire pour le bouton de suppression de l'historique
        const clearButton = document.querySelector('[onclick*="clearHistory"]');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearHistory());
        }
    }

    updateHistoryTable() {
        const analyses = window.analysisStorage.getStorage().analyses;
        const tableBody = document.querySelector('#historyTable tbody') || document.querySelector('#historyTable');
        
        if (!analyses || analyses.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-8 text-gray-500 italic">
                        <i class="fas fa-history mr-2"></i>
                        Aucun historique d'analyse disponible
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = analyses.map((analysis, index) => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-4 py-3">
                    ${this.getFileIcon(analysis)}
                    <span class="ml-2">${analysis.candidates.map(c => c.name).join(', ')}</span>
                </td>
                <td class="px-4 py-3">
                    ${this.getScoreBadge(analysis.averageScore)}
                </td>
                <td class="px-4 py-3">
                    ${this.getStatusBadge(analysis.averageScore)}
                </td>
                <td class="px-4 py-3">
                    <div class="flex flex-col">
                        <span class="font-medium">${analysis.jobTitle}</span>
                        <span class="text-sm text-gray-500">${analysis.department}</span>
                    </div>
                </td>
                <td class="px-4 py-3">
                    ${this.formatDate(analysis.timestamp)}
                </td>
                <td class="px-4 py-3">
                    <div class="flex items-center space-x-2">
                        <button onclick="window.historyManager.viewDetails('${analysis.id}')"
                                class="text-blue-600 hover:text-blue-800 transition-colors">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button onclick="window.historyManager.downloadReport('${analysis.id}')"
                                class="text-green-600 hover:text-green-800 transition-colors">
                            <i class="fas fa-download"></i>
                        </button>
                        <button onclick="window.historyManager.deleteAnalysis('${analysis.id}')"
                                class="text-red-600 hover:text-red-800 transition-colors">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    getFileIcon(analysis) {
        return `<i class="fas fa-file-alt text-blue-500"></i>`;
    }

    getScoreBadge(score) {
        let colorClass;
        if (score >= 80) colorClass = 'bg-green-100 text-green-800';
        else if (score >= 60) colorClass = 'bg-blue-100 text-blue-800';
        else if (score >= 40) colorClass = 'bg-yellow-100 text-yellow-800';
        else colorClass = 'bg-red-100 text-red-800';

        return `
            <span class="px-3 py-1 rounded-full text-sm ${colorClass}">
                ${score.toFixed(1)}%
            </span>
        `;
    }

    getStatusBadge(score) {
        let status, colorClass;
        if (score >= 80) {
            status = 'Excellent';
            colorClass = 'bg-green-100 text-green-800';
        } else if (score >= 60) {
            status = 'Bon';
            colorClass = 'bg-blue-100 text-blue-800';
        } else if (score >= 40) {
            status = 'Moyen';
            colorClass = 'bg-yellow-100 text-yellow-800';
        } else {
            status = 'Faible';
            colorClass = 'bg-red-100 text-red-800';
        }

        return `
            <span class="px-3 py-1 rounded-full text-sm ${colorClass}">
                ${status}
            </span>
        `;
    }

    formatDate(timestamp) {
        const date = new Date(timestamp);
        return `
            <div class="flex flex-col">
                <span class="font-medium">
                    ${date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })}
                </span>
                <span class="text-sm text-gray-500">
                    ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                </span>
            </div>
        `;
    }

    viewDetails(analysisId) {
        const analysis = this.findAnalysis(analysisId);
        if (!analysis) return;

        // Créer une fenêtre modale avec les détails
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div class="p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-semibold text-gray-800">
                            Détails de l'analyse
                        </h2>
                        <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    
                    <div class="space-y-6">
                        <!-- Informations sur l'offre -->
                        <div class="bg-blue-50 p-4 rounded-lg">
                            <h3 class="text-lg font-medium text-blue-800 mb-2">
                                <i class="fas fa-briefcase mr-2"></i>
                                Offre d'emploi
                            </h3>
                            <div class="space-y-2">
                                <p><span class="font-medium">Poste :</span> ${analysis.jobTitle}</p>
                                <p><span class="font-medium">Département :</span> ${analysis.department}</p>
                            </div>
                        </div>

                        <!-- Métriques globales -->
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="bg-green-50 p-4 rounded-lg text-center">
                                <p class="text-sm text-green-600">Score moyen</p>
                                <p class="text-2xl font-bold text-green-700">${analysis.averageScore.toFixed(1)}%</p>
                            </div>
                            <div class="bg-blue-50 p-4 rounded-lg text-center">
                                <p class="text-sm text-blue-600">Meilleur score</p>
                                <p class="text-2xl font-bold text-blue-700">${analysis.bestScore.toFixed(1)}%</p>
                            </div>
                            <div class="bg-purple-50 p-4 rounded-lg text-center">
                                <p class="text-sm text-purple-600">CVs analysés</p>
                                <p class="text-2xl font-bold text-purple-700">${analysis.cvCount}</p>
                            </div>
                        </div>

                        <!-- Liste des candidats -->
                        <div class="bg-white rounded-lg border border-gray-200">
                            <h3 class="text-lg font-medium text-gray-800 p-4 border-b">
                                <i class="fas fa-users mr-2"></i>
                                Candidats
                            </h3>
                            <div class="divide-y">
                                ${analysis.candidates.map((candidate, index) => `
                                    <div class="p-4 hover:bg-gray-50">
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
                                                    <p class="font-medium text-gray-800">${candidate.name}</p>
                                                    <p class="text-sm text-gray-500">Score global: ${candidate.score.toFixed(1)}%</p>
                                                </div>
                                            </div>
                                            <div class="text-sm space-y-1">
                                                <p class="text-blue-600">Compétences: ${candidate.matchingDetails.competencies}%</p>
                                                <p class="text-green-600">Expérience: ${candidate.matchingDetails.experience}%</p>
                                                <p class="text-purple-600">Formation: ${candidate.matchingDetails.education}%</p>
                                                <p class="text-indigo-600">Soft Skills: ${candidate.matchingDetails.softSkills}%</p>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    downloadReport(analysisId) {
        const analysis = this.findAnalysis(analysisId);
        if (!analysis) return;

        // Générer le contenu du rapport
        const reportContent = `
Rapport d'analyse - ${analysis.jobTitle}
Date: ${new Date(analysis.timestamp).toLocaleString('fr-FR')}

INFORMATIONS SUR L'OFFRE
-----------------------
Poste: ${analysis.jobTitle}
Département: ${analysis.department}

MÉTRIQUES GLOBALES
-----------------
Score moyen: ${analysis.averageScore.toFixed(1)}%
Meilleur score: ${analysis.bestScore.toFixed(1)}%
Nombre de CVs analysés: ${analysis.cvCount}

RÉSULTATS PAR CANDIDAT
---------------------
${analysis.candidates.map((candidate, index) => `
${index + 1}. ${candidate.name}
   Score global: ${candidate.score.toFixed(1)}%
   Compétences: ${candidate.matchingDetails.competencies}%
   Expérience: ${candidate.matchingDetails.experience}%
   Formation: ${candidate.matchingDetails.education}%
   Soft Skills: ${candidate.matchingDetails.softSkills}%
`).join('\n')}
`;

        // Créer un blob et le télécharger
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `rapport_analyse_${analysis.jobTitle.toLowerCase().replace(/\s+/g, '_')}_${new Date(analysis.timestamp).toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    deleteAnalysis(analysisId) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer cette analyse ?')) return;

        const storage = window.analysisStorage.getStorage();
        const index = storage.analyses.findIndex(a => a.id === analysisId);
        
        if (index !== -1) {
            storage.analyses.splice(index, 1);
            localStorage.setItem('talentscope_analyses', JSON.stringify(storage));
            window.dispatchEvent(new CustomEvent('analysisDataUpdated'));
        }
    }

    clearHistory() {
        if (!confirm('Êtes-vous sûr de vouloir supprimer tout l\'historique des analyses ?')) return;

        const storage = window.analysisStorage.getStorage();
        storage.analyses = [];
        localStorage.setItem('talentscope_analyses', JSON.stringify(storage));
        window.dispatchEvent(new CustomEvent('analysisDataUpdated'));
    }

    findAnalysis(analysisId) {
        const storage = window.analysisStorage.getStorage();
        return storage.analyses.find(a => a.id === analysisId);
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.historyManager = new HistoryManager();
});
