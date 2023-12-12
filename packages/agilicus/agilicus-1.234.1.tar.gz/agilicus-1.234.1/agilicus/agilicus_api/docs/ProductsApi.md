# agilicus_api.ProductsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v2_create_product**](ProductsApi.md#v2_create_product) | **POST** /v2/products | Create a product
[**v2_delete_product**](ProductsApi.md#v2_delete_product) | **DELETE** /v2/products/{product_id} | Delete a product
[**v2_get_product**](ProductsApi.md#v2_get_product) | **GET** /v2/products/{product_id} | Get a single product
[**v2_list_products**](ProductsApi.md#v2_list_products) | **GET** /v2/products | Get all products
[**v2_replace_product**](ProductsApi.md#v2_replace_product) | **PUT** /v2/products/{product_id} | Create or update a product


# **v2_create_product**
> Product v2_create_product(product)

Create a product

Create a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import products_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = products_api.ProductsApi(api_client)
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            description="description_example",
            dev_mode=True,
            label="123",
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            trial_period=25,
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
    ) # Product | 

    # example passing only required values which don't have defaults set
    try:
        # Create a product
        api_response = api_instance.v2_create_product(product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_create_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product** | [**Product**](Product.md)|  |

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New product created |  -  |
**400** | Error creating product |  -  |
**409** | Product already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v2_delete_product**
> v2_delete_product(product_id)

Delete a product

Delete a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import products_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = products_api.ProductsApi(api_client)
    product_id = "1234" # str | Product Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a product
        api_instance.v2_delete_product(product_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_delete_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Product has been deleted |  -  |
**404** | Product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v2_get_product**
> Product v2_get_product(product_id)

Get a single product

Get a single product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import products_api
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = products_api.ProductsApi(api_client)
    product_id = "1234" # str | Product Unique identifier
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single product
        api_response = api_instance.v2_get_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_get_product: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single product
        api_response = api_instance.v2_get_product(product_id, get_subscription_data=get_subscription_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_get_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a product |  -  |
**404** | product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v2_list_products**
> ListProductsResponse v2_list_products()

Get all products

Get all products

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import products_api
from agilicus_api.model.list_products_response import ListProductsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = products_api.ProductsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all products
        api_response = api_instance.v2_list_products(limit=limit, get_subscription_data=get_subscription_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_list_products: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False

### Return type

[**ListProductsResponse**](ListProductsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v2_replace_product**
> Product v2_replace_product(product_id)

Create or update a product

Create or update a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import products_api
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = products_api.ProductsApi(api_client)
    product_id = "1234" # str | Product Unique identifier
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            description="description_example",
            dev_mode=True,
            label="123",
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            trial_period=25,
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
    ) # Product |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a product
        api_response = api_instance.v2_replace_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_replace_product: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a product
        api_response = api_instance.v2_replace_product(product_id, product=product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ProductsApi->v2_replace_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |
 **product** | [**Product**](Product.md)|  | [optional]

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated product |  -  |
**404** | Product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

