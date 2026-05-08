"""
graph.py — LangGraph state graph definition for the
Regulatory Documentation Intelligence Agent.
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
import operator

from agent.nodes.parser import parse_document
from agent.nodes.retriever import retrieve_chunks
from agent.nodes.classifier import classify_obligations
from agent.nodes.extractor import extract_obligations
from agent.nodes.summariser import summarise_obligations


# ── State schema ──────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    """Shared state passed between all agent nodes."""

    # Inputs
    document_path: str
    user_query: Optional[str]

    # Parser outputs
    raw_text: str
    chunks: List[Dict[str, Any]]          # [{text, section, page, chunk_id}]
    document_metadata: Dict[str, Any]

    # Retriever outputs
    relevant_chunks: List[Dict[str, Any]] # top-k chunks for the query

    # Classifier outputs
    classified_chunks: List[Dict[str, Any]]  # chunks + obligation_type label

    # Extractor outputs
    obligations: List[Dict[str, Any]]     # structured obligation records

    # Summariser outputs
    report: Dict[str, Any]                # final structured report

    # Control flow
    errors: Annotated[List[str], operator.add]
    status: str


# ── Routing helpers ───────────────────────────────────────────────────────────

def _should_retrieve(state: AgentState) -> str:
    """Route to retriever if query present, else go straight to classifier."""
    if state.get("user_query"):
        return "retrieve"
    return "classify"


def _check_errors(state: AgentState) -> str:
    """Halt pipeline if a critical error has occurred."""
    if state.get("errors"):
        last = state["errors"][-1]
        if last.startswith("CRITICAL"):
            return "end"
    return "continue"


# ── Graph builder ─────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    """
    Construct and compile the LangGraph agentic pipeline.

    Flow:
        parse → [retrieve?] → classify → extract → summarise → END
    """
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("parse",     parse_document)
    graph.add_node("retrieve",  retrieve_chunks)
    graph.add_node("classify",  classify_obligations)
    graph.add_node("extract",   extract_obligations)
    graph.add_node("summarise", summarise_obligations)

    # Entry point
    graph.set_entry_point("parse")

    # Conditional edge after parsing: retrieve if query given, else classify
    graph.add_conditional_edges(
        "parse",
        _should_retrieve,
        {"retrieve": "retrieve", "classify": "classify"},
    )

    # Retriever always flows to classifier
    graph.add_edge("retrieve", "classify")

    # Classifier → extractor → summariser → END
    graph.add_edge("classify",  "extract")
    graph.add_edge("extract",   "summarise")
    graph.add_edge("summarise", END)

    return graph.compile()


# Singleton compiled graph
compiled_graph = build_graph()
