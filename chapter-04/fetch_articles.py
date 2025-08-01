# NYTControlledYield_v8_robust.py
"""
Recolector de Rendimiento Controlado - Completamente Robusto para Windows
"""
import requests
import pandas as pd
import time
import os
import sys
import signal
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional, Set
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict

# === CONFIGURACIÓN ROBUSTA PARA WINDOWS ===
if sys.platform.startswith('win'):
    try:
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass  # Si falla, continuamos sin emojis

# Configuración de logging SIN EMOJIS para evitar problemas
log_handlers = [
    logging.StreamHandler(),
    logging.FileHandler('controlled_yield_fetcher.log', mode='w', encoding='utf-8')
]

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=log_handlers,
    force=True
)

class NYTControlledYieldFetcher:
    SEARCH_STRATEGIES = {
        "News": {"queries": ["politics", "election", "government", "international"], "target": 300},
        "Business": {"queries": ["economy", "markets", "technology", "finance"], "target": 250},
        "Sports": {"queries": ["NFL", "NBA", "soccer", "olympics", "baseball"], "target": 200},
        "Culture": {"queries": ["movies", "music", "arts", "books", "theater"], "target": 250},
        "Science": {"queries": ["science", "health", "climate change", "medicine"], "target": 200}
    }
    
    WAIT_TIME = 12
    DAILY_LIMIT = 480
    MAX_PAGES_PER_QUERY = 10
    RATE_LIMIT_SLEEP = 60
    REQUEST_TIMEOUT = 30

    def __init__(self):
        load_dotenv()
        self.api_key = self._get_api_key()
        self.base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        
        # Session para mejor rendimiento
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NYT-Controlled-Yield-Fetcher/8.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        })
        
        # Estado del fetcher
        self.articles = defaultdict(list)
        self.seen_urls: Set[str] = set()
        self.requests_today = 0
        self.progress_tracker = {
            cat: {"query_idx": 0, "page": 0} 
            for cat in self.SEARCH_STRATEGIES.keys()
        }
        
        # Directorio de salida
        self.output_dir = Path(f"NYT_ControlledYield_Dataset_{time.strftime('%Y%m%d-%H%M%S')}")
        self.output_dir.mkdir(exist_ok=True)
        
        # Flag para manejo de interrupciones
        self.interrupted = False
        
        # Configurar manejador de interrupciones
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def __del__(self):
        """Cleanup: cierra la sesión cuando el objeto se destruye."""
        if hasattr(self, 'session'):
            self.session.close()

    def _get_api_key(self) -> str:
        """Obtiene la API key del entorno."""
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API KEY no encontrada en .env")
        return api_key

    def _save_data_to_csv(self) -> bool:
        """Guarda los datos recolectados en CSV. Retorna True si se guardó exitosamente."""
        all_articles = [article for articles_list in self.articles.values() for article in articles_list]
        
        if not all_articles:
            logging.warning("No se recolectaron articulos, no se guardara ningun archivo.")
            print("\n[WARNING] No se recolectaron artículos para guardar.")
            return False

        try:
            df = pd.DataFrame(all_articles)
            csv_path = self.output_dir / "collected_articles.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            logging.info("DATOS GUARDADOS DE FORMA SEGURA en: %s", csv_path)
            print(f"\n[SUCCESS] DATOS GUARDADOS en: {csv_path}")
            self._print_summary()
            return True
        except Exception as e:
            logging.error("Error al guardar CSV: %s", e)
            print(f"\n[ERROR] No se pudo guardar el archivo: {e}")
            return False

    def _handle_interrupt(self, signum, frame) -> None:
        """Maneja la interrupción del usuario."""
        self.interrupted = True
        print("\n\n[ALERT] INTERRUPCION DETECTADA! Guardando progreso...")
        logging.warning("INTERRUPCION DETECTADA! Guardando todo el progreso recolectado...")
        
        # Guardar datos inmediatamente
        success = self._save_data_to_csv()
        
        # Cerrar sesión
        if hasattr(self, 'session'):
            self.session.close()
        
        print("[INFO] Proceso interrumpido de forma segura.")
        sys.exit(0 if success else 1)

    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict]:
        """Realiza una petición HTTP con manejo de errores optimizado."""
        if self.requests_today >= self.DAILY_LIMIT or self.interrupted:
            return None

        # Sleep antes del request, pero permitir interrupciones
        for _ in range(self.WAIT_TIME):
            if self.interrupted:
                return None
            time.sleep(1)
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=self.REQUEST_TIMEOUT)
            self.requests_today += 1
            
            if response.status_code == 429:
                logging.warning("Rate limit alcanzado. Esperando %ds...", self.RATE_LIMIT_SLEEP)
                time.sleep(self.RATE_LIMIT_SLEEP)
                return None
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error("Error en la peticion: %s", e)
            return None

    def _process_articles(self, docs: list, category: str, target: int) -> int:
        """Procesa los artículos de una respuesta de la API."""
        new_articles_count = 0
        
        for doc in docs:
            if len(self.articles[category]) >= target or self.interrupted:
                break
                
            url = doc.get('web_url', '')
            if url and url not in self.seen_urls:
                article = self._create_article_dict(doc, category)
                self.articles[category].append(article)
                self.seen_urls.add(url)
                new_articles_count += 1
                
        return new_articles_count

    def _create_article_dict(self, doc: Dict, category: str) -> Dict[str, str]:
        """Crea un diccionario de artículo a partir de un documento de la API."""
        return {
            'url': doc.get('web_url', ''),
            'title': (doc.get('headline', {}).get('main', '') or '').strip(),
            'body': (doc.get('lead_paragraph', '') or doc.get('snippet', '') or '').strip(),
            'section': doc.get('section_name', ''),
            'category': category,
            'pub_date': doc.get('pub_date', '')
        }

    def _should_continue_category(self, category: str, strategy: Dict) -> bool:
        """Determina si se debe continuar recolectando para una categoría."""
        if self.interrupted:
            return False
            
        tracker = self.progress_tracker[category]
        target = strategy['target']
        
        return (len(self.articles[category]) < target and 
                tracker['query_idx'] < len(strategy['queries']))

    def _update_tracker(self, category: str, has_more_data: bool) -> None:
        """Actualiza el tracker de progreso para una categoría."""
        tracker = self.progress_tracker[category]
        tracker['page'] += 1
        
        if tracker['page'] >= self.MAX_PAGES_PER_QUERY or not has_more_data:
            tracker['page'] = 0
            tracker['query_idx'] += 1

    def _get_progress_stats(self) -> Dict[str, Any]:
        """Calcula estadísticas de progreso en tiempo real."""
        total_collected = len(self.seen_urls)
        total_target = sum(strategy['target'] for strategy in self.SEARCH_STRATEGIES.values())
        overall_progress = (total_collected / total_target * 100) if total_target > 0 else 0
        
        category_progress = {}
        for cat, strategy in self.SEARCH_STRATEGIES.items():
            collected = len(self.articles[cat])
            target = strategy['target']
            progress = (collected / target * 100) if target > 0 else 0
            category_progress[cat] = {
                'collected': collected,
                'target': target,
                'progress': progress,
                'completed': collected >= target
            }
        
        return {
            'total_collected': total_collected,
            'total_target': total_target,
            'overall_progress': overall_progress,
            'categories': category_progress,
            'requests_used': self.requests_today,
            'requests_limit': self.DAILY_LIMIT
        }

    def run(self) -> None:
        """Ejecuta el proceso principal de recolección."""
        print("="*60)
        print("INICIANDO RECOLECTOR DE RENDIMIENTO CONTROLADO v8.0")
        print("="*60)
        print("Presiona Ctrl+C en cualquier momento para guardar y salir")
        print("="*60)
        
        logging.info("Iniciando Recolector de Rendimiento Controlado v8.0")
        
        try:
            # Configurar progress bar principal
            with tqdm(total=self.DAILY_LIMIT, desc="API Requests", unit="req") as pbar:
                
                while self.requests_today < self.DAILY_LIMIT and not self.interrupted and self._has_work_to_do():
                    
                    for category, strategy in self.SEARCH_STRATEGIES.items():
                        if self.requests_today >= self.DAILY_LIMIT or self.interrupted:
                            break
                            
                        if not self._should_continue_category(category, strategy):
                            continue
                        
                        self._process_category(category, strategy, pbar)
                        
                        # Mostrar progreso detallado cada 5 requests
                        if self.requests_today % 5 == 0:
                            self._show_detailed_progress()
                    
        except KeyboardInterrupt:
            # Este catch es backup por si el signal handler no funciona
            self._handle_interrupt(None, None)
        except Exception as e:
            logging.critical("Error critico durante la recoleccion: %s", e, exc_info=True)
            print(f"\n[ERROR CRÍTICO] {e}")
        finally:
            if not self.interrupted:  # Solo si no fue manejado por el signal handler
                print("\n--- La recoleccion ha finalizado ---")
                logging.info("La recoleccion ha finalizado")
                self._save_data_to_csv()
                self.session.close()

    def _show_detailed_progress(self) -> None:
        """Muestra progreso detallado en consola."""
        stats = self._get_progress_stats()
        
        print(f"\n--- PROGRESO ACTUAL ---")
        print(f"Total: {stats['total_collected']}/{stats['total_target']} artículos ({stats['overall_progress']:.1f}%)")
        print(f"Requests: {stats['requests_used']}/{stats['requests_limit']}")
        
        for cat, data in stats['categories'].items():
            status = "[COMPLETADO]" if data['completed'] else f"[{data['progress']:.1f}%]"
            print(f"  {cat:<10}: {data['collected']:>3}/{data['target']} {status}")
        print("-" * 25)

    def _has_work_to_do(self) -> bool:
        """Verifica si hay trabajo pendiente en alguna categoría."""
        return any(
            self._should_continue_category(category, strategy)
            for category, strategy in self.SEARCH_STRATEGIES.items()
        )

    def _process_category(self, category: str, strategy: Dict, pbar: tqdm) -> None:
        """Procesa una categoría específica."""
        tracker = self.progress_tracker[category]
        query = strategy['queries'][tracker['query_idx']]
        
        params = {
            'api-key': self.api_key,
            'q': query,
            'page': tracker['page']
        }
        
        # Actualizar descripción de la barra de progreso
        current_count = len(self.articles[category])
        target_count = strategy['target']
        pbar.set_description(f"{category} ({current_count}/{target_count}) - '{query}'")
        
        data = self._make_request(params)
        if not data:
            self._update_tracker(category, False)
            pbar.update(1)
            return
            
        docs = data.get('response', {}).get('docs', [])
        if not docs:
            self._update_tracker(category, False)
            pbar.update(1)
            return
            
        new_articles_count = self._process_articles(docs, category, strategy['target'])
        total_articles = len(self.seen_urls)
        
        # Actualizar postfix con estadísticas
        pbar.set_postfix({
            "Total": total_articles,
            "New": new_articles_count,
            f"{category}": f"{len(self.articles[category])}/{strategy['target']}"
        })
        
        pbar.update(1)
        self._update_tracker(category, len(docs) > 0)

    def _print_summary(self) -> None:
        """Imprime el resumen final de la recolección."""
        print("\n" + "="*50)
        print("RESUMEN FINAL DE LA RECOLECCION CONTROLADA")
        print(f"Total de peticiones realizadas: {self.requests_today} / {self.DAILY_LIMIT}")
        print(f"Total de articulos UNICOS recolectados: {len(self.seen_urls)}")
        print("\nDistribucion final por categoria (Recolectado / Objetivo):")
        
        for cat, strategy in self.SEARCH_STRATEGIES.items():
            articles_count = len(self.articles[cat])
            target = strategy['target']
            percentage = (articles_count / target * 100) if target > 0 else 0
            status = "COMPLETADO" if articles_count >= target else f"{percentage:.1f}%"
            print(f"- {cat:<10}: {articles_count:>4} / {target} articulos [{status}]")
        
        print("="*50)

if __name__ == "__main__":
    fetcher = NYTControlledYieldFetcher()
    fetcher.run()