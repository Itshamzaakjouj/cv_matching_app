/**
 * Script de débogage pour le système de traduction
 * À ajouter temporairement dans modern_dashboard.html pour diagnostiquer les problèmes
 */

function debugTranslationSystem() {
    console.log('🔍 === DÉBOGAGE DU SYSTÈME DE TRADUCTION ===');
    
    // 1. Vérifier si le système de traduction est chargé
    console.log('1. Vérification du système de traduction:');
    console.log('   - window.directTranslation:', !!window.directTranslation);
    console.log('   - window.directTranslationManager:', !!window.directTranslationManager);
    
    // 2. Vérifier la langue actuelle
    const currentLang = localStorage.getItem('language') || 'fr';
    console.log('2. Langue actuelle:', currentLang);
    
    // 3. Vérifier les éléments avec data-translate
    const elementsWithTranslate = document.querySelectorAll('[data-translate]');
    console.log('3. Éléments avec data-translate:', elementsWithTranslate.length);
    
    // 4. Vérifier le sélecteur de langue
    const languageSelect = document.getElementById('config-language-select');
    console.log('4. Sélecteur de langue:');
    console.log('   - Élément trouvé:', !!languageSelect);
    if (languageSelect) {
        console.log('   - Valeur actuelle:', languageSelect.value);
        console.log('   - Options disponibles:', Array.from(languageSelect.options).map(opt => opt.value));
    }
    
    // 5. Vérifier les traductions disponibles
    if (window.directTranslation) {
        console.log('5. Traductions disponibles:');
        const translations = window.directTranslation.translations || {};
        console.log('   - Langues supportées:', Object.keys(translations));
        console.log('   - Clés françaises:', Object.keys(translations.fr || {}).length);
        console.log('   - Clés anglaises:', Object.keys(translations.en || {}).length);
    }
    
    // 6. Tester une traduction
    console.log('6. Test de traduction:');
    if (window.directTranslation && window.directTranslation.getTranslation) {
        const testKey = 'nav.home';
        const translation = window.directTranslation.getTranslation(testKey);
        console.log(`   - Clé "${testKey}":`, translation);
    }
    
    // 7. Vérifier les fonctions de changement de langue
    console.log('7. Fonctions de changement de langue:');
    console.log('   - handleLanguageChange:', typeof window.handleLanguageChange);
    console.log('   - changeLanguage (directTranslation):', typeof (window.directTranslation && window.directTranslation.changeLanguage));
    console.log('   - changeLanguage (directTranslationManager):', typeof (window.directTranslationManager && window.directTranslationManager.changeLanguage));
    
    console.log('🔍 === FIN DU DÉBOGAGE ===');
}

function testLanguageChange() {
    console.log('🧪 Test du changement de langue...');
    
    const currentLang = localStorage.getItem('language') || 'fr';
    const newLang = currentLang === 'fr' ? 'en' : 'fr';
    
    console.log(`Changement de ${currentLang} vers ${newLang}`);
    
    // Tester avec directTranslationManager
    if (window.directTranslationManager) {
        console.log('Utilisation de directTranslationManager...');
        window.directTranslationManager.changeLanguage(newLang);
    } else if (window.directTranslation) {
        console.log('Utilisation de directTranslation...');
        window.directTranslation.changeLanguage(newLang);
    } else {
        console.log('Fallback: sauvegarde manuelle...');
        localStorage.setItem('language', newLang);
    }
    
    // Vérifier le résultat
    setTimeout(() => {
        const updatedLang = localStorage.getItem('language');
        console.log(`Langue après changement: ${updatedLang}`);
        
        // Compter les éléments traduits
        const elements = document.querySelectorAll('[data-translate]');
        console.log(`Éléments avec data-translate: ${elements.length}`);
        
        // Vérifier quelques traductions
        elements.forEach((el, index) => {
            if (index < 5) { // Afficher seulement les 5 premiers
                const key = el.getAttribute('data-translate');
                const text = el.textContent;
                console.log(`  ${key}: "${text}"`);
            }
        });
    }, 100);
}

function fixLanguageSelector() {
    console.log('🔧 Correction du sélecteur de langue...');
    
    const languageSelect = document.getElementById('config-language-select');
    if (!languageSelect) {
        console.error('❌ Sélecteur de langue non trouvé');
        return;
    }
    
    // Vérifier la valeur actuelle
    const currentLang = localStorage.getItem('language') || 'fr';
    console.log(`Langue actuelle: ${currentLang}`);
    console.log(`Valeur du sélecteur: ${languageSelect.value}`);
    
    // Synchroniser
    if (languageSelect.value !== currentLang) {
        languageSelect.value = currentLang;
        console.log(`✅ Sélecteur synchronisé avec ${currentLang}`);
    }
    
    // Vérifier les options
    const options = Array.from(languageSelect.options);
    console.log('Options disponibles:', options.map(opt => `${opt.value}: ${opt.textContent}`));
    
    // Tester le changement
    console.log('Test du changement de langue...');
    const newLang = currentLang === 'fr' ? 'en' : 'fr';
    
    // Simuler un changement
    languageSelect.value = newLang;
    const event = new Event('change', { bubbles: true });
    languageSelect.dispatchEvent(event);
    
    console.log(`✅ Changement simulé vers ${newLang}`);
}

// Fonctions globales pour le débogage
window.debugTranslationSystem = debugTranslationSystem;
window.testLanguageChange = testLanguageChange;
window.fixLanguageSelector = fixLanguageSelector;

console.log('🔧 Script de débogage chargé. Utilisez:');
console.log('   - debugTranslationSystem() pour diagnostiquer');
console.log('   - testLanguageChange() pour tester le changement');
console.log('   - fixLanguageSelector() pour corriger le sélecteur');




