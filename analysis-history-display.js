// ============================================================================
// AFFICHAGE DE L'HISTORIQUE DES ANALYSES - TalentScope
// ============================================================================

class AnalysisHistoryDisplay {
    constructor(containerId = 'history-container') {
        this.container = document.getElementById(containerId);
        this.historyService = window.analysisHistoryService;
        this.currentFilters = {};
        this.sortBy = 'timestamp';
        this.sortOrder = 'desc';
        this.currentPage = 1;
        this.itemsPerPage = 10;
        
        this.init();
    }

    init() {
        if (!this.container) {
            console.error('Container d\'historique non trouvé');
            return;
        }

        this.createHistoryInterface();
        this.bindEvents();
        this.loadHistory();
    }

    createHistoryInterface() {
        this.container.innerHTML = `
            <div class="history-interface">
                <!-- En-tête avec statistiques -->
                <div class="history-header">
                    <div class="header-content">
                        <div class="title-section">
                            <h2><i class="fas fa-history"></i> Historique des Analyses</h2>
                            <p class="subtitle">Suivi complet de toutes vos analyses de CV</p>
                        </div>
                        <div class="stats-section">
                            <div class="stat-card">
                                <div class="stat-number" id="total-analyses">0</div>
                                <div class="stat-label">Total Analyses</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="avg-score">0%</div>
                                <div class="stat-label">Score Moyen</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="today-analyses">0</div>
                                <div class="stat-label">Aujourd'hui</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Filtres et contrôles -->
                <div class="history-controls">
                    <div class="filters-section">
                        <div class="filter-group">
                            <label for="search-input">Rechercher :</label>
                            <input type="text" id="search-input" placeholder="Nom CV, position, utilisateur...">
                        </div>
                        <div class="filter-group">
                            <label for="status-filter">Statut :</label>
                            <select id="status-filter">
                                <option value="">Tous les statuts</option>
                                <option value="completed">Terminé</option>
                                <option value="processing">En cours</option>
                                <option value="failed">Échoué</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="score-filter">Score minimum :</label>
                            <select id="score-filter">
                                <option value="">Tous les scores</option>
                                <option value="90">90%+ (Excellent)</option>
                                <option value="70">70%+ (Bon)</option>
                                <option value="50">50%+ (Moyen)</option>
                                <option value="0">0%+ (Tous)</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="date-filter">Période :</label>
                            <select id="date-filter">
                                <option value="">Toutes les périodes</option>
                                <option value="today">Aujourd'hui</option>
                                <option value="week">Cette semaine</option>
                                <option value="month">Ce mois</option>
                                <option value="custom">Période personnalisée</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="actions-section">
                        <button class="btn btn-secondary" id="refresh-btn">
                            <i class="fas fa-sync-alt"></i> Actualiser
                        </button>
                        <button class="btn btn-primary" id="export-btn">
                            <i class="fas fa-download"></i> Exporter
                        </button>
                        <button class="btn btn-danger" id="clear-history-btn">
                            <i class="fas fa-trash"></i> Vider l'historique
                        </button>
                    </div>
                </div>

                <!-- Tri et pagination -->
                <div class="history-sorting">
                    <div class="sort-controls">
                        <label for="sort-select">Trier par :</label>
                        <select id="sort-select">
                            <option value="timestamp">Date (récent)</option>
                            <option value="score">Score (élevé)</option>
                            <option value="cvName">Nom CV (A-Z)</option>
                            <option value="position">Position (A-Z)</option>
                        </select>
                        <button class="btn btn-sm" id="sort-order-btn">
                            <i class="fas fa-sort-amount-down"></i>
                        </button>
                    </div>
                    
                    <div class="pagination-info">
                        <span id="pagination-info">Affichage 1-10 de 0</span>
                    </div>
                </div>

                <!-- Liste des analyses -->
                <div class="history-list" id="history-list">
                    <!-- Les éléments d'historique seront insérés ici -->
                </div>

                <!-- Pagination -->
                <div class="pagination" id="pagination">
                    <!-- Les contrôles de pagination seront insérés ici -->
                </div>

                <!-- Message d'état vide -->
                <div class="empty-state" id="empty-state" style="display: none;">
                    <div class="empty-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <h3>Aucune analyse trouvée</h3>
                    <p>Il n'y a aucune analyse correspondant à vos critères de recherche.</p>
                    <button class="btn btn-primary" onclick="this.clearFilters()">
                        <i class="fas fa-times"></i> Effacer les filtres
                    </button>
                </div>
            </div>
        `;

        this.addHistoryStyles();
    }

