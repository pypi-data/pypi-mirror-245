from kubernetes import client, config

class K8S:
    def __init__(self, namespace: str):
        self.namespace = namespace
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
    
    def get_secret(self, secret_name,  key):
        try:
            secret = self.v1.read_namespaced_secret(name=secret_name, namespace=self.namespace)
            secret_value = secret.data.get(key, "")
            return secret_value
        except client.exceptions.ApiException as e:
            return None