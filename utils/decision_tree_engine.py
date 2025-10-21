"""
Decision Tree Engine for Business Games Contracts
Handles navigation, scoring, and state management for interactive story contracts
"""

import streamlit as st
from typing import Dict, List, Tuple, Optional

def initialize_decision_tree_state(contract_id: str, start_node: str):
    """Initialize session state for a decision tree contract"""
    if f"dt_{contract_id}_current" not in st.session_state:
        st.session_state[f"dt_{contract_id}_current"] = start_node
        st.session_state[f"dt_{contract_id}_path"] = []
        st.session_state[f"dt_{contract_id}_points"] = 0
        st.session_state[f"dt_{contract_id}_completed"] = False

def get_current_node(contract_id: str, nodes: Dict) -> Dict:
    """Get the current node based on session state"""
    current_node_id = st.session_state.get(f"dt_{contract_id}_current")
    return nodes.get(current_node_id)

def make_choice(contract_id: str, choice: Dict, nodes: Dict):
    """Process a player's choice and move to next node"""
    # Add to path
    path_key = f"dt_{contract_id}_path"
    if path_key not in st.session_state:
        st.session_state[path_key] = []
    
    st.session_state[path_key].append({
        "node_id": st.session_state[f"dt_{contract_id}_current"],
        "choice_text": choice["text"],
        "points": choice.get("points", 0),
        "feedback": choice.get("feedback", "")
    })
    
    # Add points
    points_key = f"dt_{contract_id}_points"
    st.session_state[points_key] = st.session_state.get(points_key, 0) + choice.get("points", 0)
    
    # Move to next node
    st.session_state[f"dt_{contract_id}_current"] = choice["next"]
    
    # Check if ending
    next_node = nodes.get(choice["next"])
    if next_node and next_node.get("is_ending", False):
        st.session_state[f"dt_{contract_id}_completed"] = True

def calculate_final_score(contract_id: str, nodes: Dict, scoring_config: Dict) -> Dict:
    """Calculate final score based on accumulated points"""
    total_points = st.session_state.get(f"dt_{contract_id}_points", 0)
    path = st.session_state.get(f"dt_{contract_id}_path", [])
    current_node_id = st.session_state.get(f"dt_{contract_id}_current")
    
    # Get ending node
    ending_node = nodes.get(current_node_id)
    
    # Convert points to stars based on thresholds
    stars = 1
    points_to_stars = scoring_config.get("points_to_stars", {})
    
    for star_level in sorted([int(k) for k in points_to_stars.keys()], reverse=True):
        if total_points >= points_to_stars[str(star_level)]:
            stars = star_level
            break
    
    # Get outcome details
    outcome = ending_node.get("outcome", {}) if ending_node else {}
    
    return {
        "stars": stars,
        "total_points": total_points,
        "path_length": len(path),
        "ending_title": ending_node.get("title", "Unknown") if ending_node else "Unknown",
        "ending_id": current_node_id,
        "outcome": outcome,
        "path": path
    }

def reset_decision_tree(contract_id: str, start_node: str):
    """Reset decision tree to beginning"""
    st.session_state[f"dt_{contract_id}_current"] = start_node
    st.session_state[f"dt_{contract_id}_path"] = []
    st.session_state[f"dt_{contract_id}_points"] = 0
    st.session_state[f"dt_{contract_id}_completed"] = False

def get_decision_tree_summary(contract_id: str) -> str:
    """Get a text summary of the player's journey"""
    path = st.session_state.get(f"dt_{contract_id}_path", [])
    
    if not path:
        return "No decisions made yet."
    
    summary_parts = []
    for i, step in enumerate(path, 1):
        points_text = f"+{step['points']}" if step['points'] > 0 else f"{step['points']}"
        summary_parts.append(f"{i}. {step['choice_text']} ({points_text} points)")
        if step.get('feedback'):
            summary_parts.append(f"   {step['feedback']}")
    
    return "\n".join(summary_parts)

def get_best_ending_id(nodes: Dict) -> Optional[str]:
    """Find the ending with highest points"""
    best_ending = None
    best_points = float('-inf')
    
    for node_id, node in nodes.items():
        if node.get("is_ending", False):
            outcome = node.get("outcome", {})
            points = outcome.get("points", 0)
            if points > best_points:
                best_points = points
                best_ending = node_id
    
    return best_ending

def calculate_replay_value(contract_id: str, nodes: Dict) -> Dict:
    """Calculate what player could discover on replay"""
    current_ending = st.session_state.get(f"dt_{contract_id}_current")
    
    # Count total endings
    total_endings = sum(1 for node in nodes.values() if node.get("is_ending", False))
    
    # Check if this is best ending
    best_ending = get_best_ending_id(nodes)
    is_best = (current_ending == best_ending)
    
    return {
        "total_endings": total_endings,
        "current_ending": current_ending,
        "is_best_ending": is_best,
        "replay_recommended": not is_best,
        "undiscovered_endings": total_endings - 1
    }