    addHistoryStyles() {
        const styles = `
            <style>
                .history-interface {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }

                .history-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 16px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                }

                .header-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 20px;
                }

                .title-section h2 {
                    font-size: 2rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                }

                .title-section .subtitle {
                    opacity: 0.9;
                    font-size: 1.1rem;
                }

                .stats-section {
                    display: flex;
                    gap: 20px;
                    flex-wrap: wrap;
                }

                .stat-card {
                    background: rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(10px);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    min-width: 120px;
                }

                .stat-number {
                    font-size: 2rem;
                    font-weight: 700;
                    margin-bottom: 5px;
                }

                .stat-label {
                    font-size: 0.9rem;
                    opacity: 0.9;
                }

                .history-controls {
                    background: white;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 20px;
                }

                .filters-section {
                    display: flex;
                    gap: 20px;
                    flex-wrap: wrap;
                    align-items: end;
                }

                .filter-group {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                }

                .filter-group label {
                    font-weight: 600;
                    color: #374151;
                    font-size: 0.9rem;
                }

                .filter-group input,
                .filter-group select {
                    padding: 8px 12px;
                    border: 1px solid #D1D5DB;
                    border-radius: 8px;
                    font-size: 14px;
                    min-width: 150px;
                }

                .filter-group input:focus,
                .filter-group select:focus {
                    outline: none;
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }

                .actions-section {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }

                .btn {
                    padding: 10px 16px;
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

                .btn-primary {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                }

                .btn-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }

                .btn-secondary {
                    background: #F3F4F6;
                    color: #374151;
                    border: 1px solid #D1D5DB;
                }

                .btn-secondary:hover {
                    background: #E5E7EB;
                }

                .btn-danger {
                    background: #EF4444;
                    color: white;
                }

                .btn-danger:hover {
                    background: #DC2626;
                }

                .btn-sm {
                    padding: 6px 10px;
                    font-size: 12px;
                }

                .history-sorting {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding: 15px 20px;
                    background: #F9FAFB;
                    border-radius: 8px;
                }

                .sort-controls {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }

                .sort-controls label {
                    font-weight: 600;
                    color: #374151;
                }

                .sort-controls select {
                    padding: 6px 10px;
                    border: 1px solid #D1D5DB;
                    border-radius: 6px;
                    font-size: 14px;
                }

                .history-list {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }

                .history-item {
                    background: white;
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                    border-left: 4px solid #667eea;
                }

                .history-item:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                }

                .history-item-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: start;
                    margin-bottom: 15px;
                }

                .history-item-title {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }

                .history-item-title h3 {
                    font-size: 1.2rem;
                    font-weight: 600;
                    color: #374151;
                    margin: 0;
                }

                .history-item-title .score-badge {
                    background: linear-gradient(135deg, #10B981, #059669);
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                }

                .history-item-meta {
                    display: flex;
                    gap: 20px;
                    color: #6B7280;
                    font-size: 0.9rem;
                }

                .history-item-details {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }

                .detail-item {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                }

                .detail-label {
                    font-weight: 600;
                    color: #374151;
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .detail-value {
                    color: #6B7280;
                    font-size: 0.9rem;
                }

                .history-item-actions {
                    display: flex;
                    gap: 10px;
                    margin-top: 15px;
                }

                .action-btn {
                    padding: 6px 12px;
                    border: 1px solid #D1D5DB;
                    background: white;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .action-btn:hover {
                    background: #F3F4F6;
                }

                .action-btn.danger {
                    border-color: #EF4444;
                    color: #EF4444;
                }

                .action-btn.danger:hover {
                    background: #FEF2F2;
                }

                .pagination {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 10px;
                    margin-top: 30px;
                }

                .pagination button {
                    padding: 8px 12px;
                    border: 1px solid #D1D5DB;
                    background: white;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .pagination button:hover:not(:disabled) {
                    background: #F3F4F6;
                }

                .pagination button:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }

                .pagination button.active {
                    background: #667eea;
                    color: white;
                    border-color: #667eea;
                }

                .empty-state {
                    text-align: center;
                    padding: 60px 20px;
                    color: #6B7280;
                }

                .empty-state .empty-icon {
                    font-size: 4rem;
                    margin-bottom: 20px;
                    opacity: 0.5;
                }

                .empty-state h3 {
                    font-size: 1.5rem;
                    margin-bottom: 10px;
                    color: #374151;
                }

                @media (max-width: 768px) {
                    .header-content {
                        flex-direction: column;
                        text-align: center;
                    }

                    .stats-section {
                        justify-content: center;
                    }

                    .history-controls {
                        flex-direction: column;
                        align-items: stretch;
                    }

                    .filters-section {
                        flex-direction: column;
                        gap: 15px;
                    }

                    .filter-group input,
                    .filter-group select {
                        min-width: auto;
                        width: 100%;
                    }

                    .actions-section {
                        justify-content: center;
                    }

                    .history-sorting {
                        flex-direction: column;
                        gap: 15px;
                        text-align: center;
                    }

                    .history-item-details {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    bindEvents() {
        // Recherche
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.currentFilters.search = e.target.value;
                this.currentPage = 1;
                this.loadHistory();
            });
        }

        // Filtres
        const statusFilter = document.getElementById('status-filter');
        if (statusFilter) {
            statusFilter.addEventListener('change', (e) => {
                this.currentFilters.status = e.target.value;
                this.currentPage = 1;
                this.loadHistory();
            });
        }

        const scoreFilter = document.getElementById('score-filter');
        if (scoreFilter) {
            scoreFilter.addEventListener('change', (e) => {
                this.currentFilters.minScore = e.target.value ? parseInt(e.target.value) : null;
                this.currentPage = 1;
                this.loadHistory();
            });
        }

        const dateFilter = document.getElementById('date-filter');
        if (dateFilter) {
            dateFilter.addEventListener('change', (e) => {
                this.currentFilters.dateRange = e.target.value;
                this.currentPage = 1;
                this.loadHistory();
            });
        }

        // Tri
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.sortBy = e.target.value;
                this.loadHistory();
            });
        }

        const sortOrderBtn = document.getElementById('sort-order-btn');
        if (sortOrderBtn) {
            sortOrderBtn.addEventListener('click', () => {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
                this.updateSortButton();
                this.loadHistory();
            });
        }

        // Actions
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadHistory());
        }

        const exportBtn = document.getElementById('export-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportHistory());
        }

        const clearHistoryBtn = document.getElementById('clear-history-btn');
        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        }

        // Écouter les mises à jour de l'historique
        window.addEventListener('analysisHistoryUpdated', () => {
            this.loadHistory();
        });
    }

    loadHistory() {
        if (!this.historyService) {
            console.error('Service d\'historique non disponible');
            return;
        }

        // Obtenir l'historique filtré
        let history = this.historyService.getHistory(this.currentFilters);

        // Recherche textuelle
        if (this.currentFilters.search) {
            history = this.historyService.searchHistory(this.currentFilters.search);
        }

        // Appliquer le tri
        history = this.sortHistory(history);

        // Appliquer la pagination
        const totalItems = history.length;
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const paginatedHistory = history.slice(startIndex, endIndex);

        // Afficher l'historique
        this.displayHistory(paginatedHistory);
        this.updatePagination(totalItems);
        this.updateStatistics();
    }

    sortHistory(history) {
        return history.sort((a, b) => {
            let aValue, bValue;

            switch (this.sortBy) {
                case 'score':
                    aValue = a.analysis.score;
                    bValue = b.analysis.score;
                    break;
                case 'cvName':
                    aValue = a.analysis.cvName.toLowerCase();
                    bValue = b.analysis.cvName.toLowerCase();
                    break;
                case 'position':
                    aValue = a.analysis.position.toLowerCase();
                    bValue = b.analysis.position.toLowerCase();
                    break;
                default:
                    aValue = new Date(a.timestamp);
                    bValue = new Date(b.timestamp);
            }

            if (this.sortOrder === 'asc') {
                return aValue > bValue ? 1 : -1;
            } else {
                return aValue < bValue ? 1 : -1;
            }
        });
    }

    displayHistory(history) {
        const historyList = document.getElementById('history-list');
        const emptyState = document.getElementById('empty-state');

        if (!historyList) return;

        if (history.length === 0) {
            historyList.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        historyList.style.display = 'block';
        emptyState.style.display = 'none';

        historyList.innerHTML = history.map(item => this.createHistoryItemHTML(item)).join('');
    }

    createHistoryItemHTML(item) {
        const date = new Date(item.timestamp);
        const scoreClass = item.analysis.score >= 70 ? 'excellent' : item.analysis.score >= 50 ? 'good' : 'poor';
        
        return `
            <div class="history-item" data-id="${item.id}">
                <div class="history-item-header">
                    <div class="history-item-title">
                        <h3>${this.escapeHtml(item.analysis.cvName)}</h3>
                        <span class="score-badge ${scoreClass}">${item.analysis.score}%</span>
                    </div>
                    <div class="history-item-meta">
                        <span><i class="fas fa-user"></i> ${this.escapeHtml(item.user.name)}</span>
                        <span><i class="fas fa-clock"></i> ${date.toLocaleString()}</span>
                        <span><i class="fas fa-tag"></i> ${this.escapeHtml(item.analysis.status)}</span>
                    </div>
                </div>
                
                <div class="history-item-details">
                    <div class="detail-item">
                        <div class="detail-label">Position</div>
                        <div class="detail-value">${this.escapeHtml(item.analysis.position)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Département</div>
                        <div class="detail-value">${this.escapeHtml(item.analysis.department)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Score Compatibilité</div>
                        <div class="detail-value">${item.results.compatibilityScore}%</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Durée</div>
                        <div class="detail-value">${item.analysis.duration}s</div>
                    </div>
                </div>

                <div class="history-item-actions">
                    <button class="action-btn" onclick="this.viewAnalysis('${item.id}')">
                        <i class="fas fa-eye"></i> Voir
                    </button>
                    <button class="action-btn" onclick="this.exportAnalysis('${item.id}')">
                        <i class="fas fa-download"></i> Exporter
                    </button>
                    <button class="action-btn danger" onclick="this.deleteAnalysis('${item.id}')">
                        <i class="fas fa-trash"></i> Supprimer
                    </button>
                </div>
            </div>
        `;
    }

    updatePagination(totalItems) {
        const pagination = document.getElementById('pagination');
        const paginationInfo = document.getElementById('pagination-info');
        
        if (!pagination || !paginationInfo) return;

        const totalPages = Math.ceil(totalItems / this.itemsPerPage);
        const startItem = (this.currentPage - 1) * this.itemsPerPage + 1;
        const endItem = Math.min(this.currentPage * this.itemsPerPage, totalItems);

        paginationInfo.textContent = `Affichage ${startItem}-${endItem} de ${totalItems}`;

        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '';

        // Bouton précédent
        paginationHTML += `
            <button ${this.currentPage === 1 ? 'disabled' : ''} onclick="this.goToPage(${this.currentPage - 1})">
                <i class="fas fa-chevron-left"></i>
            </button>
        `;

        // Pages
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                paginationHTML += `
                    <button class="${i === this.currentPage ? 'active' : ''}" onclick="this.goToPage(${i})">
                        ${i}
                    </button>
                `;
            } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
                paginationHTML += '<span>...</span>';
            }
        }

        // Bouton suivant
        paginationHTML += `
            <button ${this.currentPage === totalPages ? 'disabled' : ''} onclick="this.goToPage(${this.currentPage + 1})">
                <i class="fas fa-chevron-right"></i>
            </button>
        `;

        pagination.innerHTML = paginationHTML;
    }

    updateStatistics() {
        if (!this.historyService) return;

        const stats = this.historyService.getStatistics();
        
        document.getElementById('total-analyses').textContent = stats.total;
        document.getElementById('avg-score').textContent = stats.averageScore + '%';
        document.getElementById('today-analyses').textContent = this.historyService.getTodayAnalyses().length;
    }

    updateSortButton() {
        const sortOrderBtn = document.getElementById('sort-order-btn');
        if (sortOrderBtn) {
            const icon = this.sortOrder === 'asc' ? 'fa-sort-amount-up' : 'fa-sort-amount-down';
            sortOrderBtn.innerHTML = `<i class="fas ${icon}"></i>`;
        }
    }

    goToPage(page) {
        this.currentPage = page;
        this.loadHistory();
    }

    viewAnalysis(id) {
        const analysis = this.historyService.getAnalysisById(id);
        if (analysis) {
            // Ouvrir une modal ou rediriger vers la page de détail
            console.log('Voir analyse:', analysis);
            // TODO: Implémenter l'affichage détaillé
        }
    }

    exportAnalysis(id) {
        const analysis = this.historyService.getAnalysisById(id);
        if (analysis) {
            const data = JSON.stringify(analysis, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analyse_${analysis.analysis.cvName}_${analysis.id}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
    }

    deleteAnalysis(id) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cette analyse de l\'historique ?')) {
            this.historyService.deleteAnalysis(id);
        }
    }

    exportHistory() {
        const data = this.historyService.exportHistory('json');
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `historique_analyses_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    clearHistory() {
        if (confirm('Êtes-vous sûr de vouloir vider tout l\'historique ? Cette action est irréversible.')) {
            this.historyService.clearAllHistory();
        }
    }

    clearFilters() {
        this.currentFilters = {};
        this.currentPage = 1;
        
        // Réinitialiser les champs de filtre
        document.getElementById('search-input').value = '';
        document.getElementById('status-filter').value = '';
        document.getElementById('score-filter').value = '';
        document.getElementById('date-filter').value = '';
        
        this.loadHistory();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Export pour utilisation dans d'autres modules
window.AnalysisHistoryDisplay = AnalysisHistoryDisplay;
