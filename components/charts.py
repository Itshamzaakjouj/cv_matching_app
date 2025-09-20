"""
Composants de graphiques interactifs pour TalentScope
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import streamlit as st

class ChartFactory:
    """Factory pour créer différents types de graphiques"""
    
    @staticmethod
    def create_gauge_chart(
        value: float, 
        title: str, 
        color_scheme: str = "Blues",
        reference: float = 70,
        max_value: float = 100
    ) -> go.Figure:
        """Créer un graphique gauge pour afficher les pourcentages"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 16}},
            delta={'reference': reference, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#ffcccc'},
                    {'range': [50, 70], 'color': '#ffffcc'},
                    {'range': [70, 100], 'color': '#ccffcc'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300, 
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(family="Segoe UI, sans-serif")
        )
        return fig

    @staticmethod
    def create_trend_chart(
        data: Dict, 
        title: str,
        x_col: str = 'date',
        y_cols: List[str] = None
    ) -> go.Figure:
        """Créer un graphique de tendance"""
        if y_cols is None:
            y_cols = ['analyses', 'score']
            
        fig = go.Figure()
        
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
        
        for i, col in enumerate(y_cols):
            if col in data:
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[col],
                    mode='lines+markers',
                    name=col.replace('_', ' ').title(),
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18)),
            xaxis_title="Date",
            yaxis_title="Valeur",
            height=400,
            hovermode='x unified',
            legend=dict(x=0, y=1),
            font=dict(family="Segoe UI, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

    @staticmethod
    def create_skills_radar(
        skills_data: Dict[str, float],
        title: str = "Compétences Demandées"
    ) -> go.Figure:
        """Créer un graphique radar pour les compétences"""
        categories = list(skills_data.keys())
        values = list(skills_data.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Compétences',
            line_color='rgb(100, 149, 237)',
            fillcolor='rgba(100, 149, 237, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title=title,
            height=400,
            font=dict(family="Segoe UI, sans-serif")
        )
        
        return fig

    @staticmethod
    def create_heatmap(
        data: pd.DataFrame,
        title: str = "Heatmap de Compatibilité",
        x_col: str = 'cv_name',
        y_col: str = 'skill',
        value_col: str = 'score'
    ) -> go.Figure:
        """Créer une heatmap de compatibilité"""
        pivot_data = data.pivot(index=y_col, columns=x_col, values=value_col)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="CVs",
            yaxis_title="Compétences",
            height=400,
            font=dict(family="Segoe UI, sans-serif")
        )
        
        return fig

    @staticmethod
    def create_distribution_chart(
        scores: List[float],
        title: str = "Distribution des Scores"
    ) -> go.Figure:
        """Créer un graphique de distribution des scores"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=scores,
            nbinsx=20,
            marker_color='rgba(100, 149, 237, 0.7)',
            marker_line=dict(color='rgba(100, 149, 237, 1)', width=1)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Score (%)",
            yaxis_title="Fréquence",
            height=400,
            font=dict(family="Segoe UI, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

    @staticmethod
    def create_timeline_chart(
        data: List[Dict],
        title: str = "Timeline des Analyses"
    ) -> go.Figure:
        """Créer un graphique timeline"""
        df = pd.DataFrame(data)
        
        fig = go.Figure()
        
        for i, row in df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row['date'], row['date']],
                y=[0, 1],
                mode='lines+markers',
                name=row.get('cv_name', f'CV {i+1}'),
                line=dict(width=3),
                marker=dict(size=10),
                hovertemplate=f"<b>{row.get('cv_name', f'CV {i+1}')}</b><br>" +
                             f"Date: {row['date']}<br>" +
                             f"Score: {row.get('score', 'N/A')}%<extra></extra>"
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="",
            height=300,
            showlegend=False,
            font=dict(family="Segoe UI, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

    @staticmethod
    def create_comparison_chart(
        data: Dict[str, List[float]],
        title: str = "Comparaison des CVs"
    ) -> go.Figure:
        """Créer un graphique de comparaison"""
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3
        
        for i, (cv_name, scores) in enumerate(data.items()):
            fig.add_trace(go.Bar(
                name=cv_name,
                x=list(range(len(scores))),
                y=scores,
                marker_color=colors[i % len(colors)],
                hovertemplate=f"<b>{cv_name}</b><br>" +
                             "Critère: %{x}<br>" +
                             "Score: %{y}%<extra></extra>"
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Critères",
            yaxis_title="Score (%)",
            height=400,
            barmode='group',
            font=dict(family="Segoe UI, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

@st.cache_data
def get_sample_data() -> Dict:
    """Génère des données d'exemple pour les démonstrations"""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=7, freq='D')
    
    return {
        'trend_data': {
            'date': dates,
            'analyses': [12, 15, 8, 20, 18, 16, 8],
            'score': [75.2, 76.1, 72.8, 81.5, 79.3, 78.1, 80.2]
        },
        'skills_data': {
            'Python': 85,
            'Machine Learning': 78,
            'SQL': 72,
            'Git': 65,
            'Docker': 58,
            'JavaScript': 55,
            'React': 52,
            'AWS': 48
        },
        'cv_scores': [91.3, 76.1, 85.2, 72.8, 88.5, 69.2, 94.1, 81.7],
        'timeline_data': [
            {'date': '2024-09-15', 'cv_name': 'CV_Hamza.pdf', 'score': 91.3},
            {'date': '2024-09-16', 'cv_name': 'CV_Sophia.pdf', 'score': 76.1},
            {'date': '2024-09-17', 'cv_name': 'CV_Adam.pdf', 'score': 85.2},
            {'date': '2024-09-18', 'cv_name': 'CV_Ali.pdf', 'score': 72.8}
        ]
    }
