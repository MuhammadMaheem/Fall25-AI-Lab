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





class TemperatueSensor:
    def __init__(self, normal_temp):
        self.normal_temp = normal_temp
        self.previous_action = None 
    def get(self, current_temperature):
        return current_temperature

    def act(self, current_temperature):
        if current_temperature < self.normal_temp:
            action = "Turn on heater"
        elif current_temperature > self.normal_temp:
            action = "Turn off heater"
        else:
            action = "Do nothing"

        if action == self.previous_action:
            action = "Do nothing"

        self.previous_action = action
        return action

rooms = {
    "Living Room": 18,
    "Bedroom": 22,
    "Kitchen": 20,
    "Bathroom": 24
}
normal_temp = 22
agent = TemperatueSensor(normal_temp)

for room, temperature in rooms.items():
    action = agent.act(temperature)
    print(f"{room}: Current temperature = {temperature}°C. {action}.")



















