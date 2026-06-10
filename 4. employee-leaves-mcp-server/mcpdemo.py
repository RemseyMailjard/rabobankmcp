from mcp.server.fastmcp import FastMCP
import json
from typing import List
import threading
from flask import Flask, jsonify, request, send_from_directory

mcp = FastMCP("LeaveManager")

with open("employee_leaves.json", "r") as f:
    employee_leaves = json.load(f)
    
@mcp.tool()
def get_leave_balance_and_history(employee_id: str):
    '''Gets the leave balance and history for the given employee.'''
    return employee_leaves.get(employee_id, {})

@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]):
    '''Applies for leave for the given employee and dates.'''
    if employee_id not in employee_leaves:
        return {"error": "Employee not found"}
    
    leave_count = len(leave_dates)
    if employee_leaves[employee_id]['balance'] >= leave_count:
        employee_leaves[employee_id]['balance'] -= leave_count
        employee_leaves[employee_id]['history'].extend(leave_dates)
        
        with open("employee_leaves.json", 'w') as file:
            json.dump(employee_leaves, file, indent=2)
        return {"status": "Leave applied successfully"}
    
    else:
        return {"error": "insufficient leave balance"}

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/balance/<employee_id>')
def api_balance(employee_id):
    return jsonify(get_leave_balance_and_history(employee_id))

@app.route('/api/apply_leave/<employee_id>', methods=['POST'])
def api_apply_leave(employee_id):
    data = request.get_json()
    leave_dates = data.get('leave_dates', [])
    return jsonify(apply_leave(employee_id, leave_dates))
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)