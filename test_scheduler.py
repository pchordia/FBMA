#!/usr/bin/env python3
"""
Test script to simulate the full scheduler cycle
"""

import json
import os
from budget_scheduler_v2 import BudgetScheduler

def reset_state():
    """Reset the state file to force a fresh run"""
    state = {
        "original_budgets": {},
        "last_run": None,
        "last_mode": None
    }
    with open('budget_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    print("✅ State file reset\n")

def simulate_nightly():
    """Force a nightly budget application"""
    print("=" * 80)
    print("🌙 SIMULATING NIGHTLY MODE (12:00 AM)")
    print("=" * 80)
    
    scheduler = BudgetScheduler()
    
    # Force nightly mode
    scheduler.state['last_mode'] = None  # Force it to think we need to switch
    print("\n📊 Fetching active campaigns and ad sets...")
    updates = scheduler.apply_nightly_budgets()
    
    scheduler.state['last_mode'] = 'nightly'
    scheduler.save_state()
    
    print(f"\n✅ Nightly simulation complete: {len(updates)} budget(s) processed")
    print("=" * 80)
    return updates

def simulate_daytime():
    """Force a daytime budget restoration"""
    print("\n\n" + "=" * 80)
    print("☀️  SIMULATING DAYTIME MODE (7:00 AM)")
    print("=" * 80)
    
    scheduler = BudgetScheduler()
    
    # Force daytime mode
    scheduler.state['last_mode'] = None  # Force it to think we need to switch
    print("\n📊 Fetching active campaigns and ad sets...")
    updates = scheduler.apply_daytime_budgets()
    
    scheduler.state['last_mode'] = 'daytime'
    scheduler.save_state()
    
    print(f"\n✅ Daytime simulation complete: {len(updates)} budget(s) processed")
    print("=" * 80)
    return updates

def show_state():
    """Show current state"""
    print("\n\n" + "=" * 80)
    print("📋 CURRENT STATE")
    print("=" * 80)
    
    with open('budget_state.json', 'r') as f:
        state = json.load(f)
    
    print(f"\nLast Mode: {state.get('last_mode', 'None')}")
    print(f"Last Run: {state.get('last_run', 'Never')}")
    print(f"\nStored Original Budgets: {len(state.get('original_budgets', {}))}")
    
    if state.get('original_budgets'):
        print("\n💾 Stored Budgets:")
        for obj_id, budget in state['original_budgets'].items():
            print(f"  {obj_id}: ${budget/100:.2f}")
    
    print("=" * 80)

if __name__ == "__main__":
    print("\n🧪 TESTING BUDGET SCHEDULER V2")
    print("This will simulate the full day/night cycle\n")
    
    # Reset state
    reset_state()
    
    # Simulate nightly (will store originals and lower budgets)
    simulate_nightly()
    
    # Simulate daytime (will restore to originals)
    simulate_daytime()
    
    # Show final state
    show_state()
    
    print("\n\n✅ Test complete! Review the output above to verify behavior.")

