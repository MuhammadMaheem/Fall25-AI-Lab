# Simple Reflex Agent Example:
# This agent will check the current temperature and decide whether to turn the heater on or off.
# class SimpleReflexAgent:
#  def __init__(self, desired_temperature):
#  self.desired_temperature = desired_temperature
#  def perceive(self, current_temperature):
#  return current_temperature
#  def act(self, current_temperature):
#  if current_temperature < self.desired_temperature:
#  action = "Turn on heater"
#  else:
#  action = "Turn off heater"
#  return action
# # simulating different rooms with different current temperatures
# rooms = {
#  "Living Room": 18,
#  "Bedroom": 22,
#  "Kitchen": 20,
#  "Bathroom": 24
# }
# # desired temperature for all rooms
# desired_temperature = 22
# agent = SimpleReflexAgent(desired_temperature)
# # run the agent for each room
# for room, temperature in rooms.items():
#  action = agent.act(temperature)
#  print(f"{room}: Current temperature = {temperature}°C. {action}.")





















# Lab 3 Task:
# • Model-Based Reflex Agent
# • This agent not only checks the current temperature but also remembers the previous
# action to avoid turning the heater on or off unnecessarily
# use dict  to see if the same temperature is repeated , and if its repeated the prine "No nothing" and only 1 temputature in


def temperature_agent(current_temperature, base_temp, memory):
    if current_temperature in memory:
        return "No nothing"
    else:
        
        memory[current_temperature] = True
        if current_temperature < base_temp:
            return "Turn on heater"
        else:
            return "Turn off heater"
rooms = {
    "Living Room": 12,
    "Bedroom": 8,
    "Kitchen": 32,
    "Bathroom": 12,
    "Bathroo2m": 23
}
base_temp = 32
memory = {}
for room, temperature in rooms.items():
    action = temperature_agent(temperature, base_temp, memory)
    print(f"{room}: {temperature}... {action}.")










