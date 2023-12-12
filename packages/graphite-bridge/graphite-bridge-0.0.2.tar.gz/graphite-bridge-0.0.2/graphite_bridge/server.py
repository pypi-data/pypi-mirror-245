import requests

class GraphiteServerConnector:
    def __init__(self, serverUrl, strategy_id):
        self.__serverUrl = serverUrl
        self.__strategy_id = strategy_id

    def get_client_config(self):
        response = requests.get(self.__serverUrl + "/client/config?strategyId=" + self.__strategy_id)
        return response
    
    def upload_state(self, state):
        data = { 'strategyId': self.__strategy_id, 'state': state }
        response = requests.post(self.__serverUrl + "/client/upload", json=data)
        return response
    
