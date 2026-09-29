"""Persistencia final: red de notas Markdown para Obsidian.

No se usa SQLite, MongoDB ni Neo4j. Cada noticia y cada entidad debe
tener su propia nota, enlazada con [[wiki-links]].
"""

from collections import defaultdict
from pathlib import Path
import re

def slugify(text: str) -> str:
    """Convierte un texto en un slug seguro para nombres de archivos."""
    if not text:
        return "sin-nombre"
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

class EscritorVaultObsidian:
    def __init__(self, output_dir: str | Path = "obsidian_vault"):
        self.output_dir = Path(output_dir)
        self.dir_noticias = self.output_dir / "Noticias"
        self.dir_delitos = self.output_dir / "Delitos"
        self.dir_personas = self.output_dir / "Personas"
        self.dir_organizaciones = self.output_dir / "Organizaciones"
        self.dir_lugares = self.output_dir / "Lugares"
        self.dir_objetos = self.output_dir / "Objetos"
        self.dir_relaciones = self.output_dir / "Relaciones"

        # Crear carpetas si no existen
        for d in [
            self.output_dir,
            self.dir_noticias,
            self.dir_delitos,
            self.dir_personas,
            self.dir_organizaciones,
            self.dir_lugares,
            self.dir_objetos,
            self.dir_relaciones,
        ]:
            d.mkdir(parents=True, exist_ok=True)

    def escribir_entidades(self, noticias: list[dict]) -> None:
        indice_delitos = defaultdict(set)
        indice_personas = defaultdict(set)
        indice_orgs = defaultdict(set)
        indice_lugares = defaultdict(set)
        indice_objetos = defaultdict(set)

        for data in noticias:
            nid = data.get("id_noticia")
            if not nid:
                continue

            for d in data.get("delitos", []):
                nombre_d = d.get("nombre") if isinstance(d, dict) else d
                if nombre_d:
                    indice_delitos[nombre_d].add(nid)

            for p in data.get("personas", []):
                nombre = p.get("nombre") if isinstance(p, dict) else p
                if nombre:
                    indice_personas[nombre].add(nid)

            for o in data.get("organizaciones", []):
                nombre_o = o.get("nombre") if isinstance(o, dict) else o
                if nombre_o:
                    indice_orgs[nombre_o].add(nid)

            for l in data.get("lugares", []):
                nombre_l = l.get("nombre") if isinstance(l, dict) else l
                if nombre_l:
                    indice_lugares[nombre_l].add(nid)

            for obj in data.get("objetos", []):
                nombre_obj = obj.get("nombre") if isinstance(obj, dict) else obj
                if nombre_obj:
                    indice_objetos[nombre_obj].add(nid)

        for delito, nids in indice_delitos.items():
            path = self.dir_delitos / f"{slugify(delito)}.md"
            noticias_links = "\n".join([f"- [[{nid}]]" for nid in sorted(nids)])
            path.write_text(f"# {delito}\n\nTipo: Delito\n\n## Noticias relacionadas\n{noticias_links}\n", encoding="utf-8")

        for persona, nids in indice_personas.items():
            path = self.dir_personas / f"{slugify(persona)}.md"
            noticias_links = "\n".join([f"- [[{nid}]]" for nid in sorted(nids)])
            path.write_text(f"# {persona}\n\nTipo: Persona\n\n## Noticias relacionadas\n{noticias_links}\n", encoding="utf-8")

        for org, nids in indice_orgs.items():
            path = self.dir_organizaciones / f"{slugify(org)}.md"
            noticias_links = "\n".join([f"- [[{nid}]]" for nid in sorted(nids)])
            path.write_text(f"# {org}\n\nTipo: Organización\n\n## Noticias relacionadas\n{noticias_links}\n", encoding="utf-8")

        for lugar, nids in indice_lugares.items():
            path = self.dir_lugares / f"{slugify(lugar)}.md"
            noticias_links = "\n".join([f"- [[{nid}]]" for nid in sorted(nids)])
            path.write_text(f"# {lugar}\n\nTipo: Lugar\n\n## Noticias relacionadas\n{noticias_links}\n", encoding="utf-8")

        for objeto, nids in indice_objetos.items():
            path = self.dir_objetos / f"{slugify(objeto)}.md"
            noticias_links = "\n".join([f"- [[{nid}]]" for nid in sorted(nids)])
            path.write_text(f"# {objeto}\n\nTipo: Objeto\n\n## Noticias relacionadas\n{noticias_links}\n", encoding="utf-8")

    def escribir_vault(self, noticias: list[dict]) -> None:
        """Escribe todas las notas del vault a partir de la lista de noticias."""
        for data in noticias:
            nid = data.get("id_noticia", "desconocido")
            titulo = data.get("titulo", "Sin título")
            path = self.dir_noticias / f"{nid}.md"
            
            contenido = f"# {titulo}\n\nID: {nid}\n\n## Resumen\n{data.get('resumen', 'Sin resumen')}\n"
            path.write_text(contenido, encoding="utf-8")

        self.escribir_entidades(noticias)

        total_noticias = len(noticias)
        indice_path = self.output_dir / "00_Indice.md"
        indice_contenido = (
            "# Índice General\n\n"
            f"- Total noticias: {total_noticias}\n"
            "- [[Noticias/|Noticias/]]\n"
            "- [[Delitos/|Delitos/]]\n"
            "- [[Personas/|Personas/]]\n"
            "- [[Organizaciones/|Organizaciones/]]\n"
            "- [[Lugares/|Lugares/]]\n"
            "- [[Objetos/|Objetos/]]\n"
            "- [[Relaciones/|Relaciones/]]\n"
        )
        indice_path.write_text(indice_contenido, encoding="utf-8")

EscritorObsidian = EscritorVaultObsidian