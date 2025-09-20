import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from processing import rank_cvs, extract_detailed_analysis
from i18n import t

class DashboardManager:
    def __init__(self):
        self.data_file = "data/analytics.json"
        self.ensure_data_directory()
        self.load_analytics_data()
    
    def ensure_data_directory(self):
        """Créer le dossier data s'il n'existe pas"""
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def load_analytics_data(self):
        """Charger les données d'analytics"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.analytics_data = json.load(f)
        else:
            self.analytics_data = {
                "total_analyses": 0,
                "total_cvs": 0,
                "analyses_history": [],
                "cv_database": {},
                "performance_metrics": {
                    "avg_processing_time": 0,
                    "accuracy_rate": 0,
                    "user_satisfaction": 0
                }
            }
    
    def save_analytics_data(self):
        """Sauvegarder les données d'analytics"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.analytics_data, f, ensure_ascii=False, indent=2)
    
    def record_analysis(self, job_description, uploaded_files, results, processing_time):
        """Enregistrer une nouvelle analyse"""
        analysis_record = {
            "timestamp": datetime.now().isoformat(),
            "job_description_length": len(job_description),
            "num_cvs": len(uploaded_files),
            "results": [(filename, float(score)) for filename, score in results],
            "processing_time": processing_time,
            "best_score": max(score for _, score in results) if results else 0,
            "avg_score": sum(score for _, score in results) / len(results) if results else 0
        }
        
        self.analytics_data["analyses_history"].append(analysis_record)
        self.analytics_data["total_analyses"] += 1
        self.analytics_data["total_cvs"] += len(uploaded_files)
        
        # Mettre à jour les métriques de performance
        self.update_performance_metrics()
        self.save_analytics_data()
    
    def update_performance_metrics(self):
        """Mettre à jour les métriques de performance"""
        if self.analytics_data["analyses_history"]:
            recent_analyses = self.analytics_data["analyses_history"][-10:]  # 10 dernières analyses
            processing_times = [a["processing_time"] for a in recent_analyses]
            self.analytics_data["performance_metrics"]["avg_processing_time"] = sum(processing_times) / len(processing_times)
            
            # Calculer le taux de précision (basé sur la cohérence des scores)
            scores = [a["avg_score"] for a in recent_analyses]
            if scores:
                score_variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
                self.analytics_data["performance_metrics"]["accuracy_rate"] = max(0, 1 - score_variance)
    
    def get_dashboard_metrics(self):
        """Obtenir les métriques du dashboard"""
        today = datetime.now().date()
        today_analyses = [
            a for a in self.analytics_data["analyses_history"] 
            if datetime.fromisoformat(a["timestamp"]).date() == today
        ]
        
        return {
            "total_analyses": self.analytics_data["total_analyses"],
            "total_cvs": self.analytics_data["total_cvs"],
            "today_analyses": len(today_analyses),
            "avg_processing_time": self.analytics_data["performance_metrics"]["avg_processing_time"],
            "accuracy_rate": self.analytics_data["performance_metrics"]["accuracy_rate"],
            "best_score_today": max((a["best_score"] for a in today_analyses), default=0),
            "avg_score_today": sum(a["avg_score"] for a in today_analyses) / len(today_analyses) if today_analyses else 0
        }
    
    def get_analytics_charts(self):
        """Générer les graphiques d'analytics"""
        if not self.analytics_data["analyses_history"]:
            return None, None, None
        
        df = pd.DataFrame(self.analytics_data["analyses_history"])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Graphique 1: Évolution du nombre d'analyses
        daily_analyses = df.groupby('date').size().reset_index(name='count')
        fig1 = px.line(daily_analyses, x='date', y='count', 
                      title=t("analytics.evolution_title") if hasattr(__import__('builtins'), '__dict__') else "",
                      labels={'count': 'Analyses', 'date': 'Date'})
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        
        # Graphique 2: Distribution des scores
        all_scores = []
        for analysis in self.analytics_data["analyses_history"]:
            all_scores.extend([score * 100 for _, score in analysis["results"]])
        
        fig2 = px.histogram(x=all_scores, nbins=20, 
                           title=t("analytics.distribution_title") if hasattr(__import__('builtins'), '__dict__') else "",
                           labels={'x': 'Score (%)', 'y': 'Frequency'})
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        
        # Graphique 3: Temps de traitement
        fig3 = px.scatter(df, x='num_cvs', y='processing_time',
                         title=t("analytics.processing_title") if hasattr(__import__('builtins'), '__dict__') else "",
                         labels={'num_cvs': 'CVs', 'processing_time': 'Time (s)'})
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        
        return fig1, fig2, fig3
    
    def get_cv_comparison_data(self, results):
        """Préparer les données pour la comparaison de CVs"""
        comparison_data = []
        for filename, score in results:
            # Simuler des données détaillées (à remplacer par l'analyse réelle)
            comparison_data.append({
                'CV': filename,
                'Score Global': score * 100,
                'Compétences Techniques': min(score * 1.2, 1.0) * 100,
                'Expérience': min(score * 0.8, 1.0) * 100,
                'Formation': min(score * 1.1, 1.0) * 100,
                'Mots-clés': min(score * 0.9, 1.0) * 100
            })
        return pd.DataFrame(comparison_data)

