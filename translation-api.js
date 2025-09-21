// ============================================================================
// API BACKEND POUR LA TRADUCTION - TalentScope
// ============================================================================

const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const NodeCache = require('node-cache');

class TranslationAPI {
    constructor() {
        this.app = express();
        this.cache = new NodeCache({ stdTTL: 3600 }); // Cache de 1 heure
        this.setupMiddleware();
        this.setupRoutes();
    }

    setupMiddleware() {
        // CORS
        this.app.use(cors({
            origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000', 'http://localhost:8080'],
            credentials: true
        }));

        // Rate limiting
        const limiter = rateLimit({
            windowMs: 15 * 60 * 1000, // 15 minutes
            max: 100, // Limite de 100 requêtes par IP par fenêtre
            message: {
                error: 'Trop de requêtes, veuillez réessayer plus tard'
            }
        });
        this.app.use('/api/translate', limiter);

        // Parsing JSON
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true }));

        // Logging
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }

    setupRoutes() {
        // Route de santé
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'OK', 
                timestamp: new Date().toISOString(),
                cache: this.cache.getStats()
            });
        });

        // Traduction
        this.app.post('/api/translate', async (req, res) => {
            try {
                const { text, targetLang, sourceLang = 'auto' } = req.body;

                if (!text || !targetLang) {
                    return res.status(400).json({
                        error: 'Les paramètres text et targetLang sont requis'
                    });
                }

                if (text.length > 5000) {
                    return res.status(400).json({
                        error: 'Le texte ne peut pas dépasser 5000 caractères'
                    });
                }

                // Vérifier le cache
                const cacheKey = `translate_${text}_${sourceLang}_${targetLang}`;
                const cached = this.cache.get(cacheKey);
                if (cached) {
                    return res.json({
                        ...cached,
                        cached: true
                    });
                }

                // Effectuer la traduction
                const result = await this.translateText(text, targetLang, sourceLang);

                // Mettre en cache
                this.cache.set(cacheKey, result);

                res.json(result);

            } catch (error) {
                console.error('Erreur de traduction:', error);
                res.status(500).json({
                    error: 'Erreur interne du serveur',
                    message: error.message
                });
            }
        });

        // Détection de langue
        this.app.post('/api/detect', async (req, res) => {
            try {
                const { text } = req.body;

                if (!text) {
                    return res.status(400).json({
                        error: 'Le paramètre text est requis'
                    });
                }

                // Vérifier le cache
                const cacheKey = `detect_${text}`;
                const cached = this.cache.get(cacheKey);
                if (cached) {
                    return res.json({
                        ...cached,
                        cached: true
                    });
                }

                // Détecter la langue
                const result = await this.detectLanguage(text);

                // Mettre en cache
                this.cache.set(cacheKey, result);

                res.json(result);

            } catch (error) {
                console.error('Erreur de détection:', error);
                res.status(500).json({
                    error: 'Erreur interne du serveur',
                    message: error.message
                });
            }
        });

        // Liste des langues supportées
        this.app.get('/api/languages', (req, res) => {
            res.json({
                languages: this.getSupportedLanguages()
            });
        });

        // Historique des traductions (pour un utilisateur)
        this.app.get('/api/history/:userId', (req, res) => {
            const { userId } = req.params;
            const { limit = 50, offset = 0 } = req.query;

            // En production, récupérer depuis la base de données
            const history = this.getUserHistory(userId, parseInt(limit), parseInt(offset));
            
            res.json({
                history,
                total: history.length,
                limit: parseInt(limit),
                offset: parseInt(offset)
            });
        });

        // Sauvegarder une traduction favorite
        this.app.post('/api/favorites', (req, res) => {
            try {
                const { userId, original, translation, sourceLang, targetLang, name } = req.body;

                if (!userId || !original || !translation) {
                    return res.status(400).json({
                        error: 'Les paramètres userId, original et translation sont requis'
                    });
                }

                const favorite = {
                    id: Date.now().toString(),
                    userId,
                    original,
                    translation,
                    sourceLang,
                    targetLang,
                    name: name || 'Traduction sans nom',
                    createdAt: new Date().toISOString()
                };

                // En production, sauvegarder en base de données
                this.saveFavorite(favorite);

                res.json({
                    success: true,
                    favorite
                });

            } catch (error) {
                console.error('Erreur de sauvegarde:', error);
                res.status(500).json({
                    error: 'Erreur interne du serveur',
                    message: error.message
                });
            }
        });

        // Obtenir les favoris d'un utilisateur
        this.app.get('/api/favorites/:userId', (req, res) => {
            const { userId } = req.params;
            const favorites = this.getUserFavorites(userId);
            
            res.json({
                favorites,
                total: favorites.length
            });
        });

        // Statistiques du cache
        this.app.get('/api/cache/stats', (req, res) => {
            res.json({
                stats: this.cache.getStats(),
                timestamp: new Date().toISOString()
            });
        });

        // Vider le cache
        this.app.delete('/api/cache', (req, res) => {
            this.cache.flushAll();
            res.json({
                success: true,
                message: 'Cache vidé avec succès'
            });
        });

        // Gestion des erreurs 404
        this.app.use('*', (req, res) => {
            res.status(404).json({
                error: 'Endpoint non trouvé',
                path: req.originalUrl
            });
        });

        // Gestionnaire d'erreurs global
        this.app.use((error, req, res, next) => {
            console.error('Erreur non gérée:', error);
            res.status(500).json({
                error: 'Erreur interne du serveur',
                message: process.env.NODE_ENV === 'development' ? error.message : 'Une erreur est survenue'
            });
        });
    }

    // Méthodes de traduction (à implémenter selon les APIs disponibles)
    async translateText(text, targetLang, sourceLang) {
        // Implémentation avec Google Translate, LibreTranslate, etc.
        // Pour l'instant, retourner une traduction factice
        return {
            text: `[Traduit] ${text}`,
            sourceLang: sourceLang === 'auto' ? 'fr' : sourceLang,
            targetLang,
            confidence: 0.8,
            provider: 'mock'
        };
    }

    async detectLanguage(text) {
        // Implémentation de détection de langue
        // Pour l'instant, retourner une détection factice
        return {
            language: 'fr',
            confidence: 0.7,
            provider: 'mock'
        };
    }

    getSupportedLanguages() {
        return {
            'auto': 'Détection automatique',
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文',
            'ar': 'العربية',
            'hi': 'हिन्दी',
            'th': 'ไทย',
            'vi': 'Tiếng Việt',
            'tr': 'Türkçe',
            'pl': 'Polski',
            'nl': 'Nederlands',
            'sv': 'Svenska',
            'da': 'Dansk',
            'no': 'Norsk',
            'fi': 'Suomi',
            'cs': 'Čeština',
            'hu': 'Magyar',
            'ro': 'Română',
            'bg': 'Български',
            'hr': 'Hrvatski',
            'sk': 'Slovenčina',
            'sl': 'Slovenščina',
            'et': 'Eesti',
            'lv': 'Latviešu',
            'lt': 'Lietuvių',
            'mt': 'Malti',
            'ga': 'Gaeilge',
            'cy': 'Cymraeg',
            'eu': 'Euskera',
            'ca': 'Català',
            'gl': 'Galego',
            'is': 'Íslenska',
            'mk': 'Македонски',
            'sq': 'Shqip',
            'sr': 'Српски',
            'bs': 'Bosanski',
            'me': 'Crnogorski',
            'uk': 'Українська',
            'be': 'Беларуская',
            'ka': 'ქართული',
            'hy': 'Հայերեն',
            'az': 'Azərbaycan',
            'kk': 'Қазақ',
            'ky': 'Кыргыз',
            'uz': 'Oʻzbek',
            'tg': 'Тоҷикӣ',
            'mn': 'Монгол',
            'ne': 'नेपाली',
            'si': 'සිංහල',
            'my': 'မြန်မာ',
            'km': 'ខ្មែរ',
            'lo': 'ລາວ',
            'jw': 'Basa Jawa',
            'su': 'Basa Sunda',
            'id': 'Bahasa Indonesia',
            'ms': 'Bahasa Melayu',
            'tl': 'Filipino',
            'haw': 'ʻŌlelo Hawaiʻi',
            'mi': 'Te Reo Māori',
            'sm': 'Gagana Samoa',
            'to': 'Lea fakatonga',
            'fj': 'Na Vosa Vakaviti',
            'ty': 'Reo Tahiti',
            'mg': 'Malagasy',
            'sw': 'Kiswahili',
            'am': 'አማርኛ',
            'ha': 'Hausa',
            'ig': 'Igbo',
            'yo': 'Yorùbá',
            'zu': 'IsiZulu',
            'xh': 'IsiXhosa',
            'af': 'Afrikaans',
            'st': 'Sesotho',
            'tn': 'Setswana',
            'ss': 'SiSwati',
            've': 'Tshivenḓa',
            'ts': 'Xitsonga',
            'nr': 'IsiNdebele',
            'nso': 'Sesotho sa Leboa',
            'he': 'עברית',
            'fa': 'فارسی',
            'ur': 'اردو',
            'bn': 'বাংলা',
            'gu': 'ગુજરાતી',
            'pa': 'ਪੰਜਾਬੀ',
            'ta': 'தமிழ்',
            'te': 'తెలుగు',
            'kn': 'ಕನ್ನಡ',
            'ml': 'മലയാളം',
            'or': 'ଓଡ଼ିଆ',
            'as': 'অসমীয়া',
            'mr': 'मराठी',
            'ne': 'नेपाली'
        };
    }

    // Méthodes pour l'historique et les favoris (à implémenter avec une vraie DB)
    getUserHistory(userId, limit, offset) {
        // En production, récupérer depuis la base de données
        return [];
    }

    saveFavorite(favorite) {
        // En production, sauvegarder en base de données
        console.log('Sauvegarde du favori:', favorite);
    }

    getUserFavorites(userId) {
        // En production, récupérer depuis la base de données
        return [];
    }

    start(port = process.env.PORT || 3001) {
        this.app.listen(port, () => {
            console.log(`🚀 API de traduction démarrée sur le port ${port}`);
            console.log(`📊 Endpoints disponibles:`);
            console.log(`   - POST /api/translate - Traduire un texte`);
            console.log(`   - POST /api/detect - Détecter la langue`);
            console.log(`   - GET /api/languages - Langues supportées`);
            console.log(`   - GET /api/history/:userId - Historique utilisateur`);
            console.log(`   - POST /api/favorites - Sauvegarder favori`);
            console.log(`   - GET /api/favorites/:userId - Favoris utilisateur`);
            console.log(`   - GET /api/cache/stats - Statistiques du cache`);
            console.log(`   - DELETE /api/cache - Vider le cache`);
            console.log(`   - GET /health - Santé de l'API`);
        });
    }
}

// Démarrer l'API si ce fichier est exécuté directement
if (require.main === module) {
    const api = new TranslationAPI();
    api.start();
}

module.exports = TranslationAPI;
