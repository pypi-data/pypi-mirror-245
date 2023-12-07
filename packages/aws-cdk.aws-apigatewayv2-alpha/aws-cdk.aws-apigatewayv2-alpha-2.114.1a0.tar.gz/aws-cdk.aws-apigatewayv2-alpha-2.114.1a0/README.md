# AWS::APIGatewayv2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to aws-cdk-lib/aws-apigatewayv2.

## Table of Contents

* [Introduction](#introduction)
* [HTTP API](#http-api)

  * [Defining HTTP APIs](#defining-http-apis)
  * [Cross Origin Resource Sharing (CORS)](#cross-origin-resource-sharing-cors)
  * [Publishing HTTP APIs](#publishing-http-apis)
  * [Custom Domain](#custom-domain)
  * [Mutual TLS](#mutual-tls-mtls)
  * [Managing access to HTTP APIs](#managing-access-to-http-apis)
  * [Metrics](#metrics)
  * [VPC Link](#vpc-link)
  * [Private Integration](#private-integration)
* [WebSocket API](#websocket-api)

  * [Manage Connections Permission](#manage-connections-permission)
  * [Managing access to WebSocket APIs](#managing-access-to-websocket-apis)

## Introduction

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket
APIs at any scale. API developers can create APIs that access AWS or other web services, as well as data stored in the AWS Cloud.
As an API Gateway API developer, you can create APIs for use in your own client applications. Read the
[Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html).

This module supports features under [API Gateway v2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html)
that lets users set up Websocket and HTTP APIs.
REST APIs can be created using the `aws-cdk-lib/aws-apigateway` module.

HTTP and Websocket APIs use the same CloudFormation resources under the hood. However, this module separates them into two separate constructs for a more efficient abstraction since there are a number of CloudFormation properties that specifically apply only to each type of API.

## HTTP API

HTTP APIs enable creation of RESTful APIs that integrate with AWS Lambda functions, known as Lambda proxy integration,
or to any routable HTTP endpoint, known as HTTP proxy integration.

### Defining HTTP APIs

HTTP APIs have two fundamental concepts - Routes and Integrations.

Routes direct incoming API requests to backend resources. Routes consist of two parts: an HTTP method and a resource
path, such as, `GET /books`. Learn more at [Working with
routes](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-routes.html). Use the `ANY` method
to match any methods for a route that are not explicitly defined.

Integrations define how the HTTP API responds when a client reaches a specific Route. HTTP APIs support Lambda proxy
integration, HTTP proxy integration and, AWS service integrations, also known as private integrations. Learn more at
[Configuring integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations.html).

Integrations are available at the `aws-apigatewayv2-integrations` module and more information is available in that module.
As an early example, we have a website for a bookstore where the following code snippet configures a route `GET /books` with an HTTP proxy integration. All other HTTP method calls to `/books` route to a default lambda proxy for the bookstore.

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpUrlIntegration, HttpLambdaIntegration

# book_store_default_fn: lambda.Function


get_books_integration = HttpUrlIntegration("GetBooksIntegration", "https://get-books-proxy.example.com")
book_store_default_integration = HttpLambdaIntegration("BooksIntegration", book_store_default_fn)

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=get_books_integration
)
http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.ANY],
    integration=book_store_default_integration
)
```

The URL to the endpoint can be retrieved via the `apiEndpoint` attribute. By default this URL is enabled for clients. Use `disableExecuteApiEndpoint` to disable it.

```python
http_api = apigwv2.HttpApi(self, "HttpApi",
    disable_execute_api_endpoint=True
)
```

The `defaultIntegration` option while defining HTTP APIs lets you create a default catch-all integration that is
matched when a client reaches a route that is not explicitly defined.

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpUrlIntegration


apigwv2.HttpApi(self, "HttpProxyApi",
    default_integration=HttpUrlIntegration("DefaultIntegration", "https://example.com")
)
```

### Cross Origin Resource Sharing (CORS)

[Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a browser security
feature that restricts HTTP requests that are initiated from scripts running in the browser. Enabling CORS will allow
requests to your API from a web application hosted in a domain different from your API domain.

When configured CORS for an HTTP API, API Gateway automatically sends a response to preflight `OPTIONS` requests, even
if there isn't an `OPTIONS` route configured. Note that, when this option is used, API Gateway will ignore CORS headers
returned from your backend integration. Learn more about [Configuring CORS for an HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html).

The `corsPreflight` option lets you specify a CORS configuration for an API.

```python
apigwv2.HttpApi(self, "HttpProxyApi",
    cors_preflight=apigwv2.CorsPreflightOptions(
        allow_headers=["Authorization"],
        allow_methods=[apigwv2.CorsHttpMethod.GET, apigwv2.CorsHttpMethod.HEAD, apigwv2.CorsHttpMethod.OPTIONS, apigwv2.CorsHttpMethod.POST
        ],
        allow_origins=["*"],
        max_age=Duration.days(10)
    )
)
```

### Publishing HTTP APIs

A Stage is a logical reference to a lifecycle state of your API (for example, `dev`, `prod`, `beta`, or `v2`). API
stages are identified by their stage name. Each stage is a named reference to a deployment of the API made available for
client applications to call.

Use `HttpStage` to create a Stage resource for HTTP APIs. The following code sets up a Stage, whose URL is available at
`https://{api_id}.execute-api.{region}.amazonaws.com/beta`.

```python
# api: apigwv2.HttpApi


apigwv2.HttpStage(self, "Stage",
    http_api=api,
    stage_name="beta"
)
```

If you omit the `stageName` will create a `$default` stage. A `$default` stage is one that is served from the base of
the API's URL - `https://{api_id}.execute-api.{region}.amazonaws.com/`.

Note that, `HttpApi` will always creates a `$default` stage, unless the `createDefaultStage` property is unset.

### Custom Domain

Custom domain names are simpler and more intuitive URLs that you can provide to your API users. Custom domain name are associated to API stages.

The code snippet below creates a custom domain and configures a default domain mapping for your API that maps the
custom domain to the `$default` stage of the API.

```python
import aws_cdk.aws_certificatemanager as acm
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration

# handler: lambda.Function


cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
domain_name = "example.com"

dn = apigwv2.DomainName(self, "DN",
    domain_name=domain_name,
    certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn)
)
api = apigwv2.HttpApi(self, "HttpProxyProdApi",
    default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
    # https://${dn.domainName}/foo goes to prodApi $default stage
    default_domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="foo"
    )
)
```

To migrate a domain endpoint from one type to another, you can add a new endpoint configuration via `addEndpoint()`
and then configure DNS records to route traffic to the new endpoint. After that, you can remove the previous endpoint configuration.
Learn more at [Migrating a custom domain name](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-regional-api-custom-domain-migrate.html)

To associate a specific `Stage` to a custom domain mapping -

```python
# api: apigwv2.HttpApi
# dn: apigwv2.DomainName


api.add_stage("beta",
    stage_name="beta",
    auto_deploy=True,
    # https://${dn.domainName}/bar goes to the beta stage
    domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="bar"
    )
)
```

The same domain name can be associated with stages across different `HttpApi` as so -

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration

# handler: lambda.Function
# dn: apigwv2.DomainName


api_demo = apigwv2.HttpApi(self, "DemoApi",
    default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
    # https://${dn.domainName}/demo goes to apiDemo $default stage
    default_domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="demo"
    )
)
```

The `mappingKey` determines the base path of the URL with the custom domain. Each custom domain is only allowed
to have one API mapping with undefined `mappingKey`. If more than one API mappings are specified, `mappingKey` will be required for all of them. In the sample above, the custom domain is associated
with 3 API mapping resources across different APIs and Stages.

|        API     |     Stage   |   URL  |
| :------------: | :---------: | :----: |
| api | $default  |   `https://${domainName}/foo`  |
| api | beta  |   `https://${domainName}/bar`  |
| apiDemo | $default  |   `https://${domainName}/demo`  |

You can retrieve the full domain URL with mapping key using the `domainUrl` property as so -

```python
# api_demo: apigwv2.HttpApi

demo_domain_url = api_demo.default_stage.domain_url
```

### Mutual TLS (mTLS)

Mutual TLS can be configured to limit access to your API based by using client certificates instead of (or as an extension of) using authorization headers.

```python
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_certificatemanager as acm
# bucket: s3.Bucket


cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
domain_name = "example.com"

apigwv2.DomainName(self, "DomainName",
    domain_name=domain_name,
    certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn),
    mtls=apigwv2.MTLSConfig(
        bucket=bucket,
        key="someca.pem",
        version="version"
    )
)
```

Instructions for configuring your trust store can be found [here](https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/)

### Managing access to HTTP APIs

API Gateway supports multiple mechanisms for [controlling and managing access to your HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html) through authorizers.

These authorizers can be found in the [APIGatewayV2-Authorizers](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-authorizers-readme.html) constructs library.

### Metrics

The API Gateway v2 service sends metrics around the performance of HTTP APIs to Amazon CloudWatch.
These metrics can be referred to using the metric APIs available on the `HttpApi` construct.
The APIs with the `metric` prefix can be used to get reference to specific metrics for this API. For example,
the method below refers to the client side errors metric for this API.

```python
api = apigwv2.HttpApi(self, "my-api")
client_error_metric = api.metric_client_error()
```

Please note that this will return a metric for all the stages defined in the api. It is also possible to refer to metrics for a specific Stage using
the `metric` methods from the `Stage` construct.

```python
api = apigwv2.HttpApi(self, "my-api")
stage = apigwv2.HttpStage(self, "Stage",
    http_api=api
)
client_error_metric = stage.metric_client_error()
```

### VPC Link

Private integrations let HTTP APIs connect with AWS resources that are placed behind a VPC. These are usually Application
Load Balancers, Network Load Balancers or a Cloud Map service. The `VpcLink` construct enables this integration.
The following code creates a `VpcLink` to a private VPC.

```python
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpAlbIntegration


vpc = ec2.Vpc(self, "VPC")
alb = elb.ApplicationLoadBalancer(self, "AppLoadBalancer", vpc=vpc)

vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)

# Creating an HTTP ALB Integration:
alb_integration = HttpAlbIntegration("ALBIntegration", alb.listeners[0])
```

Any existing `VpcLink` resource can be imported into the CDK app via the `VpcLink.fromVpcLinkAttributes()`.

```python
import aws_cdk.aws_ec2 as ec2

# vpc: ec2.Vpc

awesome_link = apigwv2.VpcLink.from_vpc_link_attributes(self, "awesome-vpc-link",
    vpc_link_id="us-east-1_oiuR12Abd",
    vpc=vpc
)
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

These integrations can be found in the [aws-apigatewayv2-integrations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-integrations-readme.html) constructs library.

## WebSocket API

A WebSocket API in API Gateway is a collection of WebSocket routes that are integrated with backend HTTP endpoints,
Lambda functions, or other AWS services. You can use API Gateway features to help you with all aspects of the API
lifecycle, from creation through monitoring your production APIs. [Read more](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-overview.html)

WebSocket APIs have two fundamental concepts - Routes and Integrations.

WebSocket APIs direct JSON messages to backend integrations based on configured routes. (Non-JSON messages are directed
to the configured `$default` route.)

Integrations define how the WebSocket API behaves when a client reaches a specific Route. Learn more at
[Configuring integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-requests.html).

Integrations are available in the `aws-apigatewayv2-integrations` module and more information is available in that module.

To add the default WebSocket routes supported by API Gateway (`$connect`, `$disconnect` and `$default`), configure them as part of api props:

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import WebSocketLambdaIntegration

# connect_handler: lambda.Function
# disconnect_handler: lambda.Function
# default_handler: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi",
    connect_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("ConnectIntegration", connect_handler)),
    disconnect_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("DisconnectIntegration", disconnect_handler)),
    default_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("DefaultIntegration", default_handler))
)

apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev",
    auto_deploy=True
)
```

To retrieve a websocket URL and a callback URL:

```python
# web_socket_stage: apigwv2.WebSocketStage


web_socket_uRL = web_socket_stage.url
# wss://${this.api.apiId}.execute-api.${s.region}.${s.urlSuffix}/${urlPath}
callback_uRL = web_socket_stage.callback_url
```

To add any other route:

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import WebSocketLambdaIntegration

# message_handler: lambda.Function

web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
)
```

To add a route that can return a result:

```python
from aws_cdk.aws_apigatewayv2_integrations_alpha import WebSocketLambdaIntegration

# message_handler: lambda.Function

web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler),
    return_response=True
)
```

To import an existing WebSocketApi:

```python
web_socket_api = apigwv2.WebSocketApi.from_web_socket_api_attributes(self, "mywsapi", web_socket_id="api-1234")
```

### Manage Connections Permission

Grant permission to use API Gateway Management API of a WebSocket API by calling the `grantManageConnections` API.
You can use Management API to send a callback message to a connected client, get connection information, or disconnect the client. Learn more at [Use @connections commands in your backend service](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html).

```python
# fn: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
stage = apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev"
)
# per stage permission
stage.grant_management_api_access(fn)
# for all the stages permission
web_socket_api.grant_manage_connections(fn)
```

### Managing access to WebSocket APIs

API Gateway supports multiple mechanisms for [controlling and managing access to a WebSocket API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-control-access.html) through authorizers.

These authorizers can be found in the [APIGatewayV2-Authorizers](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-authorizers-readme.html) constructs library.

### API Keys

Websocket APIs also support usage of API Keys. An API Key is a key that is used to grant access to an API. These are useful for controlling and tracking access to an API, when used together with [usage plans](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). These together allow you to configure controls around API access such as quotas and throttling, along with per-API Key metrics on usage.

To require an API Key when accessing the Websocket API:

```python
web_socket_api = apigwv2.WebSocketApi(self, "mywsapi",
    api_key_selection_expression=apigwv2.WebSocketApiKeySelectionExpression.HEADER_X_API_KEY
)
```
