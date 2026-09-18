"""
Main execution script for the Darukaa.Earth AI Biodiversity Intelligence System.
Supports Server mode, CLI Interactive mode, and Automated Demonstration mode.
"""

import sys
import os
import argparse
import uvicorn
from src.config import HOST, PORT

# Force UTF-8 on Windows consoles to prevent cp1252 character map errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_server():
    """Starts the FastAPI web server and UI."""
    print("=" * 70)
    print("[SYSTEM] Starting Darukaa.Earth AI Biodiversity Intelligence System")
    print(f"[ONLINE] Server running at: http://{HOST}:{PORT}")
    print(f"[DASHBOARD] Interactive Dashboard: http://localhost:{PORT}")
    print(f"[DOCS] API Documentation: http://localhost:{PORT}/docs")
    print("=" * 70)
    uvicorn.run("src.api.server:app", host=HOST, port=PORT, reload=False)


def run_cli():
    """Runs interactive command-line session."""
    from src.api.server import chat_endpoint
    from src.models.schemas import ChatRequest
    import asyncio

    print("=" * 70)
    print("[SYSTEM] Darukaa.Earth AI Biodiversity Intelligence - Interactive CLI")
    print("Type your environmental query below. Type 'exit' to quit, 'reset' to clear.")
    print("=" * 70)

    session_id = "cli_session"

    while True:
        try:
            user_input = input("\nYou > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                break
            if user_input.lower() == "reset":
                from src.api.server import memory_manager
                memory_manager.reset_session(session_id)
                print("🔄 Memory reset.")
                continue

            req = ChatRequest(message=user_input, session_id=session_id)
            response = asyncio.run(chat_endpoint(req))
            print(f"\nAI Scientist >\n{response.reply}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting CLI.")
            break


def run_demo():
    """Runs the full Darukaa hackathon demonstration scenario."""
    import asyncio
    from src.api.server import chat_endpoint
    from src.models.schemas import ChatRequest

    print("=" * 70)
    print("[DEMO] Running Darukaa Hackathon Verification Scenarios")
    print("=" * 70)

    session_id = "demo_session"

    # Turn 1: Incomplete Query (PDF Example 1)
    print("\n--- TURN 1: Incomplete Input (Missing Environmental Variables) ---")
    query_1 = "Biodiversity is declining on my land."
    print(f"User: \"{query_1}\"")
    req_1 = ChatRequest(message=query_1, session_id=session_id)
    resp_1 = asyncio.run(chat_endpoint(req_1))
    print(f"Status: {resp_1.status}")
    print(f"Clarifying Questions Triggered: {len(resp_1.clarifying_questions)}")
    for q in resp_1.clarifying_questions:
        print(f"  • {q.question_text}")

    # Turn 2: Providing Missing Context (PDF Example 2)
    print("\n--- TURN 2: Multi-Turn Memory & Multi-Metric Analysis ---")
    query_2 = "Soil organic carbon is 0.3%, rainfall is low, and crop is monoculture wheat in a semi-arid region."
    print(f"User: \"{query_2}\"")
    req_2 = ChatRequest(message=query_2, session_id=session_id)
    resp_2 = asyncio.run(chat_endpoint(req_2))
    print(f"Status: {resp_2.status}")
    print(f"Variables Accumulated in Context: {resp_2.variables_in_context}")
    print(f"\nAI Environmental Scientist Response:\n{resp_2.reply}")

    print("\n[SUCCESS] Verification demonstration completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Darukaa Biodiversity Intelligence")
    parser.add_argument("--server", action="store_true", help="Launch FastAPI Web Server")
    parser.add_argument("--cli", action="store_true", help="Launch interactive CLI")
    parser.add_argument("--demo", action="store_true", help="Run automated demonstration")

    args = parser.parse_args()

    if args.cli:
        run_cli()
    elif args.demo:
        run_demo()
    else:
        run_server()
