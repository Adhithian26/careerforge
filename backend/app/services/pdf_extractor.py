import re
import zlib
from typing import Dict, Any

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts text from PDF binary streams using standard library zlib and regex.
    Zero external C-library or binary dependencies.
    """
    text_chunks = []
    
    # 1. Match and decompress FlateDecode streams
    stream_pattern = re.compile(rb'stream[\r\n]+(.*?)[\r\n]+endstream', re.DOTALL)
    for match in stream_pattern.finditer(pdf_bytes):
        stream_data = match.group(1)
        try:
            decompressed = zlib.decompress(stream_data)
        except Exception:
            decompressed = stream_data

        # Extract literal text strings from PDF content stream (Tj and TJ operators)
        # Matches text within balanced parentheses
        tj_strings = re.findall(rb'\(([^()]*)\)', decompressed)
        for s in tj_strings:
            try:
                decoded = s.decode("utf-8", errors="ignore").strip()
                if len(decoded) > 1 and any(c.isalnum() for c in decoded):
                    text_chunks.append(decoded)
            except Exception:
                pass

    if text_chunks:
        # Join chunks and clean up excess whitespace
        full_text = " ".join(text_chunks)
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        if len(full_text) > 30:
            return full_text

    # 2. Fallback heuristic: search for printable words
    raw_str = pdf_bytes.decode("latin-1", errors="ignore")
    # Clean PDF formatting artifacts
    words = re.findall(r'[A-Za-z0-9+#./@_-]{2,}', raw_str)
    # Filter out common PDF internal keywords
    stopwords = {"obj", "endobj", "stream", "endstream", "xref", "trailer", "startxref", "Font", "Type", "Page", "Pages", "Catalog", "FlateDecode"}
    clean_words = [w for w in words if w not in stopwords]
    return " ".join(clean_words[:600])

