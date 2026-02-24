import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # Updated import
from langchain_huggingface import HuggingFaceEmbeddings

# --- 1. Setup data directory ---
if not os.path.exists("data"):
    os.makedirs("data")
    print("📁 Folder 'data' created. Please place your PDFs in this folder.")
    print("⏹️  Exiting... Add PDFs and run again.")
    exit()

# Check if data folder has PDFs
pdf_files = [f for f in os.listdir("data") if f.endswith('.pdf')]
if not pdf_files:
    print("⚠️  No PDF files found in 'data' folder!")
    exit()

print(f"📚 Found {len(pdf_files)} PDF file(s): {', '.join(pdf_files)}")

# --- 2. Load PDFs ---
print("⏳ Loading PDFs...")
loader = DirectoryLoader(
    "data/", 
    glob="**/*.pdf",  # Recursive search
    loader_cls=PyPDFLoader,
    show_progress=True,
    use_multithreading=True
)

try:
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages total from PDFs.")
except Exception as e:
    print(f"❌ Error loading PDFs: {e}")
    exit()

if not documents:
    print("⚠️  No content extracted from PDFs!")
    exit()

# --- 3. Split text ---
print("✂️  Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
texts = text_splitter.split_documents(documents)
print(f"✅ Created {len(texts)} chunks from documents.")

# --- 4. Create embeddings ---
print("🧠 Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
    encode_kwargs={'normalize_embeddings': True}
)

# --- 5. Create/Reset vector DB ---
if os.path.exists("db"):
    print("🗑️  Removing old database...")
    shutil.rmtree("db")

print("💾 Creating new vector database (this may take a while)...")
try:
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="db",
        collection_metadata={"hnsw:space": "cosine"}  # Optimize for cosine similarity
    )
    # Explicit persist for older Chroma versions compatibility
    if hasattr(vectordb, 'persist'):
        vectordb.persist()
    
    print("✅ Vector database successfully created and persisted!")
    print(f"📊 Database contains {vectordb._collection.count()} vectors.")
    
except Exception as e:
    print(f"❌ Error creating vector database: {e}")
    exit()