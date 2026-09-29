"""Data Understanding sobre el corpus estructurado.

TODO(alumno): las visualizaciones no son decoración; deben revelar
cobertura, sesgos y problemas de calidad (nulos, JSON inválidos, nombres
inconsistentes).
"""

from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

from src.excepciones import EtapaPendienteAlumno


class ExploradorDatos:
    """Estadísticas y gráficos mínimos del laboratorio."""

    def __init__(self, dir_json: str | Path = "data/json"):
        self.dir_json = Path(dir_json)
        self.df = self._cargar_datos()

    def _cargar_datos(self) -> pd.DataFrame:
        """Carga todos los archivos JSON en un DataFrame de Pandas."""
        noticias = []
        if self.dir_json.exists():
            for archivo in self.dir_json.glob("*.json"):
                if archivo.name == ".gitkeep":
                    continue
                try:
                    with open(archivo, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        noticias.append(data)
                except Exception as e:
                    print(f"Error leyendo {archivo.name}: {e}")
        return pd.DataFrame(noticias)

    def noticias_por_fuente(self) -> None:
        """Gráfico de barras de noticias por fuente."""
        if self.df.empty or "fuente" not in self.df.columns:
            print("No hay datos suficientes para 'noticias_por_fuente'.")
            return

        conteo = self.df["fuente"].value_counts()
        print("\n--- Noticias por Fuente ---")
        print(conteo)

        plt.figure(figsize=(8, 5))
        conteo.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.title("Noticias por Fuente")
        plt.xlabel("Fuente")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def delitos_frecuentes(self) -> None:
        """Top 10 delitos a partir de data/json/*.json."""
        if self.df.empty or "delitos" not in self.df.columns:
            print("No hay datos suficientes para 'delitos_frecuentes'.")
            return

        delitos_lista = []
        for delitos in self.df["delitos"].dropna():
            for d in delitos:
                nombre = d.get("nombre") if isinstance(d, dict) else d
                if nombre:
                    delitos_lista.append(nombre)

        if not delitos_lista:
            print("No se encontraron delitos registrados.")
            return

        s_delitos = pd.Series(delitos_lista).value_counts().head(10)
        print("\n--- Top Delitos Frecuentes ---")
        print(s_delitos)

        plt.figure(figsize=(10, 5))
        s_delitos.plot(kind="barh", color="salmon", edgecolor="black")
        plt.title("Top 10 Delitos Más Frecuentes")
        plt.xlabel("Frecuencia")
        plt.ylabel("Delito")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def lugares_frecuentes(self) -> None:
        """Cuenta menciones de lugares y grafica los más frecuentes."""
        if self.df.empty or "lugares" not in self.df.columns:
            print("No hay datos suficientes para 'lugares_frecuentes'.")
            return

        lugares_lista = []
        for lugares in self.df["lugares"].dropna():
            for l in lugares:
                nombre = l.get("nombre") if isinstance(l, dict) else l
                if nombre:
                    lugares_lista.append(nombre)

        if not lugares_lista:
            print("No se encontraron lugares registrados.")
            return

        s_lugares = pd.Series(lugares_lista).value_counts().head(10)
        print("\n--- Lugares Más Frecuentes ---")
        print(s_lugares)

        plt.figure(figsize=(10, 5))
        s_lugares.plot(kind="bar", color="lightgreen", edgecolor="black")
        plt.title("Lugares Más Mencinados")
        plt.xlabel("Lugar")
        plt.ylabel("Menciones")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def campos_faltantes(self) -> None:
        """Calcula el porcentaje de valores nulos o vacíos por campo."""
        if self.df.empty:
            print("No hay datos para analizar campos faltantes.")
            return

        print("\n--- Porcentaje de Campos Faltantes/Vacíos ---")
        faltantes = self.df.isnull().mean() * 100
        print(faltantes)

    def evolucion_temporal(self) -> None:
        """Grafica noticias por fecha de publicación si está disponible."""
        if self.df.empty or "fecha_publicacion" not in self.df.columns:
            print("No hay columna de fecha_publicacion.")
            return

        df_temp = self.df.copy()
        df_temp["fecha_publicacion"] = pd.to_datetime(df_temp["fecha_publicacion"], errors="coerce")
        df_temp = df_temp.dropna(subset=["fecha_publicacion"])

        if df_temp.empty:
            print("No hay fechas válidas para graficar la evolución temporal.")
            return

        conteo_mes = df_temp.set_index("fecha_publicacion").resample("ME").size()
        
        print("\n--- Evolución Temporal por Mes ---")
        print(conteo_mes)

        plt.figure(figsize=(10, 4))
        conteo_mes.plot(kind="line", marker="o", color="purple")
        plt.title("Evolución Temporal de Noticias")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad de Noticias")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def ejecutar(self) -> None:
        """Corre todas las visualizaciones pedidas en la guía."""
        print("== Ejecutando Análisis de Datos (Data Understanding) ==")
        self.noticias_por_fuente()
        self.delitos_frecuentes()
        self.lugares_frecuentes()
        self.campos_faltantes()
        self.evolucion_temporal()