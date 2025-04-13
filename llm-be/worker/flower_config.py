# Flower Server Configurations
port = 5555  # Run Flower on port 5555
persistent = True  # Save task states between restarts
state_save_interval = 10  # Update task states every 10 seconds
auto_refresh = True  # Automatically refresh the Flower dashboard

# ✅ Define which columns to display in the task list
task_columns = "eta,expires"
