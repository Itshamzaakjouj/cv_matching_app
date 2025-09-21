// ============================================================================
// SERVICE DE TRADUCTION AVANCÉ - TalentScope
// ============================================================================

class TranslationService {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 3600000; // 1 heure
        this.maxCacheSize = 1000;
        this.rateLimitDelay = 100; // 100ms entre les requêtes
        this.lastRequestTime = 0;
        
        // Configuration des APIs
        this.apis = {
            google: {
                url: 'https://translation.googleapis.com/language/translate/v2',
                key: '', // À configurer
                enabled: false
            },
            libre: {
                url: 'https://libretranslate.de/translate',
                enabled: true
            },
            mymemory: {
                url: 'https://api.mymemory.translated.net/get',
                enabled: true
            }
        };
        
        // Langues supportées
        this.languages = {
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

    // Configuration de l'API Google Translate
    setGoogleApiKey(apiKey) {
        this.apis.google.key = apiKey;
        this.apis.google.enabled = !!apiKey;
    }

    // Traduction avec fallback multi-API
    async translateText(text, targetLang, sourceLang = 'auto') {
        if (!text || !text.trim()) {
            throw new Error('Le texte à traduire ne peut pas être vide');
        }

        if (text.length > 5000) {
            throw new Error('Le texte est trop long (maximum 5000 caractères)');
        }

        const cacheKey = `${text}_${sourceLang}_${targetLang}`;
        
        // Vérifier le cache
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.result;
            } else {
                this.cache.delete(cacheKey);
            }
        }

        // Rate limiting
        await this.rateLimit();

        let result;
        let error;

        // Essayer Google Translate en premier
        if (this.apis.google.enabled) {
            try {
                result = await this.translateWithGoogle(text, targetLang, sourceLang);
            } catch (err) {
                error = err;
                console.warn('Google Translate failed:', err.message);
            }
        }

        // Fallback vers LibreTranslate
        if (!result && this.apis.libre.enabled) {
            try {
                result = await this.translateWithLibre(text, targetLang, sourceLang);
            } catch (err) {
                error = err;
                console.warn('LibreTranslate failed:', err.message);
            }
        }

        // Fallback vers MyMemory
        if (!result && this.apis.mymemory.enabled) {
            try {
                result = await this.translateWithMyMemory(text, targetLang, sourceLang);
            } catch (err) {
                error = err;
                console.warn('MyMemory failed:', err.message);
            }
        }

        if (!result) {
            throw new Error(`Échec de la traduction: ${error?.message || 'Aucune API disponible'}`);
        }

        // Mettre en cache
        this.cacheResult(cacheKey, result);

        return result;
    }

    // Traduction avec Google Translate
    async translateWithGoogle(text, targetLang, sourceLang) {
        const response = await fetch(`${this.apis.google.url}?key=${this.apis.google.key}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                q: text,
                target: targetLang,
                source: sourceLang === 'auto' ? undefined : sourceLang,
                format: 'text'
            })
        });

        if (!response.ok) {
            throw new Error(`Google Translate API error: ${response.status}`);
        }

        const data = await response.json();
        return {
            text: data.data.translations[0].translatedText,
            sourceLang: data.data.translations[0].detectedSourceLanguage || sourceLang,
            confidence: 0.95
        };
    }

    // Traduction avec LibreTranslate
    async translateWithLibre(text, targetLang, sourceLang) {
        const response = await fetch(this.apis.libre.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                q: text,
                source: sourceLang === 'auto' ? 'auto' : sourceLang,
                target: targetLang,
                format: 'text'
            })
        });

        if (!response.ok) {
            throw new Error(`LibreTranslate API error: ${response.status}`);
        }

        const data = await response.json();
        return {
            text: data.translatedText,
            sourceLang: data.detectedLanguage || sourceLang,
            confidence: 0.8
        };
    }

    // Traduction avec MyMemory
    async translateWithMyMemory(text, targetLang, sourceLang) {
        const sourceCode = sourceLang === 'auto' ? 'auto' : sourceLang;
        const url = `${this.apis.mymemory.url}?q=${encodeURIComponent(text)}&langpair=${sourceCode}|${targetLang}`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`MyMemory API error: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.responseStatus !== 200) {
            throw new Error(`MyMemory translation error: ${data.responseDetails}`);
        }

        return {
            text: data.responseData.translatedText,
            sourceLang: sourceLang,
            confidence: 0.7
        };
    }

    // Détection de langue
    async detectLanguage(text) {
        if (!text || !text.trim()) {
            throw new Error('Le texte ne peut pas être vide pour la détection');
        }

        const cacheKey = `detect_${text}`;
        
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.result;
            }
        }

        await this.rateLimit();

        // Essayer Google Translate d'abord
        if (this.apis.google.enabled) {
            try {
                const response = await fetch(`https://translation.googleapis.com/language/translate/v2/detect?key=${this.apis.google.key}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ q: text })
                });

                if (response.ok) {
                    const data = await response.json();
                    const result = {
                        language: data.data.detections[0][0].language,
                        confidence: data.data.detections[0][0].confidence
                    };
                    this.cacheResult(cacheKey, result);
                    return result;
                }
            } catch (err) {
                console.warn('Google detection failed:', err.message);
            }
        }

        // Fallback simple basé sur les patterns
        const detected = this.simpleLanguageDetection(text);
        this.cacheResult(cacheKey, detected);
        return detected;
    }

    // Détection simple basée sur les patterns
    simpleLanguageDetection(text) {
        const patterns = {
            'fr': /[àâäéèêëïîôöùûüÿç]/i,
            'de': /[äöüß]/i,
            'es': /[ñáéíóúü]/i,
            'it': /[àèéìíîòóù]/i,
            'pt': /[ãõáéíóúâêôç]/i,
            'ru': /[а-яё]/i,
            'ar': /[ء-ي]/i,
            'zh': /[\u4e00-\u9fff]/i,
            'ja': /[\u3040-\u309f\u30a0-\u30ff]/i,
            'ko': /[\uac00-\ud7af]/i,
            'hi': /[\u0900-\u097f]/i,
            'th': /[\u0e00-\u0e7f]/i
        };

        for (const [lang, pattern] of Object.entries(patterns)) {
            if (pattern.test(text)) {
                return { language: lang, confidence: 0.6 };
            }
        }

        // Par défaut, considérer comme anglais
        return { language: 'en', confidence: 0.5 };
    }

    // Gestion du cache
    cacheResult(key, result) {
        // Nettoyer le cache si nécessaire
        if (this.cache.size >= this.maxCacheSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }

        this.cache.set(key, {
            result: result,
            timestamp: Date.now()
        });
    }

    // Rate limiting
    async rateLimit() {
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        
        if (timeSinceLastRequest < this.rateLimitDelay) {
            await new Promise(resolve => setTimeout(resolve, this.rateLimitDelay - timeSinceLastRequest));
        }
        
        this.lastRequestTime = Date.now();
    }

    // Obtenir la liste des langues
    getLanguages() {
        return this.languages;
    }

    // Obtenir le nom d'une langue
    getLanguageName(code) {
        return this.languages[code] || code;
    }

    // Vider le cache
    clearCache() {
        this.cache.clear();
    }

    // Obtenir les statistiques du cache
    getCacheStats() {
        return {
            size: this.cache.size,
            maxSize: this.maxCacheSize,
            timeout: this.cacheTimeout
        };
    }
}

// Instance globale
window.TranslationService = TranslationService;
