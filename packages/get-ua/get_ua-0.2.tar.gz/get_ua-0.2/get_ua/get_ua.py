import json
import random

class get_ua:
    def __init__(self):
        json_file_path = "user_agents.json"
        with open(json_file_path, 'r') as file:
            self.user_agents = json.load(file)

    def random(self, browser=None, os=None, device=None):
        filtered_agents = self.user_agents

        if browser:
            filtered_agents = [agent for agent in filtered_agents if agent['browser'] == browser]
        if os:
            filtered_agents = [agent for agent in filtered_agents if agent['os'] == os]
        if device:
            filtered_agents = [agent for agent in filtered_agents if agent['device'] == device]

        if not filtered_agents:
            return None

        return random.choice(filtered_agents)['user_agent']

    def by_browser(self, browser=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['browser'] == browser]
        return random.choice(filtered_agents)['user_agent']
    
    def by_os(self, os=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['os'] == os]
        return random.choice(filtered_agents)['user_agent']
    
    def by_device(self, device=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['device'] == device]
        return random.choice(filtered_agents)['user_agent']

    def list_by_browser(self, browser=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['browser'] == browser]
        return [agent['user_agent'] for agent in filtered_agents]
    
    def list_by_os(self, os=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['os'] == os]
        return [agent['user_agent'] for agent in filtered_agents]
    
    def list_by_device(self, device=None):
        filtered_agents = self.user_agents
        filtered_agents = [agent for agent in filtered_agents if agent['device'] == device]
        return [agent['user_agent'] for agent in filtered_agents]
    
    def list_all(self):
        return [agent['user_agent'] for agent in self.user_agents]