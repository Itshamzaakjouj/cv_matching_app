#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - OPTIMISEUR D'ASSETS
Ministère de l'Économie et des Finances
Version: 2.0 - Optimisation des ressources statiques
"""

import os
import gzip
import shutil
import json
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    Image = None
import base64
import re
from typing import Dict, List, Tuple
import hashlib

class AssetOptimizer:
    """Optimiseur d'assets pour améliorer les performances"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.optimized_dir = self.project_root / "optimized_assets"
        self.optimized_dir.mkdir(exist_ok=True)
        
        # Statistiques d'optimisation
        self.stats = {
            'images_optimized': 0,
            'css_minified': 0,
            'js_minified': 0,
            'html_minified': 0,
            'total_size_before': 0,
            'total_size_after': 0
        }
    
    def optimize_all_assets(self):
        """Optimise tous les assets du projet"""
        print("🚀 OPTIMISATION DES ASSETS TALENTSCOPE")
        print("=" * 50)
        
        # Optimiser les images
        self.optimize_images()
        
        # Minifier les fichiers CSS
        self.minify_css_files()
        
        # Minifier les fichiers JavaScript
        self.minify_js_files()
        
        # Minifier les fichiers HTML
        self.minify_html_files()
        
        # Créer les versions compressées
        self.create_compressed_versions()
        
        # Générer le rapport
        self.generate_optimization_report()
    
    def optimize_images(self):
        """Optimise les images (PNG, JPG, SVG)"""
        print("🖼️  Optimisation des images...")
        
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        for ext in image_extensions:
            for image_path in self.project_root.rglob(f"*{ext}"):
                if 'optimized_assets' in str(image_path):
                    continue
                
                try:
                    self.optimize_single_image(image_path)
                except Exception as e:
                    print(f"⚠️  Erreur lors de l'optimisation de {image_path}: {e}")
    
    def optimize_single_image(self, image_path: Path):
        """Optimise une image unique"""
        if Image is None:
            print(f"   ⚠️  PIL non disponible, copie simple: {image_path.name}")
            # Copie simple si PIL n'est pas disponible
            output_path = self.optimized_dir / image_path.name
            shutil.copy2(image_path, output_path)
            return
        
        original_size = image_path.stat().st_size
        
        try:
            with Image.open(image_path) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                        # Pour JPEG, convertir en RGB
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                
                # Redimensionner si trop grande
                max_size = 1920
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Chemin de sortie optimisé
                output_path = self.optimized_dir / image_path.name
                
                # Sauvegarder avec optimisation
                if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    img.save(output_path, 'JPEG', quality=85, optimize=True)
                elif image_path.suffix.lower() == '.png':
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, optimize=True)
                
                optimized_size = output_path.stat().st_size
                savings = original_size - optimized_size
                
                if savings > 0:
                    print(f"   ✅ {image_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
                    self.stats['images_optimized'] += 1
                    self.stats['total_size_before'] += original_size
                    self.stats['total_size_after'] += optimized_size
                
        except Exception as e:
            print(f"   ❌ Erreur avec {image_path.name}: {e}")
    
    def minify_css_files(self):
        """Minifie les fichiers CSS"""
        print("🎨 Minification des fichiers CSS...")
        
        for css_path in self.project_root.rglob("*.css"):
            if 'optimized_assets' in str(css_path):
                continue
            
            try:
                self.minify_single_css(css_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de la minification de {css_path}: {e}")
    
    def minify_single_css(self, css_path: Path):
        """Minifie un fichier CSS"""
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        original_size = len(css_content.encode('utf-8'))
        
        # Minification CSS
        minified_css = self.minify_css_content(css_content)
        
        # Sauvegarder
        output_path = self.optimized_dir / css_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        optimized_size = len(minified_css.encode('utf-8'))
        savings = original_size - optimized_size
        
        if savings > 0:
            print(f"   ✅ {css_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
            self.stats['css_minified'] += 1
            self.stats['total_size_before'] += original_size
            self.stats['total_size_after'] += optimized_size
    
    def minify_css_content(self, css_content: str) -> str:
        """Minifie le contenu CSS"""
        # Supprimer les commentaires
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples
        css_content = re.sub(r'\s+', ' ', css_content)
        
        # Supprimer les espaces autour des symboles
        css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
        
        # Supprimer les espaces en début et fin
        css_content = css_content.strip()
        
        # Supprimer les points-virgules avant les accolades fermantes
        css_content = re.sub(r';}', '}', css_content)
        
        return css_content
    
    def minify_js_files(self):
        """Minifie les fichiers JavaScript"""
        print("⚡ Minification des fichiers JavaScript...")
        
        # Chercher les scripts dans les fichiers HTML
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.extract_and_minify_js_from_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors du traitement de {html_path}: {e}")
    
    def extract_and_minify_js_from_html(self, html_path: Path):
        """Extrait et minifie le JavaScript des fichiers HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Trouver tous les blocs script
        script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        scripts = script_pattern.findall(html_content)
        
        if scripts:
            minified_html = html_content
            
            for script_content in scripts:
                if script_content.strip() and not script_content.strip().startswith('src='):
                    original_size = len(script_content.encode('utf-8'))
                    minified_script = self.minify_js_content(script_content)
                    optimized_size = len(minified_script.encode('utf-8'))
                    
                    # Remplacer dans le HTML
                    minified_html = minified_html.replace(script_content, minified_script, 1)
                    
                    savings = original_size - optimized_size
                    if savings > 0:
                        self.stats['js_minified'] += 1
                        self.stats['total_size_before'] += original_size
                        self.stats['total_size_after'] += optimized_size
            
            # Sauvegarder le HTML avec JS minifié
            output_path = self.optimized_dir / html_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(minified_html)
    
    def minify_js_content(self, js_content: str) -> str:
        """Minifie le contenu JavaScript (basique)"""
        # Supprimer les commentaires sur une ligne
        js_content = re.sub(r'//.*$', '', js_content, flags=re.MULTILINE)
        
        # Supprimer les commentaires multilignes
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples (attention aux strings)
        lines = js_content.split('\n')
        minified_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Supprimer les espaces autour des opérateurs (basique)
                line = re.sub(r'\s*([=+\-*/{}();,])\s*', r'\1', line)
                minified_lines.append(line)
        
        return ''.join(minified_lines)
    
    def minify_html_files(self):
        """Minifie les fichiers HTML"""
        print("📄 Minification des fichiers HTML...")
        
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.minify_single_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de la minification de {html_path}: {e}")
    
    def minify_single_html(self, html_path: Path):
        """Minifie un fichier HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        original_size = len(html_content.encode('utf-8'))
        
        # Minification HTML
        minified_html = self.minify_html_content(html_content)
        
        # Sauvegarder
        output_path = self.optimized_dir / html_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_html)
        
        optimized_size = len(minified_html.encode('utf-8'))
        savings = original_size - optimized_size
        
        if savings > 0:
            print(f"   ✅ {html_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
            self.stats['html_minified'] += 1
            self.stats['total_size_before'] += original_size
            self.stats['total_size_after'] += optimized_size
    
    def minify_html_content(self, html_content: str) -> str:
        """Minifie le contenu HTML"""
        # Supprimer les commentaires HTML
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples entre les balises
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        # Supprimer les espaces en début de ligne
        html_content = re.sub(r'^\s+', '', html_content, flags=re.MULTILINE)
        
        # Supprimer les lignes vides
        html_content = re.sub(r'\n\s*\n', '\n', html_content)
        
        return html_content.strip()
    
    def create_compressed_versions(self):
        """Crée des versions compressées GZIP des fichiers"""
        print("🗜️  Création des versions compressées...")
        
        compressible_extensions = ['.html', '.css', '.js', '.json', '.xml', '.svg']
        
        for ext in compressible_extensions:
            for file_path in self.optimized_dir.rglob(f"*{ext}"):
                try:
                    self.compress_file(file_path)
                except Exception as e:
                    print(f"⚠️  Erreur lors de la compression de {file_path}: {e}")
    
    def compress_file(self, file_path: Path):
        """Compresse un fichier avec GZIP"""
        with open(file_path, 'rb') as f_in:
            with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        original_size = file_path.stat().st_size
        compressed_size = Path(f"{file_path}.gz").stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"   ✅ {file_path.name}.gz: {original_size} → {compressed_size} bytes (-{compression_ratio:.1f}%)")
    
    def generate_optimization_report(self):
        """Génère un rapport d'optimisation"""
        print("\n📊 RAPPORT D'OPTIMISATION")
        print("=" * 50)
        
        total_savings = self.stats['total_size_before'] - self.stats['total_size_after']
        savings_percentage = (total_savings / self.stats['total_size_before'] * 100) if self.stats['total_size_before'] > 0 else 0
        
        print(f"📈 Statistiques globales:")
        print(f"   • Images optimisées: {self.stats['images_optimized']}")
        print(f"   • Fichiers CSS minifiés: {self.stats['css_minified']}")
        print(f"   • Scripts JS minifiés: {self.stats['js_minified']}")
        print(f"   • Fichiers HTML minifiés: {self.stats['html_minified']}")
        print(f"   • Taille avant: {self.format_bytes(self.stats['total_size_before'])}")
        print(f"   • Taille après: {self.format_bytes(self.stats['total_size_after'])}")
        print(f"   • Économie: {self.format_bytes(total_savings)} ({savings_percentage:.1f}%)")
        
        # Sauvegarder le rapport en JSON
        report_path = self.optimized_dir / "optimization_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvegardé: {report_path}")
        print(f"📁 Assets optimisés dans: {self.optimized_dir}")
    
    def format_bytes(self, bytes_size: int) -> str:
        """Formate la taille en bytes de manière lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def create_inline_assets(self):
        """Crée des versions avec assets inline pour de meilleures performances"""
        print("📦 Création d'assets inline...")
        
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.inline_assets_in_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de l'inline de {html_path}: {e}")
    
    def inline_assets_in_html(self, html_path: Path):
        """Intègre les assets directement dans le HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inline des images petites
        img_pattern = re.compile(r'<img[^>]+src="([^"]+)"[^>]*>', re.IGNORECASE)
        for match in img_pattern.finditer(html_content):
            img_src = match.group(1)
            img_path = self.project_root / img_src
            
            if img_path.exists() and img_path.stat().st_size < 10240:  # < 10KB
                try:
                    with open(img_path, 'rb') as img_file:
                        img_data = img_file.read()
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        mime_type = 'image/png' if img_path.suffix.lower() == '.png' else 'image/jpeg'
                        data_uri = f"data:{mime_type};base64,{img_base64}"
                        
                        html_content = html_content.replace(f'src="{img_src}"', f'src="{data_uri}"')
                        print(f"   ✅ Image inline: {img_src}")
                except Exception as e:
                    print(f"   ⚠️  Erreur inline {img_src}: {e}")
        
        # Sauvegarder la version inline
        output_path = self.optimized_dir / f"inline_{html_path.name}"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Fonction principale d'optimisation"""
    print("🏛️ TALENTSCOPE - OPTIMISEUR D'ASSETS")
    print("Ministère de l'Économie et des Finances")
    print("=" * 60)
    
    optimizer = AssetOptimizer()
    
    # Optimiser tous les assets
    optimizer.optimize_all_assets()
    
    # Créer les versions inline (optionnel)
    optimizer.create_inline_assets()
    
    print("\n✅ OPTIMISATION TERMINÉE!")
    print("🚀 Vos assets sont maintenant optimisés pour de meilleures performances!")

if __name__ == "__main__":
    main()

🏛️ TALENTSCOPE - OPTIMISEUR D'ASSETS
Ministère de l'Économie et des Finances
Version: 2.0 - Optimisation des ressources statiques
"""

import os
import gzip
import shutil
import json
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    Image = None
import base64
import re
from typing import Dict, List, Tuple
import hashlib

class AssetOptimizer:
    """Optimiseur d'assets pour améliorer les performances"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.optimized_dir = self.project_root / "optimized_assets"
        self.optimized_dir.mkdir(exist_ok=True)
        
        # Statistiques d'optimisation
        self.stats = {
            'images_optimized': 0,
            'css_minified': 0,
            'js_minified': 0,
            'html_minified': 0,
            'total_size_before': 0,
            'total_size_after': 0
        }
    
    def optimize_all_assets(self):
        """Optimise tous les assets du projet"""
        print("🚀 OPTIMISATION DES ASSETS TALENTSCOPE")
        print("=" * 50)
        
        # Optimiser les images
        self.optimize_images()
        
        # Minifier les fichiers CSS
        self.minify_css_files()
        
        # Minifier les fichiers JavaScript
        self.minify_js_files()
        
        # Minifier les fichiers HTML
        self.minify_html_files()
        
        # Créer les versions compressées
        self.create_compressed_versions()
        
        # Générer le rapport
        self.generate_optimization_report()
    
    def optimize_images(self):
        """Optimise les images (PNG, JPG, SVG)"""
        print("🖼️  Optimisation des images...")
        
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        for ext in image_extensions:
            for image_path in self.project_root.rglob(f"*{ext}"):
                if 'optimized_assets' in str(image_path):
                    continue
                
                try:
                    self.optimize_single_image(image_path)
                except Exception as e:
                    print(f"⚠️  Erreur lors de l'optimisation de {image_path}: {e}")
    
    def optimize_single_image(self, image_path: Path):
        """Optimise une image unique"""
        if Image is None:
            print(f"   ⚠️  PIL non disponible, copie simple: {image_path.name}")
            # Copie simple si PIL n'est pas disponible
            output_path = self.optimized_dir / image_path.name
            shutil.copy2(image_path, output_path)
            return
        
        original_size = image_path.stat().st_size
        
        try:
            with Image.open(image_path) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                        # Pour JPEG, convertir en RGB
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                
                # Redimensionner si trop grande
                max_size = 1920
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Chemin de sortie optimisé
                output_path = self.optimized_dir / image_path.name
                
                # Sauvegarder avec optimisation
                if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    img.save(output_path, 'JPEG', quality=85, optimize=True)
                elif image_path.suffix.lower() == '.png':
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, optimize=True)
                
                optimized_size = output_path.stat().st_size
                savings = original_size - optimized_size
                
                if savings > 0:
                    print(f"   ✅ {image_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
                    self.stats['images_optimized'] += 1
                    self.stats['total_size_before'] += original_size
                    self.stats['total_size_after'] += optimized_size
                
        except Exception as e:
            print(f"   ❌ Erreur avec {image_path.name}: {e}")
    
    def minify_css_files(self):
        """Minifie les fichiers CSS"""
        print("🎨 Minification des fichiers CSS...")
        
        for css_path in self.project_root.rglob("*.css"):
            if 'optimized_assets' in str(css_path):
                continue
            
            try:
                self.minify_single_css(css_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de la minification de {css_path}: {e}")
    
    def minify_single_css(self, css_path: Path):
        """Minifie un fichier CSS"""
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        original_size = len(css_content.encode('utf-8'))
        
        # Minification CSS
        minified_css = self.minify_css_content(css_content)
        
        # Sauvegarder
        output_path = self.optimized_dir / css_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        optimized_size = len(minified_css.encode('utf-8'))
        savings = original_size - optimized_size
        
        if savings > 0:
            print(f"   ✅ {css_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
            self.stats['css_minified'] += 1
            self.stats['total_size_before'] += original_size
            self.stats['total_size_after'] += optimized_size
    
    def minify_css_content(self, css_content: str) -> str:
        """Minifie le contenu CSS"""
        # Supprimer les commentaires
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples
        css_content = re.sub(r'\s+', ' ', css_content)
        
        # Supprimer les espaces autour des symboles
        css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
        
        # Supprimer les espaces en début et fin
        css_content = css_content.strip()
        
        # Supprimer les points-virgules avant les accolades fermantes
        css_content = re.sub(r';}', '}', css_content)
        
        return css_content
    
    def minify_js_files(self):
        """Minifie les fichiers JavaScript"""
        print("⚡ Minification des fichiers JavaScript...")
        
        # Chercher les scripts dans les fichiers HTML
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.extract_and_minify_js_from_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors du traitement de {html_path}: {e}")
    
    def extract_and_minify_js_from_html(self, html_path: Path):
        """Extrait et minifie le JavaScript des fichiers HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Trouver tous les blocs script
        script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        scripts = script_pattern.findall(html_content)
        
        if scripts:
            minified_html = html_content
            
            for script_content in scripts:
                if script_content.strip() and not script_content.strip().startswith('src='):
                    original_size = len(script_content.encode('utf-8'))
                    minified_script = self.minify_js_content(script_content)
                    optimized_size = len(minified_script.encode('utf-8'))
                    
                    # Remplacer dans le HTML
                    minified_html = minified_html.replace(script_content, minified_script, 1)
                    
                    savings = original_size - optimized_size
                    if savings > 0:
                        self.stats['js_minified'] += 1
                        self.stats['total_size_before'] += original_size
                        self.stats['total_size_after'] += optimized_size
            
            # Sauvegarder le HTML avec JS minifié
            output_path = self.optimized_dir / html_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(minified_html)
    
    def minify_js_content(self, js_content: str) -> str:
        """Minifie le contenu JavaScript (basique)"""
        # Supprimer les commentaires sur une ligne
        js_content = re.sub(r'//.*$', '', js_content, flags=re.MULTILINE)
        
        # Supprimer les commentaires multilignes
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples (attention aux strings)
        lines = js_content.split('\n')
        minified_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Supprimer les espaces autour des opérateurs (basique)
                line = re.sub(r'\s*([=+\-*/{}();,])\s*', r'\1', line)
                minified_lines.append(line)
        
        return ''.join(minified_lines)
    
    def minify_html_files(self):
        """Minifie les fichiers HTML"""
        print("📄 Minification des fichiers HTML...")
        
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.minify_single_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de la minification de {html_path}: {e}")
    
    def minify_single_html(self, html_path: Path):
        """Minifie un fichier HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        original_size = len(html_content.encode('utf-8'))
        
        # Minification HTML
        minified_html = self.minify_html_content(html_content)
        
        # Sauvegarder
        output_path = self.optimized_dir / html_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_html)
        
        optimized_size = len(minified_html.encode('utf-8'))
        savings = original_size - optimized_size
        
        if savings > 0:
            print(f"   ✅ {html_path.name}: {original_size} → {optimized_size} bytes (-{savings} bytes)")
            self.stats['html_minified'] += 1
            self.stats['total_size_before'] += original_size
            self.stats['total_size_after'] += optimized_size
    
    def minify_html_content(self, html_content: str) -> str:
        """Minifie le contenu HTML"""
        # Supprimer les commentaires HTML
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Supprimer les espaces multiples entre les balises
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        # Supprimer les espaces en début de ligne
        html_content = re.sub(r'^\s+', '', html_content, flags=re.MULTILINE)
        
        # Supprimer les lignes vides
        html_content = re.sub(r'\n\s*\n', '\n', html_content)
        
        return html_content.strip()
    
    def create_compressed_versions(self):
        """Crée des versions compressées GZIP des fichiers"""
        print("🗜️  Création des versions compressées...")
        
        compressible_extensions = ['.html', '.css', '.js', '.json', '.xml', '.svg']
        
        for ext in compressible_extensions:
            for file_path in self.optimized_dir.rglob(f"*{ext}"):
                try:
                    self.compress_file(file_path)
                except Exception as e:
                    print(f"⚠️  Erreur lors de la compression de {file_path}: {e}")
    
    def compress_file(self, file_path: Path):
        """Compresse un fichier avec GZIP"""
        with open(file_path, 'rb') as f_in:
            with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        original_size = file_path.stat().st_size
        compressed_size = Path(f"{file_path}.gz").stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"   ✅ {file_path.name}.gz: {original_size} → {compressed_size} bytes (-{compression_ratio:.1f}%)")
    
    def generate_optimization_report(self):
        """Génère un rapport d'optimisation"""
        print("\n📊 RAPPORT D'OPTIMISATION")
        print("=" * 50)
        
        total_savings = self.stats['total_size_before'] - self.stats['total_size_after']
        savings_percentage = (total_savings / self.stats['total_size_before'] * 100) if self.stats['total_size_before'] > 0 else 0
        
        print(f"📈 Statistiques globales:")
        print(f"   • Images optimisées: {self.stats['images_optimized']}")
        print(f"   • Fichiers CSS minifiés: {self.stats['css_minified']}")
        print(f"   • Scripts JS minifiés: {self.stats['js_minified']}")
        print(f"   • Fichiers HTML minifiés: {self.stats['html_minified']}")
        print(f"   • Taille avant: {self.format_bytes(self.stats['total_size_before'])}")
        print(f"   • Taille après: {self.format_bytes(self.stats['total_size_after'])}")
        print(f"   • Économie: {self.format_bytes(total_savings)} ({savings_percentage:.1f}%)")
        
        # Sauvegarder le rapport en JSON
        report_path = self.optimized_dir / "optimization_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvegardé: {report_path}")
        print(f"📁 Assets optimisés dans: {self.optimized_dir}")
    
    def format_bytes(self, bytes_size: int) -> str:
        """Formate la taille en bytes de manière lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def create_inline_assets(self):
        """Crée des versions avec assets inline pour de meilleures performances"""
        print("📦 Création d'assets inline...")
        
        for html_path in self.project_root.rglob("*.html"):
            if 'optimized_assets' in str(html_path):
                continue
            
            try:
                self.inline_assets_in_html(html_path)
            except Exception as e:
                print(f"⚠️  Erreur lors de l'inline de {html_path}: {e}")
    
    def inline_assets_in_html(self, html_path: Path):
        """Intègre les assets directement dans le HTML"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inline des images petites
        img_pattern = re.compile(r'<img[^>]+src="([^"]+)"[^>]*>', re.IGNORECASE)
        for match in img_pattern.finditer(html_content):
            img_src = match.group(1)
            img_path = self.project_root / img_src
            
            if img_path.exists() and img_path.stat().st_size < 10240:  # < 10KB
                try:
                    with open(img_path, 'rb') as img_file:
                        img_data = img_file.read()
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        mime_type = 'image/png' if img_path.suffix.lower() == '.png' else 'image/jpeg'
                        data_uri = f"data:{mime_type};base64,{img_base64}"
                        
                        html_content = html_content.replace(f'src="{img_src}"', f'src="{data_uri}"')
                        print(f"   ✅ Image inline: {img_src}")
                except Exception as e:
                    print(f"   ⚠️  Erreur inline {img_src}: {e}")
        
        # Sauvegarder la version inline
        output_path = self.optimized_dir / f"inline_{html_path.name}"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Fonction principale d'optimisation"""
    print("🏛️ TALENTSCOPE - OPTIMISEUR D'ASSETS")
    print("Ministère de l'Économie et des Finances")
    print("=" * 60)
    
    optimizer = AssetOptimizer()
    
    # Optimiser tous les assets
    optimizer.optimize_all_assets()
    
    # Créer les versions inline (optionnel)
    optimizer.create_inline_assets()
    
    print("\n✅ OPTIMISATION TERMINÉE!")
    print("🚀 Vos assets sont maintenant optimisés pour de meilleures performances!")

if __name__ == "__main__":
    main()







