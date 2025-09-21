// ============================================================================
// MENU DE NAVIGATION AVEC TRADUCTEUR - TalentScope
// ============================================================================

class NavigationMenu {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('analysis')) return 'analysis';
        if (path.includes('translation')) return 'translation';
        if (path.includes('auth')) return 'auth';
        return 'dashboard';
    }

    init() {
        this.createNavigationMenu();
        this.bindEvents();
    }

    createNavigationMenu() {
        const menuHTML = `
            <div class="navigation-menu">
                <div class="nav-header">
                    <div class="logo">
                        <img src="Logos/TalentScope.png" alt="TalentScope" class="logo-img">
                        <h1>TalentScope</h1>
                    </div>
                    <div class="language-selector">
                        <select id="main-language-selector">
                            <option value="fr">🇫🇷 Français</option>
                            <option value="en">🇺🇸 English</option>
                        </select>
                    </div>
                </div>
                
                <nav class="main-nav">
                    <ul class="nav-list">
                        <li class="nav-item ${this.currentPage === 'dashboard' ? 'active' : ''}">
                            <a href="modern_dashboard.html" class="nav-link">
                                <i class="fas fa-tachometer-alt"></i>
                                <span data-translate="dashboard">Tableau de bord</span>
                            </a>
                        </li>
                        <li class="nav-item ${this.currentPage === 'analysis' ? 'active' : ''}">
                            <a href="analysis_interface.html" class="nav-link">
                                <i class="fas fa-chart-line"></i>
                                <span data-translate="analysis">Analyse</span>
                            </a>
                        </li>
                        <li class="nav-item ${this.currentPage === 'translation' ? 'active' : ''}">
                            <a href="translation-widget.html" class="nav-link">
                                <i class="fas fa-language"></i>
                                <span data-translate="translator">Traducteur</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="settings.html" class="nav-link">
                                <i class="fas fa-cog"></i>
                                <span data-translate="settings">Paramètres</span>
                            </a>
                        </li>
                    </ul>
                </nav>

                <div class="nav-footer">
                    <div class="user-info">
                        <div class="user-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="user-details">
                            <span class="user-name" id="user-name">Utilisateur</span>
                            <span class="user-role" id="user-role">Administrateur</span>
                        </div>
                    </div>
                    <button class="logout-btn" onclick="logout()">
                        <i class="fas fa-sign-out-alt"></i>
                        <span data-translate="logout">Déconnexion</span>
                    </button>
                </div>
            </div>
        `;

        // Ajouter le menu à la page
        const existingMenu = document.querySelector('.navigation-menu');
        if (existingMenu) {
            existingMenu.remove();
        }

        document.body.insertAdjacentHTML('afterbegin', menuHTML);
        this.addNavigationStyles();
    }

    addNavigationStyles() {
        const styles = `
            <style>
                .navigation-menu {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 280px;
                    height: 100vh;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(15px);
                    border-radius: 0 20px 20px 0;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    z-index: 1000;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }

                .nav-header {
                    padding: 30px 20px;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                }

                .logo {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    margin-bottom: 20px;
                }

                .logo-img {
                    width: 40px;
                    height: 40px;
                    object-fit: contain;
                }

                .logo h1 {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-size: 1.5rem;
                    font-weight: 700;
                }

                .language-selector {
                    margin-top: 15px;
                }

                .language-selector select {
                    width: 100%;
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background: white;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .language-selector select:focus {
                    outline: none;
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }

                .main-nav {
                    flex: 1;
                    padding: 20px 0;
                    overflow-y: auto;
                }

                .nav-list {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }

                .nav-item {
                    margin: 5px 0;
                }

                .nav-link {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    padding: 15px 20px;
                    color: #374151;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    border-radius: 0 25px 25px 0;
                    margin-right: 20px;
                }

                .nav-link:hover {
                    background: rgba(102, 126, 234, 0.1);
                    color: #667eea;
                    transform: translateX(5px);
                }

                .nav-item.active .nav-link {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                }

                .nav-link i {
                    width: 20px;
                    text-align: center;
                    font-size: 1.1rem;
                }

                .nav-footer {
                    padding: 20px;
                    border-top: 1px solid rgba(0, 0, 0, 0.1);
                }

                .user-info {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 15px;
                    padding: 10px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 10px;
                }

                .user-avatar {
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.2rem;
                }

                .user-details {
                    flex: 1;
                }

                .user-name {
                    display: block;
                    font-weight: 600;
                    color: #374151;
                    font-size: 0.9rem;
                }

                .user-role {
                    display: block;
                    color: #6B7280;
                    font-size: 0.8rem;
                }

                .logout-btn {
                    width: 100%;
                    padding: 12px;
                    background: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    transition: all 0.3s ease;
                }

                .logout-btn:hover {
                    background: #DC2626;
                    transform: translateY(-2px);
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .navigation-menu {
                        width: 100%;
                        border-radius: 0;
                        transform: translateX(-100%);
                        transition: transform 0.3s ease;
                    }

                    .navigation-menu.open {
                        transform: translateX(0);
                    }

                    .nav-link {
                        margin-right: 0;
                        border-radius: 8px;
                        margin: 5px 10px;
                    }
                }

                /* Animation pour le changement de langue */
                .language-change {
                    animation: languageChange 0.5s ease;
                }

                @keyframes languageChange {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    bindEvents() {
        // Sélecteur de langue principal
        const languageSelector = document.getElementById('main-language-selector');
        if (languageSelector) {
            // Charger la langue sauvegardée
            const savedLang = localStorage.getItem('selectedLanguage') || 'fr';
            languageSelector.value = savedLang;

            languageSelector.addEventListener('change', (e) => {
                const newLang = e.target.value;
                this.changeLanguage(newLang);
            });
        }

        // Gestion du menu mobile
        this.setupMobileMenu();
    }

    changeLanguage(newLang) {
        // Sauvegarder la langue
        localStorage.setItem('selectedLanguage', newLang);

        // Ajouter l'animation
        const selector = document.getElementById('main-language-selector');
        if (selector) {
            selector.classList.add('language-change');
            setTimeout(() => {
                selector.classList.remove('language-change');
            }, 500);
        }

        // Utiliser le système de traduction existant si disponible
        if (window.TranslationSystem) {
            window.TranslationSystem.changeLanguage(newLang);
        } else {
            // Fallback simple
            this.simpleTranslate(newLang);
        }

        console.log(`Langue changée vers: ${newLang}`);
    }

    simpleTranslate(lang) {
        const translations = {
            fr: {
                'dashboard': 'Tableau de bord',
                'analysis': 'Analyse',
                'translator': 'Traducteur',
                'settings': 'Paramètres',
                'logout': 'Déconnexion'
            },
            en: {
                'dashboard': 'Dashboard',
                'analysis': 'Analysis',
                'translator': 'Translator',
                'settings': 'Settings',
                'logout': 'Logout'
            }
        };

        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[lang] && translations[lang][key]) {
                element.textContent = translations[lang][key];
            }
        });
    }

    setupMobileMenu() {
        // Créer le bouton hamburger pour mobile
        if (window.innerWidth <= 768) {
            const hamburger = document.createElement('button');
            hamburger.className = 'mobile-menu-btn';
            hamburger.innerHTML = '<i class="fas fa-bars"></i>';
            hamburger.style.cssText = `
                position: fixed;
                top: 20px;
                left: 20px;
                z-index: 1001;
                background: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 8px;
                padding: 10px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            `;

            hamburger.addEventListener('click', () => {
                const menu = document.querySelector('.navigation-menu');
                menu.classList.toggle('open');
            });

            document.body.appendChild(hamburger);
        }
    }

    updateUserInfo() {
        // Mettre à jour les informations utilisateur
        const currentUser = window.userDatabase?.getCurrentUser();
        if (currentUser) {
            const userName = document.getElementById('user-name');
            const userRole = document.getElementById('user-role');
            
            if (userName) userName.textContent = currentUser.fullName || 'Utilisateur';
            if (userRole) userRole.textContent = currentUser.role || 'Utilisateur';
        }
    }
}

// Fonction de déconnexion
function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        // Nettoyer les données utilisateur
        if (window.userDatabase) {
            window.userDatabase.clearCurrentUser();
        }
        
        // Rediriger vers la page d'authentification
        window.location.href = 'auth_interface.html';
    }
}

// Initialiser le menu de navigation
document.addEventListener('DOMContentLoaded', () => {
    // Ne pas initialiser sur la page d'authentification
    if (!window.location.pathname.includes('auth_interface.html')) {
        const navMenu = new NavigationMenu();
        navMenu.updateUserInfo();
    }
});

// Export pour utilisation dans d'autres modules
window.NavigationMenu = NavigationMenu;
