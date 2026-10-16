"""CI fixture: serve the production build under the actual repository subpath."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        route=unquote(urlsplit(path).path)
        if not route.startswith('/banking-model-atlas/'):
            return str(ROOT/'__not_found__')
        relative=route[len('/banking-model-atlas/'):]
        resolved=(ROOT/relative).resolve()
        if not resolved.is_relative_to(ROOT):return str(ROOT/'__not_found__')
        return str(resolved)
ThreadingHTTPServer(('127.0.0.1',4173),Handler).serve_forever()
