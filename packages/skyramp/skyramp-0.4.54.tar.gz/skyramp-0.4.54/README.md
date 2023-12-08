# Skyramp
Skyramp is a pip module that provides utility functions for leveraging [Skyramp CLI](https://skyramp.dev/docs/reference/cli-commands/) commands. It offers functionalities to create and apply mock configurations for gRPC and REST APIs, as well as testing and asserting scenarios in various test environments. The package provides classes such as GrpcEndpoint, RestEndpoint, Scenario, and Client to facilitate these tasks.

## Installation
To install Skyramp, simply run the following command in your terminal:
```bash
pip install skyramp
```

## Usage
Once you've installed Skyramp, you can import it into your project like this:
```python
import skyramp
```

## Client
The Client class is the primary entry point to interact with the skyramp package. It allows you to apply configurations, start test scenarios, and deploy or delete workers. First, set up the Client with a Kubernetes cluster.

**Example: Provision Local Cluster with Skyramp**
```python
skyramp_client = skyramp.Client()
skyramp_client.apply_local()
```
Once you have a Client instance configured with a Kubernetes cluster, you can deploy the Skyramp Worker in-cluster to apply mocks and run tests.

**Example: Deploy Skyramp Worker**
```python
skyramp_client.deploy_skyramp_worker("test-worker", image, True)
```

### RestEndpoint
The RestEndpoint class represents a REST API endpoint and provides methods to configure mock responses and apply them using the Client.

**Example: Create REST Mock Configuration**
```python
rest_endpoint = skyramp.RestEndpoint("artists", "", 50050, "api/openapi/artists.yaml")
rest_endpoint.mock_method_from_file("artists-GET", "files/rest-values.yaml")
skyramp_client.mocker_apply("test-worker", "", rest_endpoint)
```

### GrpcEndpoint
The GrpcEndpoint class represents a gRPC API endpoint and provides methods to configure mock responses and apply them using the Client.

**Example: Create gRPC Mock Configuration**
```python
grpc_endpoint = skyramp.GrpcEndpoint("helloworld", "Greeter", 50051, "../../../examples/pb/helloworld.proto")
mock_object = {
    "responseValue": {
        "name": "HelloReply",
        "blob": "{\n  \"message\": \"Hello!\"\n}"
    }
}
grpc_endpoint.mock_method("SayHello", mock_object)
skyramp_client.mocker_apply("test-worker", "", grpc_endpoint)
```

### Scenario
The Scenario class allows you to define test scenarios by specifying a sequence of API requests and assertions. Once a Scenario is created, you can start it using the Client instance.

**Example: Test Assert Scenario (REST)**
```python
scenario = skyramp.Scenario("rest-test")
step_name = scenario.add_request(endpoint=rest_endpoint, method_name="artists-GET")
scenario.add_assert_equal(f"{step_name}.res.message", "Hello!")
skyramp_client.tester_start("test-worker", "", scenario)
```

**Example: Test Assert Scenario (gRPC)**
```python
scenario = skyramp.Scenario("grpc-test")
step_name = scenario.add_request_from_file(endpoint=grpc_endpoint, method_name="SayHello", request_file="files/grpc-request.yaml")
scenario.add_assert_equal(f"{step_name}.res.message", "Hello!")
skyramp_client.tester_start("test-worker", "", scenario)
```
