from backend.core.vectordatabase import VectorDatabase
from backend.core.text_utils import PDFLoader, TextFileLoader, CharacterTextSplitter

class VectorStore:
    def __init__(self):
        self.vector_db = None
        self.splitter = CharacterTextSplitter()

    async def process_file(self, file_path: str, is_pdf: bool) -> int:
        """Process a file and store its chunks in the vector database"""
        loader = PDFLoader(file_path) if is_pdf else TextFileLoader(file_path)
        documents = loader.load_documents()
        chunks = self.splitter.split_texts(documents)

        self.vector_db = VectorDatabase()
        await self.vector_db.abuild_from_list(chunks)
        return len(chunks)

    def search(self, query: str, k: int = 4):
        """Search the vector database for relevant context"""
        if self.vector_db is None:
            return []
        return self.vector_db.search_by_text(query, k=k)

    @property
    def is_initialized(self) -> bool:
        """Check if the vector database has been initialized"""
        return self.vector_db is not None 