from src.services.vector_service.retriever import Retriever
from src.services.llm_service.prompt_builder import PromptBuilder
from src.services.llm_service.answer_generator import AnswerGenerator
from src.services.learning_service.optimizer import RankingOptimizer

def run_query(query, vector_store, embedder):
    retriever = Retriever(vector_store, embedder)
    raw_chunks = retriever.get_relevant_chunks(query, top_k=10)

    optimizer = RankingOptimizer()
    best_chunks_dicts = optimizer.boost_chunks(raw_chunks)
    final_docs = [item['doc'] for item in best_chunks_dicts[:5]]

    physical_structure = vector_store.get_verified_structure()
    
    builder = PromptBuilder()
    full_prompt = builder.build_code_qa_prompt(
        query=query, 
        context_docs=final_docs, 
        physical_files=physical_structure
    )

    generator = AnswerGenerator()
    return generator.generate_answer(full_prompt)