from dotenv import load_dotenv
from pwc import extract_papers
import click
import os
from upstash import UpstashVectorStore
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from upstash_vector import Index

# @click.command()
# @click.option("--query")
# @click.option("--batch_size")
# @click.option("--limit")
def return_documents_list(query,batch_size,limit):
    load_dotenv()
    # click.echo("Extracting papers matching this query: {query}")
    papers = extract_papers(query)
    # click.echo("Extraction complete.",len(papers))
    documents = [
        Document(
            page_content = paper['abstract'],
            metadata = {
                "id":paper["id"] if paper["id"] else "",
                "arxiv_id":paper["arxiv_id"] if paper["arxiv_id"] else "",
                "url_pdf":paper["url_pdf"] if paper["url_pdf"] else "",
                "title":paper["title"] if paper["title"] else "",
                "authors":paper["authors"] if paper["authors"] else "",
                "published":paper["published"] if paper["published"] else ""
            },
        )
        for paper in papers
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1200,
        chunk_overlap=200,
        # separator=["."]
    )

    splits = text_splitter.split_documents(documents)
    splits = splits[:limit]

    index = Index(
        url = os.environ.get("UPSTASH_URL"),
        token = os.environ.get("UPSTASH_TOKEN")
    )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",dimensions=256)
    vector_store = UpstashVectorStore(index,embeddings)
    # click.echo("Indexing to upstash..")
    print("\n\n\n\n",splits,"\n\n\n\n")
    ids = vector_store.add_documents(splits,batch_size = batch_size)
    # click.echo("Successfully indexed {len(ids)} vectors to upstash vector store")
