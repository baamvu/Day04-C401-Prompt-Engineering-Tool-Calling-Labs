import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools

load_lab_env(ROOT)

ARTIFACTS_DIR = ROOT / "artifacts"

# ── Page config ──
st.set_page_config(page_title="Research Agent", page_icon="🔍", layout="wide")
st.title("🔍 Research Agent")
st.caption("Day 04 Lab — Prompt Engineering & Tool Calling")

# ── Sidebar ──
with st.sidebar:
    st.header("Settings")
    provider_name = st.selectbox("Provider", ["mimo", "openrouter", "openai", "anthropic", "gemini"], index=0)
    version = st.text_input("Artifact version", value="v3")
    if st.button("🔄 Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ── Init agent ──
@st.cache_resource
def init_agent(provider_name: str, version: str):
    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider(provider_name)
    model = getattr(provider, "default_model", None)
    return system_prompt, openai_tools, provider, model

system_prompt, openai_tools, provider, model = init_agent(provider_name, version)

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display history ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_calls"):
            with st.expander("🔧 Tool calls"):
                st.json(msg["tool_calls"])
        if msg.get("tool_results"):
            with st.expander("📦 Tool results"):
                st.json(msg["tool_results"])

# ── User input ──
if user_input := st.chat_input("Nhập yêu cầu research..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    llm_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        llm_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        # Multi-round tool loop
        working_messages = list(llm_messages)
        final_text = ""
        all_tool_calls = []
        all_tool_results = []

        for round_idx in range(4):
            with st.spinner("Đang suy nghĩ..." if round_idx == 0 else "Đang gọi tool..."):
                try:
                    response = provider.complete(
                        working_messages, openai_tools, model=model, temperature=0.0
                    )
                except Exception as e:
                    st.error(f"Provider error: {e}")
                    st.stop()

            if response.text:
                final_text = response.text

            if not response.tool_calls:
                break

            with st.expander(f"🔧 Tool calls (round {round_idx + 1})"):
                for call in response.tool_calls:
                    st.write(f"**{call.name}**")
                    st.json(call.args)
                    all_tool_calls.append({"name": call.name, "args": call.args})

                    func = TOOL_FUNCTIONS.get(call.name)
                    if func:
                        try:
                            result = func(**call.args)
                        except Exception as exc:
                            result = {"error": type(exc).__name__, "message": str(exc)}
                    else:
                        result = {"error": "unknown_tool"}
                    all_tool_results.append({"tool": call.name, "args": call.args, "result": result})

            with st.expander(f"📦 Tool results (round {round_idx + 1})"):
                st.json(all_tool_results[-len(response.tool_calls):])

            for event in all_tool_results[-len(response.tool_calls):]:
                res = event.get("result", {})
                if isinstance(res, dict) and res.get("awaiting_user"):
                    question = res.get("question", "Vui lòng bổ sung thông tin.")
                    final_text = question

            tool_summary = json.dumps(
                all_tool_results[-len(response.tool_calls):],
                ensure_ascii=False, indent=2, default=str
            )
            working_messages.append({"role": "assistant", "content": f"Tool calls executed:\n{tool_summary}"})
            working_messages.append({"role": "user", "content": "Based on the tool results above, provide a helpful response to the user. If there were errors, explain what happened and suggest alternatives."})

        if final_text:
            st.markdown(final_text)

        st.session_state.messages.append({
            "role": "assistant",
            "content": final_text,
            "tool_calls": all_tool_calls if all_tool_calls else None,
            "tool_results": all_tool_results if all_tool_results else None,
        })