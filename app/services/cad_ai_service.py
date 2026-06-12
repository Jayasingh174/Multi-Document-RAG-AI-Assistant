import ezdxf
import os
from typing import List, Dict

from app.services.dwg_service import convert_dwg_to_dxf


class CADExtractor:

    def __init__(self, file_path: str):
        self.file_path = file_path

        if file_path.lower().endswith(".dwg"):
            self.file_path = convert_dwg_to_dxf(file_path)

        self.doc = ezdxf.readfile(self.file_path)
        self.msp = self.doc.modelspace()

    # -------------------------
    # LAYER EXTRACTION
    # -------------------------
    def extract_layers(self) -> List[str]:

        layers = []

        for layer in self.doc.layers:
            layers.append(layer.dxf.name)

        return layers

    # -------------------------
    # TEXT EXTRACTION
    # -------------------------
    def extract_text(self) -> List[str]:

        texts = []

        for entity in self.msp:

            if entity.dxftype() == "TEXT":
                texts.append(entity.dxf.text)

            elif entity.dxftype() == "MTEXT":
                texts.append(entity.text)

        return texts

    # -------------------------
    # BLOCK EXTRACTION
    # -------------------------
    def extract_blocks(self) -> List[Dict]:

        blocks = []

        for entity in self.msp:

            if entity.dxftype() == "INSERT":

                block_data = {
                    "block_name": entity.dxf.name,
                    "layer": entity.dxf.layer,
                    "position": entity.dxf.insert
                }

                blocks.append(block_data)

        return blocks

    # -------------------------
    # DIMENSION EXTRACTION
    # -------------------------
    def extract_dimensions(self) -> List[str]:

        dims = []

        for entity in self.msp:

            if entity.dxftype() == "DIMENSION":

                try:
                    dims.append(entity.dxf.text)
                except:
                    dims.append("dimension")

        return dims

    # -------------------------
    # LINE EXTRACTION
    # -------------------------
    def extract_lines(self) -> List[Dict]:

        lines = []

        for entity in self.msp:

            if entity.dxftype() == "LINE":

                line = {
                    "start": entity.dxf.start,
                    "end": entity.dxf.end,
                    "layer": entity.dxf.layer
                }

                lines.append(line)

        return lines

    # -------------------------
    # POLYLINE EXTRACTION
    # -------------------------
    def extract_polylines(self) -> List[List]:

        polylines = []

        for entity in self.msp:

            if entity.dxftype() in ["LWPOLYLINE", "POLYLINE"]:

                points = []

                for p in entity.get_points():
                    points.append(p)

                polylines.append(points)

        return polylines

    # -------------------------
    # GEOMETRY EXTRACTION
    # -------------------------
    def extract_geometry(self) -> List[Dict]:

        geometry = []

        for entity in self.msp:

            if entity.dxftype() == "CIRCLE":

                geometry.append({
                    "type": "circle",
                    "center": entity.dxf.center,
                    "radius": entity.dxf.radius
                })

            elif entity.dxftype() == "ARC":

                geometry.append({
                    "type": "arc",
                    "center": entity.dxf.center,
                    "radius": entity.dxf.radius
                })

        return geometry

    # -------------------------
    # COORDINATE EXTRACTION
    # -------------------------
    def extract_coordinates(self) -> List:

        coords = []

        for entity in self.msp:

            if hasattr(entity.dxf, "insert"):
                coords.append(entity.dxf.insert)

        return coords

    # -------------------------
    # FULL SEMANTIC EXTRACTION
    # -------------------------
    def extract_all(self) -> str:

        layers = self.extract_layers()
        text = self.extract_text()
        blocks = self.extract_blocks()
        dims = self.extract_dimensions()
        lines = self.extract_lines()
        geometry = self.extract_geometry()

        results = []

        for layer in layers:
            results.append(f"Layer: {layer}")

        for t in text:
            results.append(f"Text: {t}")

        for b in blocks:
            results.append(f"Block: {b['block_name']} at {b['position']}")

        for d in dims:
            results.append(f"Dimension: {d}")

        for l in lines:
            results.append(f"Line from {l['start']} to {l['end']}")

        for g in geometry:
            results.append(f"Geometry: {g}")

        return "\n".join(results)