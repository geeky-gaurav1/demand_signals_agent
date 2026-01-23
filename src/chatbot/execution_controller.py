import subprocess
import sys
from src.chatbot.intent_classifier import Intent

INTENT_SCRIPT_MAP = {
    Intent.SALES_HISTORY: "src/data_generation/run_all.py",
    Intent.CONSOLIDATED_INSIGHTS: "src/data_generation/consolidation.py",
    Intent.CLEANUP: "src/data_cleanup/cleanup.py",
    Intent.GOLD_SIGNAL: "src/gold_layer/demand_signal_generator.py"
}

def execute_pipeline_step(intent: Intent):
    script_path = INTENT_SCRIPT_MAP.get(intent)

    if not script_path:
        print("❌ No executable step mapped for this intent.")
        return

    print(f"\n▶ Executing: {script_path}\n")

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )
        print("\n✅ Step execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print("\n❌ Step execution failed.")
        print(e)
