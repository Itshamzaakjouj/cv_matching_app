# 🌍 Système de Traduction React - TalentScope

## 📋 Vue d'ensemble

Ce système de traduction complet pour React permet de gérer facilement les traductions français/anglais dans votre application d'analyse de CVs. Il utilise le Context API de React et des hooks personnalisés pour une intégration transparente.

## 🚀 Fonctionnalités

- ✅ **Context API React** pour la gestion globale des traductions
- ✅ **Hook useTranslation personnalisé** pour une utilisation facile
- ✅ **Composant LanguageSelector** avec 3 variantes (dropdown, boutons, compact)
- ✅ **Sauvegarde automatique** dans localStorage
- ✅ **Support des paramètres** dans les traductions
- ✅ **Formatage des dates et nombres** selon la locale
- ✅ **Support RTL/LTR** automatique
- ✅ **Thème sombre/clair** intégré
- ✅ **Responsive design** complet
- ✅ **Accessibilité** optimisée

## 📁 Structure des fichiers

```
src/
├── contexts/
│   └── TranslationContext.jsx     # Context API principal
├── hooks/
│   └── useTranslation.js          # Hooks personnalisés
├── components/
│   ├── LanguageSelector.jsx       # Sélecteur de langue
│   ├── LanguageSelector.css       # Styles du sélecteur
│   ├── Navigation.jsx             # Navigation avec traduction
│   └── Navigation.css             # Styles de navigation
├── pages/
│   ├── Dashboard.jsx              # Tableau de bord traduit
│   ├── Dashboard.css              # Styles dashboard
│   ├── CVAnalysis.jsx             # Analyse CV traduite
│   ├── CVAnalysis.css             # Styles analyse
│   ├── ProcessedCVs.jsx           # CVs traités traduits
│   ├── ProcessedCVs.css           # Styles CVs traités
│   ├── Settings.jsx               # Paramètres traduits
│   └── Settings.css               # Styles paramètres
├── utils/
│   └── translations.js            # Fichier de traductions FR/EN
├── App.jsx                        # App principal avec Provider
├── App.css                        # Styles globaux
├── index.js                       # Point d'entrée
└── index.css                      # Styles de base
```

## 🛠️ Installation et Configuration

### 1. Installation des dépendances

```bash
npm install react react-dom
# ou
yarn add react react-dom
```

### 2. Configuration du Provider

Dans votre `App.jsx` principal :

```jsx
import { TranslationProvider } from './contexts/TranslationContext';

function App() {
  return (
    <TranslationProvider>
      {/* Votre application */}
    </TranslationProvider>
  );
}
```

### 3. Utilisation dans les composants

```jsx
import { useTranslation } from './hooks/useTranslation';

function MonComposant() {
  const { t, language, changeLanguage } = useTranslation();
  
  return (
    <div>
      <h1>{t('navigation.home')}</h1>
      <p>{t('info.loading')}</p>
      <button onClick={() => changeLanguage('en')}>
        English
      </button>
    </div>
  );
}
```

## 🎯 Utilisation des Hooks

### Hook principal `useTranslation`

```jsx
const { 
  t,                    // Fonction de traduction
  language,             // Langue actuelle
  changeLanguage,       // Changer de langue
  formatDate,           // Formater les dates
  formatNumber,         // Formater les nombres
  isRTL                 // Direction du texte
} = useTranslation();
```

### Hooks spécialisés

```jsx
import { 
  useT,                 // Fonction de traduction uniquement
  useLanguage,          // Langue actuelle uniquement
  useChangeLanguage,    // Fonction de changement uniquement
  useIsRTL,             // Direction RTL uniquement
  useFormatDate,        // Formatage de dates uniquement
  useFormatNumber       // Formatage de nombres uniquement
} from './hooks/useTranslation';
```

## 🌐 Gestion des Traductions

### Structure des traductions

```javascript
// src/utils/translations.js
export const translations = {
  fr: {
    navigation: {
      home: 'Accueil',
      dashboard: 'Tableau de Bord'
    },
    errors: {
      generic: 'Une erreur est survenue'
    }
  },
  en: {
    navigation: {
      home: 'Home',
      dashboard: 'Dashboard'
    },
    errors: {
      generic: 'An error occurred'
    }
  }
};
```

### Utilisation avec paramètres

```javascript
// Dans translations.js
{
  fr: {
    welcome: 'Bienvenue {{name}}, vous avez {{count}} messages'
  },
  en: {
    welcome: 'Welcome {{name}}, you have {{count}} messages'
  }
}

// Dans le composant
const message = t('welcome', { name: 'John', count: 5 });
// Résultat: "Bienvenue John, vous avez 5 messages"
```

## 🎨 Composant LanguageSelector

### Variantes disponibles

```jsx
// Dropdown (par défaut)
<LanguageSelector variant="dropdown" />

// Boutons
<LanguageSelector variant="buttons" />

// Compact (icônes seulement)
<LanguageSelector variant="compact" />
```

### Props disponibles

```jsx
<LanguageSelector
  variant="dropdown"        // 'dropdown', 'buttons', 'compact'
  showLabels={true}         // Afficher les labels
  className="custom-class"  // Classe CSS personnalisée
  size="medium"            // 'small', 'medium', 'large'
/>
```

## 📱 Pages Traduites

### 1. Dashboard
- Métriques traduites
- Graphiques avec labels traduits
- Formatage des dates et nombres

