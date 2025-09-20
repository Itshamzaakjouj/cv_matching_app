// ===== TALENTSCOPE - DASHBOARD JAVASCRIPT =====

// Gestionnaire du tableau de bord
const DashboardManager = {
    // Configuration
    config: {
        refreshInterval: 30000, // 30 secondes
        chartColors: {
            primary: '#2563eb',
            success: '#10b981',
            warning: '#f59e0b',
            error: '#ef4444',
            info: '#06b6d4'
        }
    },

    // Données du dashboard
    data: {
        stats: null,
        charts: {
            analyses: null,
            scores: null
        },
        activities: []
    },

    // Initialisation
    init: () => {
        Utils.log('Initialisation du tableau de bord');
        
        // Vérifier l'authentification
        if (!AuthManager.isLoggedIn()) {
            Utils.log('Utilisateur non authentifié, redirection...');
            window.location.href = '/auth';
            return;
        }

        // Initialiser les composants
        DashboardManager.initNavigation();
        DashboardManager.initCharts();
        DashboardManager.loadData();
        DashboardManager.initRefresh();
    },

    // Initialiser la navigation
    initNavigation: () => {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                DashboardManager.navigateToPage(page);
            });
        });
    },

    // Navigation entre pages
    navigateToPage: (page) => {
        const sessionId = AuthManager.getSessionId();
        
        switch (page) {
            case 'dashboard':
                window.location.href = `/dashboard?session_id=${sessionId}`;
                break;
            case 'analysis':
                window.location.href = `/analysis?session_id=${sessionId}`;
                break;
            case 'cvs':
                // Page CVs traités (à implémenter)
                Notifications.info('Page CVs traités en cours de développement');
                break;
            case 'config':
                // Page de configuration (à implémenter)
                Notifications.info('Page de configuration en cours de développement');
                break;
            default:
                Utils.log(`Page inconnue: ${page}`);
        }
    },

    // Charger les données
    loadData: async () => {
        try {
            Utils.log('Chargement des données du dashboard');
            
            // Charger les statistiques
            await DashboardManager.loadStats();
            
            // Charger les activités récentes
            await DashboardManager.loadActivities();
            
            // Mettre à jour les graphiques
            DashboardManager.updateCharts();
            
        } catch (error) {
            Utils.log('Erreur lors du chargement des données', error);
            Notifications.error('Erreur lors du chargement des données');
        }
    },

    // Charger les statistiques
    loadStats: async () => {
        try {
            const sessionId = AuthManager.getSessionId();
            const response = await API.get(`/api/dashboard-data?session_id=${sessionId}`);
            
            if (response) {
                DashboardManager.data.stats = response.stats;
                DashboardManager.data.charts.analyses = response.trends;
                DashboardManager.updateStatsDisplay();
            }
        } catch (error) {
            Utils.log('Erreur lors du chargement des statistiques', error);
            // Utiliser des données de démonstration
            DashboardManager.loadDemoStats();
        }
    },

    // Charger les données de démonstration
    loadDemoStats: () => {
        DashboardManager.data.stats = {
            total_analyses: 24,
            total_cvs: 156,
            average_score: 78.5,
            success_rate: 92.3
        };

        DashboardManager.data.charts.analyses = {
            daily_analyses: [12, 15, 8, 20, 18, 16, 8],
            scores: [75.2, 76.1, 72.8, 81.5, 79.3, 78.1, 80.2]
        };

        DashboardManager.data.activities = [
            {
                icon: 'fas fa-file-pdf',
                title: 'CV analysé',
                description: 'cv_hamza.pdf - Score: 91.3%',
                time: 'Il y a 2 minutes'
            },
            {
                icon: 'fas fa-chart-line',
                title: 'Analyse terminée',
                description: '5 CVs analysés avec succès',
                time: 'Il y a 15 minutes'
            },
            {
                icon: 'fas fa-user-plus',
                title: 'Nouvel utilisateur',
                description: 'Utilisateur ajouté au système',
                time: 'Il y a 1 heure'
            }
        ];

        DashboardManager.updateStatsDisplay();
        DashboardManager.updateActivitiesDisplay();
    },

    // Mettre à jour l'affichage des statistiques
    updateStatsDisplay: () => {
        const stats = DashboardManager.data.stats;
        if (!stats) return;

        // Animer les compteurs
        DashboardManager.animateCounter('totalAnalyses', stats.total_analyses);
        DashboardManager.animateCounter('totalCVs', stats.total_cvs);
        DashboardManager.animateCounter('averageScore', stats.average_score, '%');
        DashboardManager.animateCounter('successRate', stats.success_rate, '%');
    },

    // Animer un compteur
    animateCounter: (elementId, targetValue, suffix = '') => {
        const element = document.getElementById(elementId);
        if (!element) return;

        const startValue = 0;
        const duration = 2000;
        const startTime = performance.now();

        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = startValue + (targetValue - startValue) * easeOutQuart;
            
            element.textContent = Math.round(currentValue) + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    },

    // Charger les activités récentes
    loadActivities: async () => {
        // Simulation de chargement des activités
        setTimeout(() => {
            DashboardManager.updateActivitiesDisplay();
        }, 1000);
    },

    // Mettre à jour l'affichage des activités
    updateActivitiesDisplay: () => {
        const container = document.getElementById('recentActivity');
        if (!container) return;

        const activities = DashboardManager.data.activities;
        if (!activities || activities.length === 0) return;

        container.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="${activity.icon}"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-description">${activity.description}</div>
                </div>
                <div class="activity-time">${activity.time}</div>
            </div>
        `).join('');
    },

    // Initialiser les graphiques
    initCharts: () => {
        DashboardManager.initAnalysesChart();
        DashboardManager.initScoresChart();
    },

    // Graphique des analyses
    initAnalysesChart: () => {
        const ctx = document.getElementById('analysesChart');
        if (!ctx) return;

        DashboardManager.data.charts.analysesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
                datasets: [{
                    label: 'Analyses',
                    data: [12, 15, 8, 20, 18, 16, 8],
                    borderColor: DashboardManager.config.chartColors.primary,
                    backgroundColor: `${DashboardManager.config.chartColors.primary}20`,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#f1f5f9'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    },

    // Graphique des scores
    initScoresChart: () => {
        const ctx = document.getElementById('scoresChart');
        if (!ctx) return;

        DashboardManager.data.charts.scoresChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Excellent', 'Très bon', 'Bon', 'Moyen'],
                datasets: [{
                    data: [35, 40, 20, 5],
                    backgroundColor: [
                        DashboardManager.config.chartColors.success,
                        DashboardManager.config.chartColors.primary,
                        DashboardManager.config.chartColors.warning,
                        DashboardManager.config.chartColors.error
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    },

    // Mettre à jour les graphiques
    updateCharts: () => {
        if (DashboardManager.data.charts.analyses) {
            DashboardManager.updateAnalysesChart();
        }
    },

    // Mettre à jour le graphique des analyses
    updateAnalysesChart: () => {
        const chart = DashboardManager.data.charts.analysesChart;
        if (!chart) return;

        const trends = DashboardManager.data.charts.analyses;
        if (!trends) return;

        chart.data.datasets[0].data = trends.daily_analyses;
        chart.update();
    },

    // Initialiser le rafraîchissement automatique
    initRefresh: () => {
        // Rafraîchir les données toutes les 30 secondes
        setInterval(() => {
            DashboardManager.loadData();
        }, DashboardManager.config.refreshInterval);

        // Rafraîchir au focus de la fenêtre
        window.addEventListener('focus', () => {
            DashboardManager.loadData();
        });
    },

    // Gérer les contrôles des graphiques
    initChartControls: () => {
        const controls = document.querySelectorAll('.chart-controls .btn-small');
        controls.forEach(control => {
            control.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Retirer la classe active de tous les contrôles
                controls.forEach(c => c.classList.remove('active'));
                
                // Ajouter la classe active au contrôle cliqué
                control.classList.add('active');
                
                // Mettre à jour le graphique selon la période
                const period = control.dataset.period;
                DashboardManager.updateChartPeriod(period);
            });
        });
    },

    // Mettre à jour la période du graphique
    updateChartPeriod: (period) => {
        Utils.log(`Mise à jour de la période du graphique: ${period}`);
        
        // Simulation de données selon la période
        let data;
        switch (period) {
            case '7d':
                data = [12, 15, 8, 20, 18, 16, 8];
                break;
            case '30d':
                data = Array.from({length: 30}, () => Math.floor(Math.random() * 20) + 5);
                break;
            case '90d':
                data = Array.from({length: 90}, () => Math.floor(Math.random() * 25) + 3);
                break;
            default:
                data = [12, 15, 8, 20, 18, 16, 8];
        }

        if (DashboardManager.data.charts.analysesChart) {
            DashboardManager.data.charts.analysesChart.data.datasets[0].data = data;
            DashboardManager.data.charts.analysesChart.update();
        }
    }
};

// Fonction globale pour la déconnexion
window.logout = () => {
    AuthManager.logout();
};

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    Utils.log('Initialisation de la page du tableau de bord');
    DashboardManager.init();
});

// Export pour utilisation globale
window.DashboardManager = DashboardManager;
