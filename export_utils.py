import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO
import json

def generate_pdf_report(results, job_description, analysis_details=None):
    """Générer un rapport PDF (simulation avec HTML)"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport d'Analyse CV - {datetime.now().strftime('%d/%m/%Y')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
            .result-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
            .score {{ font-size: 24px; font-weight: bold; color: #667eea; }}
            .excellent {{ border-left: 4px solid #4CAF50; }}
            .good {{ border-left: 4px solid #FFC107; }}
            .partial {{ border-left: 4px solid #FF9800; }}
            .weak {{ border-left: 4px solid #F44336; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 Rapport d'Analyse CV</h1>
            <p>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
        </div>
        
        <h2>📝 Description du Poste</h2>
        <p>{job_description[:500]}{'...' if len(job_description) > 500 else ''}</p>
        
        <h2>📊 Résultats de l'Analyse</h2>
    """
    
    for rank, (filename, score, _) in enumerate(results, 1):
        if score >= 0.7:
            card_class = "excellent"
            status = "Excellent match"
        elif score >= 0.5:
            card_class = "good"
            status = "Bon match"
        elif score >= 0.3:
            card_class = "partial"
            status = "Match partiel"
        else:
            card_class = "weak"
            status = "Match faible"
        
        html_content += f"""
        <div class="result-card {card_class}">
            <h3>#{rank} - {filename}</h3>
            <div class="score">{score*100:.1f}%</div>
            <p><strong>{status}</strong></p>
        </div>
        """
    
    # Calculer les statistiques avec vérification
    if len(results) > 0:
        avg_score = (sum(score for _, score in results) / len(results)) * 100
        max_score = max(score for _, score in results) * 100
    else:
        avg_score = 0
        max_score = 0
    
    html_content += f"""
        <h2>📈 Statistiques</h2>
        <ul>
            <li>Nombre de CVs analysés: {len(results)}</li>
            <li>Score moyen: {avg_score:.1f}%</li>
            <li>Meilleur score: {max_score:.1f}%</li>
        </ul>
    </body>
    </html>
    """
    
    return html_content

def generate_excel_report(results, job_description, analysis_details=None):
    """Générer un rapport Excel (CSV)"""
    # Données principales
    main_data = []
    for rank, (filename, score, _) in enumerate(results, 1):
        main_data.append({
            "Rang": rank,
            "Nom du CV": filename,
            "Score (%)": f"{score*100:.1f}%",
            "Score Décimal": f"{score:.3f}",
            "Statut": get_score_status(score)
        })
    
    # Statistiques avec vérification
    if len(results) > 0:
        avg_score = sum(score for _, score in results) / len(results)
        best_score = max(score for _, score in results)
        worst_score = min(score for _, score in results)
    else:
        avg_score = 0
        best_score = 0
        worst_score = 0
    
    stats_data = {
        "Métrique": ["Nombre de CVs", "Score moyen (%)", "Meilleur score (%)", "Score minimum (%)"],
        "Valeur": [
            str(len(results)),
            f"{avg_score*100:.1f}%",
            f"{best_score*100:.1f}%",
            f"{worst_score*100:.1f}%"
        ]
    }
    
    return main_data, stats_data

def generate_charts_export(results):
    """Générer des graphiques pour l'export"""
    df = pd.DataFrame([
        {"CV": filename, "Score": score*100, "Pourcentage": score*100}
        for filename, score, _ in results
    ])
    
    # Graphique en barres
    fig_bar = px.bar(
        df, 
        x="CV", 
        y="Score",
        title="Scores de pertinence par CV (%)",
        color="Score",
        color_continuous_scale="RdYlGn",
        labels={"Score": "Score (%)"}
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    # Graphique en camembert
    fig_pie = px.pie(
        df,
        values="Score",
        names="CV",
        title="Répartition des scores (%)"
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig_bar, fig_pie

def get_score_status(score):
    """Obtenir le statut basé sur le score"""
    if score >= 0.7:
        return "Excellent"
    elif score >= 0.5:
        return "Bon"
    elif score >= 0.3:
        return "Partiel"
    else:
        return "Faible"

def create_download_link(data, filename, mime_type):
    """Créer un lien de téléchargement"""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Télécharger {filename}</a>'
    return href

def export_analysis_data(results, job_description, analysis_details=None):
    """Exporter toutes les données d'analyse"""
    export_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "job_description": job_description,
            "num_cvs": len(results),
            "version": "1.0"
        },
        "results": [
            {
                "rank": rank,
                "filename": filename,
                "score_decimal": float(score),
                "score_percentage": float(score * 100),
                "status": get_score_status(score)
            }
            for rank, (filename, score, _) in enumerate(results, 1)
        ],
        "statistics": {
        "average_score_percentage": float(sum(score for _, score, _ in results) / len(results) * 100) if len(results) > 0 else 0.0,
        "best_score_percentage": float(max(score for _, score, _ in results) * 100) if len(results) > 0 else 0.0,
        "worst_score_percentage": float(min(score for _, score, _ in results) * 100) if len(results) > 0 else 0.0,
        "score_range_percentage": float((max(score for _, score, _ in results) - min(score for _, score, _ in results)) * 100) if len(results) > 0 else 0.0
        }
    }
    
    if analysis_details:
        export_data["analysis_details"] = analysis_details
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def render_export_buttons(results, job_description, analysis_details=None):
    """Rendre les boutons d'export"""
    st.markdown("## 📤 Export des Résultats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Export PDF (HTML)
        html_report = generate_pdf_report(results, job_description, analysis_details)
        st.download_button(
            label="📄 Export PDF",
            data=html_report,
            file_name=f"cv_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col2:
        # Export Excel (CSV)
        main_data, stats_data = generate_excel_report(results, job_description, analysis_details)
        csv_data = pd.DataFrame(main_data).to_csv(index=False)
        st.download_button(
            label="📊 Export Excel",
            data=csv_data,
            file_name=f"cv_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        # Export JSON
        json_data = export_analysis_data(results, job_description, analysis_details)
        st.download_button(
            label="📋 Export JSON",
            data=json_data,
            file_name=f"cv_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        # Export des graphiques
        if st.button("📈 Aperçu Graphiques", use_container_width=True):
            fig_bar, fig_pie = generate_charts_export(results)
            
            st.plotly_chart(fig_bar, use_container_width=True)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Section de statistiques détaillées
    st.markdown("### 📊 Statistiques Détaillées")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("CVs analysés", len(results))
    
    with col2:
        avg_score = sum(score for _, score, _ in results) / len(results) if len(results) > 0 else 0
        st.metric("Score moyen", f"{avg_score*100:.1f}%")
    
    with col3:
        best_score = max(score for _, score, _ in results) if len(results) > 0 else 0
        st.metric("Meilleur score", f"{best_score*100:.1f}%")
    
    # Tableau détaillé
    st.markdown("### 📋 Détail des Résultats")
    df_results = pd.DataFrame([
        {
            "CV": filename,
            "Score (%)": f"{score*100:.1f}%",
            "Score Décimal": f"{score:.3f}",
            "Statut": get_score_status(score)
        }
        for rank, (filename, score, _) in enumerate(results, 1)
    ])
    
    # Ajouter l'index pour commencer par 1
    df_results.index = range(1, len(df_results) + 1)
    df_results.index.name = "Rang"
    
    st.dataframe(df_results, use_container_width=True)