### 2. Analyse de CV
- Interface d'upload traduite
- Messages d'erreur traduits
- Résultats d'analyse traduits

### 3. CVs Traités
- Tableau d'historique traduit
- Filtres et recherche traduits
- Actions traduites

### 4. Paramètres
- Toutes les options traduites
- Sélecteur de langue intégré
- Thèmes traduits

## 🎯 Exemples d'Utilisation

### Traduction simple

```jsx
function Header() {
  const { t } = useTranslation();
  
  return (
    <header>
      <h1>{t('navigation.home')}</h1>
      <nav>
        <a href="/dashboard">{t('navigation.dashboard')}</a>
        <a href="/analysis">{t('navigation.newAnalysis')}</a>
      </nav>
    </header>
  );
}
```

### Traduction avec paramètres

```jsx
function UserProfile({ user }) {
  const { t } = useTranslation();
  
  return (
    <div>
      <h2>{t('profile.welcome', { name: user.name })}</h2>
      <p>{t('profile.lastLogin', { date: user.lastLogin })}</p>
    </div>
  );
}
```

### Formatage des dates

```jsx
function AnalysisResults({ results }) {
  const { t, formatDate } = useTranslation();
  
  return (
    <div>
      <h3>{t('results.title')}</h3>
      <p>{t('results.generated', { 
        date: formatDate(results.date, { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })
      })}</p>
    </div>
  );
}
```

### Formatage des nombres

```jsx
function Metrics({ data }) {
  const { t, formatNumber } = useTranslation();
  
  return (
    <div>
      <div>{t('metrics.analyses')}: {formatNumber(data.analyses)}</div>
      <div>{t('metrics.score')}: {formatNumber(data.score, { 
        style: 'percent', 
        minimumFractionDigits: 1 
      })}</div>
    </div>
  );
}
```

## 🔧 Personnalisation

### Ajouter une nouvelle langue

1. **Ajouter dans translations.js** :

```javascript
export const translations = {
  fr: { /* traductions françaises */ },
  en: { /* traductions anglaises */ },
  es: { /* nouvelles traductions espagnoles */ }
};
```

2. **Mettre à jour le LanguageSelector** :

```jsx
const languages = [
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Español', flag: '🇪🇸' }  // Nouvelle langue
];
```

### Ajouter de nouvelles traductions

```javascript
// Dans translations.js
{
  fr: {
    // Traductions existantes...
    newSection: {
      title: 'Nouvelle Section',
      description: 'Description de la nouvelle section'
    }
  },
  en: {
    // Traductions existantes...
    newSection: {
      title: 'New Section',
      description: 'Description of the new section'
    }
  }
}
```

## 🎨 Thèmes et Styles

### Support du thème sombre

```css
/* Les styles s'adaptent automatiquement avec [data-theme="dark"] */
[data-theme="dark"] .my-component {
  background: #1f2937;
  color: #f9fafb;
}
```

### Variables CSS personnalisées

```css
:root {
  --language-primary: #4f46e5;
  --language-secondary: #6b7280;
  --language-border: #e5e7eb;
  --language-background: #ffffff;
}

[data-theme="dark"] {
  --language-primary: #6366f1;
  --language-secondary: #9ca3af;
  --language-border: #374151;
  --language-background: #1f2937;
}
```

## 📱 Responsive Design

Le système est entièrement responsive avec des breakpoints :

- **Desktop** : > 1024px
- **Tablet** : 768px - 1024px
- **Mobile** : < 768px
- **Small Mobile** : < 480px

## ♿ Accessibilité

- ✅ **Focus visible** sur tous les éléments interactifs
- ✅ **Support clavier** complet
- ✅ **ARIA labels** appropriés
- ✅ **Contraste élevé** en mode high-contrast
- ✅ **Mouvement réduit** en mode reduced-motion
- ✅ **Screen readers** compatibles

## 🧪 Tests

### Test du changement de langue

```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { TranslationProvider } from './contexts/TranslationContext';
import LanguageSelector from './components/LanguageSelector';

test('change language', () => {
  render(
    <TranslationProvider>
      <LanguageSelector />
    </TranslationProvider>
  );
  
  const englishButton = screen.getByText('English');
  fireEvent.click(englishButton);
  
  expect(localStorage.getItem('app-language')).toBe('en');
});
```

### Test des traductions

```jsx
import { useTranslation } from './hooks/useTranslation';

function TestComponent() {
  const { t } = useTranslation();
  return <div data-testid="translation">{t('navigation.home')}</div>;
}

test('displays correct translation', () => {
  render(
    <TranslationProvider>
      <TestComponent />
    </TranslationProvider>
  );
  
  expect(screen.getByTestId('translation')).toHaveTextContent('Accueil');
});
```

## 🚀 Déploiement

### Variables d'environnement

```bash
# .env
REACT_APP_DEFAULT_LANGUAGE=fr
REACT_APP_SUPPORTED_LANGUAGES=fr,en
```

### Build de production

```bash
npm run build
# ou
yarn build
```

## 📚 Ressources Utiles

- [React Context API](https://reactjs.org/docs/context.html)
- [React Hooks](https://reactjs.org/docs/hooks-intro.html)
- [Intl API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**🎉 Votre système de traduction React est maintenant prêt !**

Pour toute question ou support, n'hésitez pas à ouvrir une issue sur GitHub.