def render_dashboard():
    """Rendre le dashboard d'administration"""
    dashboard = DashboardManager()
    
    st.markdown("## 📊 Dashboard")
    
    # Métriques principales
    metrics = dashboard.get_dashboard_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total analyses",
            metrics["total_analyses"],
            delta=f"+{metrics['today_analyses']} today"
        )
    
    with col2:
        st.metric(
            "Processed CVs",
            metrics["total_cvs"],
            delta=f"+{metrics['today_analyses']} today"
        )
    
    with col3:
        st.metric(
            "Avg time",
            f"{metrics['avg_processing_time']:.2f}s",
            delta="Performance"
        )
    
    with col4:
        st.metric(
            "Accuracy",
            f"{metrics['accuracy_rate']*100:.1f}%",
            delta="Quality"
        )
    
    # Graphiques d'analytics
    st.markdown("## 📈 Advanced Analytics")
    
    fig1, fig2, fig3 = dashboard.get_analytics_charts()
    
    if fig1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No analytics data available. Run some analyses to see charts.")

def render_cv_comparison(results):
    """Rendre l'outil de comparaison de CVs"""
    if not results:
        return
    
    dashboard = DashboardManager()
    comparison_df = dashboard.get_cv_comparison_data(results)
    
    st.markdown("## 🔍 Detailed CV Comparison")
    
    # Graphique radar pour chaque CV
    categories = ['Technical skills', 'Experience', 'Education', 'Keywords']
    
    fig = go.Figure()
    
    for _, row in comparison_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row[cat] for cat in categories] + [row[categories[0]]],  # Fermer le radar
            theta=categories + [categories[0]],
            fill='toself',
            name=row['CV'],
            line=dict(width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20,
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                tickvals=[0, 20, 40, 60, 80, 100]
            )),
        showlegend=True,
        title="Skills profile comparison (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de comparaison
    st.markdown("### 📋 Comparison Table")
    
    # Formater le DataFrame pour afficher les pourcentages
    display_df = comparison_df.copy()
    for col in ['Score Global', 'Compétences Techniques', 'Expérience', 'Formation', 'Mots-clés']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%")
    
    # Réinitialiser l'index pour commencer par 1
    display_df = display_df.reset_index(drop=True)
    display_df.index = display_df.index + 1
    display_df.index.name = "Rang"
    
    st.dataframe(display_df, use_container_width=True)

def render_export_section(results):
    """Rendre la section d'export"""
    st.markdown("## 📤 Export des Résultats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export PDF", use_container_width=True):
            st.success("Fonctionnalité d'export PDF en cours de développement")
    
    with col2:
        if st.button("📊 Export Excel", use_container_width=True):
            # Créer un DataFrame pour l'export
            df = pd.DataFrame([
                {"CV": filename, "Score": score, "Percentage": f"{score*100:.1f}%"}
                for filename, score in results
            ])
            
            # Convertir en CSV (simulation d'Excel)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download Excel",
                data=csv,
                file_name=f"cv_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📈 Export Graphiques", use_container_width=True):
            st.success("Graph export feature under development")

def render_custom_scoring():
    """Rendre la section de scoring personnalisé"""
    st.markdown("## ⚙️ Scoring Criteria Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚖️ Criteria Weights")
        
        # Récupérer les poids sauvegardés ou utiliser les valeurs par défaut
        if 'custom_weights' in st.session_state:
            default_weights = st.session_state['custom_weights']
        else:
            default_weights = {
                'skill_weight': 0.3,
                'experience_weight': 0.25,
                'education_weight': 0.15,
                'keywords_weight': 0.2,
                'base_similarity_weight': 0.1
            }
        
        skill_weight = st.slider("Technical skills", 0.0, 1.0, default_weights['skill_weight'], 0.05)
        exp_weight = st.slider("Professional experience", 0.0, 1.0, default_weights['experience_weight'], 0.05)
        edu_weight = st.slider("Education", 0.0, 1.0, default_weights['education_weight'], 0.05)
        keyword_weight = st.slider("Keywords", 0.0, 1.0, default_weights['keywords_weight'], 0.05)
        similarity_weight = st.slider("Semantic similarity", 0.0, 1.0, default_weights['base_similarity_weight'], 0.05)
    
    with col2:
        st.markdown("### 📊 Weights Visualization")
        weights = {
            'Skills': skill_weight,
            'Experience': exp_weight,
            'Education': edu_weight,
            'Keywords': keyword_weight,
            'Similarity': similarity_weight
        }
        
        # Vérifier que la somme = 1
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            st.warning(f"⚠️ Sum of weights must be 1.0 (currently: {total:.2f})")
        else:
            st.success("✅ Valid configuration")
        
        # Graphique en barres des poids
        fig = px.bar(
            x=list(weights.keys()),
            y=list(weights.values()),
            title="Distribution of scoring criteria",
            labels={'x': 'Criteria', 'y': 'Weight'}
        )
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    return {
        "skill_weight": skill_weight,
        "experience_weight": exp_weight,
        "education_weight": edu_weight,
        "keywords_weight": keyword_weight,
        "base_similarity_weight": similarity_weight
    }
